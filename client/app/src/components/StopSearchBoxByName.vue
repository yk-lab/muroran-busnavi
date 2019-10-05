<template id="">
<v-form ref="form" v-model="valid">
  <v-layout wrap>
    <v-flex sm6 class="px-4">
      <v-autocomplete v-model="busstop" :items="busstop_list" :loading="isLoading" :search-input.sync="searchbox" item-text="name" item-value="stop_code" cache-items label="停留所名" prepend-icon="mdi-bus" no-data-text="一致する停留所は見つかりませんでした" :rules="nameRules"></v-autocomplete>
    </v-flex>
  </v-layout>
  <v-snackbar v-model="snackbar">
    {{ text }}
    <v-btn color="pink" text @click="snackbar = false">
      Close
    </v-btn>
  </v-snackbar>
</v-form>
</template>

<script>
// import moment from "moment/moment"
import axios from "axios"

export default {
  data: () => ({
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
  methods: {
    validate() {
      return this.$refs.form.validate()
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
    searchbox() {
      this.search()
    },
    busstop() {
      this.$router.push({ name: 'Stop', params: {
        id: this.busstop,
      }})
    }
  },
}
</script>
