<template>
  <v-card class="mx-auto" :loading="running" elevation="12" max-width="300">
    <v-card-title>{{name}}</v-card-title>
    <v-card-text>
      <p v-if="last_run">
        Last run:<br>
        {{ last_run.timestamp }}
        ({{ last_run.successful ? 'success' : 'error'}})
      </p>
      <p v-else>Last run: never</p>
      <p>Jobs: {{ jobs }}</p>
      <p>Cache size: {{ cache_size }}</p>
    </v-card-text>
    <v-card-actions>
      <v-btn @click="crawl()" v-if="!running">Crawl</v-btn>
      <v-btn disabled v-else>Running...</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  export default {
    name: "Project",
    props: {
      host: String,
      name: String
    },
    data() {
      return {
        healthy: false,
        cache_size: null,
        running: false,
        jobs: 0,
        last_run: null,
      }
    },
    methods: {
      crawl() {
        this.running = true
        this.jobs++
        fetch(`http://${this.host}/crawl/${this.name}`)
          .then(res => res.json())
          .then(data => {
            this.running = false
            var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
            var dummy = document.createElement('a');
            dummy.setAttribute("href", dataStr);
            dummy.setAttribute("download", `${this.name}-${new Date().toISOString()}.json`);
            document.body.appendChild(dummy);
            dummy.click();
            dummy.remove();
            this.status()
          })
          .catch(err => {
            this.running = false
            alert(err)
          })
      },
      status() {
        fetch(`http://${this.host}/status/${this.name}`)
        .then(res => res.json())
        .then(data => {
          this.healthy = true
          this.cache_size = data.cache_size
          this.jobs = data.jobs
          this.last_run = data.last_run
        })
      }
    },
    created() {
      this.status()
    }
  }
</script>

<style scoped>

</style>
