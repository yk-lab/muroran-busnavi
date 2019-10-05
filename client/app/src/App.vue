<template>
<v-app>
  <v-app-bar app color="indigo" dark>
    <v-toolbar-title :to="{name: 'Home'}">むろらんバスなび</v-toolbar-title>
    <template v-slot:extension>
      <v-tabs
        align-with-title
        background-color="transparent"
      >
        <v-tab :to="{name: 'Home'}">時刻検索</v-tab>
        <v-tab :to="{name: 'Stops'}">バス停検索</v-tab>
      </v-tabs>
    </template>
  </v-app-bar>

  <!-- Sizes your content based upon application components -->
  <v-content>

    <!-- Provides the application the proper gutter -->
    <v-container fluid>

      <!-- If using vue-router -->
      <router-view></router-view>
    </v-container>
  </v-content>

  <v-footer padless dark>
    <v-card
      flat
      tile
      width="100%"
      class="indigo lighten-1 white--text text-center"
    >
      <v-card-text>
        <v-btn
          v-for="icon in icons"
          :key="icon"
          class="mx-4 white--text"
          icon
        >
          <v-icon size="24px">{{ icon }}</v-icon>
        </v-btn>
      </v-card-text>

      <v-card-text class="white--text pt-0">
        このサイトやこのサイトの情報を利用したことに起因するいかなる被害、損害について責任を負いかねます。
      </v-card-text>

      <v-divider></v-divider>

      <v-card-text class="white--text">
        {{ new Date().getFullYear() }} — <strong>むろらんバスなび</strong>
      </v-card-text>
    </v-card>
    <!-- <v-subheader>注意事項</v-subheader>
    以下の事項についてあらかじめご了承ください
    このサイトやこのサイトの情報を利用したことに起因するいかなる被害、損害について責任を負いかねます
    予告なくサービス提供の中止、停止を行う場合があります
    データの不備がないように万全を期していますがデータに誤りがある場合があります
    プログラム、アルゴリズムに不備がないように万全を期していますが誤りがある場合があります
    一部のデータは元データを総合的に判断して加筆・修正などを行っております
    時刻表などのデータについては以下を使用しています
    道南バス
    むろらんオープンデータライブラリ
    GitHub: aruneko/DonanBusGTFS 道南バスGTFS化プロジェクト
    GitHub: yk-lab/DonanBusGTFS (forked from aruneko/DonanBusGTFS)
    提供範囲
    道南バス
    室蘭市内線
    平成28年12月1日改正ダイヤ
    平成29年4月1日改正ダイヤ
    年末年始特別ダイヤを含む
    平成30年4月1日改正ダイヤ
    平成31年4月1日改正ダイヤ -->
  </v-footer>
</v-app>
</template>

<script>
  export default {
    name: 'App',
    data: () => ({
      icons: [
        "mdi-github-circle",
        "mdi-twitter-circle",
        "mdi-facebook-box",
        "mdi-youtube"
      ]
    })
  }
</script>
