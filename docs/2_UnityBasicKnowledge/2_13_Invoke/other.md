Unityでは、さまざまな方法でメソッドを実行することができます。

イベント実行方法をいくつか


<br>

### 1. **コールバックメソッド**

- **概要**: 特定の条件が満たされたときに実行されるメソッドを設定することができます。
- **使用例**: イベントや条件の判定があるクラスにコールバックメソッドを定義し、他のクラスからそのメソッドを呼び出す。

```csharp
public class EventPublisher
{
    public Action OnSomethingHappened;

    public void DoSomething()
    {
        OnSomethingHappened?.Invoke();
    }
}

public class EventSubscriber
{
    private void Start()
    {
        EventPublisher publisher = FindObjectOfType<EventPublisher>();
        publisher.OnSomethingHappened += HandleSomethingHappened;
    }

    private void HandleSomethingHappened()
    {
        // 何かの処理
    }
}
```

### 2. **Unityのコルーチン**

- **概要**: コルーチンを使用して、一定の時間待ったり、非同期に処理を実行することができます。
- **使用例**: `StartCoroutine`を使って、処理を遅延させたり、順次実行する。

```csharp
public class CoroutineExample : MonoBehaviour
{
    private void Start()
    {
        StartCoroutine(ExecuteAfterTime(2));
    }

    private IEnumerator ExecuteAfterTime(float time)
    {
        yield return new WaitForSeconds(time);
        // メソッドを実行
    }
}
```

### 3. **Unityのイベントシステム（UIイベント）**

- **概要**: UnityのUIシステムを使用して、ボタンやスライダーなどのUI要素にイベントリスナーを追加することができます。
- **使用例**: `Button`の`onClick`イベントにメソッドを割り当てる。

```csharp
public class UIButtonExample : MonoBehaviour
{
    public Button myButton;

    private void Start()
    {
        myButton.onClick.AddListener(OnButtonClick);
    }

    private void OnButtonClick()
    {
        // ボタンがクリックされたときの処理
    }
}
```

### 4. **カスタムイベント**

- **概要**: 自分自身でイベントを定義して、メソッドを実行することができます。
- **使用例**: カスタムイベントを作成し、特定の条件でそのイベントを発火させる。

```csharp
public class CustomEventExample : MonoBehaviour
{
    public event Action MyCustomEvent;

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            MyCustomEvent?.Invoke();
        }
    }
}
```

### 5. **インターフェースを利用した実行**

- **概要**: インターフェースを定義し、そのインターフェースを実装したクラスのメソッドを呼び出します。
- **使用例**: 共通のインターフェースを持つ複数のクラスからメソッドを呼び出すことができます。

```csharp
public interface IExecutable
{
    void Execute();
}

public class ExecutableClass : MonoBehaviour, IExecutable
{
    public void Execute()
    {
        // 実行する処理
    }
}

public class Executor : MonoBehaviour
{
    public IExecutable target;

    private void Start()
    {
        target.Execute(); // IExecutableを実装したクラスのメソッドを実行
    }
}
```

### 6. **アセットバンドルやリソースマネージャを使った動的実行**

- **概要**: アセットバンドルやリソースマネージャを使って、動的にオブジェクトをロードし、そのオブジェクトのメソッドを実行します。
- **使用例**: アセットバンドルからPrefabをロードし、そのPrefabのコンポーネントにあるメソッドを実行します。

### 7. **状態管理を用いた実行**

- **概要**: 状態パターンを利用して、現在の状態に応じたメソッドを実行します。
- **使用例**: 状態に基づいて異なる処理を行う。

```csharp
public interface IState
{
    void Execute();
}

public class IdleState : IState
{
    public void Execute()
    {
        // Idle処理
    }
}

public class RunningState : IState
{
    public void Execute()
    {
        // Running処理
    }
}

public class Character : MonoBehaviour
{
    private IState currentState;

    private void Update()
    {
        currentState.Execute();
    }
}
```

