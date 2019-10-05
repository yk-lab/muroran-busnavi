<template>
<v-container>
  <v-flex v-if="data">
    <h1>{{data.now_name.name}}</h1>
    <LMap
      class="col-12"
      style="min-height: 380px; max-height: 520px;z-index: 0;"
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
    >
      <LTileLayer :url="url"></LTileLayer>
      <LMarker v-for="position in positions" :key="position.id" :lat-lng="position.lat_lng">
        <LTooltip v-if="$route.query.departure && $route.query.departure === position.id" :options="{permanent: true}">乗車</LTooltip>
        <LTooltip v-if="$route.query.arrival && $route.query.arrival === position.id" :options="{permanent: true}">下車</LTooltip>
        <LTooltip v-if="$route.query.passing && $route.query.passing === position.id" :options="{permanent: true}">経由</LTooltip>
      </LMarker>
    </LMap>
     <v-list subheader>
        <v-subheader>近隣の駅・停留所 (直線距離)</v-subheader>
        <v-list-item-group color="primary">
          <v-list-item
            v-for="ns in neighbor_stops"
            :key="ns.stop.id"
            :to="{name: 'Stop', params:{
              id: ns.stop.id
            }}"
          >
            <v-list-item-content>
              <v-list-item-title v-text="ns.stop.now_name.name"></v-list-item-title>
              <v-list-item-subtitle v-if="ns.dist && ns.dist > 0" v-text="`約${ns.dist}m`"></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
    </v-list>
  </v-flex>
  <div v-else-if="!data">
    <StopLoader />
  </div>
  <v-snackbar v-model="snackbar">
    {{ text }}
    <v-btn color="pink" text @click="snackbar = false">
      Close
    </v-btn>
  </v-snackbar>
</v-container>
</template>

<style>
</style>

<script>
import axios from "axios"
import moment from "moment"

import  'leaflet/dist/leaflet.css'
import {LMap, LTileLayer, LMarker, LTooltip} from 'vue2-leaflet'

import StopLoader from "@/components/StopLoader"

export default {
  data: () => ({
    data: null,
    positions: null,
    url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
    zoom: 16,
    center: null,
    bounds: null,
    snackbar: false,
    text: null,
    neighbor_stops: null
  }),
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
    StopLoader
  },
  created() {
    this.render()
  },
  methods: {
    render() {
      axios.get(
          `/api/1/stops/${this.$route.params.id}`
        ).then(res => {
          this.data = res.data.data
          this.neighbor_stops = res.data.neighbor_stops
        })
        .catch(err => {
          this.text = err
          this.snackbar = true
        })
        .finally(() => {})
    },
    availability(obj) {
      return moment(obj.application_start) <= moment.utc() && (moment(obj.application_end) >= moment.utc() || obj.application_end === null)
    },
    zoomUpdated (zoom) {
      this.zoom = zoom;
    },
    centerUpdated (center) {
      this.center = center;
    },
    boundsUpdated (bounds) {
      this.bounds = bounds;
    }
  },
  watch: {
    data: function(val) {
      if (val){
        this.positions = val.positions.filter(
          position => this.availability(position)
        ).map(
          d => {return {id: d.id, lat_lng: [parseFloat(d.lat), parseFloat(d.lng)]}}
        );
        const lat = this.positions.map(d => d.lat_lng[0]);
        const lng = this.positions.map(d => d.lat_lng[1]);
        this.center = [
          lat.reduce((prev, current) => prev+current)/lat.length,
          lng.reduce((prev, current) => prev+current)/lng.length
        ]
      }
    },
    $route: function() {
      this.data = null
      this.render()
      window.scrollTo(0,0)
    }
  }
}
</script>
