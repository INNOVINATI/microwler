<template>
  <v-app dark>
    <v-app-bar fixed app>
      <v-toolbar-title>Microwler UI</v-toolbar-title>
      <v-spacer />
      <div class="py-auto">
        <v-switch class="mt-4" v-model="$vuetify.theme.dark" label="Dark / Light"></v-switch>
      </div>

    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data () {
    return {

    }
  }
}
</script>
