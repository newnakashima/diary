---
templateKey: blog-post
title: WSLでVagrantのSynced_folder
date: 2020-11-07 00:29:44
tags:
  - WSL
  - Windows
  - Linux
  - Vagrant
---

WSLでVagrant使うの自体はすんなりできたんだけど、いざ `vagrant up` してみたら下記のようなエラーが出てきた。

```
➜  vagrant git:(aws) ✗ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Box 'bento/amazonlinux-2' could not be found. Attempting to find and install...
    default: Box Provider: virtualbox
    default: Box Version: >= 0
==> default: Loading metadata for box 'bento/amazonlinux-2'
    default: URL: https://vagrantcloud.com/bento/amazonlinux-2
==> default: Adding box 'bento/amazonlinux-2' (v1.2.1) for provider: virtualbox
    default: Downloading: https://vagrantcloud.com/bento/boxes/amazonlinux-2/versions/1.2.1/providers/virtualbox.box
Download redirected to host: vagrantcloud-files-production.s3.amazonaws.com
==> default: Successfully added box 'bento/amazonlinux-2' (v1.2.1) for 'virtualbox'!
There are errors in the configuration of this machine. Please fix
the following errors and try again:

vm:
* The host path of the shared folder is not supported from WSL. Host
path of the shared folder must be located on a file system with
DrvFs type. Host path: .
```

これ何を言われてるのかというと、VirtualBox自体はWindows側で動いてるのでVagrantとフォルダを共有できるのはWindowsのフォルダやで、ということらしい。  
DrvFsというのがWSLがマウントしてるWindowsのフォルダのこと（/mnt/c/ みたいなパス）

そういうわけだから、WindowsのC:\Users\Publicにvagrantというフォルダを作ったあと、Vagrantfileに以下のような一文を書く。

```
    config.vm.synced_folder "/mnt/c/Users/Public/vagrant", "/vagrant"
```

その後 `vagrant up` することでVagrantの仮想環境内の/vagrantディレクトリとWindows側のvagrantフォルダが共有できた。

関係ないけどWindows側でVagrant仮想環境と共有するフォルダってどこに作れば良いんだろうか。最初ProgramDataに作ろうかと思ったけど書き込み権限はファイル作成者にしかないらしい。かといってUsers配下のパスをVagrantfileに書いてそれがリポジトリにコミットされるのはイヤンな感じだ。

最近Windowsで開発たまにしてるけどなかなか良い。こころなしかWindows版のVSCodeの方がキビキビしてる感じすらする。MacはARM化するしWindowsがWeb開発に向いたOSになってきてるし、なんか潮目が来てるのかも知んない。Macはスマホアプリワールドに生きる人のためのOSになるのかもしれない。Web開発でARMだと色々とビルドとかミドルウェアのインストールでハマったりしそう。ARMのサーバーがどこまで一般的になるか次第だが、AWS EC2にはARMのインスタンスあるよな。。。どうなるんだろう。。。

