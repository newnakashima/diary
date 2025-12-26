---
templateKey: blog-post
title: macでRubyをビルドしたときにRUBY_FUNCTION_NAME_STRINGのerrorが出た場合
date: 2022-03-01 19:57:38
tags:
  - Ruby
  - mac
---

```sh
sudo rm -rf /Library/Developer/CommandLineTools
sudo xcode-select --install
```
で解決した（自分の場合は）。

---

久しぶりにrbenvを使って違うバージョンのRuby使ってみよっかなって思ったときに `RUBY_FUNCTION_NAME_STRING` が未定義だとかいうエラーが出てハマった。Homebrewから入れると大丈夫だけど、これはコンパイル済みのものを落としてきているだけなので問題は解決していない。

https://github.com/rbenv/ruby-build/issues/1431

上記のissueに書いてある対応法はほとんどすべて試したがダメ。もうRubyやめるか、と思っていたときに、今まで見落としていたあるコメントが目に入った。

https://github.com/rbenv/ruby-build/issues/1409#issuecomment-752223239
> Updating of the command tools helped me:
>
> ```sh
> sudo rm -rf /Library/Developer/CommandLineTools
> sudo xcode-select --install
> ```

なるほど……？　と思い実行して、その後改めて `rbenv install 3.1.1` とかやってみたらビルドできた。Xcodeのコマンドラインツールがおかしいという場合もあるらしい。

まあ、コマンドラインツールのインストールし直しでだいぶ時間がふっとんだけど。そしてrbenvは新しいバージョンをインストールするといつもビルドが走る。ビルド待ちの間にmacのファンが回るのを聴きながらYouTubeでニュース見てるといつの間にか不毛な一日がまた終わってく。
