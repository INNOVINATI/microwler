<template>
  <v-row align="center" justify="center">
    <v-col cols="12" lg="4" md="6" sm="12">
      <div>
        <img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/logo.png" width="200">
        <v-row align="center">
          <v-col cols="12" lg="8" sm="12">
            <v-text-field placeholder="Enter your service domain" v-model="input" :loading="connecting"></v-text-field>
          </v-col>
          <v-col cols="12" lg="4" sm="12">
            <v-btn primary @click="connect()" :disabled="!input || connecting">Connect</v-btn>
          </v-col>
          <v-col cols="12">
            <v-card v-if="!!domain" outlined>
              <v-card-title>
                {{ domain }}
                <v-spacer></v-spacer>
                <v-icon>
                  mdi-server
                </v-icon>
              </v-card-title>
              <v-card-text>
                <p>Version: Microwler v.{{ status.version}}</p>
                <p>Up since: {{ status.up_since }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

    </v-col>

    <v-col cols="12" lg="8" md="6" sm="12">
      <v-row justify="space-around">
        <v-col cols="12" lg="6" sm="12" v-if="!!projects" v-for="(project, i) in projects" :key="i">
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

  export default {
    components: {Project},
    data() {
      return {
        input: null,
        connecting: false,
        domain: null,
        status: null,
        projects: null
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
