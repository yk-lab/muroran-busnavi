<template id="">
<v-row>
  <template v-if="stoptimes && stoptimes.length > 0">
    <v-col v-for="(stoptime, i) in stoptimes" :key="i" cols="12">
      <v-card>
        <v-card-title class="overline">{{sec2time(stoptime.departure.departure_time)}}発 → {{sec2time(stoptime.arrival.arrival_time)}}着</v-card-title>
        <v-list-item three-line>
          <v-list-item-content>
            <v-list-item-title class="headline">
              {{sec2time(stoptime.departure.departure_time)}}
              {{stoptime.departure.position.stop.now_name.name}}
              <span v-if="stoptime.departure.position.sub_name">({{stoptime.departure.position.sub_name}})</span>
              <v-btn text small :to="{name: 'Stop', params: {
                id: stoptime.departure.position.stop_code
              }, query: {
                departure: stoptime.departure.position.id
              }}" target="_blank"><v-icon small dense>mdi-map-marker</v-icon>地図</v-btn>
            </v-list-item-title>
            <v-list-item-subtitle class="text--primary d-flex align-stretch">
              <div class="align-self-center pa-2">
                <v-icon>mdi-arrow-down-thick</v-icon>
              </div>
              <v-layout wrap class="align-content-center">
                <v-flex xs12>
                  {{stoptime.arrival.trip.route.route_short_name}}
                  {{stoptime.arrival.trip.route.route_long_name}}
                  <span v-if="stoptime.arrival.trip.route.route_desc">({{stoptime.arrival.trip.route.route_desc}})</span>
                </v-flex>
                <v-flex v-if="fare[stoptime.departure.trip.route_code + '/' + stoptime.departure.position.id + '/' + stoptime.arrival.position.id]" xs12 sm4 md2 xl1>運賃: {{fare[stoptime.departure.trip.route_code + '/' + stoptime.departure.position.id + '/' + stoptime.arrival.position.id].fare_attribute.price}}円</v-flex>
                <v-flex xs12 sm4 md2 xl1>所要時間: 約{{Math.round((stoptime.arrival.arrival_time - stoptime.departure.departure_time)/60)}}分</v-flex>
                <v-flex xs12 sm4 md2 xl1><v-btn text x-small @click="get_passing_times(stoptime)"><v-icon small dense left>mdi-bus</v-icon>通過停留所</v-btn></v-flex>
              </v-layout>
            </v-list-item-subtitle>
            <v-list-item-title class="headline">
              {{sec2time(stoptime.arrival.arrival_time)}}
              {{stoptime.arrival.position.stop.now_name.name}}
              <span v-if="stoptime.arrival.position.sub_name">({{stoptime.arrival.position.sub_name}})</span>
              <v-btn text small :to="{name: 'Stop', params: {
                id: stoptime.arrival.position.stop_code
              }, query: {
                arrival: stoptime.arrival.position.id
              }}" target="_blank"><v-icon small dense>mdi-map-marker</v-icon>地図</v-btn>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-card>
    </v-col>
  </template>
  <template v-else-if="stoptimes">
    <v-col cols="12">
      <v-card>
        <v-card-title>
          条件に一致するバスはありませんでした
        </v-card-title>
      </v-card>
    </v-col>
  </template>
  <template v-else>
    <v-col v-for="n of 5" cols="12" :key="n">
      <v-card>
        <StopTimesItemLoader />
      </v-card>
    </v-col>
  </template>
  <v-dialog v-model="dialog" width="600px">
    <v-card>
      <v-card-title>
        <span class="headline" v-if="passing_times">
          {{passing_times[0].trip.route.route_short_name}}
          {{passing_times[0].trip.route.route_long_name}}
        </span>
        <span class="overline" v-if="passing_times">
          ({{passing_times[0].position.stop.now_name.name}}
          →
          {{passing_times[passing_times.length - 1].position.stop.now_name.name}})
        </span>
      </v-card-title>
      <v-timeline dense align-top>
        <v-timeline-item small fill-dot icon="mdi-map-marker" v-for="time in passing_times" :key="`${time.trip_code}_${time.stop_sequence}`">
          {{sec2time(time.arrival_time)}} {{time.position.stop.now_name.name}}
          <v-btn text small :to="{name: 'Stop', params: {
            id: time.position.stop_code
          }, query: {
            passing: time.position.id
          }}" target="_blank"><v-icon small dense>mdi-map-marker</v-icon>地図</v-btn>
        </v-timeline-item>
      </v-timeline>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="" text @click="dialog = false">閉じる</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-snackbar v-model="snackbar">
    {{ text }}
    <v-btn color="pink" text @click="snackbar = false">
      Close
    </v-btn>
  </v-snackbar>
</v-row>
</template>

<style lang="scss" media="screen">

</style>

<script type="text/javascript">
import axios from "axios"
import moment from "moment"

import StopTimesItemLoader from "@/components/StopTimesItemLoader"

export default {
  props: {
    from: {
      type: String,
      default: null
    },
    to: {
      type: String,
      default: null
    },
    date: {
      type: String,
      default: null
    },
    time: {
      type: String,
      default: null
    },
  },
  data: () => ({
    stoptimes: null,
    fare: null,
    text: "",
    snackbar: false,
    dialog: false,
    passing_times: null,
    passing_fare: null,
  }),
  components: {
    StopTimesItemLoader
  },
  created() {
    axios.get(
        "/api/1/stoptimes", {
          params:{
            from_busstop: this.$route.query.from_busstop,
            to_busstop: this.$route.query.to_busstop,
            date: this.$route.query.date,
            time: this.$route.query.time
          }
        }
      ).then(res => {
        this.fare = res.data.fare
        this.stoptimes = res.data.times
      })
      .catch(err => {
        this.text = err
        this.snackbar = true
      })
      .finally(() => {})
  },
  methods: {
    sec2time(sec) {
      return moment().startOf('day').seconds(sec).format('H:mm');
    },
    get_passing_times(stoptime){
      this.passing_times = null
      this.dialog = true
      axios.get(
          "/api/1/passing_times", {
            params:{
              origin: stoptime.departure.stop_sequence,
              destination: stoptime.arrival.stop_sequence,
              trip: stoptime.departure.trip_code
            }
          }
        ).then(res => {
          this.passing_fare = res.data.fare
          this.passing_times = res.data.times
        })
        .catch(err => {
          this.text = err
          this.snackbar = true
        })
        .finally(() => {})
    }
  }
}
</script>
