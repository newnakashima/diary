---
templateKey: blog-post
title: typescript-eslintでno-unused-varsをoffにする
date: 2020-05-04T07:48:45.389Z
tags:
  - TypeScript
  - ESLint
  - JSX
---
`.eslintrc.js`に下記の設定を追加する。

```javascript
module.exports = {
  // 省略
  "rules": {
    "@typescript-eslint/no-unused-vars": ["off"]
  }
};
```

ESLintの公式ドキュメントとかだと、`"ルール名": "off"`って書き方がしてあったけど、TypeScriptの場合はルール名は `@typescript-eslint/no-unused-vars` だし、値は配列にしてやらないといけないっぽい。

react-scriptsで`yarn start` で開発サーバーが立ち上がるのは良いんだけど、Vue CLIと違ってESLintが自動で動かないの地味に嫌だなあと思っていた。JSXだとコンポーネント呼び出すだけじゃunusedのwarningが大量に出てくるからoffにした😭  
renderメソッドのデータ型とかいちいち書くのもアレかも知んないけどlinterあるとなんか安心する。

普通のlinterが使えないのはJSXのバッドなところだなと感じた。