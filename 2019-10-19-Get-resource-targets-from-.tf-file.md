---
templateKey: blog-post
title:  "Terraformのtargetをfileから抽出する"
date:   2019-10-19 15:08:00 +0900
categories: terraform
---

terraformを使ってると、一発で全部のリソースじゃなくて一部のリソースだけapplyしたくなることがある。ファイル単位で。ファイルを開いていちいちリソース名を確認してから `-target` オプションを書くのがほんとにトホホ。。。という感じでめんどくさい。

そこで、ファイルからリソース名を抽出する方法を考えた。

```
$ grep "^resource" ./ecs.tf | cut -d ' ' -f 2- | sed 's/"\(.*\)"\s\+"\(.*\)"\s\+{/\1.\2/'
```

↑のコマンドでリソースだけ抜き出すことはできた。これを引数の形に加工して変数に格納する。

```
$ resources=$(grep "^resource" ./ecs.tf | cut -d ' ' -f 2- | sed 's/"\(.*\)"\s\+"\(.*\)"\s\+{/\1.\2/' | xargs echo | sed 's/ / -target=/g')
```

そして `terraform plan` したらうまくいった。

```
$ terraform plan -target=$resources
```

シェルスクリプトにする。

plan.sh

```sh
#!/usr/bin/env bash

set -euo pipefail

scriptpath=${0%%.sh}
execname=${scriptpath##*/}

filename=$1
shift

resources=$(grep "^resource" $filename \
    | cut -d ' ' -f 2- \
    | sed 's/"\(.*\)"\s\+"\(.*\)"\s\+{/\1.\2/' \
    | xargs echo \
    | sed 's/ / -target=/g')

terraform $execname -target=$resources $@
```

apply.sh という名前でsymlinkを作ってapply用のスクリプトとして使うこともできると思う。
