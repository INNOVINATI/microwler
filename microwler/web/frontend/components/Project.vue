<template>
    <v-card
      :loading="loading"
    class="mx-auto elevation-10"
    max-width="344"
  >
      <v-card-title>{{ name.replace(/_/g, '.') }}</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12" lg="4">
          <p>Last run: {{ last_run ? last_run.timestamp : 'never'}}</p>
      <div class="text--primary">
        Jobs: {{ jobs }}<br>
        Cache: {{ cache ? cache.meta.size : 'empty'}}
      </div>
        </v-col>
        <v-col cols="12" lg="8">
          <div>
            <iframe src="https://startups.saarland/" width="300" height="200" id="scaled-frame"></iframe>
          </div>

        </v-col>
      </v-row>

    </v-card-text>
    <v-card-actions>
      <v-btn @click="crawl()" v-if="!loading">Run crawler</v-btn>
      <v-btn disabled v-else>Running...</v-btn>
      <v-btn
        text
        color="primary accent-2"
      >
        Download cache
      </v-btn>
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
        loading: false,
        jobs: 0,
        last_run: null,
      }
    },
    methods: {
      crawl() {
        this.loading = true
        this.jobs++
        fetch(`http://${this.host}/crawl/${this.name}`)
          .then(res => res.json())
          .then(data => {
            this.loading = false
            this.download(data)
            return this.getStatus()
          })
          .catch(err => {
            this.loading = false
            alert(err)
          })
      },
      getStatus() {
        this.loading = true
        fetch(`http://${this.host}/status/${this.name}`)
        .then(res => res.json())
        .then(data => {
          this.healthy = true
          this.jobs = data.jobs
          this.last_run = data.last_run
          this.getCache()
        })
        .catch(err => {
          this.loading = false
          alert(err)
        })
      },
      getCache() {
        fetch(`http://${this.host}/data/${this.name}`)
          .then(res => res.json())
          .then(data => {
            this.loading = false
            this.cache = data
          })
          .catch(err => {
            this.loading = false
            alert(err)
          })
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
#scaled-frame {
  zoom: 0.75;
  -moz-transform: scale(0.75);
  -moz-transform-origin: 0 0;
  -o-transform: scale(0.75);
  -o-transform-origin: 0 0;
  -webkit-transform: scale(0.75);
  -webkit-transform-origin: 0 0;
}
</style>
