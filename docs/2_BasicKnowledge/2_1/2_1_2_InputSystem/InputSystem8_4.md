**InputSystem 2**

# Input SystemのカスタムInteractionで、ダブルタップなどでキャラクターをダッシュさせるダッシュ操作を実装する

https://nekojara.city/unity-input-system-custom-interaction-sprint




Interactionで検知できる操作
WASDキーのダブルタップ（ダブルタップスプリント）
スティックを素早く倒す



Input SystemのInteractionはこのような特定の入力パターンを検知した時に入力を通知する機能を有しているため、今回のケースに適したものと言えるでしょう。 [1]
ダブルタップ操作のInteractionには、Multi Tap Interactionというプリセットが用意されていますが、ダブルタップ直後にダッシュキャンセルされてしまう問題があったため、今回は自作のInteractionを実装して対応することとしました。

本記事では、自作のInteractionを実装して、ダブルタップやスティック早倒しによるダッシュ操作を実現する方法を解説




## ダブルタップスプリントの実装の流れ

本記事では、WASDキーのダブルタップ操作などを検知したときに「ダッシュボタンが押された」ような振る舞いをさせることを目標とします。

具体的には、ダッシュ操作を検知した時にPerformedコールバックを発火し、その後にボタンを離したらCanceledコールバックが発火するようなInteractionの実装を目指します。

本記事で紹介する実装の流れは以下のようになります。

・実装の流れ
+ カスタムInteractionの実装
+ カスタムComposite Bindingの実装
+ 上記InteractionとComposite BindingをダッシュActionに適用


２つ目のカスタムComposite Bindingの実装ですが、これはスクリプト側からボタン入力として入力値を受け取りたい場合に必要になることがあります。

理由は、２軸のWASD入力がVector2型であるのに対し、ボタン入力はfloat型であり、両者の型不一致が生じるためです。



## マルチタップ＆ホールドを検知するInteractionの実装

次のような挙動をするカスタムInteractionを実装するものとします。


<img src="images/8/8_4/unity-input-system-custom-interaction-sprint-2.png.avif" width="50%" alt="" title="">

<br>

指定された回数だけ素早くタップし、押しっぱなしになった時にPerformedコールバックを通知します。

Performedコールバックの後に入力がなくなった場合、一定時間ウェイトを置いてからCanceledコールバックを通知することとします。これは、入力方向を切り替えた瞬間などにダッシュキャンセルにならなくするための処置です。

以下、Interactionの実装例です。

```cs:MultiTapAndHoldInteraction.cs

using UnityEngine;
using UnityEngine.InputSystem;

internal class MultiTapAndHoldInteraction : IInputInteraction
{
    // 最大のタップ時間[s]
    public float tapTime;

    // 次のタップまでの最大待機時間[s]
    public float tapDelay;

    // 必要なタップ数
    public int tapCount = 2;

    // 入力判定の閾値(0でデフォルト値)
    public float pressPoint;

    // リリース判定の閾値(0でデフォルト値)
    public float releasePoint;

    // マルチタップ＆ホールド後、入力がなくなってから終了するまでの時間
    public float endDelay;

    // タップ状態の内部フェーズ
    private enum TapPhase
    {
        None,
        WaitingForNextRelease,
        WaitingForNextPress,
        WaitingForRelease,
        WaitingForEnd,
    }

    // 設定値かデフォルト値の値を格納するフィールド
    private float tapTimeOrDefault => tapTime > 0.0 ? tapTime : InputSystem.settings.defaultTapTime;
    private float tapDelayOrDefault => tapDelay > 0.0 ? tapDelay : InputSystem.settings.multiTapDelayTime;
    private float pressPointOrDefault => pressPoint > 0 ? pressPoint : InputSystem.settings.defaultButtonPressPoint;
    private float releasePointOrDefault => pressPointOrDefault * InputSystem.settings.buttonReleaseThreshold;

    // Interactionの内部状態
    private TapPhase _currentTapPhase = TapPhase.None;
    private double _currentTapStartTime;
    private double _lastTapReleaseTime;
    private int _currentTapCount;

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
        InputSystem.RegisterInteraction<MultiTapAndHoldInteraction>();
    }

    /// <summary>
    /// Interactionの内部処理
    /// </summary>
    public void Process(ref InputInteractionContext context)
    {
        // タイムアウト判定
        if (context.timerHasExpired)
        {
            // 最大許容時間を超えてタイムアウトになった場合はキャンセル
            context.Canceled();
            return;
        }

        switch (_currentTapPhase)
        {
            case TapPhase.None:
                // 初期状態

                // タップされたかチェック
                if (context.ControlIsActuated(pressPointOrDefault))
                {
                    _currentTapStartTime = context.time;

                    if (++_currentTapCount >= tapCount)
                    {
                        // 必要なタップ数に達したらPerformedコールバック実行
                        _currentTapPhase = TapPhase.WaitingForRelease;
                        context.Started();
                        context.PerformedAndStayPerformed();
                    }
                    else
                    {
                        // 入力がなくなるまで待機
                        _currentTapPhase = TapPhase.WaitingForNextRelease;
                        context.Started();
                        context.SetTimeout(tapTimeOrDefault);
                    }
                }

                break;

            case TapPhase.WaitingForNextRelease:
                // 入力がなくなるまで待機している状態
                if (!context.ControlIsActuated(releasePointOrDefault))
                {
                    if (context.time - _currentTapStartTime > tapTimeOrDefault)
                    {
                        // 最大許容時間を超えたのでキャンセル
                        context.Canceled();
                        break;
                    }

                    // 次の入力待ち状態に遷移
                    _lastTapReleaseTime = context.time;
                    _currentTapPhase = TapPhase.WaitingForNextPress;
                    context.SetTimeout(tapDelayOrDefault);
                }

                break;

            case TapPhase.WaitingForNextPress:
                // 次の入力待ちの状態
                if (context.ControlIsActuated(pressPointOrDefault))
                {
                    if (context.time - _lastTapReleaseTime > tapDelayOrDefault)
                    {
                        // 最大許容時間を超えたのでキャンセル
                        context.Canceled();
                        break;
                    }

                    ++_currentTapCount;
                    _currentTapStartTime = context.time;

                    if (_currentTapCount >= tapCount)
                    {
                        // 必要なタップ数に達したので、Performedコールバック通知
                        // 終了まで待機する状態に遷移
                        _currentTapPhase = TapPhase.WaitingForRelease;
                        context.PerformedAndStayPerformed();
                    }
                    else
                    {
                        // 必要タップ数に達していないので、入力がなくなるまで待機
                        _currentTapPhase = TapPhase.WaitingForNextRelease;
                        context.SetTimeout(tapTimeOrDefault);
                    }

                    _currentTapStartTime = context.time;
                }

                break;

            case TapPhase.WaitingForRelease:
                // マルチタップ判定後、入力がなくなるまで待機している状態

                // 入力チェック
                if (!context.ControlIsActuated(releasePointOrDefault))
                {
                    // 入力がなくなったので終了
                    _currentTapPhase = TapPhase.WaitingForEnd;
                    _lastTapReleaseTime = context.time;
                    context.SetTimeout(endDelay);
                }

                break;

            case TapPhase.WaitingForEnd:
                // 入力がなくなってからInteractionを終了するまで待機している状態
                if (context.time - _lastTapReleaseTime >= endDelay)
                {
                    // 一定時間経過したので終了する
                    context.Canceled();
                }
                else if (context.ControlIsActuated(pressPointOrDefault))
                {
                    // 再び入力があった
                    // 一定時間経過していないので、継続とみなす
                    _currentTapPhase = TapPhase.WaitingForRelease;
                    context.PerformedAndStayPerformed();
                }

                break;
        }
    }

    /// <summary>
    /// Interactionの状態リセット
    /// </summary>
    public void Reset()
    {
        _currentTapPhase = TapPhase.None;
        _currentTapStartTime = 0;
        _lastTapReleaseTime = 0;
        _currentTapCount = 0;
    }
}

```


上記をMultiTapAndHoldInteraction.csという名前でUnityプロジェクトに保存すると、以下のようにInteractionが使用可能になります。


<img src="images/8/8_4/unity-input-system-custom-interaction-sprint-3.png.avif" width="50%" alt="" title="">

<br>

ダブルタップのみならず、任意回数のタップにも対応することとしました。

処理内容については、ソースコード中のコメントをご覧ください。


## カスタムComposite Bindingの実装

WASDキー入力などをComposite BindingとしてActionに定義しているとき、入力値の型はVector2となります。

この場合、ボタン入力として受け取る場合はfloat型入力値となり、型不一致によるエラーとなります。この状態で入力値を取得しようとすると、次のようなエラーがログ出力されます。

```cs:
InvalidOperationException: Cannot read value of type 'Single' from composite 'UnityEngine.InputSystem.Composites.Vector2Composite' bound to action 'Player/Sprint[/Keyboard/leftShift,/Keyboard/w,/Keyboard/s,/Keyboard/a,/Keyboard/d]' (composite is a 'Int32' with value type 'Vector2')
```

本記事のようなWASDキー入力の大きさを１軸入力（float）として扱いたい場合、４方向入力の大きさをfloat型入力とするカスタムComposite Bindingを実装して適用すれば解決できます。

以下、カスタムComposite Bindingの実装例です。


```cs:DPadMagnitudeComposite.cs
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Controls;
using UnityEngine.InputSystem.Layouts;

internal class DPadMagnitudeComposite : InputBindingComposite<float>
{
    // 4方向ボタン入力
    [InputControl(layout = "Button")] public int up = 0;
    [InputControl(layout = "Button")] public int down = 0;
    [InputControl(layout = "Button")] public int left = 0;
    [InputControl(layout = "Button")] public int right = 0;

    /// <summary>
    /// 初期化
    /// </summary>
#if UNITY_EDITOR
    [UnityEditor.InitializeOnLoadMethod]
#else
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
#endif
    private static void Initialize()
    {
        // 初回にCompositeBindingを登録する必要がある
        InputSystem.RegisterBindingComposite(typeof(DPadMagnitudeComposite), "2DVectorMagnitude");
    }
    
    /// <summary>
    /// 4方向入力からベクトルの大きさに変換して返す
    /// </summary>
    public override float ReadValue(ref InputBindingCompositeContext context)
    {
        var upValue = context.ReadValue<float>(up);
        var downValue = context.ReadValue<float>(down);
        var leftValue = context.ReadValue<float>(left);
        var rightValue = context.ReadValue<float>(right);

        return DpadControl.MakeDpadVector(upValue, downValue, leftValue, rightValue).magnitude;
    }
    
    /// <summary>
    /// 値の大きさを返す
    /// </summary>
    public override float EvaluateMagnitude(ref InputBindingCompositeContext context)
    {
        return ReadValue(ref context);
    }
}

```
上記スクリプトをDPadMagnitudeComposite.csという名前でUnityプロジェクトに保存すると、以下のようにカスタムComposite Bindingが選択可能になります。


<img src="images/8/8_4/unity-input-system-custom-interaction-sprint-4.png.avif" width="50%" alt="" title="">

<br>


## Actionへの適用
該当するダッシュ操作のActionにInteractionとComposite Bindingを適用します。

例では、SprintというActionに対して適用するものとします。

まず、該当Actionの下に、先ほど実装したComposite Bindingを追加します。

<img src="images/8/8_4/unity-input-system-custom-interaction-sprint-m2.mp4.gif" width="50%" alt="" title="">

<br>

そして、方向キーを設定します。例ではWASDキーを上下左右の入力として設定することにします。
