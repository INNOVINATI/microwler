<template>

  <v-card
    class="mx-auto"
    max-width="344"
    :loading="loading"
  >
    <iframe v-bind:src="startUrl" width="344" height="200"></iframe>

    <v-card-title>
      {{ name.replace(/_/g, '.') }}
    </v-card-title>

    <v-card-subtitle v-if="healthy">
        <p v-if="!!lastRun">
          <span v-if="lastRun.hasOwnProperty('timestamp')">Last crawl at {{ lastRun.timestamp }}<br>{{ lastRun.state }}.</span>
          <span v-else>No crawls recorded.<br><br></span>
        </p>
        <p>Cache: {{ cacheInfo }}</p>
    </v-card-subtitle>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="crawl()" v-if="!loading">Run crawler</v-btn>
      <v-btn text disabled v-else>Running...</v-btn>
      <v-btn color="secondary" text @click="download(cache, 'cache')" :disabled="cache.length === 0">Download cache</v-btn>
      <v-spacer></v-spacer>
    </v-card-actions>
    <ResultDialog
      v-if="showDialog"
      :project-name="name"
      :show="showDialog"
      :results="newData"
      v-on:close="closeDialog()"
    ></ResultDialog>
  </v-card>
</template>

<script>
  import ResultDialog from "./ResultDialog";
  export default {
    name: "Project",
    components: {ResultDialog},
    props: {
      host: String,
      name: String
    },
    data() {
      return {
        healthy: false,
        cache: null,
        loading: false,
        startUrl: null,
        lastRun: null,
        showDialog: false,
        newData: null
      }
    },
    computed: {
      cacheInfo() {
        if (!!this.cache)
          return this.cache.length > 0 ? this.cache.length + ' pages' : 'empty'
        else
          return 'connection error'
      },
    },
    methods: {
      crawl() {
        this.loading = true
        fetch(`http://${this.host}/crawl/${this.name}`)
          .then(res => res.json())
          .then(data => {
            this.loading = false
            this.newData = data
            this.showDialog = true
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
          this.startUrl = data.start_url
          this.lastRun = data.last_run
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
            this.cache = data.data
          })
          .catch(err => {
            this.loading = false
            alert(err)
          })
      },
      download(data, title) {
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
        var dummy = document.createElement('a');
        dummy.setAttribute("href", dataStr);
        dummy.setAttribute("download", `${this.name}-${title}-${new Date().toISOString()}.json`);
        document.body.appendChild(dummy);
        dummy.click();
        dummy.remove();
      },
      closeDialog() {
        this.newData = null
        this.showDialog = false
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
