import Vue from 'vue'
import 'babel-polyfill'
import vuetify from '@/plugins/vuetify'
import router from '@/router'

import LoadView from "@/components/LoadView"

import { Icon }  from 'leaflet'
import 'leaflet/dist/leaflet.css'

import * as Sentry from '@sentry/browser';
import * as Integrations from '@sentry/integrations';

import config from 'config';

Vue.config.productionTip = false

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Sentry.init({
  environment: process.env.NODE_ENV,
  dsn: config.sentry.dsn,
  integrations: [new Integrations.Vue({Vue, attachProps: true, logErrors: true})],
  beforeSend(event, hint) {
    // Check if it is an exception, and if so, show the report dialog
    if (event.exception) {
      Sentry.showReportDialog({ eventId: event.event_id })
    }
    return event
  }
});

const AsyncComponent = () => ({
  // ロードすべきコンポーネント (Promiseであるべき)
  component: import('@/App.vue'),
  // 非同期コンポーネントのロード中に使うコンポーネント
  loading: LoadView,
  // ロード失敗時に使うコンポーネント
  // error: ErrorComponent,
  // loading コンポーネントが表示されるまでの遅延時間。 デフォルト: 200ms
  delay: 0,
  // timeout が設定され経過すると、error コンポーネントが表示されます。
  // デフォルト: Infinity
  timeout: 3000
})

new Vue({
  router,
  vuetify,
  render: h => h(AsyncComponent)
}).$mount('#app')
