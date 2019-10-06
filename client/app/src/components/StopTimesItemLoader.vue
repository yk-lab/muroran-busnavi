<template>
<ContentLoader
  :height="140"
  :width="600"
  :speed="2"
  primaryColor="#dde0e3"
  secondaryColor="#ecebeb"
>
  <rect x="25" y="15" rx="5" ry="5" width="380" height="10" />
  <rect x="25" y="35" rx="5" ry="5" width="380" height="20" />
  <rect x="50" y="60" rx="5" ry="5" width="220" height="15" />
  <rect x="50" y="80" rx="5" ry="5" width="80" height="15" />
  <rect x="150" y="80" rx="5" ry="5" width="80" height="15" />
  <rect x="250" y="80" rx="5" ry="5" width="80" height="15" />
  <rect x="25" y="100" rx="5" ry="5" width="380" height="20" />
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
