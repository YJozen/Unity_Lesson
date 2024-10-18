インスペクター単体だと単一のメソッドに限定されるが、
複数のリスナーが同じイベントを受け取れる


# 2-1. EventHandlerを用いてイベント実行

```csharp
using System;
using UnityEngine;

public class EventExample : MonoBehaviour
{
    public event EventHandler MyEvent;

    void Start()
    {
        MyEvent += OnMyEvent;
        MyEvent?.Invoke(this, EventArgs.Empty); // イベントを発火
    }

    private void OnMyEvent(object sender, EventArgs e)
    {
        Debug.Log("Event triggered!");
    }
}
```

<br>


# 2-2. EventHandlerを用いてイベント実行(引数使用)

(サンプルの方では、シングルトンパターンで用意したInstanceを利用している)

## ファイル構成
1. **`MyEventArgs.cs`** (カスタムイベント引数クラス)
2. **`Publisher.cs`** (イベント発火側のクラス)
3. **`Subscriber.cs`** (イベント受信側のクラス)

<br>

---

<br>

### 1. `MyEventArgs.cs` (カスタムイベント引数クラス)

```csharp
using System;

// カスタムイベントの引数として使用するクラス
public class MyEventArgs : EventArgs
{
    public string Message { get; }
    public int Value { get; }

    public MyEventArgs(string message, int value)
    {
        Message = message;
        Value = value;
    }
}
```

#### 説明
- `MyEventArgs` クラスは、イベントに渡すデータ（メッセージと数値）を含んでいます。
- `EventArgs` を継承することで、`EventHandler` のイベント引数として使用できます。

<br>

---

<br>

### 2. `Publisher.cs` (イベント発火側のクラス)

```csharp
using System;
using UnityEngine;

public class Publisher : MonoBehaviour
{
    // EventHandlerを使用したイベント定義
    public event EventHandler<MyEventArgs> MyEvent;

    // イベントを発火するメソッド
    public void TriggerEvent(string message, int value)
    {
        // イベントが登録されていればInvokeで発火
        MyEvent?.Invoke(this, new MyEventArgs(message, value));
    }
}
```

#### 説明
- `Publisher` クラスは、イベントを発火させる側です。Unityの `MonoBehaviour` を継承し、イベントを保持しています。
- `TriggerEvent` メソッドを呼び出すことで、イベントを発火し、登録されているメソッドに通知します。

<br>

---

<br>

### 3. `Subscriber.cs` (イベント受信側のクラス)
```csharp
using UnityEngine;

public class Subscriber : MonoBehaviour
{
    [SerializeField] private Publisher publisher;

    private void OnEnable()
    {
        // Publisherのイベントにメソッドを登録
        if (publisher != null)
        {
            publisher.MyEvent += OnEventReceived;
        }
    }

    private void OnDisable()
    {
        // イベントの登録を解除
        if (publisher != null)
        {
            publisher.MyEvent -= OnEventReceived;
        }
    }

    // イベントが発火されたときに呼び出されるメソッド
    private void OnEventReceived(object sender, MyEventArgs e)
    {
        // イベントの引数を利用してメッセージを表示
        Debug.Log($"イベントを受信しました: メッセージ = {e.Message}, 値 = {e.Value}");
    }
}
```

#### 説明
- `Subscriber` クラスはイベントを受信する側で、 `OnEnable` でイベントを登録し、 `OnDisable` で登録解除します。
- `OnEventReceived` メソッドが、イベント発火時に呼び出され、引数として渡されたデータを使用します。

---

---

### Unityのシーン設定
1. シーンに `Publisher` と `Subscriber` のオブジェクトを作成してアタッチ。
2. `Subscriber` のインスペクターで、 `Publisher` オブジェクトを `publisher` フィールドにドラッグ＆ドロップします。
3. `Publisher` の `TriggerEvent` メソッドを適切なタイミングで呼び出すように設定します（ボタンやタイマー、コライダーなど）。


---

## 使用例

```cs
using UnityEngine;

public class TriggerEventExample : MonoBehaviour
{
    [SerializeField] private Publisher publisher;  // Publisherの参照

    void Update()
    {
        // スペースキーが押されたらイベントを発火
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // 引数としてメッセージと数値を渡す
            publisher.TriggerEvent("スペースキーが押されました", 42);
        }
    }
}
```






