Input Systemでシングルタップとマルチタップを判別する

【Unity】Input Systemでシングルタップとマルチタップを判別する
2024年7月3日2024年7月2日


https://nekojara.city/unity-input-system-tap-and-multi-tap

こじゃら
マウスのシングルクリックとダブルクリックのどちらかを判定する方法を知りたいの。

このは
Input SystemのInteractionを活用すれば出来るわ。シングルクリック判定との共存をどう解決していくかを交えて解説していくわ。

Input Systemの環境下でマウスやタッチパネルのクリック・タップとマルチクリック・マルチタップを判別する方法の解説記事です。

判別方法としては、主に次の2種類が考えられます。

判別方法
シングルタップとマルチタップのイベントを同時に拾う
シングルタップ判定の遅延が無いが、マルチタップ時にシングルタップのロールバックが必要
シングルタップとマルチタップのイベントを排他的に拾う
ロールバック処理は不要だが、シングルタップ判定まで遅延がある
それぞれの方法には一長一短があり、状況に応じて使い分けるのが適切でしょう。

このようなシングルタップとマルチタップの判別方法は、以下ドキュメントでも言及されています。


クリックとダブルクリックを区別する方法 – Windows Forms .NET
.NET 用 Windows フォームのコントロールまたはフォームを使用してクリックとダブルクリックの違いを検出するさまざまな方法について説明します。
learn.microsoft.com
また、Input Systemにはシングルタップとマルチタップを判定する機能がInteractionとして提供されており、これらを活用すると比較的楽に実装できます。

参考：Interactions | Input System | 1.7.0

本記事では、Input SystemのInteractionを活用して、シングルタップとマルチタップを判別する方法を解説していきます。

注意
本記事では、シングルタップ（クリック）とマルチタップ（クリック）を検知する部分に絞って解説します。

マルチタップされた場合のシングルタップ処理のロールバックなど、アプリケーション側の対処方法までは取り扱いません。

 動作環境
Unity 2023.2.19f1
Input System 1.7.0
スポンサーリンク


目次 非表示
前提条件
シングル・マルチタップ両方を検知する
Input Actionの設定
サンプルスクリプト
実行結果
スクリプトの説明
シングル・マルチタップを排他的に検知する
Input Actionの設定
サンプルスクリプト
実行結果
スクリプトの説明
カスタムInteractionで実現する
カスタムInteractionの実装
Input Actionの設定
入力受取り側のスクリプトの実装例
実行結果
スクリプトの説明
複数のInteractionを共存させて実装する方法について
さいごに
関連記事
参考サイト
前提条件
事前にInput Systemパッケージがインストールされ、有効化されているものとします。ここまでの手順が分からない方は、以下記事を参考にセットアップを済ませてください。


【Unity】Input Systemの使い方入門
Unity公式の新しい入力システムパッケージInput Systemの入門者向け記事です。 本記事では、Input Systemパッケージのインストール方法から、最低限使えるようにするところまでを解説していきます。 また…
2021年11月29日
また、本記事のタップ判定を実現するためには、Input ActionおよびInteractionを用います。事前に両者の基本を押さえておくと理解がスムーズです。


【Unity】Input Actionの基本的な使い方
Input Systemでは、マウスやキーボード、ゲームパッドなどあらゆる入力デバイスを抽象的に扱えるようにするInput Actionが用意されています。 Input Actionを使うと、次のように入力デバイスに依存…
2021年12月1日

【Unity】Input SystemのInteractionの仕組みと使い方
Input Systemの基本機能の一つとして、Interactionがあります。 これは、次のような特定の入力パターンを検知するための仕組みです。 基本的な入力パターンは幾つかプリセットとして用意されていますが、これら…
2023年6月30日
シングル・マルチタップ両方を検知する
1つ目の方法はシングルタップとマルチタップ両方を検知する方法です。次のメリットとデメリットがあります。

メリット・デメリット
メリット
シングル・マルチタップ共に判定までの遅延が無い
デメリット
マルチタップを検知したとき、アプリケーション側でシングルタップ処理をロールバックする必要がある
マルチタップされた場合でも、シングルタップイベントが必ず発火してしまうため、シングルタップ操作が競合してしまうケースに注意する必要があります。

適した操作例
メニューのボタン操作
シングルタップでフォーカス
マルチタップで詳細情報のポップアップを開く
キャラクター操作
シングルタップで移動
マルチタップで攻撃・特殊なアクション
適さない操作例
メニューのボタン操作（不適切な例）
シングルタップで詳細情報のポップアップを開く
マルチタップでボタンを押す
キャラクター操作（不適切な例）
シングルタップで攻撃・特殊なアクション
マルチタップで移動
適さない例ですが、例えばシングルタップでポップアップを開き、マルチタップで別の意味のある操作を行おうとした場合、タップした瞬間にポップアップが必ず開いて消滅するなど不自然な挙動になってしまうでしょう。

このようにシングルタップとマルチタップが全く異なる意味を持ち、それぞれ排他的に実行したい場合は、後述する排他的に判別方法が適しています。

Input Actionの設定
シングルタップおよびマルチタップ用のActionを2つ用意し、アプリケーション側からそれぞれ入力を取得して判定するものとします。


Action構成
本記事では、Input Action Assetを新規作成して、ここにそれぞれのActionを定義するものとします。

Input Action Assetが作成されていなければ、プロジェクトウィンドウより右クリック > Create > Input Actionsを選択して、新しいアセットを作成します。

Mapを作成します。例では「Player」としました。

シングルタップ（クリック）となるActionを作成して設定します。例では「Tap」という名前のActionを作成し、「<Pointer>/press」というパスのBindingを定義するものとします。

このActionではタップ判定を行いたいため、Tapという名前のInteractionを追加します。

同様に、マルチタップ判定用のActionも追加します。例では「MultiTap」という名前のActionを作成し、「<Pointer>/press」というパスのBindingを定義し、Multi TapというInteractionを追加するものとします。

ここまでの設定したら、Save Assetボタンをクリックして内容を保存しておきます。

サンプルスクリプト
前述で定義したActionを用いて、シングルタップおよびマルチタップを判別するスクリプトを実装します。

以下、シングルタップとマルチタップが検知されたらログ出力する例です。マルチタップする場合でも、必ずシングルタップは反応します。

BothExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class BothExample : MonoBehaviour
{
    // タップ用Action
    [SerializeField] private InputActionProperty _tapAction;

    // マルチタップ用Action
    [SerializeField] private InputActionProperty _multiTapAction;

    // タップが行われたかどうか(イベントの重複検知防止用)
    private bool _isTapPerformed;

    private void OnEnable()
    {
        // Actionのコールバック登録
        _tapAction.action.performed += TapActionCallback;
        _multiTapAction.action.performed += MultiTapActionCallback;
        _multiTapAction.action.canceled += MultiTapActionCallback;

        // Actionの有効化
        _multiTapAction.action.Enable();
        _tapAction.action.Enable();
    }

    private void OnDisable()
    {
        // Actionのコールバック登録解除
        _tapAction.action.performed -= TapActionCallback;
        _multiTapAction.action.performed -= MultiTapActionCallback;
        _multiTapAction.action.canceled -= MultiTapActionCallback;

        // Actionの無効化
        _multiTapAction.action.Disable();
        _tapAction.action.Disable();
    }

    // タップ時のコールバック
    private void TapActionCallback(InputAction.CallbackContext context)
    {
        switch (context.phase)
        {
            case InputActionPhase.Performed:
                // タップがまだされておらず、マルチタップが行われていない場合は
                // タップが行われたと判定
                if (!_isTapPerformed && _multiTapAction.action.phase != InputActionPhase.Waiting)
                {
                    _isTapPerformed = true;
                    OnTap();
                }

                break;
        }
    }

    // マルチタップ時のコールバック
    private void MultiTapActionCallback(InputAction.CallbackContext context)
    {
        switch (context.phase)
        {
            case InputActionPhase.Performed:
                // マルチタップが行われた場合
                _isTapPerformed = false;
                OnTapCanceled();
                OnMultiTap();
                break;

            case InputActionPhase.Canceled:
                // マルチタップが中断された場合
                _isTapPerformed = false;
                break;
        }
    }

    // タップされた時の処理
    private void OnTap()
    {
        print("タップされた！");
    }

    // タップのロールバック処理
    private void OnTapCanceled()
    {
        print("タップがキャンセルされた！");
    }

    // マルチタップされた時の処理
    private void OnMultiTap()
    {
        print("マルチタップされた！");
    }
}
上記をBothExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりタップおよびマルチタップ用のActionを指定してください。

最終的に次のようにActionが指定されていれば良いです。


実行結果
シングルタップ、マルチタップ時にそれぞれのログが出力されます。

マルチタップを検知した場合、シングルタップのロールバック処理を行ってからマルチタップ処理を行うような挙動になっています。

スクリプトの説明
まず、フィールドとしてタップ、マルチタップ用のActionをそれぞれ定義しています。

// タップ用Action
[SerializeField] private InputActionProperty _tapAction;

// マルチタップ用Action
[SerializeField] private InputActionProperty _multiTapAction;

【Unity】Actionの指定を便利にするInputActionPropertyの使い方
Input SystemのActionをスクリプトから扱う際、インスペクターからActionを指定する方法は主に次の2通りが考えられます。 両者はそれぞれデータの持ち方が別ですが、InputActionProperty構…
2023年5月2日
スクリプトが有効化された時に、それぞれのActionに対してコールバックを登録し、Actionを有効化しています。

private void OnEnable()
{
    // Actionのコールバック登録
    _tapAction.action.performed += TapActionCallback;
    _multiTapAction.action.performed += MultiTapActionCallback;
    _multiTapAction.action.canceled += MultiTapActionCallback;

    // Actionの有効化
    _multiTapAction.action.Enable();
    _tapAction.action.Enable();
}
参考：Class InputAction| Input System | 1.7.0

スクリプト無効化時は、逆にコールバック登録を解除してActionも無効化しています。

private void OnDisable()
{
    // Actionのコールバック登録解除
    _tapAction.action.performed -= TapActionCallback;
    _multiTapAction.action.performed -= MultiTapActionCallback;
    _multiTapAction.action.canceled -= MultiTapActionCallback;

    // Actionの無効化
    _multiTapAction.action.Disable();
    _tapAction.action.Disable();
}
シングルタップのコールバック処理は以下の通りです。

// タップ時のコールバック
private void TapActionCallback(InputAction.CallbackContext context)
{
    switch (context.phase)
    {
        case InputActionPhase.Performed:
            // タップがまだされておらず、マルチタップが行われていない場合は
            // タップが行われたと判定
            if (!_isTapPerformed && _multiTapAction.action.phase != InputActionPhase.Waiting)
            {
                _isTapPerformed = true;
                OnTap();
            }

            break;
    }
}
タップ（ボタンを押してすぐ離した瞬間）を検知したときはフェーズ（context.phase）がPerformedとなるため、その場合にタップ処理を行っています。

ただし、マルチタップされる時は何度もタップを検知してしまうため、初回のタップかどうかを_isTapPerformedフラグでチェックしています。また、マルチタップされた際にもコールバックが呼ばれる可能性があるため、マルチタップActionのフェーズもチェックしています。


【Unity】Input SystemのInteractionの仕組みと使い方
Input Systemの基本機能の一つとして、Interactionがあります。 これは、次のような特定の入力パターンを検知するための仕組みです。 基本的な入力パターンは幾つかプリセットとして用意されていますが、これら…
2023年6月30日

【Unity】Input Actionの３種類のコールバック挙動
Input SystemのActionでは、スティックやボタン入力の変化などによって、次の３種類のコールバックが呼ばれるようになっています。 これらのコールバックは、例えば次のように使います。 コールバックが呼び出される…
2022年5月28日
マルチタップのコールバック処理は以下の通りです。

// マルチタップ時のコールバック
private void MultiTapActionCallback(InputAction.CallbackContext context)
{
    switch (context.phase)
    {
        case InputActionPhase.Performed:
            // マルチタップが行われた場合
            _isTapPerformed = false;
            OnTapCanceled();
            OnMultiTap();
            break;

        case InputActionPhase.Canceled:
            // マルチタップが中断された場合
            _isTapPerformed = false;
            break;
    }
}
マルチタップ（指定回数の指定時間以内の素早いタップ）を検知した際はフェーズがPerformedになるため、ここでシングルタップのロールバック処理を行ってからマルチタップ処理を行うようにしています。

マルチタップ操作が中断されるとフェーズがCanceledになるため、状態変数をリセットしています。

シングル・マルチタップを排他的に検知する
1つ目の例では、マルチタップ操作する際も必ず最初のタップでシングルタップを検知していました。シングルタップされた瞬間を検知できる反面、マルチタップされた時のロールバック処理が必須になります。

もしシングルタップの反応遅延を許容できるのであれば、次に紹介する排他的にイベントを通知する方法が適しています。

これは、シングルタップ後、マルチタップ操作の要件（タップ間隔）を満たさないと判断した瞬間に検知するため、若干の遅延があります。

メリット・デメリット
メリット
マルチタップ操作する際、シングルタップイベントが発火されない
デメリット
シングルタップ判定ではイベント発火までのラグがある
Input Actionの設定
1つ目の例のAction構成とします。設定済みならそのままで問題ありません。

サンプルスクリプト
シングルタップとマルチタップを排他的に検知する例です。

ExclusiveExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class ExclusiveExample : MonoBehaviour
{
    // タップ用Action
    [SerializeField] private InputActionProperty _tapAction;

    // マルチタップ用Action
    [SerializeField] private InputActionProperty _multiTapAction;

    // マルチタップ中のタップ回数
    private int _tapCount;

    private void OnEnable()
    {
        // Actionのコールバック登録
        _tapAction.action.performed += TapActionCallback;
        _multiTapAction.action.performed += MultiTapActionCallback;
        _multiTapAction.action.canceled += MultiTapActionCallback;

        // Actionの有効化
        _multiTapAction.action.Enable();
        _tapAction.action.Enable();
    }

    private void OnDisable()
    {
        // Actionのコールバック登録解除
        _tapAction.action.performed -= TapActionCallback;
        _multiTapAction.action.performed -= MultiTapActionCallback;
        _multiTapAction.action.canceled -= MultiTapActionCallback;

        // Actionの無効化
        _multiTapAction.action.Disable();
        _tapAction.action.Disable();
    }

    // タップ時のコールバック
    private void TapActionCallback(InputAction.CallbackContext context)
    {
        switch (context.phase)
        {
            case InputActionPhase.Performed:
                // タップが行われたらカウントアップ
                _tapCount++;
                break;
        }
    }

    // マルチタップ時のコールバック
    private void MultiTapActionCallback(InputAction.CallbackContext context)
    {
        switch (context.phase)
        {
            case InputActionPhase.Performed:
                // マルチタップが行われたらタップ回数をリセット
                OnMultiTap();
                _tapCount = 0;
                break;

            case InputActionPhase.Canceled:
                // タップ回数が1回で、マルチタップが中断されたらタップと判定
                // タップActionの押下状態もチェックし、押されている間はタップと判定しない
                if (_tapCount == 1 && !_tapAction.action.IsPressed())
                {
                    OnTap();
                }

                // タップ回数をリセット
                _tapCount = 0;
                break;
        }
    }

    // タップされた時の処理
    private void OnTap()
    {
        print("タップされた！");
    }

    // マルチタップされた時の処理
    private void OnMultiTap()
    {
        print("マルチタップされた！");
    }
}
上記をExclusiveExample.csという名前で保存し、適当なゲームオブジェクトにアタッチし、1つ目の例同様にインスペクターよりActionを設定してください。


実行結果
マルチタップ操作された時にシングルタップ処理が行われなくなりました。

シングルタップ操作では、ワンテンポ遅れて反応するようになっています。

スクリプトの説明
3回以上のマルチタップ対策のため、タップ数を独自で持つようにしています。

// マルチタップ中のタップ回数
private int _tapCount;
タップされるたびに、タップ数をカウントするようにしています。

// タップ時のコールバック
private void TapActionCallback(InputAction.CallbackContext context)
{
    switch (context.phase)
    {
        case InputActionPhase.Performed:
            // タップが行われたらカウントアップ
            _tapCount++;
            break;
    }
}
マルチタップのコールバック処理は次のように変更されています。

// マルチタップ時のコールバック
private void MultiTapActionCallback(InputAction.CallbackContext context)
{
    switch (context.phase)
    {
        case InputActionPhase.Performed:
            // マルチタップが行われたらタップ回数をリセット
            OnMultiTap();
            _tapCount = 0;
            break;

        case InputActionPhase.Canceled:
            // タップ回数が1回で、マルチタップが中断されたらタップと判定
            // タップActionの押下状態もチェックし、押されている間はタップと判定しない
            if (_tapCount == 1 && !_tapAction.action.IsPressed())
            {
                OnTap();
            }

            // タップ回数をリセット
            _tapCount = 0;
            break;
    }
}
マルチタップされた瞬間（フェーズがPerformed）はマルチタップ処理を行って状態リセット（タップ回数初期化）しています。

マルチタップが途中でキャンセルされた際（フェーズがCanceled）は、中途半端な回数のマルチタップを無視するため、1回だけのタップ（タップ回数が1）の時かつボタンが離された時だけタップとみなしています。

ボタン状態もチェックする理由は、押しっぱなしでタップ判定されてしまうのを防止するためです。

参考：Class InputAction| Input System | 1.7.0

カスタムInteractionで実現する
ここまで2通りの判別方法を紹介してきましたが、いずれもアプリケーション側のロジックが複雑になる弱点が存在します。

実装量が増えますが、カスタムInteractionを介して判定するようにすればこの問題をある程度解消できます。

メリットとデメリットは次の通りです。

メリット・デメリット
メリット
アプリケーション側のロジックが単純になる
1つのActionだけで実現できる
デメリット
カスタムInteractionを独自実装する必要がある
コールバック内部でInteractionオブジェクトにアクセスして判別する必要がある
カスタムInteractionの実装
シングル・マルチ両方のタップを検知するためのInteractionを実装します。

例では、シングルタップ、マルチタップ、シングルタップ中断それぞれのタイミングでperformedイベントを発火するようにしました。

以下、実装例です。

TapAndMultiTapInteraction.cs
using UnityEngine;
using UnityEngine.InputSystem;

// タップとマルチタップを同時に認識するInteraction
// MultiTapInteractionの内部実装を参考にしました
public class TapAndMultiTapInteraction : IInputInteraction
{
    // ボタン押し込みの最大許容時間[s]
    public float tapTime;

    // 次のタップまでの最大待機時間[s]
    public float tapDelay;

    // マルチタップの必要回数
    public int tapCount = 2;

    // ボタン押し込みの閾値(0でデフォルト値)
    public float pressPoint;

    // タップとマルチタップを排他的に認識するか
    public bool exclusive;

    public enum TapType
    {
        None,
        Tap,
        MultiTap,
        TapCanceled,
    }

    // タップの種類(コールバック側で参照することを想定)
    public TapType CurrentTapType { get; private set; }

    // マルチタップかどうか(コールバック側で参照することを想定)
    public bool IsMultiTap => _currentTapCount > 1;

    private float TapTimeOrDefault => tapTime > 0.0 ? tapTime : InputSystem.settings.defaultTapTime;
    internal float TapDelayOrDefault => tapDelay > 0.0 ? tapDelay : InputSystem.settings.multiTapDelayTime;
    private float PressPointOrDefault => pressPoint > 0 ? pressPoint : InputSystem.settings.defaultButtonPressPoint;
    private float ReleasePointOrDefault => PressPointOrDefault * InputSystem.settings.buttonReleaseThreshold;

    // タップの内部フェーズ
    private enum TapPhase
    {
        None,
        WaitingForNextRelease,
        WaitingForNextPress,
    }

    // 内部状態
    private TapPhase _currentTapPhase;
    private int _currentTapCount;
    private double _currentTapStartTime;
    private double _lastTapReleaseTime;

#if UNITY_EDITOR
    [UnityEditor.InitializeOnLoadMethod]
#else
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
#endif
    public static void Initialize()
    {
        // 初回にInteractionを登録する必要がある
        InputSystem.RegisterInteraction<TapAndMultiTapInteraction>();
    }

    public void Process(ref InputInteractionContext context)
    {
        if (context.timerHasExpired)
        {
            // タイムアウト時のInteractionの終了処理
            if (exclusive && _currentTapCount == 1)
            {
                // シングルタップを排他的に認識する場合
                CurrentTapType = TapType.Tap;
                context.Performed();
            }
            else
            {
                context.Canceled();
            }

            return;
        }

        switch (_currentTapPhase)
        {
            case TapPhase.None:
                // 初期状態

                // ボタンがおされたらInteractionを開始する
                if (context.ControlIsActuated(PressPointOrDefault))
                {
                    // タップ開始
                    _currentTapPhase = TapPhase.WaitingForNextRelease;
                    _currentTapStartTime = context.time;

                    _currentTapCount++;

                    // Startedフェーズに遷移
                    context.Started();
                    context.SetTimeout(TapTimeOrDefault);
                }

                break;

            case TapPhase.WaitingForNextRelease:
                // ボタンが離されるまで待機する状態

                // ボタンが離されたかチェック
                if (!context.ControlIsActuated(ReleasePointOrDefault))
                {
                    // 指定時間以内に離されたらタップとして認識する
                    if (context.time - _currentTapStartTime <= TapTimeOrDefault)
                    {
                        if (!exclusive && _currentTapCount > 1 && CurrentTapType == TapType.Tap)
                        {
                            // シングルタップのロールバック処理
                            CurrentTapType = TapType.TapCanceled;
                            context.PerformedAndStayPerformed();
                        }
                        
                        if (_currentTapCount >= tapCount)
                        {
                            // マルチタップの場合
                            CurrentTapType = TapType.MultiTap;
                            context.Performed();
                        }
                        else if (!exclusive && _currentTapCount == 1)
                        {
                            // マルチタップ途中のシングルタップの場合
                            CurrentTapType = TapType.Tap;
                            context.PerformedAndStayPerformed();
                        }

                        if (context.phase != InputActionPhase.Canceled)
                        {
                            // マルチタップが継続される場合は、ボタンが離されるまで待機する状態に遷移
                            _currentTapPhase = TapPhase.WaitingForNextPress;
                            _lastTapReleaseTime = context.time;
                            context.SetTimeout(TapDelayOrDefault);
                        }
                    }
                    else
                    {
                        // マルチタップの条件を満たさないのでキャンセル
                        context.Canceled();
                    }
                }

                break;

            case TapPhase.WaitingForNextPress:
                // 次のボタン押下を待機する状態

                // ボタンが押されたかチェック
                if (context.ControlIsActuated(PressPointOrDefault))
                {
                    // ここでタップ回数をカウント
                    _currentTapCount++;

                    // 指定時間以内に押されたらタップとして認識する
                    if (context.time - _lastTapReleaseTime <= TapDelayOrDefault)
                    {
                        // ボタンが離されるまで待機する状態に遷移
                        _currentTapPhase = TapPhase.WaitingForNextRelease;
                        _currentTapStartTime = context.time;
                        context.SetTimeout(TapDelayOrDefault);
                    }
                    else
                    {
                        // タップの条件を満たさないのでキャンセル
                        context.Canceled();
                    }
                }

                break;
        }
    }

    public void Reset()
    {
        // 内部状態をリセット
        CurrentTapType = TapType.None;
        _currentTapPhase = TapPhase.None;
        _currentTapCount = 0;
        _currentTapStartTime = 0;
        _lastTapReleaseTime = 0;
    }
}
上記をTapAndMultiTapInteraction.csという名前でUnityプロジェクトに保存すると、Interactionが使用可能になります。

実装はInput SystemのInteractionのプリセットであるMultiTapInteractionクラスの内部実装を参考にしています。

参考：Class MultiTapInteraction| Input System | 1.7.0

Input Actionの設定
例で示したカスタムInteractionを登録したActionを一つ定義します。

例では、「TapAndMultiTap」という名前のActionを定義し、Bindingには「＜Pointer＞/press」なるパスを指定し、Interactionに実装例のTap And Multi Tapという名前のInteractionを登録するものとします。

Action Properties > Interactionsから各種パラメータを指定できます。

Tap Time – ボタンを押し込む最大許容時間[s]
Tap Delay – タップの最大時間間隔[s]
Tap Count – マルチタップに必要な回数
Press Point – ボタン押下判定の閾値（0でInput Systemのデフォルト設定値）
Exclusive – シングル・マルチタップを排他的に反応させるかどうか

入力受取り側のスクリプトの実装例
カスタムInteractionを適用したActionからシングル・マルチタップを判定するためのスクリプトを実装します。

以下、実装例です。

CustomInteractionExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class CustomInteractionExample : MonoBehaviour
{
    // タップとマルチタップ両方を検知するためのAction
    [SerializeField] private InputActionProperty _tapAndMultiTapAction;

    private void OnEnable()
    {
        // Actionのコールバック登録
        _tapAndMultiTapAction.action.performed += OnTapAndMultiTap;

        // Actionの有効化
        _tapAndMultiTapAction.action.Enable();
    }

    private void OnDisable()
    {
        // Actionのコールバック登録解除
        _tapAndMultiTapAction.action.performed -= OnTapAndMultiTap;

        // Actionの無効化
        _tapAndMultiTapAction.action.Disable();
    }

    private void OnTapAndMultiTap(InputAction.CallbackContext context)
    {
        // タップとマルチタップの両方を検知するためのInteractionかどうかを判定
        if (context.interaction is not TapAndMultiTapInteraction tapAndMultiTapInteraction)
            return;

        // タップ種別をログ出力
        switch (tapAndMultiTapInteraction.CurrentTapType)
        {
            case TapAndMultiTapInteraction.TapType.Tap:
                print("タップされた！");
                break;

            case TapAndMultiTapInteraction.TapType.MultiTap:
                print("マルチタップされた！");
                break;

            case TapAndMultiTapInteraction.TapType.TapCanceled:
                print("タップがキャンセルされた！");
                break;
        }
    }
}
上記をCustomInteractionExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりActionを指定してください。


実行結果
前述の例同様にシングル・マルチタップの操作でログ出力されます。

スクリプトの説明
Action Propertiesより指定可能な設定項目は、以下publicフィールドとして定義しています。

// ボタン押し込みの最大許容時間[s]
public float tapTime;

// 次のタップまでの最大待機時間[s]
public float tapDelay;

// マルチタップの必要回数
public int tapCount = 2;

// ボタン押し込みの閾値(0でデフォルト値)
public float pressPoint;

// タップとマルチタップを排他的に認識するか
public bool exclusive;
受取り側に通知する際、シングルタップ、マルチタップ、シングルタップのロールバックのどれかを判定可能にするため、enum型プロパティとして種別を提供するようにしています。

public enum TapType
{
    None,
    Tap,
    MultiTap,
    TapCanceled,
}

// タップの種類(コールバック側で参照することを想定)
public TapType CurrentTapType { get; private set; }
マルチタップ処理に必要な状態変数は、MultiTapInteractionの内部実装を参考に定義しています。

// タップの内部フェーズ
private enum TapPhase
{
    None,
    WaitingForNextRelease,
    WaitingForNextPress,
}

// 内部状態
private TapPhase _currentTapPhase;
private int _currentTapCount;
private double _currentTapStartTime;
private double _lastTapReleaseTime;
カスタムInteractionはそのままではInput System側から認識されないたえめ、初期化時に登録しています。

#if UNITY_EDITOR
    [UnityEditor.InitializeOnLoadMethod]
#else
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
#endif
    public static void Initialize()
    {
        // 初回にInteractionを登録する必要がある
        InputSystem.RegisterInteraction<TapAndMultiTapInteraction>();
    }
参考：Interactions | Input System | 1.7.0

デバイスから入力があった際のInteraction処理はProcessメソッドとして実装しています。

public void Process(ref InputInteractionContext context)
参考：Interface IInputInteraction| Input System | 1.7.0

Processメソッドの最初では、タップやマルチタップが中断したときの判定処理を行っています。

if (context.timerHasExpired)
{
    // タイムアウト時のInteractionの終了処理
    if (exclusive && _currentTapCount == 1)
    {
        // シングルタップを排他的に認識する場合
        CurrentTapType = TapType.Tap;
        context.Performed();
    }
    else
    {
        context.Canceled();
    }

    return;
}
マルチタップが中断された時にシングルタップを排他的に通知する設定の場合は、シングルタップ通知してから一連のInteractionを終了します。

それ以外、例えばマルチタップの途中やタップを満たさない操作などで中断する場合は、そのままCanceledフェーズに遷移してInteractionを終了します。

参考：Struct InputInteractionContext| Input System | 1.7.0

処理のタイムアウト以外の場合は、入力に何らかの変化があったとみなし、タップ状態に基づいて処理を分岐します。

初期状態からボタン入力があった場合、タップ処理に移行します。タップ回数は必ず押された瞬間にカウントするようにしました。

switch (_currentTapPhase)
{
    case TapPhase.None:
        // 初期状態

        // ボタンがおされたらInteractionを開始する
        if (context.ControlIsActuated(PressPointOrDefault))
        {
            // タップ開始
            _currentTapPhase = TapPhase.WaitingForNextRelease;
            _currentTapStartTime = context.time;

            _currentTapCount++;

            // Startedフェーズに遷移
            context.Started();
            context.SetTimeout(TapTimeOrDefault);
        }

        break;
ボタンが押された後、離されるまで待機する処理は以下部分です。

case TapPhase.WaitingForNextRelease:
    // ボタンが離されるまで待機する状態

    // ボタンが離されたかチェック
    if (!context.ControlIsActuated(ReleasePointOrDefault))
    {
        // 指定時間以内に離されたらタップとして認識する
        if (context.time - _currentTapStartTime <= TapTimeOrDefault)
        {
            if (!exclusive && _currentTapCount > 1 && CurrentTapType == TapType.Tap)
            {
                // シングルタップのロールバック処理
                CurrentTapType = TapType.TapCanceled;
                context.PerformedAndStayPerformed();
            }
            
            if (_currentTapCount >= tapCount)
            {
                // マルチタップの場合
                CurrentTapType = TapType.MultiTap;
                context.Performed();
            }
            else if (!exclusive && _currentTapCount == 1)
            {
                // マルチタップ途中のシングルタップの場合
                CurrentTapType = TapType.Tap;
                context.PerformedAndStayPerformed();
            }

            if (context.phase != InputActionPhase.Canceled)
            {
                // マルチタップが継続される場合は、ボタンが離されるまで待機する状態に遷移
                _currentTapPhase = TapPhase.WaitingForNextPress;
                _lastTapReleaseTime = context.time;
                context.SetTimeout(TapDelayOrDefault);
            }
        }
        else
        {
            // マルチタップの条件を満たさないのでキャンセル
            context.Canceled();
        }
    }

    break;
許容時間内にボタンが離されるとタップ処理をif文の内部で実行します。その際、排他フラグとタップ回数に応じてタップ種別（CurrentTapType）を指定した後にPerformedフェーズに遷移させ、performedイベントを通知しています。

ボタンを離した後、再度押下するまで待機する処理は以下部分です。

case TapPhase.WaitingForNextPress:
    // 次のボタン押下を待機する状態

    // ボタンが押されたかチェック
    if (context.ControlIsActuated(PressPointOrDefault))
    {
        // ここでタップ回数をカウント
        _currentTapCount++;

        // 指定時間以内に押されたらタップとして認識する
        if (context.time - _lastTapReleaseTime <= TapDelayOrDefault)
        {
            // ボタンが離されるまで待機する状態に遷移
            _currentTapPhase = TapPhase.WaitingForNextRelease;
            _currentTapStartTime = context.time;
            context.SetTimeout(TapDelayOrDefault);
        }
        else
        {
            // タップの条件を満たさないのでキャンセル
            context.Canceled();
        }
    }

    break;
ここでタップ回数をカウントして、内部状態をボタンが離されるまで待機する状態に更新しています。

受取り側のスクリプトでは、コールバック処理内部でTapAndMultiTapInteractionインスタンスを取得して、タップ種別のプロパティCurrentTapTypeから処理を振り分けています。

private void OnTapAndMultiTap(InputAction.CallbackContext context)
{
    // タップとマルチタップの両方を検知するためのInteractionかどうかを判定
    if (context.interaction is not TapAndMultiTapInteraction tapAndMultiTapInteraction)
        return;

    // タップ種別をログ出力
    switch (tapAndMultiTapInteraction.CurrentTapType)
    {
        case TapAndMultiTapInteraction.TapType.Tap:
            print("タップされた！");
            break;

        case TapAndMultiTapInteraction.TapType.MultiTap:
            print("マルチタップされた！");
            break;

        case TapAndMultiTapInteraction.TapType.TapCanceled:
            print("タップがキャンセルされた！");
            break;
    }
}
複数のInteractionを共存させて実装する方法について
本記事では軽く触れる程度に留めますが、プリセットのInteractionであるTapとMulti Tapを1つのActionに定義して、スクリプトからInteractionを判別する方法もあります。


private void OnPointer(InputAction.CallbackContext context)
{
    switch (context.interaction)
    {
        case TapInteraction:
            Debug.Log("タップされた！");
            break;
        
        case MultiTapInteraction:
            Debug.Log("マルチタップされた！");
            break;
    }
    
    context.action.Reset();
}
実装は手軽ですが、タップ後に押しっぱなしにするとシングルタップとして判定される挙動であったため、本記事では軽く触れる程度にとどめておきます。

これを許容できる場合は、全体的な実装量が大幅に減り、アプリケーション側のロジックもシンプルになって良いでしょう。

参考：(New Input System) Single Tap vs Double Tap – Unity Forum

参考：New Input System – Mouse Double Click – Unity Forum

さいごに
シングルタップとマルチタップをそれぞれ判別するためには、アプリケーション側の挙動を適切に設計する必要があります。

レスポンスを優先してシングルタップとマルチタップを両方通知する方法、レスポンスを犠牲にする代わりに排他的に通知する方法があります。

これらをInput Systemを用いて実装する場合として、2つのActionを用いたり、カスタムInteractionを用いて1つのActionにまとめて実装したりする方法を紹介させていただきました。

