オブザーバーパターン

Unityで使用する際は、デリゲートやイベントシステムやUnityEventSystemなどを使えばいいと思うが、紹介しておこうと思う。


## 定義: 
オブザーバーパターンは、あるオブジェクト（サブジェクト）の状態が変わったときに、それに依存する他のオブジェクト（オブザーバー）に自動的に通知が行くようにするデザインパターンです。


## 目的: 
オブジェクト間の疎結合を実現し、変更の影響を最小限に抑える。


## 使用例
+ イベントシステム: GUIイベント、ゲームイベントなどでの使用。
+ データバインディング: データの変更を自動的にUIに反映する。
+ リアルタイム通知: ストックマーケットやニュースフィードなどのリアルタイム更新。



## オブザーバーパターンの実装例
C#でのオブザーバーパターン実装
サブジェクトのインターフェース:

```cs
public interface ISubject {
    void Attach(IObserver observer);
    void Detach(IObserver observer);
    void Notify();
}
```
オブザーバーのインターフェース:

```cs
public interface IObserver {
    void Update(ISubject subject);
}
```
具体的なサブジェクトクラス:

```cs
using System;
using System.Collections.Generic;

public class ConcreteSubject : ISubject {
    private List<IObserver> observers = new List<IObserver>();
    private int state;

    public int State {
        get { return state; }
        set {
            state = value;
            Notify();
        }
    }

    public void Attach(IObserver observer) {
        observers.Add(observer);
    }

    public void Detach(IObserver observer) {
        observers.Remove(observer);
    }

    public void Notify() {
        foreach (var observer in observers) {
            observer.Update(this);
        }
    }
}
```
具体的なオブザーバークラス:

csharp
Copy code
```cs
using System;

public class ConcreteObserver : IObserver {
    private string name;

    public ConcreteObserver(string name) {
        this.name = name;
    }

    public void Update(ISubject subject) {
        if (subject is ConcreteSubject concreteSubject) {
            Console.WriteLine($"Observer {name}: Subject state changed to {concreteSubject.State}");
        }
    }
}
```
使用例:
```cs
csharp
Copy code
public class Program {
    public static void Main(string[] args) {
        ConcreteSubject subject = new ConcreteSubject();

        ConcreteObserver observerA = new ConcreteObserver("A");
        ConcreteObserver observerB = new ConcreteObserver("B");

        subject.Attach(observerA);
        subject.Attach(observerB);

        subject.State = 1; // Observer A and B will be notified
        subject.State = 2; // Observer A and B will be notified

        subject.Detach(observerA);
        subject.State = 3; // Only Observer B will be notified
    }
}
```

4. オブザーバーパターンの利点と欠点
利点
疎結合: サブジェクトとオブザーバーが疎結合となるため、拡張性と再利用性が高まる。
リアルタイム通知: サブジェクトの状態変化をリアルタイムでオブザーバーに通知できる。
欠点
複雑性の増加: オブザーバーとサブジェクトの管理が複雑になる場合がある。
パフォーマンスの問題: 多数のオブザーバーが存在する場合、通知のオーバーヘッドが発生する。
5. 実際のオブザーバーパターンの使用例
Unityでのオブザーバーパターンの使用例
サブジェクトのクラス:

csharp
Copy code
```cs
using System;
using System.Collections.Generic;
using UnityEngine;

public class GameEventManager : MonoBehaviour {
    private List<IObserver> observers = new List<IObserver>();

    public void Attach(IObserver observer) {
        observers.Add(observer);
    }

    public void Detach(IObserver observer) {
        observers.Remove(observer);
    }

    public void Notify() {
        foreach (var observer in observers) {
            observer.Update(this);
        }
    }

    public void TriggerEvent() {
        Debug.Log("Event Triggered!");
        Notify();
    }
}
```
オブザーバークラス:

csharp
Copy code
```cs
using System;
using UnityEngine;

public class EventObserver : MonoBehaviour, IObserver {
    public void Update(ISubject subject) {
        if (subject is GameEventManager) {
            Debug.Log("Observer: Event received!");
        }
    }
}
```
使用例:

csharp
Copy code
using UnityEngine;

public class GameManager : MonoBehaviour {
    void Start() {
        GameEventManager eventManager = new GameObject("EventManager").AddComponent<GameEventManager>();
        EventObserver observerA = new GameObject("ObserverA").AddComponent<EventObserver>();
        EventObserver observerB = new GameObject("ObserverB").AddComponent<EventObserver>();

        eventManager.Attach(observerA);
        eventManager.Attach(observerB);

        eventManager.TriggerEvent(); // Both observerA and observerB will be notified
    }
}
まとめと質疑応答
まとめ:

オブザーバーパターンの定義と目的を復習
オブザーバーパターンの適用シナリオを確認
オブザーバーパターンの実装方法を理解
オブザーバーパターンの利点と欠点を再確認
質疑応答:

学生からの質問に答える
オブザーバーパターンの具体的な使用例や問題点についてディスカッション
まとめ
オブザーバーパターンは、オブジェクト間の疎結合を実現し、サブジェクトの状態変化をリアルタイムでオブザーバーに通知するためのデザインパターンです。正しく使用することで、コードの再利用性と拡張性が向上し、変更の影響を最小限に抑えることができます。この授業を通じて、オブザーバーパターンの正しい使い方とその限界を理解し、適切な場面で効果的に活用できるようになります。




















オブザーバーパターン

講義内容:

オブザーバーパターンの概念とユースケース
オブザーバーパターンのメリットとデメリット
実践:

csharp
Copy code
public class Subject : MonoBehaviour
{
    private List<IObserver> observers = new List<IObserver>();

    public void AddObserver(IObserver observer)
    {
        observers.Add(observer);
    }

    public void RemoveObserver(IObserver observer)
    {
        observers.Remove(observer);
    }

    public void NotifyObservers()
    {
        foreach (var observer in observers)
        {
            observer.Update();
        }
    }
}

public interface IObserver
{
    void Update();
}

public class ConcreteObserver : MonoBehaviour, IObserver
{
    public void Update()
    {
        Debug.Log("Observer updated!");
    }
}
オブザーバーパターンを使用して、ゲーム内イベントの通知システムを実装













Unityにおけるイベントシステムやデリゲートの使用は、オブザーバーパターンのシンプルかつ効率的な代替手段として非常に有効です。以下に、Unityでのイベントシステムやデリゲートの使用が適切な理由を説明し、その実装例を紹介します。

イベントシステムやデリゲートの利点
+ 簡潔さと可読性: イベントシステムやデリゲートを使うことで、コードがシンプルになり、読みやすくなります。特に小規模なプロジェクトやシンプルな通知システムでは有効です。
+ Unityとの親和性: UnityのAPIやエディタとの統合が容易で、標準的なC#の機能を利用できるため、開発がスムーズに進みます。
+ パフォーマンス: デリゲートやイベントは、オブザーバーパターンよりも効率的な場合が多く、オーバーヘッドが少ない。
イベントシステムとデリゲートの実装方法
デリゲートを使った実装
デリゲートの定義とイベントの宣言:


```cs
using UnityEngine;
using System;

public class GameEventManager : MonoBehaviour {
    public delegate void GameEvent();
    public static event GameEvent OnGameEvent;

    public void TriggerEvent() {
        Debug.Log("Event Triggered!");
        OnGameEvent?.Invoke();
    }
}
```
イベントを購読するオブザーバー:

```cs
using UnityEngine;

public class EventObserver : MonoBehaviour {
    void OnEnable() {
        GameEventManager.OnGameEvent += OnEventTriggered;
    }

    void OnDisable() {
        GameEventManager.OnGameEvent -= OnEventTriggered;
    }

    void OnEventTriggered() {
        Debug.Log("Observer: Event received!");
    }
}
```

使用例:

```cs
using UnityEngine;

public class GameManager : MonoBehaviour {
    void Start() {
        GameEventManager eventManager = new GameObject("EventManager").AddComponent<GameEventManager>();
        EventObserver observerA = new GameObject("ObserverA").AddComponent<EventObserver>();
        EventObserver observerB = new GameObject("ObserverB").AddComponent<EventObserver>();

        eventManager.TriggerEvent(); // Both observerA and observerB will be notified
    }
}
```

Unityのイベントシステムの使用
UnityのUnityEventを使うと、エディタ上でイベントの購読者を簡単に設定できます。

イベントの宣言:

```cs
using UnityEngine;
using UnityEngine.Events;

public class GameEventManager : MonoBehaviour {
    public UnityEvent OnGameEvent;

    public void TriggerEvent() {
        Debug.Log("Event Triggered!");
        OnGameEvent?.Invoke();
    }
}
```
イベントを購読するオブザーバー:

```cs
using UnityEngine;

public class EventObserver : MonoBehaviour {
    public void OnEventTriggered() {
        Debug.Log("Observer: Event received!");
    }
}
```


エディタでの設定:

GameEventManagerを持つゲームオブジェクトを作成し、OnGameEventに購読するメソッド（例えば、EventObserverのOnEventTriggered）を追加します。
EventObserverを持つゲームオブジェクトを作成し、OnEnableやOnDisableでの購読は必要ありません。エディタで設定されたメソッドが自動的に呼び出されます。
まとめ
Unityでは、標準的なデリゲートやイベントシステムを使用することで、オブザーバーパターンの実装をシンプルかつ効果的に行うことができます。これにより、開発の効率性が向上し、コードの可読性が改善されます。デリゲートやイベントシステムは、特にUnity環境において、通知システムの構築に最適な方法です。

この授業を通じて、Unityでのイベントシステムやデリゲートの使用方法を理解し、適切な場面で効果的に活用できるようになります。

