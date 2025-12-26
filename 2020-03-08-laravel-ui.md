---
templateKey: blog-post
title:  "laravel/uiでフロントエンドの開発環境をサクッとつくる"
date:   2020-03-08 12:45:43 +0900
categories: laravel php javascript frontend
---

まあ[公式サイト](https://readouble.com/laravel/6.x/ja/frontend.html)に書いてあるとおりなんだけど。  
たとえばBootstrapとVueの環境つくりたい場合は下記のコマンド打つだけでサクッとできる。

```
composer require laravel/ui --dev
php artisan ui bootstrap
php artisan ui vue
```

blade.phpファイルでvueのコンポーネント使うことも可能。

```
@extends('layouts.app')

@section('content')
    <example-component></example-component>
@endsection
```

とりあえず始めるだけならwebpackのこととかnpmのこととかなんも考えなくていい。ビルドして動かすには下記のコマンドを打つ。

```
npm install
npm run dev
```

小規模かつスピードが求められる開発では一人のエンジニアがバックエンドもフロントエンドもやんないといけないことあると思う。

そういうときは一個のコードベースで全て把握できるので便利そう。  

まだまだバックエンドは複雑なビジネスロジックがあってテーブルの結合に次ぐ結合が必要なプロジェクトとかある（ダッシュボード系のやつとか）。  

サーバーレス&NoSQLだとゆくゆくつらい思いをすることになる気がする。

あと、バックエンドばっかりやってるエンジニアがフロント側も担当しないと行けないとき。色々しらべて環境作りやらなくてもlaravelがいい感じに作ってくれる。

LaravelはWEB業務システム受託開発で生きてる奴らの救世主。。。

