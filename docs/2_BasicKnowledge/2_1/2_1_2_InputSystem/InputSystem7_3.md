**InputSystem 2**

# Interactionで連打を判定する

## 1.実装目標

+ 連打されるたびにperformedコールバックを通知　　
+ ボタンの連打時間間隔の最大値を指定可能にする　　
+ ボタンが連打された回数を取得可能にする

### フェーズ

Interactionでは、内部的に次の5つのフェーズ（状態）を持つステートマシンとして管理されます。

+ Waiting – 入力待ち状態
+ Started – Interactionが開始された状態
+ Performed – Interactionが期待する入力を満たした状態
+ Canceled – Interactionがキャンセルされた状態
+ Disable – Actionが無効な状態

( Interactionが使用するのはDisableを除く4フェーズ )

### 2.目指すフェーズごとの遷移
![](images/7/7_3/unity-input-system-button-mashing-1.png.avif "")


t秒以内にボタン変化（押された状態と離された状態の変化）が無ければ連打終了とみなします。

上記のボタンが押された判定ですが、これはフェーズとは別にボタンフェーズとして別のステートマシンで実現します。

![](images/7/7_3/unity-input-system-button-mashing-2.png.avif "")

入力値の大きさの変化をチェックし、入力無しから有りに変化するたびに連打回数を加算していくようにします。通常は回数を保持する変数をインクリメントすれば良いです。

そして、1つ目のフェーズの遷移でCanceledに移行したら、連打終了として連打回数をリセット（0に初期化）します。

本記事では、ボタンが押された瞬間、すなわちWaitingForNextReleaseに遷移する時に連打回数を加算してボタンが押された判定とします。


## 3.連打判定を行うInteractionの実装例

前述のフェーズやボタンフェーズの遷移に基づいて連打判定を行うInteractionを実装する例

```cs:MashInteraction.cs

    using UnityEngine;
    using UnityEngine.InputSystem;

    public class MashInteraction : IInputInteraction
    {
        // 各タップの最大許容時間間隔[s]
        public float tapDelay;

        // 入力判定の閾値(0でデフォルト値)
        public float pressPoint;

        // 連打判定に必要な回数
        public int requiredTapCount = 2;

        // 連打された回数
        public int TapCount { get; private set; }

        // 設定値かデフォルト値の値を格納するフィールド
        private float PressPointOrDefault => pressPoint > 0 ? pressPoint : InputSystem.settings.defaultButtonPressPoint;
        private float ReleasePointOrDefault => PressPointOrDefault * InputSystem.settings.buttonReleaseThreshold;
        private float TapDelayOrDefault => tapDelay > 0 ? tapDelay : InputSystem.settings.multiTapDelayTime;

        // ボタンフェーズ
        private enum ButtonPhase
        {
            None,
            WaitingForNextRelease,
            WaitingForNextPress,
        }

        private ButtonPhase _currentButtonPhase;
        private int _remainingRequiredTapCount;

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
            InputSystem.RegisterInteraction<MashInteraction>();
        }

        public void Process(ref InputInteractionContext context)
        {
            // タイムアウトチェック
            if (context.timerHasExpired)
            {
                // 最大許容時間以上ボタン変化が無かったら、連打終了とみなす
                context.Canceled();
                return;
            }

            switch (_currentButtonPhase)
            {
                case ButtonPhase.None:
                    // 入力され始めた
                    if (context.ControlIsActuated(PressPointOrDefault))
                    {
                        // ボタンを離すまで待機
                        _currentButtonPhase = ButtonPhase.WaitingForNextRelease;

                        // 残りのタップ回数を初期化
                        _remainingRequiredTapCount = requiredTapCount - 1;

                        // Startedフェーズに移行
                        context.Started();

                        // 必要タップ回数以上タップされたら連打判定とする
                        if (_remainingRequiredTapCount <= 0)
                        {
                            TapCount++;

                            // Performedフェーズに移行
                            context.PerformedAndStayPerformed();
                        }

                        // タイムアウトを設定
                        context.SetTimeout(TapDelayOrDefault);
                    }

                    break;

                case ButtonPhase.WaitingForNextRelease:
                    if (!context.ControlIsActuated(ReleasePointOrDefault))
                    {
                        // ボタンを押すまで待機
                        _currentButtonPhase = ButtonPhase.WaitingForNextPress;
                    }

                    break;

                case ButtonPhase.WaitingForNextPress:
                    if (context.ControlIsActuated(PressPointOrDefault))
                    {
                        // ボタンを離すまで待機
                        _currentButtonPhase = ButtonPhase.WaitingForNextRelease;

                        // 必要タップ回数に満たなければ、残りの必要タップ回数を更新
                        if (_remainingRequiredTapCount > 0)
                        {
                            _remainingRequiredTapCount--;
                        }

                        // 必要タップ回数以上タップされたら連打判定とする
                        if (_remainingRequiredTapCount <= 0)
                        {
                            // 連打回数をカウント
                            TapCount++;

                            // Performedフェーズに移行
                            context.PerformedAndStayPerformed();
                        }

                        // タイムアウトを設定
                        context.SetTimeout(TapDelayOrDefault);
                    }

                    break;
            }
        }

        public void Reset()
        {
            _currentButtonPhase = ButtonPhase.None;
            TapCount = 0;
        }
    }

```


上記をMashInteraction.csという名前でUnityプロジェクトに保存すると、Interactionが使えるようになります。


## 4.入力を受け取るスクリプトの実装
次のようにInput Actionのコールバックを受け取ってログ出力するスクリプトから連打判定結果を受け取るものとします。あくまで使用例のため必須ではありません。


UseExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチすると機能します。

アタッチすると、インスペクターからActionを設定できるようになるため、Bindingを設定してください。

![](images/7/7_3/unity-input-system-button-mashing-3.png.avif "")


```cs:UseExample.cs
    using UnityEngine;
    using UnityEngine.InputSystem;

    public class UseExample : MonoBehaviour
    {
        [SerializeField] private InputAction _action;

        private void Awake()
        {
            _action.started += OnAction;
            _action.performed += OnAction;
            _action.canceled += OnAction;
        }

        private void OnDestroy()
        {
            _action.started -= OnAction;
            _action.performed -= OnAction;
            _action.canceled -= OnAction;

            _action.Dispose();
        }

        private void OnEnable()
        {
            _action.Enable();
        }

        private void OnDisable()
        {
            _action.Disable();
        }

        private void OnAction(InputAction.CallbackContext context)
        {
            switch (context.phase)
            {
                case InputActionPhase.Started:
                    print("ボタンが押された！");
                    break;

                case InputActionPhase.Performed:
                    print("ボタンが連打された！");
                    break;

                case InputActionPhase.Canceled:
                    print("連打がキャンセルされた！");
                    break;
            }
        }
    }


```

## 5.Interactionの適用・実装例

連打判定を行いたいInput ActionのInteractionにMash Interactionを適用します。(該当するActionまたはBindingをダブルクリックし、Action PropertyのInteraction右の＋アイコンをクリックし、Mashを選択します。)    
すると、次のように連打判定を行うMash Interactionが追加されるので、必要に応じて項目を設定してください
![](images/7/7_3/unity-input-system-button-mashing-4.png.avif "")

+ Tap Delay – タップの最大許容時間間隔[s]。この時間を超えてタップが無いと連打終了とみなす。0はInput System側のデフォルト値。
+ Press Point – ボタンを押したとみなす入力値の大きさの閾値。0の時はデフォルト値となる。
+ Required Tap Count – 連打判定に必要な最低回数。この回数以上ボタンが連打されたら連打判定となる。

ボタンを短い時間間隔（Tap Delayに設定した時間以内）で連打すると、コンソールログに連打の旨のメッセージが出力されます。  
連打するたびにperformedコールバックが実行されて連打メッセージが表示されます。  
ボタンを一定時間操作（押したり離したり）しなければ、canceledコールバックが実行されて終了します。

## 6.スクリプトの説明

Interactionの設定パラメータは、以下のようにpublicフィールドとして定義しています。

```cs:

// 各タップの最大許容時間間隔[s]
public float tapDelay;

// 入力判定の閾値(0でデフォルト値)
public float pressPoint;

// 連打判定に必要な回数
public int requiredTapCount = 2;

```
<br>

ボタンが押されたとみなす閾値Press Pointやタップの最大許容時間間隔などは、0ならデフォルト値を使うように以下プロパティが管理しています。

```cs:
// 設定値かデフォルト値の値を格納するフィールド
private float PressPointOrDefault => pressPoint > 0 ? pressPoint : InputSystem.settings.defaultButtonPressPoint;
private float ReleasePointOrDefault => PressPointOrDefault * InputSystem.settings.buttonReleaseThreshold;
private float TapDelayOrDefault => tapDelay > 0 ? tapDelay : InputSystem.settings.multiTapDelayTime;
```

<br>
また、ボタンの状態変化を管理するために、独自のボタンフェーズをenumフィールドで定義しています。

```cs:
// ボタンフェーズ
private enum ButtonPhase
{
    None,
    WaitingForNextRelease,
    WaitingForNextPress,
}

private ButtonPhase _currentButtonPhase;
```
<br>

ある一定時間以上ボタン変化が無かったら連打終了とする判定は、次の処理で行っています。
```cs:
// タイムアウトチェック
if (context.timerHasExpired)
{
    // 最大許容時間以上ボタン変化が無かったら、連打終了とみなす
    context.Canceled();
    return;
}
```
context.timerHasExpiredプロパティは、予め設定しておいたタイムアウト時間を過ぎたときにtrueを返します。


タイムアウト時間はボタンが押されるたびにcontext.SetTimeoutメソッドで設定するようにします。
```cs:
// タイムアウトを設定
context.SetTimeout(TapDelayOrDefault);
```

待機状態からボタンが押される（入力値がPress Point以上になる）と、ボタンフェーズを「ボタンを離すまで待機」する状態に移行させます。

入力値が閾値以上かどうかの判定は、context.ControlIsActuatedメソッドで行えます。trueなら閾値以上（ただし閾値0なら0より大きい）、falseなら閾値未満（ただし閾値0の場合は入力値0）と判断できます。

```cs:
case ButtonPhase.None:
    // 入力され始めた
    if (context.ControlIsActuated(PressPointOrDefault))
    {
        // ボタンを離すまで待機
        _currentButtonPhase = ButtonPhase.WaitingForNextRelease;

        // 残りのタップ回数を初期化
        _remainingRequiredTapCount = requiredTapCount - 1;

        // Startedフェーズに移行
        context.Started();

        // 必要タップ回数以上タップされたら連打判定とする
        if (_remainingRequiredTapCount <= 0)
        {
            TapCount++;

            // Performedフェーズに移行
            context.PerformedAndStayPerformed();
        }

        // タイムアウトを設定
        context.SetTimeout(TapDelayOrDefault);
    }

    break;
```
Noneの時、連打に必要な残りのタップ回数_remainingRequiredTapCountを初期化したり、フェーズをStartedに移行したりしています。

ボタンが押されたときに_remainingRequiredTapCountが0以下になったら連打と判定し、連打回数TapCountをインクリメントでカウントしています。

ボタンが押された状態から離されたかを判定する処理は以下部分です。

```cs:
case ButtonPhase.WaitingForNextRelease:
    if (!context.ControlIsActuated(ReleasePointOrDefault))
    {
        // ボタンを押すまで待機
        _currentButtonPhase = ButtonPhase.WaitingForNextPress;
    }

    break;
```

ここでボタンフェーズを「ボタンが押されるまで待機」する状態に移行しています。

<br>

```cs:
case ButtonPhase.WaitingForNextPress:
    if (context.ControlIsActuated(PressPointOrDefault))
    {
        // ボタンを離すまで待機
        _currentButtonPhase = ButtonPhase.WaitingForNextRelease;

        // 必要タップ回数に満たなければ、残りの必要タップ回数を更新
        if (_remainingRequiredTapCount > 0)
        {
            _remainingRequiredTapCount--;
        }

        // 必要タップ回数以上タップされたら連打判定とする
        if (_remainingRequiredTapCount <= 0)
        {
            // 連打回数をカウント
            TapCount++;

            // Performedフェーズに移行
            context.PerformedAndStayPerformed();
        }

        // タイムアウトを設定
        context.SetTimeout(TapDelayOrDefault);
    }

    break;
```
連打判定のロジックは、NoneからWaitingForNextReleaseに遷移する時と一緒です。

連打判定されたら、フェーズをPerformedに移行し、連打終了するまでPerformedに留まらせます。

この時も忘れずにcontext.SetTimeoutメソッドでタイムアウト設定する必要があります。



## 7.連打された回数を取得する

応用例として、連打された回数を取得する例を紹介します。

入力の受取り側で変数管理しても良いですが、本記事では連打回数をInteraction側で管理するようにします。

前述のMash Interactionでは、TapCountプロパティから連打回数を取得できるようになっています。これを次のようにコールバック引数からInteraction経由で取得できます。

```cs:
private void OnPerformed(InputAction.CallbackContext context)
{
    if (context.interaction is not MashInteraction mashInteraction) return;

    // 連打回数を表示
    print($"連打回数 : {mashInteraction.TapCount}");
}
```

コールバックで受け取る引数contextのinteractionプロパティより、実際に反応したInteractionを取得できます。

必要に応じてキャストして使います。


連打回数をスクリプトから取得してログ出力する例

```cs:TapCountExample.cs

    using UnityEngine;
    using UnityEngine.InputSystem;

    public class TapCountExample : MonoBehaviour
    {
        // 連打判定Interactionが指定されていると想定するAction
        [SerializeField] private InputAction _action;

        private void Awake()
        {
            // Performedコールバックのみ登録
            _action.performed += OnPerformed;
        }

        private void OnDestroy()
        {
            _action.performed -= OnPerformed;
            _action.Dispose();
        }

        private void OnEnable()
        {
            _action.Enable();
        }

        private void OnDisable()
        {
            _action.Disable();
        }

        private void OnPerformed(InputAction.CallbackContext context)
        {
            // 連打判定Interactionをキャストして取得
            // キャストに失敗したら何もしない
            if (context.interaction is not MashInteraction mashInteraction) return;

            // 連打回数を表示
            print($"連打回数 : {mashInteraction.TapCount}");
        }
    }
```
上記をTapCountExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、ActionよりBindingとMash Interactionを設定してください。


![](images/7/7_3/unity-input-system-button-mashing-5.png.avif "")


Actionに登録したボタンを連打すると、その連打回数がログ出力されます。



