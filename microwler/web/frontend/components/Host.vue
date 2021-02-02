<template>
  <v-card
    class="mt-4 mx-auto"
    max-width="400"
  >
    <v-sheet
      class="v-sheet--offset mx-auto"
      color="#FD8539"
      elevation="12"
      max-width="calc(100% - 32px)"
    >
      <v-sparkline
        :value="jobCount"
        color="white"
        line-width="2"
        padding="16"
      ></v-sparkline>
    </v-sheet>

    <v-card-text class="pt-0">
      <div class="title font-weight-light mb-2">
        {{ domain }}
      </div>
      <div class="subheading font-weight-light grey--text">
        Microwler v{{ status.version }}
      </div>
      <v-divider class="my-2"></v-divider>
      <v-icon class="mr-2" small>mdi-clock</v-icon>
      <span class="caption grey--text font-weight-light">up since {{ status.up_since }}</span>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    props: {
      domain: String,
      status: Object,
    },
    data() {
      return {
        jobCount: [1,2,3,4,5,6,12,3,2,1]
      }
    },
  }
</script>

<style scoped>
  .v-sheet--offset {
    top: -24px;
    position: relative;
  }
</style>
