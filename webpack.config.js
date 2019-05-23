const webpack = require('webpack');

module.exports = {
  // モード値を production に設定すると最適化された状態で、
  // development に設定するとソースマップ有効でJSファイルが出力される
  mode: "production",
  entry: {
    main: "./static/src/main.ts",
    stop_times: "./static/src/stop_times.ts",
    stop_search: "./static/src/stop_search.tsx"
  },  // ファイルの出力設定
  output: {
    //  出力ファイルのディレクトリ名
    path: `${__dirname}/static/dist`,
    // 出力ファイル名
    filename: '[name].js',
  },
  plugins: [
    // bootstrap のコードから jQuery が直接見えるように
    // http://getbootstrap.com/docs/4.0/getting-started/webpack/#importing-javascript
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery",
      Popper: ["popper.js", "default"]
    })
  ],
  module: {
    rules: [
      // Sassファイルの読み込みとコンパイル
      {
        test: /\.scss$/, // 対象となるファイルの拡張子
        use: [
          // linkタグに出力する機能
          "style-loader",
          // CSSをバンドルするための機能
          {
            loader: "css-loader",
            options: {
              // オプションでCSS内のurl()メソッドの取り込みを禁止する
              url: false,

              // 0 => no loaders (default);
              // 1 => postcss-loader;
              // 2 => postcss-loader, sass-loader
              importLoaders: 2
            }
          },
          {
            loader: "sass-loader",
          }
        ]
      },
      {
        // 対象となるファイルの拡張子(cssのみ)
        test: /\.css$/,
        // Sassファイルの読み込みとコンパイル
        use: [
          // スタイルシートをJSからlinkタグに展開する機能
          "style-loader",
          // CSSをバンドルするための機能
          "css-loader"
        ]
      },
      {
        // 拡張子 .ts の場合
        test: /\.tsx?$/,
        // TypeScript をコンパイルする
        use: "ts-loader"
      },
      {
        test: /\.(woff|woff2|eot|ttf|svg)$/,
        // loader: 'file-loader?name=../font/[name].[ext]'
        use: [
            {
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath : '../font/',
                    publicPath : (url, resourcePath, context) => `/static/font/${url}`
                }
            }
        ]
      }
    ]
  },
  // import 文で .ts ファイルを解決するため
  resolve: {
    extensions: [".ts", ".tsx", ".js"]
  }
};
