<template id="">
  <AsyncComponent />
</template>

<style lang="scss" media="screen">

</style>

<script type="text/javascript">
import LoadView from "@/components/LoadView"

const AsyncComponent = () => ({
  // ロードすべきコンポーネント (Promiseであるべき)
  component: import('@/pages/StopTimes.vue'),
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


export default {
  components: {
    AsyncComponent
  },
}
</script>
