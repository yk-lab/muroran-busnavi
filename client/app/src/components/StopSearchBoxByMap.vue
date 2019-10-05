<template id="">
<v-form ref="form" v-model="valid">
  <v-layout wrap>
    <LMap
      class="col-12 px-4"
      style="height: 280px;z-index: 0;"
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
    >
      <LTileLayer :url="url"></LTileLayer>
      <template v-for="(item, i) in busstop_list">
        <template v-for="position in item.positions">
          <LMarker :key="position.id" :lat-lng="[parseFloat(position.lat), parseFloat(position.lng)]">
            <LTooltip :options="{permanent: true}">{{i+1}}. {{item.stop_name}}</LTooltip>
            <LPopup>
              <router-link :to="{name: 'Stop', params: {id: item.stop_id}}">
                {{item.stop_name}}
              </router-link>
            </LPopup>
          </LMarker>
        </template>
      </template>
    </LMap>
    <ol>
      <li v-for="(item, i) in busstop_list" :key="i">
        <router-link :to="{name: 'Stop', params: {id: item.stop_id}}">
          {{item.stop_name}}
        </router-link>
      </li>
    </ol>
  </v-layout>
  <v-card-actions>
    <v-btn :disabled="!valid" color="success" @click="set_center_now_position">
      現在地
    </v-btn>
  </v-card-actions>
  <v-snackbar v-model="snackbar">
    {{ text }}
    <v-btn color="pink" text @click="snackbar = false">
      Close
    </v-btn>
  </v-snackbar>
</v-form>
</template>

<script>
import moment from "moment/moment"
import axios from "axios"

import  'leaflet/dist/leaflet.css'
import L from 'leaflet'
import {LMap, LTileLayer, LMarker, LTooltip, LPopup} from 'vue2-leaflet'

export default {
  data: () => ({
    url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
    zoom: 12,
    center: L.latLng(42.3690762, 140.9911693),
    bounds: null,

    isLoading: false,
    valid: true,
    busstop: null,
    busstop_list: [],
    nameRules: [
      v => !!v || '必須です',
    ],
    snackbar: false,
    text: null,
    searchbox: null,
  }),
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
    LPopup
  },
  methods: {
    set_center_now_position () {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (pos) =>  this.center = L.latLng(pos.coords.latitude, pos.coords.longitude),
          () => window.alert("位置情報が取得できませんでした。")
        );
      } else {
        window.alert("本ブラウザではGeolocationが使えません");
      }
    },
    zoomUpdated (zoom) {
      this.zoom = zoom;
    },
    centerUpdated (center) {
      this.center = center;
    },
    boundsUpdated (bounds) {
      this.bounds = bounds;
    },
    validate() {
      return this.$refs.form.validate()
    },
    availability(obj) {
      return moment(obj.application_start) <= moment.utc() && (moment(obj.application_end) >= moment.utc() || obj.application_end === null)
    },
    select_stop(stops) {
      this.busstop_list = stops
      this.dialog = true
    },
    reset() {
      this.$refs.form.reset()
    },
    search() {
      // Items have already been loaded
      if (this.busstop_list.length > 0) return

      // Items have already been requested
      if (this.isLoading) return
      this.isLoading = true

      axios.get(
          "/api/1/stop_names"
        ).then(res => {
          this.busstop_list = res.data.result.stops
        })
        .catch(err => {
          this.text = err
          this.snackbar = true
        })
        .finally(() => {
          this.isLoading = false
        })
    }
  },
  watch: {
    center() {
      axios.get(
        "/api/v1.0/stop_search", {
          params:{
            type: "latlng",
            lat: this.center.lat,
            lng: this.center.lng,
            radius: 500
          }
        }
      ).then(res => {
        this.busstop_list = res.data.result.stops
      })
      .catch(err => {
        this.text = err
        this.snackbar = true
      })
      .finally(() => {
        this.isLoading = false
      })
    },
  },
}
</script>
