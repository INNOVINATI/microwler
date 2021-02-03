<template>
  <v-row>
    <v-col cols="12" lg="4" md="6" sm="12" align="center">
      <div>
        <img src="logo.png" width="200">
        <v-row align="center">
          <v-col cols="12" lg="12" sm="12" align="center">
            <v-text-field
              placeholder="Enter your service domain"
              v-model="input"
              :loading="connecting"
              style="width: 60%"
            ></v-text-field>
          </v-col>
          <v-col cols="12" lg="12" sm="12" align="center">
            <v-btn primary @click="connect()" :disabled="!input || connecting">Connect</v-btn>
          </v-col>
          <v-col cols="12" lg="12" style="margin: 5% 0">
            <Host
              v-if="domain"
              :domain="domain"
              :status="status"
              :job-count="jobCount"
            ></Host>
          </v-col>
        </v-row>
      </div>

    </v-col>

    <v-col cols="12" lg="8" md="6" sm="12" style="margin-top: 5vh">
      <v-row >
        <v-col cols="12" lg="6" sm="12" v-if="!!projects" v-for="(project, i) in projects" :key="i" justify="space-around">
          <Project
            :host="domain"
            :name="project"
          ></Project>
        </v-col>
      </v-row>
    </v-col>
  </v-row>

</template>

<script>
  import Project from "../components/Project";
  import Host from "../components/Host";

  export default {
    components: {Host, Project},
    data() {
      return {
        input: null,
        connecting: false,
        domain: null,
        getStatus: null,
        jobCount: [],
        projects: null,
      }
    },
    methods: {
      connect() {
        if (!!this.input) {
          this.connecting = true
          fetch(`http://${this.input}/status`)
            .then(async res => await res.json())
            .then(data => {
              this.domain = this.input
              this.input = null
              this.connecting = false
              this.status = data.app
              this.projects = data.projects
            })
            .catch(err => {
              this.connecting = false
              this.domain = null
              alert(err)
            })
        }
      }
    }
  }
</script>
