const path = require('path')
const MomentLocalesPlugin = require('moment-locales-webpack-plugin');

module.exports = {
  lintOnSave: true,
  chainWebpack: config => {
    config
      .entry("app")
      .clear()
      .add("./client/app/src/main.js")
      .end();
    config.resolve.alias
      .set("@", path.join(__dirname, "./client/app/src"))
  },
  configureWebpack: {
    plugins: [
      new MomentLocalesPlugin({
        localesToKeep: ['es-us', 'ja'],
      }),
    ]
  },
  outputDir: path.join(__dirname, "./client/dist"),
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000",
      },
    },
  },
}
