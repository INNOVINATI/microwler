<template>
  <v-row style="margin-bottom: 5vh">
    <v-col cols="12" lg="4" md="6" sm="12" align="center" style="margin-top: 5vh">
      <div>
        <img src="logo.png" width="250">
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
            <v-skeleton-loader v-if="!host"></v-skeleton-loader>
            <Host v-else :data="host"></Host>
          </v-col>
        </v-row>
      </div>

    </v-col>

    <v-col cols="12" lg="8" md="6" sm="12" style="margin-top: 5vh">
      <v-row>
        <v-col cols="12" lg="6" sm="12" v-if="!host" justify="space-around">
          <v-skeleton-loader></v-skeleton-loader>
        </v-col>
        <v-col v-else cols="12" lg="6" sm="12" v-for="(project, i) in host.projects" :key="i" justify="space-around">
          <Project :name="project"></Project>
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
      }
    },
    computed: {
      host() {
        return this.$store.state.host
      },
    },
    methods: {
      connect() {
        if (!!this.input) {
          this.connecting = true
          this.$store.dispatch('connect', this.input)
            .then(() => {
              this.input = null
              this.connecting = false
            })
        }
      }
    }
  }
</script>
