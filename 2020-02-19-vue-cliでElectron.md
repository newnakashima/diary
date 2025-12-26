---
templateKey: blog-post
title:  "vue-cliでElectron"
date:   2020-02-19 23:42:28 +0900
categories: vue vue-cli electron
---
Electronアプリをvue-cliを使って開発しよっかなーと思って環境作ってたら、アプリは起動するけど画面に何も表示されない。devtool開いてみると、どうもjsとかcssが読めてない。リソースのパスが `/js/hoge.js` とかになってる。

これはvueで普通にWEBページを作る場合なら問題ないんだろうけど、今回はElectronなのでHTTPで公開してるディレクトリからの絶対パスでは見れるわけがない。試しにビルド後のindex.htmlの各リソースへのhrefを`./js/hoge.js` みたいな感じにしてあげたら普通に動いた。

ネットで検索したら、`public/index.html` に `<base href="./">`って入れればいいよ、と言ってる人とかもいたけど効果なし。
更にググったらそのものズバリな処方箋を見つけた。

[Vue-CLI3でbuildすると画面が真っ白になる](https://qiita.com/heyheyww/items/5d06936745118045a308)

vue.config.jsファイルに`publicPath: './'` と書くだけで解決。このへんの情報、Electron側でもVue側でもいいのでドキュメントの割と最初の方に書いといてほしい。。。

ちなみにvue-cli 4.2.2、Electron 8.0.1でも動いた。

