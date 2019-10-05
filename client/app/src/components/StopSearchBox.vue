<template id="">
<v-card max-width="620" class="mx-auto">
  <v-card-title>バス停検索</v-card-title>

  <v-tabs
    v-model="tab"
    dark
  >
    <v-tabs-slider></v-tabs-slider>

    <v-tab href="#tab-name">
      バス停名から検索
    </v-tab>
    <v-tab-item value="tab-name">
      <StopSearchBoxByName />
    </v-tab-item>

    <v-tab href="#tab-map">
      地図から検索
    </v-tab>
    <v-tab-item value="tab-map">
      <StopSearchBoxByMap />
    </v-tab-item>
  </v-tabs>
</v-card>
</template>

<script>
import StopSearchBoxByName from '@/components/StopSearchBoxByName'
import StopSearchBoxByMap from '@/components/StopSearchBoxByMap'

export default {
  data: () => ({
    tab: null
  }),
  components: {
    StopSearchBoxByName,
    StopSearchBoxByMap
  }
}
</script>
