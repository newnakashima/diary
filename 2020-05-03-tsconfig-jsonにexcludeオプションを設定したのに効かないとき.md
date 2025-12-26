---
templateKey: blog-post
title: tsconfig.jsonにexcludeオプションを設定したのに効かないとき
date: 2020-05-03T02:15:06.220Z
description: ""
tags:
  - TypeScript
  - tsconfig.json
---
tsconfig.jsonに下記の項目を設定した。

```json
{
  (省略)
  "exclude": [
    "node_modules"
  ]
}
```

でtscしてみると下記のエラーが出ることがある。

```
../node_modules/@types/d3-array/index.d.ts:236:93 - error TS2583: Cannot find name 'Map'. Do you need to change your target library? Try changing the `lib` compiler option to es2015 or later.
```

excludeでnode_modulesを設定してるのにnode_modules配下のTSファイルをコンパイルしようとしているっぽい。ぐぐったら下記のページを見つけた。

[node.js - "exclude" property of tsconfig.json is not being respected - Stack Overflow](https://stackoverflow.com/questions/34312252/exclude-property-of-tsconfig-json-is-not-being-respected)

`compilerOptions`の`skipLibCheck`を`true`にすれば良いようだ。

エラーメッセージみて従おうとするとターゲットのECMAスクリプトバージョンをあげたくなってしまうが、多分それだと意図した動きにならない。node_modules配下をコンパイルの対象から完全に外すには、excludeを設定した上で依存ライブラリもコンパイル対象から外せばよいらしい。

[tsconfig.jsonの公式ドキュメント](https://www.typescriptlang.org/tsconfig#skipLibCheck)をみると、このオプション使いたいと思うのはnode_modulesに同じライブラリが2回以上入ってるときだからyarnを使うのを検討せよと書いてある。多分そういうことではないがと思いながらyarn使ってみたらやっぱりだめだった。

TypeScriptをグローバルインストールではなくてローカルインストールしてるとかも関係してそうではある。ただ

- package.jsonにtypescriptのバージョンまで入れたい
- フロントエンドの開発にDocker使いたくない（イメージ・コンテナの管理とか手間だし）

以上の理由によりTypeScriptもプロジェクトローカルにインストールしたいんだよな。。。

まあこの方法でやってみて色々不都合でてきたらdockerとかグローバルインストールとか検討する。CI回すときもTypeScript入りのイメージでビルドしたほうが時間短縮できそうではある。