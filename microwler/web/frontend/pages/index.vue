<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <img src="https://github.com/INNOVINATI/microwler/raw/master/docs/static/logo.png" width="200">
      <v-card>
        <v-card-title class="headline">
          Welcome to Microwler UI
        </v-card-title>
        <v-card-text>
          <p>
            This is a simple web client for your Microwler services.
          </p>
          <p>
            For more information on Microwler, check out the <a
              href="https://innovinati.github.io/microwler"
              target="_blank"
              rel="noopener noreferrer"
            >
              documentation
            </a>.
          </p>
          <p>
            Found a bug? Report it on the github <a
              href="https://github.com/innovinati/microwler/issues"
              target="_blank"
              rel="noopener noreferrer"
              title="contribute"
            >
              issue board
            </a>.
          </p>
          <p>Thank you for using Microwler!</p>
          <hr class="my-3">
          <a
            href="https://innovinati.com/"
            target="_blank"
            rel="noopener noreferrer"
          >
            powered by INNOVINATI
          </a>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            nuxt
            to="/connect"
          >
            Start app
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import Logo from '~/components/Logo.vue'
import VuetifyLogo from '~/components/VuetifyLogo.vue'

export default {
  components: {
    Logo,
    VuetifyLogo
  }
}
</script>
