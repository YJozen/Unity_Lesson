**InputSystem 2**
InteractionとProcessor
# Input Systemで連打防止を実現するInteraction

https://nekojara.city/unity-input-system-prevent-button-mashing

---
## Input Systemでボタンを短い間隔で連打できないようにする

Input SystemのInteractionを使用し、ボタンが押されたら一定時間だけ入力を受け付けなくなるようにします。

Interactionで連打防止を実装するメリットとして
+ 連打防止のロジックとそれ以外のゲームロジックを綺麗に分離できる
+ 複数のInput Actionに流用できる


## 連打防止のInteractionの実装方法
次のような状態遷移のInteractionを実装すれば連打防止が実現できます。


![](images/7/7_4/unity-input-system-prevent-button-mashing-1.png.avif "")


Performedに遷移するための２つの条件
+ 入力値がPress以上
+ 前回のPerformedへの遷移（performedコールバック発火）からn秒以上経過

通常のDefault InteractionのButtonの場合は１つ目の条件しかありませんが、連打防止Interactionでは時間経過の条件が追加します。

## Interactionの実装例
以下、連打防止Interactionの実装例

```cs:PreventMashInteraction.cs

using UnityEngine;
using UnityEngine.InputSystem;

public class PreventMashInteraction : IInputInteraction
{
    // 最小の入力間隔[s]（押された後、入力を受け付けない時間[s]）
    public float minInputDuration;

    // 入力判定の閾値(0でデフォルト値)
    public float pressPoint;

    // 設定値かデフォルト値の値を格納するフィールド
    private float pressPointOrDefault => pressPoint > 0 ? pressPoint : InputSystem.settings.defaultButtonPressPoint;
    private float releasePointOrDefault => pressPointOrDefault * InputSystem.settings.buttonReleaseThreshold;

    // 直近のPerformed状態に遷移した時刻
    private double _lastPerformedTime;

    /// <summary>
    /// 初期化
    /// </summary>
#if UNITY_EDITOR
    [UnityEditor.InitializeOnLoadMethod]
#else
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
#endif
    public static void Initialize()
    {
        // 初回にInteractionを登録する必要がある
        InputSystem.RegisterInteraction<PreventMashInteraction>();
    }

    public void Process(ref InputInteractionContext context)
    {
        if (context.isWaiting)// Waiting状態
        {
            // 入力が０以外かどうか
            if (context.ControlIsActuated())
            {     
                context.Started();// ０以外ならStarted状態に遷移
            }
        }

        if (context.isStarted)// Started状態
        {
            // 入力がPress以上
            //     かつ
            // 前回のPerformed状態遷移から「minInputDuration」以上経過 したかどうか
            if (context.ControlIsActuated(pressPointOrDefault) && context.time >= _lastPerformedTime + minInputDuration)
            {
                // Performed状態に遷移
                context.PerformedAndStayPerformed();

                // Performed状態遷移時の時刻を保持
                _lastPerformedTime = context.time;
            }
            // 入力が０かどうか
            else if (!context.ControlIsActuated())
            {    
                context.Canceled();// ０ならCanceled状態に遷移
            }
        }

        if (context.phase == InputActionPhase.Performed)// Performed状態
        {
            // 入力がRelease以下かどうか
            if (!context.ControlIsActuated(releasePointOrDefault))
            {
                context.Canceled();// Canceled状態に遷移
            }
        }
    }

    public void Reset()
    {
    }
}


```
上記スクリプトをPreventMashInteraction.csという名前でUnityプロジェクトに保存すると機能するようになります。


## Interactionの適用例
Actionに対して連打防止を適用させます。


![](images/7/7_4/unity-input-system-prevent-button-mashing-2.png.avif "")

適用したい対象のActionを選択し、Action PropertiesのInteractions右の＋アイコンをクリックし、Pervent Mashを選択。

以下のように自作のInteractionが追加されますので、必要に応じてパラメータを調整してください。


![](images/7/7_4/unity-input-system-prevent-button-mashing-3.png.avif "")


例ではボタンが押されてから入力を受け付けない時間（Min Input Duration）を1秒としました。Press Pointはデフォルト値を示す0としました。
設定が済んだら忘れずにSave AssetボタンをクリックしてInput Actionの設定内容を保存してください。


## テスト用スクリプトの実装
正しくInteractionが適用されたか確認するために、テスト用スクリプトから入力受け取りの確認を行ってみます。こちらは必須の手順ではないため、不要ならスキップして構いません。

以下、Player Input経由でボタン入力を受け取る例です

```cs:CheckSubmitExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class CheckSubmitExample : MonoBehaviour
{
    // Player Inputから経由で受け取るコールバック
    public void OnSubmit(InputAction.CallbackContext context)
    {
        // コールバックを受け取ったら、Phase（Interactionの状態）をログ出力
        Debug.Log($"Submit action phase = {context.phase}");
    }
}


```

上記スクリプトをCheckSubmitExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチしておきます。

![](images/7/7_4/unity-input-system-prevent-button-mashing-4.png.avif "")

入力を受け取れるように、適当なゲームオブジェクトにPlayer Inputコンポーネントをアタッチします。次に、インスペクターのPlayer InputコンポーネントのActions項目に、該当するInput Action Assetを指定。Behaviourには ”Invoke Unity Events” を指定し、Eventsに、該当GameObjectとActionを登録。

さいごに実行確認。

ボタンを連打しても、一定時間より短い間隔では、performedコールバックが発火されないようになっているはずです。  
（startedコールバックは押される度に、canceledコールバックは離される度に発火するようにしているため、連打するとperformedコールバックだけが少ない回数になるかと思います。）
![](images/7/7_4/unity-input-system-prevent-button-mashing-5.png.avif "")



## スクリプトの解説
Interactionの実装は、IInputInteractionインタフェースを実装することで行います。IInputInteractionはUnityEngine.InputSystem名前空間に属するため、次のようにusingしてインタフェースを実装しています。

```cs:
using UnityEngine;
using UnityEngine.InputSystem;

public class PreventMashInteraction : IInputInteraction
```

Interactionの設定項目はpublicフィールドとして定義します。

```cs:
// 最小の入力間隔[s]（押された後、入力を受け付けない時間[s]）
public float minInputDuration;

// 入力判定の閾値(0でデフォルト値)
public float pressPoint;
```

受け取った入力の処理はProcessメソッド内で行います。この中でInteractionのPhaseの状態遷移を記述していきます。

```cs:
public void Process(ref InputInteractionContext context)
```

Processメソッドはコントローラーなどの入力値が変更されるたびに呼ばれます。

Waiting状態のときに０以外が入力されたときにStartedに遷移する処理を行っています。
```cs:
if (context.isWaiting)// Waiting状態
{
    // 入力が０以外かどうか
    if (context.ControlIsActuated())
    {
        // ０以外ならStarted状態に遷移
        context.Started();
    }
}
```
context.isWaitingプロパティでInteractionがWaiting状態かを判定しています。

次の書き方でも同様の判定ができます。

```cs:
if (context.phase == InputActionPhase.Waiting)
```

context.ControlIsActuatedメソッドで入力値の大きさが0より大きいかどうかを判定し、条件が真ならcontext.Startedメソッド呼び出しでStarted状態に遷移しています。

Phaseの遷移が発生すると、コールバックが呼び出されます。例えばPhaseがWaitingからStartedに遷移すると、startedコールバックが呼び出されます。

Startedからの状態遷移は以下で行っています。
```cs:
if (context.isStarted)
{
    // Started状態

    // 入力がPress以上
    //     かつ
    // 前回のPerformed状態遷移から「minInputDuration」以上経過 したかどうか
    if (context.ControlIsActuated(pressPointOrDefault) && context.time >= _lastPerformedTime + minInputDuration)
    {
        // Performed状態に遷移
        context.PerformedAndStayPerformed();

        // Performed状態遷移時の時刻を保持
        _lastPerformedTime = context.time;
    }
    // 入力が０かどうか
    else if (!context.ControlIsActuated())
    {
        // ０ならCanceled状態に遷移
        context.Canceled();
    }
}
```

context.ControlIsActuatedメソッドは引数に閾値を渡せるため、ボタンが押された判定となる閾値Press Pointを渡しています。また、入力された時の時刻context.timeを用い、前回のボタン押下から指定時間経過しているかを判定する条件が追加されています。

両方の条件を満たした時だけcontext.PerformedAndStayPerformedメソッドを呼び出してPerformed状態に遷移させます。

入力が０に戻ったら、処理を中断するためにcontext.Canceledメソッド呼び出しでCanceled状態に遷移させます。

Performed状態では、ボタンが離された時にCanceled状態に遷移させるようにしています。
```cs:
if (context.phase == InputActionPhase.Performed)// Performed状態
{
    // 入力がRelease以下かどうか
    if (!context.ControlIsActuated(releasePointOrDefault))
    {
        // Canceled状態に遷移
        context.Canceled();
    }
}
```

ボタンが離された判定に用いる閾値には、Press Pointではなくそれより小さな値のRelease Pointを使います。これは値のぶれによってボタンが押されているにも関わらず離された判定になるのを防ぐためです。







