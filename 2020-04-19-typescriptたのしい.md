---
templateKey: blog-post
title: TypeScriptたのしい
date: 2020-04-19T13:30:52.014Z
featuredimage: /img/remoteworks458a3421_tp_v.jpg
tags:
  - TypeScript
  - Vue
---
![](/img/remoteworks458a3421_tp_v.jpg)

本当に遅ればせながらだが、やっとTypeScriptを使うようになってきた。というか今日から使い始めた。

最初はVSCode上で色々怒られてめんどくさいなあ、、、とか思っていたけど、guard節を強制させてくる感じとか、asキーワードでキャストする感じとか、モダンな言語という感じがして書いていて気持ちが良い。昔SwiftとかKotlinを触ってた時の感覚を思い出す。

その頃と全く違うのは、エディタの快適さ。VSCodeはTypeScriptを書くときに最も力を発揮するのだとようやく知った。補完は速いし頭いい。Swift、Kotlinで重たいIDEを使ってるときとは段違いに気持ちいい。

ちょっとだけハマったところがあるのでメモ。

### Vue + TypeScriptでforEachが使えない

Vue + TypeScriptで開発してるとforEachが使えないことがある。この場合は、core-jsというライブラリをアップデートするなりバージョン下げるなりすると使えるようになるっぽい。自分の場合は下記のコマンド打ったら使えるようになった。

```
$ npm install --save core-js@3
```

コンパイル時のエラメッセージで、

```
$ npm install --save core-js/modules/es.array.for-each core-js/modules/web.dom-collections.for-each
```

をやれ、みたいなのも出てくるんだけど、そもそもこのコマンド自体がうまくいかなかった。単純にcore-jsを入れ直せば解決した。

（ちなみに最近core-jsは作者が交通事故で収監されることになりメンテされなくなるのでは？　ということでちょっと話題になってた。<https://qiita.com/yumetodo/items/eaf3b97aeae3d8c4a07e>）

### object is possibly null とかいうメッセージがでてコンパイルできない

guard節を書けばいい。多分、以下のような書き方してると↑のメッセージが出る。

```
methods: {
  hoge: function (event: Event): void {
    event.target.querySelector(".my-class").classList.add("fuga");
  }
}
```

下記のようにguard節をつければOK。

```
methods: {
  hoge: function (event: Event): void {
    if (event.target === null) return;
    event.target.querySelector(".my-class").classList.add("fuga");
  }
}
```

### Vueで書いてるのにESlintがJSX関連の警告出してくる

例えば、下記のようなキャストの仕方をすると怒られる。

```
const text = (<HTMLElement>e).innerText;
```

<HTMLElement>の閉じタグがねーぞ、みたいなことを言われてしまう。

これは流石にVueで書いてるんだからESLintの設定とかで無効化できそうだけど、そもそもこのキャストの書き方は読みづらいからasを使ったほうが良さげ。

```
const text = (e as HTMLElement).innerText;
```

- - -

万事こんな感じなので、タイプする量はJSに比べて増える。けれども書き心地は圧倒的にこっちのほうがいい。絶対バグも少ないし。

フロント側のJSはただでさえテストを書くことが少ないので、バグが出にくい書き方を強制されるくらいで丁度いいかな、と思う。Web APIの関数（querySelector()とか）の返り値も都度MDNで調べる癖ができるので勉強にもなる。

あと、型をつけておくとVSCodeの補完が効くようになる。補完が効くの地味に気持ちいい。型無しで、とりあえずanyで書いてても動くんだけど、それだとTypeScriptで書いてる意味がなくなるし恩恵も得られないし、後で型つけるとか絶対やらないし。普段から型ありで書くのが大切なような気がする。

良い言語は良いプログラマーを育てる、ってやつの良い例だ。TypeScript流行ってる理由ようやくわかった。たのしい。

何周周回遅れかはわからないが、これからTypeScriptも頑張っていきたい。

（※画像は **[ぱくたそ https://www.pakutaso.com/](https://www.pakutaso.com/)** 様のフリー素材です）