# 実例によるPureScript 4章の最後の問題

[実例によるPureScript4章の最後の問題](https://gemmaro.github.io/purescript-book/chapter4.html#%E6%BC%94%E7%BF%92-4)の2問目だが、問題の意味がわからない。なのでちょっとズルだがテストコードから先に見た。

```purs
samplePicture :: Picture
samplePicture =
  [ Circle origin 2.0
  , Circle { x: 2.0, y: 2.0 } 3.0
  , Rectangle { x: 5.0, y: 5.0 } 4.0 4.0
  ]

-- 省略

      test "Exercise - Clipped shapeBounds" do
        Assert.equal { top: -2.0, left: -2.0, right: 2.0, bottom: 2.0 }
          -- Note to users: You'll need to manually import shapeBounds
          -- from Data.Picture. Don't import from Test.NoPeeking.Solutions.
          $ shapeBounds (Clipped samplePicture { x: 0.0, y: 0.0 } 4.0 4.0)
        Assert.equal { top: 3.0, left: 3.0, right: 7.0, bottom: 7.0 }
          $ shapeBounds (Clipped samplePicture { x: 5.0, y: 5.0 } 4.0 4.0)
        Assert.equal { top: 2.0, left: 2.0, right: 7.0, bottom: 7.0 }
          $ shapeBounds (Clipped samplePicture { x: 5.0, y: 5.0 } 6.0 6.0)
```

shapeBoundsという関数があれば良さそうではあるが、ClippedでShapeを拡張するというのが意味がわからない。多分これまでと違いMySolutions.pursに回答を書くのではなく、Picture.pursを直接上書きしろということだと解釈。以下のようにした。

```purs
data Shape
  = Circle Point Number
  | Rectangle Point Number Number
  | Line Point Point
  | Text Point String
  -- 以下を追加
  | Clipped Picture Point Number Number
```

当然これまでShapeを使ってた関数は軒並みエラーになるので、Clippedのケースを各所に追加してやる。

Pictures.pursを眺めていると、shapeBoundsはもうあって、そこにClippedのケースを追加すれば良さそうだ。最初は普通にRectangleと同じのを書いてみた。

```purs
shapeBounds (Clipped picture {x, y} w h) =
  { top:    y - h / 2.0
  , left:   x - w / 2.0
  , bottom: y + h / 2.0
  , right:  x + w / 2.0
  }
```

これだと一個目二個目のテストケースは通るが、三個目が通らない。当然ながら、単に矩形のサイズを計算すれば良いわけが無く、pictureも考慮に入れねばならないはずだ。が、テストの期待値を見ると、pictureに含まれてる図形が切り取り範囲よりも小さければそっちに合わせれば良いっぽい？　のでそんな風に書いてみる。

ここではすでに定義されてるboundsなる関数が使えそう。boundsはPictureの矩形を計算してくれるものだ。

```purs
bounds :: Picture -> Bounds
bounds = foldl combine emptyBounds
  where
  combine :: Bounds -> Shape -> Bounds
  combine b shape = union (shapeBounds shape) b
```

これを使って以下のように書いた。

```purs
shapeBounds :: Shape -> Bounds
-- 他の図形は省略
shapeBounds (Clipped picture {x, y} w h) =
  { top:    max b.top    $ y - h / 2.0
  , left:   max b.left   $ x - w / 2.0
  , bottom: min b.bottom $ y + h / 2.0
  , right:  min b.right  $ x + w / 2.0
  }
  where
    b = bounds picture
```

そしたらテストは通った。これであってるのかわからないが、良しとする。

ちなみにこれよりもshowShapeにClippedを追加した時のほうがパズル感があって楽しかった。

```purs
showShape :: Shape -> String
-- 省略
showShape (Clipped picture p w h) =
  "Clipped [picture: " <> pictureShown <> ", center: " <> showPoint p <> ", width: " <> show w <> ", height: "<> show h <> "]"
  where
    pictureShown = intercalate ", " $ map showShape picture
```

showShape は Shape を出力するための関数だが、Clippedに関しては型の引数に Shape 自身が含まれているため、showShapeを再帰的に呼び出して出力するように書いた。

```
> showShape (Clipped samplePicture origin 4.0 4.0)
"Clipped [picture: Circle [center: (0.0, 0.0), radius: 2.0], Circle [center: (2.0, 2.0), radius: 3.0], Rectangle [center: (5.0, 5.0), width: 4.0, height: 4.0], center: (0.0, 0.0), width: 4.0, height: 4.0]"
```

## 感想

PureScriptを書くのは楽しいが、書いているとすぐ時間が経ってしまう。良いのか悪いのかわからない。
