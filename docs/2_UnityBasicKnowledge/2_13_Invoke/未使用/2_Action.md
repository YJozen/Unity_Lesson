
### イベントベースの管理についての講義

イベントベースの管理は、特定の条件やアクションが発生したときに、そのタイミングで特定の処理を実行するための方法です。ゲーム開発やアプリケーションの開発において、ユーザーのインタラクションやシステムの状態変化に応じて柔軟に対応できる仕組みを提供します。

#### 1. イベントの基本概念
イベントは、何か特定の「出来事」や「動作」が発生したときに、事前に登録された処理を実行するトリガーです。例えば、ボタンがクリックされたとき、キャラクターが特定のアイテムに触れたとき、または一定時間が経過したときなどに、イベントが発生します。

#### 2. イベントの仕組み
イベントベースの管理では、以下のような仕組みで動作します。

1. **イベントの定義:** イベントを定義し、それに対応するデリゲート（メソッドの参照）を設定します。
2. **イベントの登録:** イベントに対して処理を登録します。これを「イベントハンドラ」と呼びます。
3. **イベントの発生:** イベントが発生すると、登録されたハンドラが呼び出されます。

#### 3. C#におけるイベントの実装例

ここでは、UnityでのC#を使ったイベントベースの管理の基本的な例を示します。

```csharp
using UnityEngine;
using System;

public class EventExample : MonoBehaviour
{
    // 1. イベントの定義
    public event Action OnSpacePressed;

    void Update()
    {
        // 2. イベントの発生トリガー
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // 3. イベントの発生
            OnSpacePressed?.Invoke();
        }
    }

    void OnEnable()
    {
        // 4. イベントハンドラの登録
        OnSpacePressed += HandleSpacePressed;
    }

    void OnDisable()
    {
        // 5. イベントハンドラの解除
        OnSpacePressed -= HandleSpacePressed;
    }

    // 6. イベントハンドラ（処理）の実装
    void HandleSpacePressed()
    {
        Debug.Log("Space key was pressed!");
    }
}
```

#### 4. 詳細な解説

1. **イベントの定義:**
   - `public event Action OnSpacePressed;` でイベントを定義します。`Action`は引数も戻り値も持たないメソッドを示すデリゲートです。カスタムイベントを作りたい場合は、デリゲートを作成し、引数や戻り値を指定することも可能です。

2. **イベントの発生トリガー:**
   - `if (Input.GetKeyDown(KeyCode.Space))` でスペースキーが押されたときの処理を確認します。

3. **イベントの発生:**
   - `OnSpacePressed?.Invoke();` でイベントが発生します。`?.` は`OnSpacePressed`がnullでない場合にのみイベントを発火させるための演算子です。

4. **イベントハンドラの登録:**
   - `OnEnable`メソッドで、イベントハンドラとして`HandleSpacePressed`を`OnSpacePressed`に登録します。これにより、イベントが発生したときにこのメソッドが呼ばれます。

5. **イベントハンドラの解除:**
   - `OnDisable`メソッドで、イベントハンドラを解除します。これにより、無駄なメモリ消費や意図しない挙動を防ぐことができます。

6. **イベントハンドラ（処理）の実装:**
   - `HandleSpacePressed`メソッドは、スペースキーが押されたときに実行される処理です。この例では、単純にログを出力しています。

#### 5. 応用例

イベントベースの管理は、以下のような場面で活用できます。

- **UI操作:** ボタンが押されたとき、スライダーが動かされたときなど、ユーザーインターフェースでのインタラクション。
- **ゲームイベント:** 敵が倒されたとき、レベルアップしたときなど、ゲーム内の重要な出来事。
- **非同期処理:** ダウンロードが完了したとき、一定時間が経過したときなど。

#### 6. メリットと注意点

- **メリット:**
  - 処理の柔軟性が高く、複数のリスナーが同じイベントを監視できます。
  - コードの再利用性が高まり、イベント発生場所と処理を分離できるため、コードの可読性が向上します。

- **注意点:**
  - 過剰にイベントを使用すると、デバッグが難しくなる可能性があります。
  - イベントハンドラの解除を忘れると、メモリリークの原因になります。

イベントベースの管理は、システムの柔軟性と拡張性を高める強力な方法です。ゲームやアプリケーションの中でどのようなイベントが発生し、そのイベントに対してどのように応答するかをしっかりと設計することで、より洗練されたシステムを構築することができます。


<br>

---

<br>

イベントベースの管理の発展系として、引数を渡す方法などがあります。これにより、イベントが発生したときに、追加の情報やデータをリスナーに伝えることができるようになります。

### 引数を使用したイベントの基本例

まず、引数を渡すイベントの基本的な例を示します。ここでは、イベントが発生した際に、イベントの引数として `int` 型のデータを渡す例です。

```csharp
using UnityEngine;

public class EventManager : MonoBehaviour
{
    // イベントのデリゲート定義
    public delegate void OnScoreChanged(int newScore);

    // イベントの宣言
    public static event OnScoreChanged ScoreChanged;

    private int _score;

    // スコアが変更されたときにイベントを発火
    public void ChangeScore(int amount)
    {
        _score += amount;
        // イベントの発火
        ScoreChanged?.Invoke(_score);
    }
}

public class ScoreListener : MonoBehaviour
{
    void OnEnable()
    {
        // イベントにリスナーを追加
        EventManager.ScoreChanged += OnScoreChanged;
    }

    void OnDisable()
    {
        // イベントからリスナーを削除
        EventManager.ScoreChanged -= OnScoreChanged;
    }

    // イベント発生時に実行されるメソッド
    void OnScoreChanged(int newScore)
    {
        Debug.Log("New Score: " + newScore);
    }
}
```

### 発展系：カスタムイベント引数

引数を複数渡す必要がある場合、カスタムイベント引数クラスを使用することができます。この方法では、クラスに必要なデータをまとめてイベント引数として渡すことができます。

```csharp
using UnityEngine;

// カスタムイベント引数クラス
public class ScoreEventArgs : System.EventArgs
{
    public int NewScore { get; private set; }
    public string PlayerName { get; private set; }

    public ScoreEventArgs(int newScore, string playerName)
    {
        NewScore = newScore;
        PlayerName = playerName;
    }
}

public class EventManager : MonoBehaviour
{
    // イベントのデリゲート定義
    public delegate void OnScoreChanged(object sender, ScoreEventArgs e);

    // イベントの宣言
    public static event OnScoreChanged ScoreChanged;

    private int _score;

    // スコアが変更されたときにイベントを発火
    public void ChangeScore(int amount, string playerName)
    {
        _score += amount;
        // カスタム引数を用いたイベントの発火
        ScoreChanged?.Invoke(this, new ScoreEventArgs(_score, playerName));
    }
}

public class ScoreListener : MonoBehaviour
{
    void OnEnable()
    {
        // イベントにリスナーを追加
        EventManager.ScoreChanged += OnScoreChanged;
    }

    void OnDisable()
    {
        // イベントからリスナーを削除
        EventManager.ScoreChanged -= OnScoreChanged;
    }

    // イベント発生時に実行されるメソッド
    void OnScoreChanged(object sender, ScoreEventArgs e)
    {
        Debug.Log($"Player {e.PlayerName} has a new score: {e.NewScore}");
    }
}
```

### 発展系の使用例

この発展系を使用すると、イベントが発生した際に複数のデータを一度にリスナーに伝えることができ、より複雑なイベント管理が可能になります。例えば、ゲーム内でプレイヤーが特定のアイテムを取得したときに、そのアイテムの詳細（名前、効果、取得したプレイヤーの名前など）を引数としてイベントリスナーに伝えることができます。










複数のリスナーが同じイベントを受け取れるというのは、1つのイベント（例えば `OnEventTriggered`）が発生したときに、**複数のリスナー（イベントを受け取る側）**がそのイベントを受け取って、それぞれ自分に対応した処理を行うことができるという意味です。

具体的には、1つのイベントに対して**複数のメソッド**を登録しておくと、そのイベントが発生したときに、**登録されたすべてのメソッドが順番に実行される**ということです。

### サンプルコード：複数のリスナーが同じイベントを受け取る例

#### Publisher (イベントを発行する側)
```csharp
using System;
using UnityEngine;

public class Publisher : MonoBehaviour
{
    // イベントを定義。引数としてメッセージと数値を渡す
    public event Action<string, int> OnEventTriggered;

    // イベントを発火するメソッド
    public void TriggerEvent(string message, int value)
    {
        Debug.Log("イベントを発火します");
        OnEventTriggered?.Invoke(message, value); // 登録されたメソッドがあれば実行
    }

    void Update()
    {
        // スペースキーが押されたらイベントを発火
        if (Input.GetKeyDown(KeyCode.Space))
        {
            TriggerEvent("スペースキーが押されました", 42);
        }
    }
}
```

#### リスナー1 (イベントを受け取る側)
```csharp
using UnityEngine;

public class Listener1 : MonoBehaviour
{
    [SerializeField] private Publisher publisher;  // Publisherの参照をインスペクターで設定

    void Start()
    {
        // Publisherのイベントにメソッドを登録
        if (publisher != null)
        {
            publisher.OnEventTriggered += HandleEvent;
        }
    }

    // イベントが発火された際に呼ばれるメソッド
    private void HandleEvent(string message, int value)
    {
        Debug.Log($"Listener1: イベントを受け取りました - メッセージ: {message}, 値: {value}");
    }

    void OnDestroy()
    {
        // イベントの登録を解除（必要な場合）
        if (publisher != null)
        {
            publisher.OnEventTriggered -= HandleEvent;
        }
    }
}
```

#### リスナー2 (イベントを受け取る側)
```csharp
using UnityEngine;

public class Listener2 : MonoBehaviour
{
    [SerializeField] private Publisher publisher;  // Publisherの参照をインスペクターで設定

    void Start()
    {
        // Publisherのイベントにメソッドを登録
        if (publisher != null)
        {
            publisher.OnEventTriggered += HandleEvent;
        }
    }

    // イベントが発火された際に呼ばれるメソッド
    private void HandleEvent(string message, int value)
    {
        Debug.Log($"Listener2: イベントを受け取りました - メッセージ: {message}, 値: {value}");
    }

    void OnDestroy()
    {
        // イベントの登録を解除（必要な場合）
        if (publisher != null)
        {
            publisher.OnEventTriggered -= HandleEvent;
        }
    }
}
```

### 仕組みの説明
1. `Publisher` は `OnEventTriggered` というイベントを持っています。このイベントは `Action<string, int>` 型であり、引数として文字列と数値を受け取ります。
2. `Listener1` と `Listener2` はそれぞれ、 `Publisher` のイベントに対してリスナーとして登録しています。
3. `Publisher` の `TriggerEvent` メソッドが呼ばれると、 `OnEventTriggered` イベントが発生し、登録された `Listener1` と `Listener2` の `HandleEvent` メソッドが実行されます。
4. 両方のリスナーが同じイベントを受け取りますが、それぞれ独自のメッセージを表示しています。

### 実行結果の例：
```
イベントを発火します
Listener1: イベントを受け取りました - メッセージ: スペースキーが押されました, 値: 42
Listener2: イベントを受け取りました - メッセージ: スペースキーが押されました, 値: 42
```

このように、1つのイベントが発生すると、複数のリスナー（`Listener1` と `Listener2`）が同時にそのイベントを受け取って、自分に割り当てられた処理を実行します。これにより、1つのイベントで複数のオブジェクトや処理を制御することが可能になります。