# Interactionを自作する

基本的な入力パターンは幾つかプリセットとして用意されていますが、これらで物足りない場合は自作することも可能。


## Interactionの実装例
以下、
「ボタンが押されたらStarted→Performedフェーズの順に遷移し、ボタンが離されるとCanceled→Waitingフェーズの順に遷移するといったもの。」
のInteraction全体の実装例です。 
 
<br>


MyButtonInteraction.cs
```cs
    using UnityEngine.InputSystem;

    public class MyButtonInteraction : IInputInteraction
    {
    #if UNITY_EDITOR
        [UnityEditor.InitializeOnLoadMethod]
    #else
        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
    #endif

        public static void Initialize()
        {
            // 初回にInteractionを登録する必要がある
            InputSystem.RegisterInteraction<MyButtonInteraction>();
        }

        public void Process(ref InputInteractionContext context)
        {
            switch (context.phase)
            {
                case InputActionPhase.Waiting:
                    // ボタンが押されたらStarted→Performedフェーズの順に遷移
                    if (context.ControlIsActuated(InputSystem.settings.defaultButtonPressPoint))
                    {
                        // ボタンが押された時の処理
                        context.Started();
                        context.PerformedAndStayPerformed();
                    }

                    break;

                case InputActionPhase.Performed:
                    // ボタンが離されたらCanceledフェーズに遷移
                    if (!context.ControlIsActuated(InputSystem.settings.buttonReleaseThreshold))
                    {
                        // ボタンが押された時の処理
                        context.Canceled();
                    }

                    break;
            }
        }

        public void Reset()
        {
        }
    }

```

上記をMyButtonInteraction.csという名前でUnityプロジェクトに保存すると、Input System側にInteractionとして登録され、使用できるようになります。

<img src="images/7/7_2/unity-input-system-interaction-15.png.avif" width="80%" alt="" title="">



<br>

・Interaction関係なく補足

+ #if UNITY_EDITOR  
コードがUnityエディタ上で実行される場合にのみ、そのブロック内のコードをコンパイルするための条件です。

+ #else  
#if UNITY_EDITORが満たされない場合、つまりビルド後のゲーム実行環境でコンパイルされるコードを指定します。

+ #endif  
条件付きコンパイルディレクティブの終了を示します。


+ [UnityEditor.InitializeOnLoadMethod]  
エディタでスクリプトがロードされたときに実行されるメソッドを指定。
このメソッドは、Unityエディタが起動するたびに、もしくはスクリプトがリコンパイルされるたびに呼び出されます。

+ [RuntimeInitializeOnLoadMethod]は、ビルドされたゲームが起動したときに実行されるメソッドを指定。
  - (RuntimeInitializeLoadType.SubsystemRegistration)  
  サブシステムが登録されるタイミングでこのメソッドが呼び出されることを示しています。これはゲームの非常に早い段階での初期化に使用されます。


このように条件付きコンパイルディレクティブを使用することで、「開発中のエディタ環境」と「実際のゲーム環境」で異なる初期化コードを簡単に分けることができます。これにより、「デバッグやエディタ専用の設定」と、「実際のゲームロジックの初期化」を適切に管理することができます。



### 第一歩 

```IInputInteraction```インタフェースを実装したクラスとして作成できます。
特定の型の入力値に限定したい場合、IInputInteraction<T>インタフェースを実装して作成することも可能。

また、カスタムInteractionはアプリケーション初期化などのタイミングで、```InputSystem.RegisterInteraction<T>```メソッドにより、Tに指定したInteractionをInput System側に登録する必要がある。

<br>

### 入力の評価

そのほか、プリセットのInteractionでは、ボタンが押されたか、離されたかどうかの判定が何度か出てきました。  
このような判定は、入力値の大きさがある閾値以上か否かを調べています。  
これは、```InputInteractionContext.ControlIsActuated```メソッドで行います。
引数には閾値を指定します。入力値の大きさが閾値以上ならtrue、そうでなければfalseを返します。  
ただし、引数に指定された閾値が0の時に限り、入力値の大きさが0より大きければtrue、0ならfalseを返す挙動に変化します。

<br>

### 各フェーズへの遷移  ( Process()に記述 )
+ Started() – Startedフェーズへ遷移  
+ Performed() – Performedフェーズへ遷移し、その後Waitingフェーズへ遷移  
+ PerformedAndStayPerformed() – Performedフェーズへ遷移し、そのままPerformedフェーズに留まる  
+ PerformedAndStayStarted() – Performedフェーズへ遷移し、その後Startedフェーズへ遷移  
+ Canceled() – Canceledフェーズへ遷移し、その後Waitingフェーズへ遷移  
+ Waiting() – Waitingフェーズへ遷移し、そのままWaitingフェーズに留まる  

現在のフェーズは、InputInteractionContext.phaseプロパティから取得。

<br>

### タイムアウトの設定
Interactionの処理には、タイムアウトを設けることも可能です。  
設定にはInputInteractionContext.SetTimeoutメソッドを使います。

```public void SetTimeout(float seconds)```
引数に指定された時間（秒）経過したら、強制的にCanceledフェーズに遷移します。  
また、タイムアウトになったかどうかを判定する```InputInteractionContext.timerHasExpired```プロパティ```public bool timerHasExpired { get; }```もあります。
必要に応じて活用すると良いでしょう。




### リセット処理
フェーズがキャンセルされると、Resetメソッドが実行されます。  
Interaction側で独自に使用している状態変数などを初期化したい場合に使えます。









