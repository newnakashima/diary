---
templateKey: blog-post
title: MySQLのSET foreign_key_checks = 0
date: 2020-09-07 19:33:39
tags:
  - MySQL
---

MySQL で foreign key の親テーブルを truncate しようとすると `Cannot truncate a table referenced in a foreign key constraint 云々` などというエラーが出てできない。なんでだろと思ってググると以下の記事が見つかった。

[MySQLで外部キーの制約があるテーブルをtruncateする方法](https://hacknote.jp/archives/19470/)

つまり、こんなふうにしてやれば truncate できる。
```
mysql> SET foreign_key_checks = 0;
mysql> TRUNCATE table_name;
mysql> SET foreign_key_checks = 1;
```

で、実務上必要なのは以上で終わりなわけだが foreign\_key\_checks の設定値についてもう少し知りたかったので調べた。

[MySQL5.6 の公式ドキュメント](https://dev.mysql.com/doc/refman/5.6/ja/create-table-foreign-keys.html)から引用。

> foreign\_key\_checks を 0 に設定することは、LOAD DATA および ALTER TABLE 操作中に外部キー制約を無視するためにも役立つ場合があります。ただし、foreign\_key\_checks = 0 の場合でも、MySQL では、カラムが一致しないカラム型を参照している外部キー制約の作成は許可されません。また、テーブルに外部キー制約が存在する場合は、ALTER TABLE を使用して、そのテーブルを別のストレージエンジンを使用するように変更することはできません。ストレージエンジンを変更するには、まず外部キー制約をすべて削除する必要があります。

> SET foreign\_key\_checks = 0 を実行しないかぎり、FOREIGN KEY 制約によって参照されるテーブルに対して DROP TABLE を発行できません。テーブルを削除すると、そのテーブルを作成するために使用されたステートメントで定義されていた制約もすべて削除されます。

つまり、削除以外でもレコード作成とかテーブル定義変更のときとかも外部キー制約のチェックがあるけどこれを 0 にしておくと無視できるらしい。ただ型のチェックは 0 にしてても行われる、ということか。

ここには DROP TABLE については書いてあるけど TRUNCATE については書いてない。今まで TRUNCATE は速い DELETE くらいにしか思ってなくてあまり気にして無かったけど、改めてMySQLのドキュメント読むと TRUNCATE は DML ではなくて DDL に分類されるらしい。

[参考：TRUNCATE に関する公式ドキュメント](https://dev.mysql.com/doc/refman/5.6/ja/truncate-table.html)

だから、下記のような違いが生まれてくる。

- DELETE よりもめっちゃ速い
- DELETE と違ってロールバックできない
- DELETE と違って削除された行数が返ってこない
- AUTO\_INCREMENT のシーケンスがリセットされる
- ON DELETE のトリガーが起動しない

なので関連性の強いテーブルのことも気にしながら TRUNCATE する必要がありそう。ON DELETE のトリガーで他のテーブルに操作をしている場合などは特に。

この説明を聞くと、外部キー制約で参照されてるときに TRUNCATE できないというのも多少納得できた。
