import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

function loadView (view) {
  return () => import(/* webpackChunkName: "view-[request]" */ `@/views/${view}.vue`)
}

const routes = [
  {
    path: '/', name: "Home", component: loadView('Home'),
  },
  {
    path: '/stops', name: "Stops", component: loadView('Stops'),
  },
  {
    path: '/stoptimes', name: "StopTimes", component: loadView('StopTimes')
  },
  {
    path: '/stops/:id', name: "Stop", component: loadView('Stop')
  },
]

const router  = new VueRouter({
  routes,
  mode: 'history',
})
export default router;
