<template>
<ContentLoader
  :height="240"
  :width="400"
  :speed="2"
  primaryColor="#f3f3f3"
  secondaryColor="#ecebeb"
>
  <rect x="8" y="0" rx="0" ry="0" width="184" height="24" />
  <rect x="8" y="32" rx="0" ry="0" width="384" height="80" />
  <rect x="8" y="120" rx="0" ry="0" width="384" height="16" />
  <rect x="8" y="144" rx="0" ry="0" width="384" height="16" />
  <rect x="8" y="168" rx="0" ry="0" width="384" height="16" />
  <rect x="8" y="192" rx="0" ry="0" width="384" height="16" />
  <rect x="8" y="216" rx="0" ry="0" width="384" height="16" />
</ContentLoader>
</template>

<script type="text/javascript">
import { ContentLoader } from 'vue-content-loader'

export default {
  components: {
    ContentLoader
  }
}
</script>
