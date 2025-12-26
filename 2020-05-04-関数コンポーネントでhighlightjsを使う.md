---
templateKey: blog-post
title: 関数コンポーネントでhighlightjsを使う
date: 2020-05-04T04:11:00.000Z
description: ""
tags:
  - JavaScript
  - highlight.js
  - React
  - NetlifyCMS
---
このブログは [gatsby-starter-netlify-cms](https://github.com/netlify-templates/gatsby-starter-netlify-cms) を使っているのだが、このテンプレートはReact製で、関数コンポーネントで作ってある。

コードブロックをハイライトしたくてhighlight.jsを導入したかったけど、クラスコンポーネントで導入している例はみつけたが関数コンポーネントで導入する方法を調べるのに少し時間がかかった。

クラスコンポーネントの場合はライフサイクルメソッドをフックにして、そこでコードブロックをハイライトすれば良い。

```javascript
export default class Hoge extends React.Component {
  componentDidMount() {
    this.highlight();
  }

  componentDidUpdate() {
    this.highlight();
  }

  highlight = () => {
    document.querySelectorAll("pre code").forEach(block => {
      hljs.highlightBlock(block);
    });
  };

  render() {
    // 省略
  }
}
```

しかし、`componentDidMount()` や `componentDidUpdate()` はクラスコンポーネントでしか使えないようだ。コンポーネントのライフサイクルイベントにアクセスできないと、DOMをレンダリングしてからコードブロックの内容をハイライトする、という処理を実行することができない。

幸い、昨年のv16.8からReact Hooksという仕組みが実装され、関数コンポーネントでもライフサイクルイベントにアクセスできるようになったらしい。以下のように実装した。

```javascript
import React, { useEffect } from 'react';
// 省略

export const Hoge = () => {
  useEffect(() => {
    document.querySelector("pre code").forEach(block => {
      hljs.highlightBlock(block);
    })
  });

  return (
    // 省略
  )
}
```

useEffectという関数でコンポーネントが初期化されたときや更新されたときに処理を入れることができるようになるらしい。

コードブロックに行番号を表示するようにしたのにも一工夫必要だったがそれはまた次回書こうと思う。  
（色々調べたらhighlight.jsを使うよりは今どきはPrismというライブラリを使ったほうが良さそうということがわかった、、、）

---
参考:
- [https://stackoverflow.com/questions/49368326/cant-get-highlight-js-to-highlight-react-rendered-code](https://stackoverflow.com/questions/49368326/cant-get-highlight-js-to-highlight-react-rendered-code)
- [https://github.com/highlightjs/highlight.js/issues/925#issuecomment-466638119](https://github.com/highlightjs/highlight.js/issues/925#issuecomment-466638119)
- [https://www.themikelewis.com/post/highlightjs-with-react](https://www.themikelewis.com/post/highlightjs-with-react)
- [https://itnext.io/add-state-and-lifecycle-methods-to-function-components-with-react-hooks-8e2bdc44d43d](https://itnext.io/add-state-and-lifecycle-methods-to-function-components-with-react-hooks-8e2bdc44d43d)
- [https://ja.reactjs.org/docs/hooks-effect.html](https://ja.reactjs.org/docs/hooks-effect.html)
