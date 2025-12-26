---
templateKey: blog-post
title: Railsのlink_toでDELETEメソッドが使えないとき
date: 2022-02-23 19:15:35
tags:
  - Ruby
  - Rails
  - link_to
---

Railsは7.0.0。Rubyは3.0.3。

Railsのlink_toで以下のようなやつを書いていた。

```
= link_to 'ログアウト', destroy_user_session_path, :method => :delete
```

しかし「idがsign_outのユーザーはいません」的なエラーが帰ってきていた。しかもメソッドがGETになってしまっている。はじめはDeviseがおかしいのかと思ったけど違うようだ。

Turboを使っているからなのか、どうも `:method => :delete` をつけてもDELETEになってくれないようだった。色々ググっていたら下記を見つけた。

https://github.com/heartcombo/devise/issues/4486#issuecomment-444534885

つまり、`link_to` ではなくて `button_to` を使えばいいっぽい。

```
= button_to 'ログアウト', destroy_user_session_path, :method => :delete
```

他の方法で頑張る場合は自分でAjaxの処理を書かないといけないらしい。

最近Railsはじめたけどかったるいことが多い。正直生産性が高いとは思えない。すごくみじめな気持ちになる。なんでこんなのが流行っていたのかわからない。けど修行だと思って頑張る、、、
