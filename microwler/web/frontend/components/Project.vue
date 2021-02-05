<template>
  <v-card
    class="mx-auto elevation-8"
    max-width="360"
    :loading="loading"
    @click="$store.dispatch('updateChart', name)"
  >
    <v-skeleton-loader v-if="!project" type="card-avatar, article, actions" max-width="344">

    </v-skeleton-loader>
    <div v-else>
      <iframe v-bind:src="project.startUrl" width="360" height="200"></iframe>

    <v-card-title>
      {{ name.replace(/_/g, '.') }}
    </v-card-title>

    <v-card-subtitle>
        <p v-if="!!project.lastRun">
          <span v-if="project.lastRun.hasOwnProperty('timestamp')">
            Last crawl at {{ project.lastRun.timestamp }}<br>{{ project.lastRun.state }}.
          </span>
          <span v-else>No crawls recorded.<br><br></span>
        </p>
        <v-chip color="grey" dark small>
          Cache: {{ cacheInfo }}
        </v-chip>
    </v-card-subtitle>

    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        text
        @click="crawl()"
        v-if="!loading"
      >
        Run crawler
      </v-btn>
      <v-btn
        text
        disabled
        v-else
      >
        Running...
      </v-btn>
      <v-btn
        v-if="!!project"
        color="secondary"
        text
        @click="download(project.cache, 'snapshot')"
        :disabled="!project.cache || project.cache.length === 0"
      >
        Download snapshot
      </v-btn>
      <v-spacer></v-spacer>
    </v-card-actions>
    <ResultDialog
      v-if="showDialog"
      :project-name="name"
      :show="showDialog"
      :results="results"
      v-on:close="closeDialog()"
    ></ResultDialog>
    </div>
  </v-card>
</template>

<script>
  import ResultDialog from "./ResultDialog";
  export default {
    name: "Project",
    components: {ResultDialog},
    props: {
      name: String
    },
    data() {
      return {
        loading: false,
        showDialog: false,
        results: null
      }
    },
    computed: {
      project() {
        return this.$store.getters.getProjectByName(this.name)
      },
      cacheInfo() {
        if (!!this.project.cache)
          return this.project.cache.length > 0 ? this.project.cache.length + ' pages' : 'empty'
        else
          return 'connection error'
      },
    },
    methods: {
      crawl() {
        this.loading = true
        this.$store.dispatch('runProject', this.name)
          .then(() => {
            this.loading = false
            this.results = this.project.latestResults
            this.showDialog = true
            this.loadProject()
          })
          .catch(err => {
            this.loading = false
            alert(err)
          })
      },
      loadProject() {
        this.loading = true
        this.$store.dispatch('getProject', this.name)
          .then(() => this.loading = false)
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
        this.results = null
        this.showDialog = false
      }
    },
    created() {
      this.loadProject()
    }
  }
</script>

<style scoped>
iframe {
  border: none;
  border-bottom: 1px solid lightgrey;
}
</style>
