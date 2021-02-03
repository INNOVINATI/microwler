<template>
  <v-row justify="center">
    <v-dialog v-model="show" fullscreen hide-overlay transition="dialog-bottom-transition">
      <v-card color="white">
        <v-toolbar dark color="primary">
          <v-btn icon dark @click="$emit('close')">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Results</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
            <v-btn dark text @click="download(results, 'crawl')">Download</v-btn>
          </v-toolbar-items>
        </v-toolbar>
        <vue-json-viewer :value="results" copyable></vue-json-viewer>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
  import VueJsonViewer from "vue-json-viewer"

  export default {
    name: "ResultDialog",
    components: {VueJsonViewer},
    props: {
      projectName: String,
      results: Array,
      show: Boolean,
    },
    methods: {
      download(data, title) {
        var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(data));
        var dummy = document.createElement('a');
        dummy.setAttribute("href", dataStr);
        dummy.setAttribute("download", `${this.projectName}-${title}-${new Date().toISOString()}.json`);
        document.body.appendChild(dummy);
        dummy.click();
        dummy.remove();
        this.$emit('close')
      }
    }
  }
</script>

<style scoped>

</style>
