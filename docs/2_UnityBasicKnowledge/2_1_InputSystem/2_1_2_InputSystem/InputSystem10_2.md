# Input SystemのカスタムInteractionで、特殊な操作を実装する

・今回カスタムInteractionで実装する操作
+ スティックを素早く倒すことによってダッシュするという想定

## スティック早倒しの実装例
「ゲームパッドのスティックを素早く倒したときにダッシュさせる」を考えてみます。

実装の流れはダブルタップスプリントと一緒ですが、実装するInteractionとComposite Bindingの内容が異なります。

<img src="images/8/8_5/unity-input-system-custom-interaction-sprint-5.png.avif" width="80%" alt="" title="">

<br>

入力値の大きさがStart Press PointからEnd Press Pointまで時間Max Delay以内に変化したときにPerformedコールバックを通知するものとします。

時間以内に変化しなかった場合や、入力がなくなった時（Release Point以下となった時）、Canceledコールバックを通知するものとします。

以下、Interactionの実装例です。

QuickPressInteraction.cs
```cs
using UnityEngine;
using UnityEngine.InputSystem;

internal class QuickPressInteraction : IInputInteraction
{
    // スティック倒し始めの入力値の大きさ
    public float startPressPoint = 0.2f;
    
    // スティック倒し終わりの入力値の大きさ
    public float endPressPoint = 0.9f;
    
    // スティックを完全に倒し終わるまでの最大許容時間[s]
    public float maxDelay = 0.1f;
    
    // スティックを離したと判断する閾値
    public float releasePoint = 0.375f;

    private double _startPressTime;
    private bool _isFree = true;

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
        InputSystem.RegisterInteraction<QuickPressInteraction>();
    }

    public void Process(ref InputInteractionContext context)
    {
        // タイムアウト判定
        if (context.timerHasExpired)
        {
            // 最大許容時間を超えてタイムアウトになった場合はキャンセル
            context.Canceled();
            return;
        }

        switch (context.phase)
        {
            case InputActionPhase.Waiting:
                // 入力待機状態

                if (!_isFree)
                {
                    // ニュートラル位置チェック
                    if (!context.ControlIsActuated(startPressPoint))
                    {
                        _isFree = true;
                    }

                    break;
                }

                // スティックがニュートラル位置なら、入力チェック
                if (context.ControlIsActuated(endPressPoint))
                {
                    // 一気にスティックが倒された場合
                    _isFree = false;
                    _startPressTime = context.time;

                    // Started、Performedコールバックを一気に発火
                    context.Started();
                    context.PerformedAndStayPerformed();
                }
                else if (context.ControlIsActuated(startPressPoint))
                {
                    // スティックが倒され始めた場合
                    _isFree = false;
                    _startPressTime = context.time;

                    // Startedコールバック発火
                    context.Started();
                    context.SetTimeout(maxDelay);
                }

                break;

            case InputActionPhase.Started:
                // スティックが倒され始めている状態

                if (context.time - _startPressTime <= maxDelay)
                {
                    // 最大許容時間内にスティックが完全に倒されたかチェック
                    if (context.ControlIsActuated(endPressPoint))
                    {
                        // 倒されたらPerformedコールバックを発火
                        context.PerformedAndStayPerformed();
                    }
                }
                else
                {
                    // 最大許容時間内にスティックが完全に倒されなければ中断とみなす
                    context.Canceled();
                }

                break;

            case InputActionPhase.Performed:
                // スティック早倒し中

                // スティックが戻されているかどうかのチェック
                if (!context.ControlIsActuated(releasePoint))
                {
                    context.Canceled();
                }
                else if (context.ControlIsActuated())
                {
                    context.PerformedAndStayPerformed();
                }

                break;
        }
    }

    public void Reset()
    {
        _startPressTime = 0;
    }
}
```

上記をQuickPressInteraction.csという名前で保存するとInteractionが使えるようになります。


## 入力値の大きさに変換するComposite Bindingの実装

スティック入力はVector2型の入力ですが、これをfloat型に変換するComposite Bindingを実装します。

MagnitudeComposite.cs
```cs
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Layouts;

internal class MagnitudeComposite : InputBindingComposite<float>
{
    // 入力
    [InputControl] public int input = 0;

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
        InputSystem.RegisterBindingComposite(typeof(MagnitudeComposite), "Magnitude");
    }
    
    /// <summary>
    /// 入力値の大きさに変換して返す
    /// </summary>
    public override float ReadValue(ref InputBindingCompositeContext context)
    {
        return context.EvaluateMagnitude(input);
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

上記をMagnitudeComposite.csという名前で保存しておきます。

<br>

## Actionへの適用
先述のComposite BindingをActionに追加します。

<img src="images/8/8_5/unity-input-system-custom-interaction-sprint-m8.mp4.gif" width="80%" alt="" title="">

<br>

追加したComposite Bindingにスティック入力などのControl Pathを設定します。


<img src="images/8/8_5/unity-input-system-custom-interaction-sprint-m9.mp4.gif" width="80%" alt="" title="">

<br>


そして、Quick Press Interactionを先述のComposite Bindingに適用し、必要に応じてパラメータの設定を行います。


<img src="images/8/8_5/unity-input-system-custom-interaction-sprint-m10.mp4.gif" width="80%" alt="" title="">

<br>


設定したら、忘れずにSave Assetボタンクリックで内容を保存してください。

あとは好きな方法でActionを実行してみてください。成功すると、スティックを素早く倒すと入力が通知され、ゆっくり倒すと通知されなくなります。

<br>


## Interactionを適用する場合の注意点
複数のダッシュ操作を適用する際、ボタン操作とInteractionを共存させると、操作が競合して次のようなエラーが出る場合があるようです。

Value type actions should not be left in performed state
主にダブルタップなどのInteraction操作とボタン押下を同時に行った際にエラーとなります。理由は、InteractionのフェーズがPerformedのままになっているためです。

一般的に、Unity提供のプリセットでも同様の問題が起こるため、現状ではInteractionを使用する場合はAction TypeをPass Throughにしておくか、ボタン入力のBindingを消す（必要なら別Actionにしてしまう）などの対策が必要になるかもしれません。


<img src="images/8/8_5/unity-input-system-custom-interaction-sprint-6.png.avif" width="80%" alt="" title="">

Input Systemのクラス仕様を理解したうえで実装しないといけない点が面倒かもしれませんが、一度実装すると使いまわせる点では良いかもしれません。

入力タイミングの検知という時系列が絡む複雑な処理をInteraction側に任せることにより、入力値を処理するロジックとキャラクター操作のロジックが綺麗に分かれるメリットがあります。

開発するコンテンツに合わせて検討すると良いでしょう。