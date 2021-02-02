<template>
  <v-card class="mx-auto" :loading="running" elevation="10" max-width="300">
    <v-card-title>{{name}}</v-card-title>
    <v-card-text>
      <div v-if="last_run">
        <p>Last run:<br>
        {{ last_run.timestamp }}
        ({{ last_run.successful ? 'success' : 'error'}})
        </p>
        <p>Jobs: {{ jobs }}</p>
        Cache: <v-btn text x-small @click="download(cache)">Download</v-btn> <small>({{ Object.keys(cache).length}} items)</small>
      </div>
      <div v-else>
        <p>Last run: never</p>
        <p>Jobs: 0</p>
        <p>No cached pages.</p>
      </div>
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
        cache: null,
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
            this.download(data)
            return this.getStatus()
          })
          .catch(err => {
            this.running = false
            alert(err)
          })
      },
      getStatus() {
        fetch(`http://${this.host}/status/${this.name}`)
        .then(res => res.json())
        .then(data => {
          this.healthy = true
          this.jobs = data.jobs
          this.last_run = data.last_run
          return this.getCache()
        })
      },
      getCache() {
        fetch(`http://${this.host}/data/${this.name}`)
          .then(res => res.json())
          .then(data => this.cache = data)
          .catch(err => alert(err))
      },
      download(data) {
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
        var dummy = document.createElement('a');
        dummy.setAttribute("href", dataStr);
        dummy.setAttribute("download", `${this.name}-${new Date().toISOString()}.json`);
        document.body.appendChild(dummy);
        dummy.click();
        dummy.remove();
      }
    },
    created() {
      this.getStatus()
    }
  }
</script>

<style scoped>

</style>
