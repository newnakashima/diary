---
templateKey: blog-post
title:  "Electronのインストール"
date:   2020-02-13 00:07:04 +0900
categories: electron
---

Electronでアプリ作ろうかと思って `node install --save-dev electron` とかやってみたのだが `> node install.js` とか出たまま一向にインストールされる気配がない。

何かがおかしいと思ってぐぐったら下記のissueを見つけた。

[https://github.com/electron/electron/issues/21069](https://www.electronjs.org/docs/tutorial/installation)

> It may seem stuck, but it is actually downloading the release zip of Electron from GitHub.
> But GitHub's downloads are currently slow (~40KB/s for me) so just give it a while.
> The zip is around 60 MB. You can see the progress in the Network tab of the Activity Monitor in macOS.

アクティビティモニタ開けばファイルダウンロードが進んでるのがわかるよ、って書いてあるんだけど、たしかにアクティビティモニタ開いたら見えたけど、でも数十分もうんともすんとも言わないのは流石にあんまりじゃないか。

せめて今どのくらいダウンロード終わったよ、っていうプログレスバー的なやつは出したほうが良いんじゃないだろうか。

で、待つこと30分。結果、 `ECONNRESET` のエラーが出てた。公式サイトにはこうある。

[https://www.electronjs.org/docs/tutorial/installation](https://www.electronjs.org/docs/tutorial/installation)

> When running npm install electron, some users occasionally encounter installation errors.
> 
> In almost all cases, these errors are the result of network problems and not actual issues with the electron npm package. Errors like ELIFECYCLE, EAI_AGAIN, ECONNRESET, and ETIMEDOUT are all indications of such network problems. The best resolution is to try switching networks, or wait a bit and try installing again.

ふーん。ネットワークのせいね。そうかそうか。。同じ問題でこんなに困ってる人が世界中にいるのもすべてネットワークが悪い。ネットなんてこの世になければよかったんだ、、、そんな気持ちにさせられる。

10回くらい `npm i -D electron` を叩いたらいつの間にかインストールされていた。`--unsafe-perm=true` とかも試してみたけど無関係っぽかった。`--verbose` オプションをつけても肝心の `> node install.js` で沈黙するところでは何も情報を出してくれないので無意味だった。

**Electronのインストールには運が必要。**

とてもためになる教訓が得られた。
