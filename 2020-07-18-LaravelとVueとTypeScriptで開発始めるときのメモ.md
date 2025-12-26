---
templateKey: blog-post
title: LaravelとVueとTypeScriptで開発始めるときのメモ
date: 2020-07-18
---

LaravelとVueで開発始めるのは簡単なのだが、TypeScriptをやろうとするといくつかエラーが出たのでメモ。

まず、 app.js を app.ts に変える。

```sh
mv resources/js/app.js resources/js/app.ts
```

そして、いつも忘れがちだが app.ts 内の Vue のインポート方法を変える。

```typescript
window.Vue = require('vue');
// ↓
import Vue from 'vue';
```

あと、tsconfig.jsonがないと叱られるのでプロジェクトルートにファイルを作成する。[Vue公式ドキュメントから拝借](https://jp.vuejs.org/v2/guide/typescript.html)

```json
{
  "compilerOptions": {
    "target": "es5",
    "strict": true,
    "module": "es2015",
    "moduleResolution": "node"
  }
}
```

そして webpack.mix.js を書き換える。

```typescript
mix.js('resources/js/app.js', 'public/js')
    .sass('resources/sass/app.scss', 'public/css');
// ↓
mix.ts('resources/js/app.ts', 'public/js')
    .sass('resources/sass/app.scss', 'public/css');
```

npm run dev してコンパイル通れば成功。

[Laravel Mixのドキュメント](https://laravel-mix.com/docs/5.0/mixjs) に、

> Simply update your mix.js() call to mix.ts(), and then use the exact same set of arguments.  
> Of course, you'll still want to do the necessary tweeks like creating tsconfig.json file and installing DefinitelyTyped, but everything else should be taken care of.

と書いてあるので、最初はこれだけ書き変えれば良いのかなんて楽なんだと思ってたけど当然それだけではダメでした。残念。
