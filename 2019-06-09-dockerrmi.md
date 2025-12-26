---
templateKey: blog-post
title: "dockerでREPOSITORYが<none>になってるイメージを消す"
date: 2019-06-09 00:00:00 +09:00
---

Dockerを使ってるとイメージを更新したときとかにREPOSITORYが\<none\>になってるやつが生まれてくる。

こういうやつ。
```
$ docker images
REPOSITORY             TAG                 IMAGE ID            CREATED             SIZE
kotlintrial            latest              858cfd2443af        About an hour ago   826MB
my-appliaction         latest              58a75a473622        44 hours ago        492MB
<none>                 <none>              23b086fc3865        44 hours ago        494MB
<none>                 <none>              34dcbcbe22c5        44 hours ago        494MB
my-application         latest              2c12748b798f        3 days ago          505MB
<none>                 <none>              4c895ee3d84c        3 days ago          505MB
...
```

この\<none\>だけを消したいとき、以前はこんな感じで無理やりやっていた。

```
$ docker rmi $(docker images | grep '<none>' | awk '{print $3}')
```

でも普通に考えたら公式で提供してる手段があるはずなので調べたらあった。

[http://docs.docker.jp/engine/reference/commandline/images.html](http://docs.docker.jp/engine/reference/commandline/images.html){:target="_blank"}

下記のようにやれば同じことがdockerコマンドだけでできる。

```
$ docker rmi $(docker images -f "dangling=true" -q)
```

Docker使う上ではdockerコマンドでできることはdockerコマンドだけでやったほうが良いと思われるが、なんとなくしゃらくささを感じるのも事実。テキスト処理コマンドのパワーって特定のなにかに依存しないことだとも思うし。。
