<template id="">
<v-form ref="form" v-model="valid">
  <v-card max-width="620" class="mx-auto">
    <v-card-title>時刻検索</v-card-title>
    <v-layout wrap>
      <v-flex sm6 class="px-4">
        <v-autocomplete v-model="from_busstop" :items="busstop_list" :loading="f_isLoading" :search-input.sync="from_search" item-text="name" item-value="id" cache-items label="乗車" prepend-icon="mdi-bus" no-data-text="一致する停留所は見つかりませんでした" :rules="nameRules"></v-autocomplete>
      </v-flex>
      <v-flex sm6 class="px-4">
        <v-autocomplete v-model="to_busstop" :items="busstop_list" :loading="t_isLoading" :search-input.sync="to_search" item-text="name" item-value="id" cache-items label="下車" prepend-icon="mdi-bus" no-data-text="一致する停留所は見つかりませんでした" :rules="nameRules"></v-autocomplete>
      </v-flex>
      <v-dialog ref="dialog1" v-model="modal1" :return-value.sync="date" persistent full-width width="290px">
        <template v-slot:activator="{ on }">
          <v-flex sm6 class="px-4">
            <v-text-field v-model="date" label="日付" prepend-icon="mdi-calendar-month" readonly v-on="on"></v-text-field>
          </v-flex>
        </template>
        <v-date-picker
          v-model="date"
          locale="jp-ja"
          :day-format="date => new Date(date).getDate()"
          scrollable
        >
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="modal1 = false">キャンセル</v-btn>
          <v-btn text color="primary" @click="$refs.dialog1.save(date)">OK</v-btn>
        </v-date-picker>
      </v-dialog>
      <v-dialog ref="dialog2" v-model="modal2" :return-value.sync="time" persistent full-width width="290px">
        <template v-slot:activator="{ on }">
          <v-flex sm6 class="px-4">
            <v-text-field v-model="time" label="時間" prepend-icon="mdi-clock-outline" readonly v-on="on"></v-text-field>
          </v-flex>
        </template>
        <v-time-picker v-if="modal2" v-model="time" format="24hr" full-width scrollable>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="modal2 = false">キャンセル</v-btn>
          <v-btn text color="primary" @click="$refs.dialog2.save(time)">OK</v-btn>
        </v-time-picker>
      </v-dialog>
    </v-layout>
    <v-card-actions>
      <v-btn :disabled="!valid" color="success" @click="validate" :to="{ path: 'stoptimes', query: {
        from_busstop: from_busstop,
        to_busstop: to_busstop,
        date: date,
        time: time
      }}">
        検索
      </v-btn>

      <v-btn color="error" @click="reset">
        リセット
      </v-btn>
    </v-card-actions>
  </v-card>
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

export default {
  data: () => ({
    f_isLoading: false,
    t_isLoading: false,
    modal1: false,
    modal2: false,
    date: moment().format().substr(0, 10),
    time: moment().format().substr(11, 5),
    valid: true,
    from_busstop: null,
    to_busstop: null,
    busstop_list: [],
    nameRules: [
      v => !!v || '必須です',
    ],
    snackbar: false,
    text: null,
    from_search: null,
    to_search: null,
  }),
  methods: {
    validate() {
      return this.$refs.form.validate()
    },
    select_stop(stops, mode) {
      this.busstop_list = stops
      this.dialog_mode = mode
      this.dialog = true
    },
    reset() {
      this.$refs.form.reset()
    },
    search(mode) {
      // Items have already been loaded
      if (this.busstop_list.length > 0) return

      // Items have already been requested
      if (mode === "from") {
        if (this.f_isLoading) return
        this.f_isLoading = true
      } else if (mode === "to") {
        if (this.t_isLoading) return
        this.t_isLoading = true
      }

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
          if (mode === "from") {
            this.f_isLoading = false
          } else if (mode === "to") {
            this.t_isLoading = false
          }
        })
    }
  },
  watch: {
    from_search() {
      this.search("from")
    },
    to_search() {
      this.search("to")
    }
  },
}
</script>
