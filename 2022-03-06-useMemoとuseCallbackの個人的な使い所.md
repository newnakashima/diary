---
templateKey: blog-post
title: useMemoとuseCallbackの個人的な使い所
date: 2022-03-06 12:40:09
tags:
  - React
  - useMemo
  - useCallback
---

useMemoとuseCallbackの使い所について最近色々感じることがあるのでメモ。個人的な感想。一般的にどうなのかはよくわからない。

## useMemo

例えば、以下のようなコンポーネントがあるとする。

```jsx
export default function MyComponent() {
  const [flag1, setFlag1] = useState(false)
  const [flag2, setFlag2] = useState(false)

  return (
    <div>
      {flag1 &&
        <p>フラグ1がonになっている</p>
      }
      {flag2 &&
        <p>フラグ2がonになっている</p>
      }
      {flag1 && flag2 &&
        <p>フラグ1とフラグ2が両方onになっている</p>
      }
    </div>
  )
}
```

こんな感じで、特定の部品のレンダリングに複数の条件が関わってくるとuseMemoしたくなる。上の例だとbooleanのフラグが２つなのでまだ許せるが、これがnumber型で３つとかになると以下のようになる。

```jsx
export default function MyComponent() {
  const [variable1, setVariable1] = useState(0)
  const [variable2, setVariable2] = useState(0)
  const [variable3, setVariable3] = useState(0)

  return (
    <div>
      {variable1 > 10 &&
        <p>変数1が10より大きい</p>
      }
      {variable2 < 20 &&
        <p>変数2が20未満</p>
      }
      {variable3 === 50 &&
        <p>変数3が50と等しい</p>
      }
      {variable1 > 10 && variable2 < 20 &&
        <p>変数1と変数2が条件を満たしている</p>
      }
      {variable1 > 10 && variable3 === 50 &&
        <p>変数1と変数3が条件を満たしている</p>
      }
      {variable2 < 20 && variable3 === 50 &&
        <p>変数2と変数3が条件を満たしている</p>
      }
      {variable1 > 10 && variable2 < 20 && variable3 === 50 &&
        <p>全ての変数が条件を満たしている</p>
      }
      <div>
        <label>
          変数1
          <input
            type="number"
            value={variable1}
            onChange={(e) => setVariable1(+e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          変数2
          <input
            type="number"
            value={variable2}
            onChange={(e) => setVariable2(+e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          変数3
          <input
            type="number"
            value={variable3}
            onChange={(e) => setVariable3(++e.target.value)}
          />
        </label>
      </div>
    </div>
```

`variable1 > 10 && variable2 < 20 && variable3 === 50 &&` みたいなのは読みづらいので変数や関数にしたくなるのがプログラマーの習性だろう。そうすると次のような感じになる。

```jsx
export default function MyComponent() {
  const [variable1, setVariable1] = useState(0)
  const [variable2, setVariable2] = useState(0)
  const [variable3, setVariable3] = useState(0)

  const variable1and2 = variable1 > 10 && variable2 < 20
  const variable1and3 = variable1 > 10 && variable3 === 50
  const variable2and3 = variable2 < 20 && variable3 === 50
  const allVariables = variable1 > 10 && variable2 < 20 && variable3 === 50

  return (
    <div>
      {variable1 > 10 &&
        <p>変数1が10より大きい</p>
      }
      {variable2 < 20 &&
        <p>変数2が20未満</p>
      }
      {variable3 === 50 &&
        <p>変数3が50と等しい</p>
      }
      {variable1and2 &&
        <p>変数1と変数2が条件を満たしている</p>
      }
      {variable1and3 &&
        <p>変数1と変数3が条件を満たしている</p>
      }
      {variable2and3 &&
        <p>変数2と変数3が条件を満たしている</p>
      }
      {allVariables &&
        <p>全ての変数が条件を満たしている</p>
      }
      <div>
        <label>
          変数1
          <input
            type="number"
            value={variable1}
            onChange={(e) => setVariable1(+e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          変数2
          <input
            type="number"
            value={variable2}
            onChange={(e) => setVariable2(+e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          変数3
          <input
            type="number"
            value={variable3}
            onChange={(e) => setVariable3(++e.target.value)}
          />
        </label>
      </div>
    </div>
  )
}
```

見た目だけなら多少はマシになったが、例えば `variable1and2` はvariable3の値が変わったときも毎回再計算してしまうという問題がある。なのでこういうときはuseMemo使いましょうというのがよく言われることなんじゃないかと思う。以下のようにする。

```jsx
export default function MyComponent() {
  const [variable1, setVariable1] = useState(0)
  const [variable2, setVariable2] = useState(0)
  const [variable3, setVariable3] = useState(0)

  const variable1and2 = useMemo(() => {
    return variable1 > 10 && variable2 < 20
  }, [variable1, variable2])

  const variable1and3 = useMemo(() => {
    return variable1 > 10 && variable3 === 50
  }, [variable1, variable3])

  const variable2and3 = useMemo(() => {
    return variable2 < 20 && variable3 === 50
  }, [variable2, variable3])

  const allVariables = useMemo(() => {
    return variable1 > 10 && variable2 < 20 && variable3 === 50
  }, [variable1, variable2, variable3])

  return (
    <div>
      {variable1 > 10 &&
        <p>変数1が10より大きい</p>
      }
      {variable2 < 20 &&
        <p>変数2が20未満</p>
      }
      {variable3 === 50 &&
        <p>変数3が50と等しい</p>
      }
      {variable1and2 &&
        <p>変数1と変数2が条件を満たしている</p>
      }
      {variable1and3 &&
        <p>変数1と変数3が条件を満たしている</p>
      }
      {variable2and3 &&
        <p>変数2と変数3が条件を満たしている</p>
      }
      {allVariables &&
        <p>全ての変数が条件を満たしている</p>
      }
      <div>
        <label>
          変数1
          <input
            type="number"
            value={variable1}
            onChange={(e) => setVariable1(+e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          変数2
          <input
            type="number"
            value={variable2}
            onChange={(e) => setVariable2(+e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          変数3
          <input
            type="number"
            value={variable3}
            onChange={(e) => setVariable3(++e.target.value)}
          />
        </label>
      </div>
    </div>
  )
}
```

このとき、そもそも各変数が単体で条件を満たしているかどうかをメモしてもいいと思う。メモ化した値を更にメモ化するみたいな感じになる。

[Reactの公式ドキュメント](https://ja.reactjs.org/docs/hooks-reference.html#usememo)では、

> **useMemo はパフォーマンス最適化のために使うものであり、意味上の保証があるものだと考えないでください。**

と太字で強調してあるのだが、 個人的にはuseMemoはどんどん使うべきだと思っている。なぜなら、パフォーマンス目的以外にも以下のメリットがあると感じるからだ。

- 関数として計算結果を返すのでデバッグしやすい。処理する前に console.log などを仕込める
  - もちろんuseMemoしなくてもできるのだが、スコープが明確に区切られるのでcommitする前にconsole.logを消し忘れるみたいなゴミが減る
- ESLintが依存関係に関するWarningを出してくれる
  - 変数の値が何に依存してるかが見えやすくなり、つまらないバグの発生を防げてる気がする
  - と同時に、なんとか変数間の依存を減らそうという意識が働くのでロジックを細かく切り出せる

## useCallback

useCallbackもuseMemoと使い所は基本的には同じで、[公式ドキュメント](https://ja.reactjs.org/docs/hooks-reference.html#usecallback)にもこう書いてある。

> useCallback(fn, deps) は useMemo(() => fn, deps) と等価です。

だが、明示的に「このメモは引数を取りますよ」という意図を表すのに有用だ。じゃあどういうときに引数使いたい気持ちになるのかというと、典型的には配列からコンポーネントを生成するときかなと思う。

例えば以下のような感じで配列を出力してるとする。

```jsx
export default function MyComponent() {
  const myArray = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
  ];
  const [selected, setSelected] = useState(0);
  const [bgColor, setBgColor] = useState('red');

  return (
    <div style={{ backgroundColor: 'gray' }}>
      <div style={{ backgroundColor: bgColor }}>
        <label style={{ color: 'white' }}>
          赤
          <input
            type="radio"
            name="bgColor"
            onChange={(e) => e.target.checked && setBgColor('red')}
            defaultChecked={bgColor === 'red'}
          />
        </label>
        <label style={{ color: 'white' }}>
          黒
          <input
            type="radio"
            name="bgColor"
            onChange={(e) => e.target.checked && setBgColor('black')}
            defaultChecked={bgColor === 'black'}
          />
        </label>
      </div>
      <ul>
        {myArray.map((item, i) => {
          return (
            <li
              key={i}
              onClick={() => setSelected(i)}
              style={{
                color: 'white',
                backgroundColor: i === selected ? 'blue' : Math.abs(selected - i) === 1 ? 'steelblue' : 'transparent'
              }}
            >
              {item}
            </li>
          );
        })}
      </ul>
    </div>
  )
}
```

`backgroundColor: i === selected ? 'blue' : Math.abs(selected - i) === 1 ? 'steelblue' : 'transparent'`
のように複数の条件や出力結果が絡んでいる場合にインラインで書くと可読性が著しく落ちる。なので関数化したくなる。自分はここでuseCallbackを使うことが多い。

```jsx
export default function MyComponent() {
  const myArray = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
  ];
  const [selected, setSelected] = useState(0);
  const [bgColor, setBgColor] = useState('red');

  // ↓↓↓関数化したやつ↓↓↓
  const getLiBgColor = useCallback((i) => {
    if (i === selected) {
      return 'blue'
    }

    if (Math.abs(selected - i) === 1) {
      return 'steelblue'
    }

    return 'transparent'
  }, [selected])
  // ↑↑↑関数化したやつ↑↑↑

  return (
    <div style={{ backgroundColor: 'gray' }}>
      <div style={{ backgroundColor: bgColor }}>
        <label style={{ color: 'white' }}>
          赤
          <input
            type="radio"
            name="bgColor"
            onChange={(e) => e.target.checked && setBgColor('red')}
            defaultChecked={bgColor === 'red'}
          />
        </label>
        <label style={{ color: 'white' }}>
          黒
          <input
            type="radio"
            name="bgColor"
            onChange={(e) => e.target.checked && setBgColor('black')}
            defaultChecked={bgColor === 'black'}
          />
        </label>
      </div>
      <ul>
        {myArray.map((item, i) => {
          return (
            <li
              key={i}
              onClick={() => setSelected(i)}
              style={{
                color: 'white',
                backgroundColor: getLiBgColor(i)
              }}
            >
              {item}
            </li>
          );
        })}
      </ul>
    </div>
  )
}
```

注意すべき点としては、useCallbackは関数の計算結果をメモしているのではなくて関数を生成する処理をメモ化しているようで、依存関係に入っていない `bgColor` を変更した場合も関数自体は呼ばれるという点である。つまり `bgColor` だけを変更した場合であっても配列のサイズ=6回分無駄な処理が走る。DOMツリー上ulの配下は `bgColor` の影響を受けなくてもそうなる。

これを避けるには、`bgColor` を使ってる要素を別のコンポーネントに切り出すと良いっぽい。

```jsx
const BgColorComp => () => {
  const [bgColor, setBgColor] = useState('red');
  return (
    <div style={{ backgroundColor: bgColor }}>
      <label style={{ color: 'white' }}>
        赤
        <input
          type="radio"
          name="bgColor"
          onChange={(e) => e.target.checked && setBgColor('red')}
          defaultChecked={bgColor === 'red'}
        />
      </label>
      <label style={{ color: 'white' }}>
        黒
        <input
          type="radio"
          name="bgColor"
          onChange={(e) => e.target.checked && setBgColor('black')}
          defaultChecked={bgColor === 'black'}
        />
      </label>
    </div>
  )
}

export default function MyComponent() {
  const myArray = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
  ];
  const [selected, setSelected] = useState(0);

  const getLiBgColor = useCallback((i) => {
    if (i === selected) {
      return 'blue'
    }

    if (Math.abs(selected - i) === 1) {
      return 'steelblue'
    }

    return 'transparent'
  }, [selected])

  return (
    <div style={{ backgroundColor: 'gray' }}>
      <BgColorComp />
      <ul>
        {myArray.map((item, i) => {
          return (
            <li
              key={i}
              onClick={() => setSelected(i)}
              style={{
                color: 'white',
                backgroundColor: getLiBgColor(i)
              }}
            >
              {item}
            </li>
          );
        })}
      </ul>
    </div>
  )
}
```

また、useCallbackを使ってるとあるあるなのだが依存関係に変数を入れ忘れて生成された関数が更新されてなくてデバッグに時間を費やすというハマりがよくあって、地味に時間を削られて痛いのでuseCallbackのサイズは大きくならないように気をつけたいところだ。
