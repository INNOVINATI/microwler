<template>
  <v-card
    class="mt-4 mx-auto"
    max-width="400"
  >

    <v-sheet

      class="v-sheet--offset mx-auto"
      color="primary"
      :elevation=elevation
      max-width="calc(100% - 32px)"
    >
      <v-sparkline
        v-if="!!values && values.length > 1"
        color="white"
        :value="values"
        line-width="2"
        padding="16"
      ></v-sparkline>
      <small v-if="!!values && values.length < 2" class="white--text">
        Not enough data to show chart
      </small>
      <small v-else class="white--text">
        Select a project to visualize its crawl history
      </small>
    </v-sheet>

    <v-card-text class="pt-0">
      <div class="title font-weight-light mb-2">
        {{ data.domain }}
      </div>
      <div class="subheading font-weight-light grey--text">
        Microwler v{{ data.status.version }}
      </div>
      <v-divider class="my-2"></v-divider>
      <v-icon class="mr-2" small>mdi-clock</v-icon>
      <span class="caption grey--text font-weight-light">up since {{ data.status.up_since }}</span>
      <v-spacer></v-spacer>
      <v-icon class="mr-2" small>mdi-database</v-icon>
      <span class="caption grey--text font-weight-light">total cache size: {{ $store.getters.getCacheSize }} pages</span>
    </v-card-text>
  </v-card>
</template>

<script>
  export default {
    props: {
      data: Object
    },
    computed: {
      values() {
        console.log(this.$store.state.chartData)
        return this.$store.state.chartData
      },
      elevation() {
        if (!!this.values)
          return this.values.length > 1 ? 10 : 0
      }
    }
  }
</script>

<style scoped>
  .v-sheet--offset {
    top: -24px;
    position: relative;
  }
</style>
