---
templateKey: blog-post
title: VSCodeでシステムのSolargraphを使うときのメモ
date: 2022-02-28 13:59:36
tags:
  - Ruby
  - VSCode
  - Solargraph
---

## 結論
先に結論を書いておくと、以下のようにsettings.jsonに書けば解決した。

```json
{
    // 省略
    "solargraph.useBundler": false,
    "solargraph.commandPath": "/usr/local/lib/ruby/gems/3.1.0/bin/solargraph",
    // 省略
}
```

## 結論に至るまで

VSCodeでRuby Solargraphという拡張を使ってSolargraph使おうとしたら以下のようなエラーが表示された。

```
Solargraph gem not found. Run `gem install solargraph` or update your Gemfile.
```

Ruby初心者なので意味がわからず、とりあえず言われた通りのコマンドを実行してインストールしてみた。
が、やはり同じエラーが出る。

パスが通っていないから？　と思い以下のような感じでパスを通した。

```
# ~/.zshrc
export PATH="/usr/local/lib/ruby/gems/3.1.0/bin:$PATH"
```

これでシェルで直接 `solargraph` を実行することはできるようになった。それでもVSCode上ではエラーになる。

色々調べたら、プロジェクトではなくシステムにインストールしてあるSolargraphを使いたい場合は、`solargraph.useBundler` という設定値にfalseを渡してやる必要があるようだ。
なので、settings.jsonに以下のように書いてみた。

```json
{
    // 省略
    "solargraph.useBundler": false,
    // 省略
}
```

でもやっぱりだめ。さらにググると、`solargraph.commandPath` なる設定項目もあるらしい。これが怪しそう。なので、ローカルに入ってるSolargarphのパスを直接指定。

```json
{
    // 省略
    "solargraph.useBundler": false,
    "solargraph.commandPath": "/usr/local/lib/ruby/gems/3.1.0/bin/solargraph",
    // 省略
}
```

動くようになった。

本来はプロジェクトごとにRubyのバージョンも違うだろうし、プロジェクト単位でSolargraphをインストールして使う想定なのだろうが、ちょっとしたスクリプトを書きたい場合などにはシステム側のRubyを使うこともある。頻繁にある。
なので基本はグローバルにインストールされてるSolargraphを使うことにしていきたいと思う。
