<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-toolbar-title>Microwler UI</v-toolbar-title>
      <v-spacer/>


    </v-app-bar>
    <v-main>
      <v-container fluid>
        <nuxt/>
      </v-container>
    </v-main>
    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} MIT License</span>
      <v-spacer></v-spacer>
      <span>powered by <a href="https://innovinati.com/">INNOVINATI</a></span>
      <v-spacer></v-spacer>
      <div class="py-auto">
        <v-switch v-model="$vuetify.theme.dark" dense>
          <template v-slot:label>
            <v-icon dark v-if="$vuetify.theme.dark">mdi-lightbulb-off-outline</v-icon>
            <v-icon v-else>mdi-lightbulb-on-outline</v-icon>
          </template>
        </v-switch>
      </div>
    </v-footer>
  </v-app>
</template>

<script>
  export default {
    data() {
      return {}
    },
    computed: {
      detectDarkMode() {

      }
    },
    created() {
      this.$vuetify.theme.dark = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
  }
</script>
