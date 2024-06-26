# Input Systemでキーコンフィグを実装する

https://nekojara.city/unity-input-system-rebinding




キーコンフィグの実装の流れは次のようになります。

実装の流れ
設定用のUIの配置
リバインドを実施するスクリプトの実装
UIにスクリプトを適用




スクリプトで実装するリバインド（Interactive Rebinding）の処理の流れは次のようになります。

スクリプト実装の流れ
リバインド対象のActionを無効化する
どのBindingをリバインドするかを決定する
Actionに対してリバインドの動作設定を行う
リバインドを開始する
リバインドが完了または中断した時、Actionを有効化する
また、リバインドにより上書きされた設定は、ストレージなどに対してセーブ・ロードしたりできます。

本記事では、このようなキーコンフィグの実装方法について順を追って解説していきます。





例では次のようなInput Action Assetが予め作成されているものとします。




<img src="images/11/11_2/unity-input-system-rebinding-1.png.avif" width="90%" alt="" title="">

<br>

KeyboardとGamepadというスキームが定義され、JumpとMoveというActionの各Bindingに設定しています。

本記事で解説するキーコンフィグの実装方法は、Input Systemパッケージの公式サンプルの一つである「Rebinding UI」を参考にしています。


UIの準備
本記事では、次のようにジャンプと移動操作に対してキー割当てを変更するものとして解説を進めます。


<img src="images/11/11_2/unity-input-system-rebinding-2.png.avif" width="90%" alt="" title="">

<br>

このパネルは普段は非表示ですが、リバインド中のみ表示されて他のUIを押せなくする役割を持ちます。

リバインド（Interactive Rebinding）を行うスクリプトの実装
リバインド関連の処理は、Input Actionに対してキー割当て設定の「上書き」を行うことで実現します。

例えば、ジャンプ操作に元々割り当てられていた「スペースキー」を「Aキー」に上書きしたりできます。上書きした情報は、Actionの本来の情報とは別で管理されます。

<img src="images/11/11_2/unity-input-system-rebinding-3.png.avif" width="90%" alt="" title="">

<br>

このように「上書き」でキー割当てを変更することで、例えば後からデフォルト設定に戻すと言った操作（リセット）が簡単になります。これは、「上書き」情報を削除するだけで済み、初期設定を別で保持する必要がなくなるためです。


<img src="images/11/11_2/unity-input-system-rebinding-4.png.avif" width="90%" alt="" title="">

<br>


ここまで説明した「上書き」関連の機能は、InputActionRebindingExtensions拡張クラスとして提供されています。

参考：Input Bindings | Input System | 1.5.1

何かキー入力があったらそのキーで割り当てるといったインタラクティブなリバインドは、PerformInteractiveRebinding拡張メソッドを通じて実装できます。

参考：Class InputActionRebindingExtensions| Input System | 1.5.1

次に、このようなインタラクティブなリバインドの実装の流れを解説していきます。

対象Actionを無効化する
インタラクティブなリバインドを実施する直前に、対象となるActionを無効化しておく必要があります。

InputAction action;

・・・（中略）・・・

// リバインド前にActionを無効化する必要がある
action.Disable();
注意
無効化せずにリバインドを実施してしまった場合、次のようなエラー（例外）が出てしまいます。 [2]
InvalidOperationException: Cannot rebind action 'Player/Jump[/Keyboard/a,/XInputControllerWindows/buttonSouth]' while it is enabled
参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

Bindingの決定
一つのActionには複数のBindingが存在している可能性があります。

例えば、ジャンプ操作のActionにキーボードのスペースキーとゲームパッドのSouthキーが割り当てられている場合などが該当します。

そのため、複数あるBindingのうち、どのインデックスのBindingにするかを決める必要が出てくる可能性があります。




<img src="images/11/11_2/unity-input-system-rebinding-5.png.avif" width="90%" alt="" title="">

<br>



Bindingの決定方法は一通りではなく、例えば次のように条件を設けたり、IDなどで検索したりして決定します。

Binding決定の例
スキーム（Keyboard、Gamepadなど）で決定する
BindingのユニークID（GUID）で決定する
その他のBinding内の内容に基づいて決定する
直接インデックス指定で決定する
開発でのメンテナンス性を考えると、2つ目までの方法で決定するのが無難でしょう。 [3] ここではスキームに基づいて決定することを例にとって解説します。

以下、特定スキームのBindingを決定する処理の例です。

InputAction action;
string scheme = "Keyboard";

・・・（中略）・・・

// リバインド対象のBindingIndexを取得
int bindingIndex = action.GetBindingIndex(
    InputBinding.MaskByGroup(scheme)
);
スキームから最終的なBindingのインデックスを決定しています。

指定された条件のBindingインデックスを取得するには、GetBindingIndex拡張メソッドを使います。

参考：Class InputActionRebindingExtensions| Input System | 1.5.1

引数には、マスクする条件を示す情報をInputBinding構造体で指定します。

スキームでマスクする場合は、InputBinding.MaskByGroupメソッドを使うのが手軽です。

参考：Struct InputBinding| Input System | 1.5.1

注意
Bindingのインデックスは省略することも可能ですが、その場合すべてのBindingに対してリバインドが行われてしまうのでご注意ください。

リバインドの設定
PerformInteractiveRebinding拡張メソッドにより、リバインド用の非同期オペレーションを作成します。

// リバインド対象のAction
InputAction action;
// 決定されたBindingのインデックス
int bindingIndex;
// リバインドの非同期オペレーション
InputActionRebindingExtensions.RebindingOperation rebindOperation;

・・・（中略）・・・

// オペレーションの作成
rebindOperation = action.PerformInteractiveRebinding(bindingIndex);
参考：Class InputActionRebindingExtensions| Input System | 1.5.1

オペレーションを作成するときは、次のようにメソッドチェインで設定できます。

InputAction action;
int bindingIndex;
InputActionRebindingExtensions.RebindingOperation rebindOperation;

・・・（中略）・・・

// オペレーション作成
// メソッドチェインでコールバックを登録
rebindOperation = action
    .PerformInteractiveRebinding(bindingIndex)
    .OnComplete(_ =>
    {
        // リバインドが完了した時の処理
    })
    .OnCancel(_ =>
    {
        // リバインドがキャンセルされた時の処理
    });
リバインドが完了したときにUIの表示を更新したい場合などは、コールバックを使います。

OnCompleteは操作入力の割り当てが完了したときに呼ばれるコールバックです。

参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

OnCancelは操作入力の割り当てが中断されたときに呼ばれるコールバックです。

参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

上記で作成した非同期オペレーションは、最後に必ずDisposeメソッドで破棄する必要があります。 [4]
// オペレーションの破棄
rebindOperation?.Dispose();
rebindOperation = null;
注意
Disposeメソッドによる破棄を忘れると、メモリリークが発生してしまいます。これは、内部的にアンマネージドメモリのアロケーションが行われているためです。 [5]
参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

リバインドの開始
リバインド用の非同期オペレーションを作成し、一通り設定できたら、オペレーションに対してStartメソッドを実行してリバインドを開始します。

// インタラクティブなリバインドを開始する
rebindOperation.Start();
リバインドが完了または中断されると、前述のコールバックが呼び出されます。

参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

開始までの処理は、次のようにメソッドチェインでまとめて書けます。

// オペレーション作成から開始まで
// メソッドチェインで記述できる
rebindOperation = action
    .PerformInteractiveRebinding(bindingIndex)
    .OnComplete(_ =>
    {
        // リバインドが完了した時の処理
    })
    .OnCancel(_ =>
    {
        // リバインドがキャンセルされた時の処理
    })
    .Start();
サンプルスクリプト
リバインドの要求があったらインタラクティブなリバインドを実施するスクリプトの例です。

RebindUI.cs
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class RebindUI : MonoBehaviour
{
    // リバインド対象のAction
    [SerializeField] private InputActionReference _actionRef;

    // リバインド対象のScheme
    [SerializeField] private string _scheme = "Keyboard";

    // 現在のBindingのパスを表示するテキスト
    [SerializeField] private TMP_Text _pathText;

    // リバインド中のマスク用オブジェクト
    [SerializeField] private GameObject _mask;

    private InputAction _action;
    private InputActionRebindingExtensions.RebindingOperation _rebindOperation;

    // 初期化
    private void Awake()
    {
        if (_actionRef == null) return;

        // InputActionインスタンスを保持しておく
        _action = _actionRef.action;

        // キーバインドの表示を反映する
        RefreshDisplay();
    }

    // 後処理
    private void OnDestroy()
    {
        // オペレーションは必ず破棄する必要がある
        CleanUpOperation();
    }

    // リバインドを開始する
    public void StartRebinding()
    {
        // もしActionが設定されていなければ、何もしない
        if (_action == null) return;

        // もしリバインド中なら、強制的にキャンセル
        // Cancelメソッドを実行すると、OnCancelイベントが発火する
        _rebindOperation?.Cancel();

        // リバインド前にActionを無効化する必要がある
        _action.Disable();

        // リバインド対象のBindingIndexを取得
        var bindingIndex = _action.GetBindingIndex(
            InputBinding.MaskByGroup(_scheme)
        );

        // ブロッキング用マスクを表示
        if (_mask != null)
            _mask.SetActive(true);

        // リバインドが終了した時の処理を行うローカル関数
        void OnFinished()
        {
            // オペレーションの後処理
            CleanUpOperation();

            // 一時的に無効化したActionを有効化する
            _action.Enable();

            // ブロッキング用マスクを非表示
            if (_mask != null)
                _mask.SetActive(false);
        }

        // リバインドのオペレーションを作成し、
        // 各種コールバックの設定を実施し、
        // 開始する
        _rebindOperation = _action
            .PerformInteractiveRebinding(bindingIndex)
            .OnComplete(_ =>
            {
                // リバインドが完了した時の処理
                RefreshDisplay();
                OnFinished();
            })
            .OnCancel(_ =>
            {
                // リバインドがキャンセルされた時の処理
                OnFinished();
            })
            .Start(); // ここでリバインドを開始する
    }

    // 現在のキーバインド表示を更新
    public void RefreshDisplay()
    {
        if (_action == null || _pathText == null) return;

        _pathText.text = _action.GetBindingDisplayString();
    }

    // リバインドオペレーションを破棄する
    private void CleanUpOperation()
    {
        // オペレーションを作成したら、Disposeしないとメモリリークする
        _rebindOperation?.Dispose();
        _rebindOperation = null;
    }
}
上記をRebindUI.csという名前で保存し、ゲームオブジェクト（ボタンなど）に割り当て、インスペクターから各種設定を行います。







そして、ボタンが押されたときなどに上記スクリプトのStartRebindingメソッドを呼び出すようにします。

例では、リバインドボタンのOnClickイベントにStartRebindingメソッドを登録することで呼び出すこととします。














入力確認用スクリプト
以下、正しくリバインドされているかどうかを確認するスクリプトです。

ReadJumpExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class ReadJumpExample : MonoBehaviour
{
    [SerializeField] private InputActionReference _actionRef;

    private void Awake()
    {
        if (_actionRef == null) return;

        _actionRef.action.performed += OnJump;

        _actionRef.action.Enable();
    }

    private void OnDestroy()
    {
        if (_actionRef == null) return;

        _actionRef.action.performed -= OnJump;
        _actionRef.action.Dispose();
    }

    private void OnJump(InputAction.CallbackContext obj)
    {
        print("Jump");
    }
}
上記は確認用スクリプトのため必須ではありません。必要に応じてお使いください。

ReadJumpExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、Action Refにリバインドされる対象のActionを指定すると機能するようになります。

キー入力があるたびに（performedコールバックが発火するたびに）Jumpという文字列をログ出力します。

実行結果
リバインドボタンを押すと入力待ちの画面に切り替わり、キーボードから何かキーを入力すると入力したキーが割り当てられるようになりました。











マウスやゲームパッドの入力は受け付けず、キーボードのみ操作を受け付けるようになっています。

スクリプトの説明
インタラクティブなリバインドを実施するために、Input Actionとオペレーションのフィールドを定義しています。

private InputAction _action;
private InputActionRebindingExtensions.RebindingOperation _rebindOperation;
オペレーションをフィールドとして定義する理由は、ゲームオブジェクトが破棄された際に確実に後処理できるようにするためです。

// 後処理
private void OnDestroy()
{
    // オペレーションは必ず破棄する必要がある
    CleanUpOperation();
}

・・・（中略）・・・

// リバインドオペレーションを破棄する
private void CleanUpOperation()
{
    // オペレーションを作成したら、Disposeしないとメモリリークする
    _rebindOperation?.Dispose();
    _rebindOperation = null;
}
ボタンが押されたらインタラクティブなリバインドを開始する動作は、以下のpublicメソッドを公開して外部から呼び出してもらうことで実現しています。

// リバインドを開始する
public void StartRebinding()
{
    // もしActionが設定されていなければ、何もしない
    if (_action == null) return;
インタラクティブなリバインドを開始する前に、安全のため前回の非同期オペレーションが実行されていないかチェックしています。

// もしリバインド中なら、強制的にキャンセル
// Cancelメソッドを実行すると、OnCancelイベントが発火する
_rebindOperation?.Cancel();
Cancelメソッドを実行することで、リバインドを中断することができます。これにより、OnCancelコールバックが呼び出され、オペレーションの破棄など必要な後処理を行うことができるようになります。

参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

これでようやくインタラクティブなリバインドの開始処理に移ることができます。

Actionの無効化とBindingのインデックス決定までの処理は以下部分です。

// リバインド前にActionを無効化する必要がある
_action.Disable();

// リバインド対象のBindingIndexを取得
var bindingIndex = _action.GetBindingIndex(
    InputBinding.MaskByGroup(_scheme)
);
そして、入力待ちを示すための全画面表示を行います。

// ブロッキング用マスクを表示
if (_mask != null)
    _mask.SetActive(true);
インタラクティブなリバインドのオペレーション作成・コールバック登録・開始までの処理は以下部分です。

// リバインドのオペレーションを作成し、
// 各種コールバックの設定を実施し、
// 開始する
_rebindOperation = _action
    .PerformInteractiveRebinding(bindingIndex)
    .OnComplete(_ =>
    {
        // リバインドが完了した時の処理
        RefreshDisplay();
        OnFinished();
    })
    .OnCancel(_ =>
    {
        // リバインドがキャンセルされた時の処理
        OnFinished();
    })
    .Start(); // ここでリバインドを開始する
リバインドが完了またはキャンセルされたときには、以下ローカル関数が呼ばれるようにして非同期オペレーションの破棄をしたり、Actionを再び有効化したり、入力待ちパネルを消したりしています。

// リバインドが終了した時の処理を行うローカル関数
void OnFinished()
{
    // オペレーションの後処理
    CleanUpOperation();

    // 一時的に無効化したActionを有効化する
    _action.Enable();

    // ブロッキング用マスクを非表示
    if (_mask != null)
        _mask.SetActive(false);
}
リバインドが完了したときは、どのキーが割り当てられているかを確認できるようにUIに反映するようにしています。これは、以下メソッド内で行っています。

// 現在のキーバインド表示を更新
public void RefreshDisplay()
{
    if (_action == null || _pathText == null) return;

    _pathText.text = _action.GetBindingDisplayString();
}
GetBindingDisplayStringメソッドはInputActionRebindingExtensionsクラスの拡張メソッドで、表示用のキーバインドの文字列を返します。

例ではすべてのBindingを表示対象としていますが、一部のスキームのみ表示するといったことも可能です。詳細はリファレンスをご確認ください。

参考：Class InputActionRebindingExtensions| Input System | 1.5.1

設定をリセットする
リバインドによって上書きされたキー割当ては、リセットして無かったことにすることも可能です。

上書き情報はActionのBinding情報とは別で管理されているため、内部的には上書き情報を削除するだけで済みます。



<img src="images/11/11_2/unity-input-system-rebinding-4.png.avif" width="90%" alt="" title="">

<br>






リセットには、RemoveBindingOverride拡張メソッドまたはRemoveAllBindingOverrides拡張メソッドを使います。

InputAction action;

・・・（中略）・・・

// Bindingの上書きを全て解除する
action.RemoveAllBindingOverrides();
参考：Class InputActionRebindingExtensions| Input System | 1.5.1

サンプルスクリプト
前述のスクリプトにリセットメソッドを追加した例です。

RebindUI.cs
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class RebindUI : MonoBehaviour
{
    // リバインド対象のAction
    [SerializeField] private InputActionReference _actionRef;

    // リバインド対象のScheme
    [SerializeField] private string _scheme = "Keyboard";

    // 現在のBindingのパスを表示するテキスト
    [SerializeField] private TMP_Text _pathText;

    // リバインド中のマスク用オブジェクト
    [SerializeField] private GameObject _mask;

    private InputAction _action;
    private InputActionRebindingExtensions.RebindingOperation _rebindOperation;

    // 初期化
    private void Awake()
    {
        if (_actionRef == null) return;

        // InputActionインスタンスを保持しておく
        _action = _actionRef.action;

        // キーバインドの表示を反映する
        RefreshDisplay();
    }

    // 後処理
    private void OnDestroy()
    {
        // オペレーションは必ず破棄する必要がある
        CleanUpOperation();
    }

    // リバインドを開始する
    public void StartRebinding()
    {
        // もしActionが設定されていなければ、何もしない
        if (_action == null) return;

        // もしリバインド中なら、強制的にキャンセル
        // Cancelメソッドを実行すると、OnCancelイベントが発火する
        _rebindOperation?.Cancel();

        // リバインド前にActionを無効化する必要がある
        _action.Disable();

        // リバインド対象のBindingIndexを取得
        var bindingIndex = _action.GetBindingIndex(
            InputBinding.MaskByGroup(_scheme)
        );

        // ブロッキング用マスクを表示
        if (_mask != null)
            _mask.SetActive(true);

        // リバインドが終了した時の処理を行うローカル関数
        void OnFinished()
        {
            // オペレーションの後処理
            CleanUpOperation();

            // 一時的に無効化したActionを有効化する
            _action.Enable();

            // ブロッキング用マスクを非表示
            if (_mask != null)
                _mask.SetActive(false);
        }

        // リバインドのオペレーションを作成し、
        // 各種コールバックの設定を実施し、
        // 開始する
        _rebindOperation = _action
            .PerformInteractiveRebinding(bindingIndex)
            .OnComplete(_ =>
            {
                // リバインドが完了した時の処理
                RefreshDisplay();
                OnFinished();
            })
            .OnCancel(_ =>
            {
                // リバインドがキャンセルされた時の処理
                OnFinished();
            })
            .Start(); // ここでリバインドを開始する
    }
    
    // 上書きされた情報をリセットする
    public void ResetOverrides()
    {
        // Bindingの上書きを全て解除する
        _action?.RemoveAllBindingOverrides();
        RefreshDisplay();
    }

    // 現在のキーバインド表示を更新
    public void RefreshDisplay()
    {
        if (_action == null || _pathText == null) return;

        _pathText.text = _action.GetBindingDisplayString();
    }

    // リバインドオペレーションを破棄する
    private void CleanUpOperation()
    {
        // オペレーションを作成したら、Disposeしないとメモリリークする
        _rebindOperation?.Dispose();
        _rebindOperation = null;
    }
}
RebindUI.csを上記の内容に置き換えれば機能します。インスペクターからの設定方法は変わりありません。

リセットボタンなどが押された際にResetOverridesメソッドを呼び出すと上書き情報がすべて削除されてリセットされます。








実行結果
リセットボタンを押すと、キー割り当てが初期設定（Space）に戻っていることが確認できました。







スクリプトの説明
リセットする処理は以下部分です。

// 上書きされた情報をリセットする
public void ResetOverrides()
{
    // Bindingの上書きを全て解除する
    _action?.RemoveAllBindingOverrides();
    RefreshDisplay();
}
リセットした後は、画面を更新するようにしています。

Composite Bindingに対してリバインドする
WASDキーや十字キー移動などで使われるComposite Bindingに対してもリバインドできます。

Composite Bindingでは複数のBindingを合成した一つのBindingのように振る舞いますが、Bindingとしては次のようにComposite Bindingおよびその内包されるBindingが一緒に配置されています。




<img src="images/11/11_2/unity-input-system-rebinding-6.png.avif" width="90%" alt="" title="">

<br>

リバインドするときはComposite Bindingそのものではなく、内包されるBindingに対して行う必要があります。

例えば、移動操作の4方向を順番にリバインドしたい場合、前述のインタラクティブなリバインドを順に繰り返すといった方法で実現できます。

Composite Bindingが内包する数分だけ繰り返せばよいことになります。

サンプルスクリプト
以下、Composite Bindingに対応するようにスクリプトを改良した例です。

RebindUI.cs
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class RebindUI : MonoBehaviour
{
    // リバインド対象のAction
    [SerializeField] private InputActionReference _actionRef;

    // リバインド対象のScheme
    [SerializeField] private string _scheme = "Keyboard";

    // 現在のBindingのパスを表示するテキスト
    [SerializeField] private TMP_Text _pathText;

    // リバインド中のマスク用オブジェクト
    [SerializeField] private GameObject _mask;

    private InputAction _action;
    private InputActionRebindingExtensions.RebindingOperation _rebindOperation;

    // 初期化
    private void Awake()
    {
        if (_actionRef == null) return;

        // InputActionインスタンスを保持しておく
        _action = _actionRef.action;

        // キーバインドの表示を反映する
        RefreshDisplay();
    }

    // 後処理
    private void OnDestroy()
    {
        // オペレーションは必ず破棄する必要がある
        CleanUpOperation();
    }

    // リバインドを開始する
    public void StartRebinding()
    {
        // もしActionが設定されていなければ、何もしない
        if (_action == null) return;

        // リバインド対象のBindingIndexを取得
        var bindingIndex = _action.GetBindingIndex(
            InputBinding.MaskByGroup(_scheme)
        );

        // リバインドを開始する
        OnStartRebinding(bindingIndex);
    }

    // 上書きされた情報をリセットする
    public void ResetOverrides()
    {
        // Bindingの上書きを全て解除する
        _action?.RemoveAllBindingOverrides();
        RefreshDisplay();
    }

    // 現在のキーバインド表示を更新
    public void RefreshDisplay()
    {
        if (_action == null || _pathText == null) return;

        _pathText.text = _action.GetBindingDisplayString();
    }

    // 指定されたインデックスのBindingのリバインドを開始する
    private void OnStartRebinding(int bindingIndex)
    {
        // もしリバインド中なら、強制的にキャンセル
        // Cancelメソッドを実行すると、OnCancelイベントが発火する
        _rebindOperation?.Cancel();

        // リバインド前にActionを無効化する必要がある
        _action.Disable();

        // ブロッキング用マスクを表示
        if (_mask != null)
            _mask.SetActive(true);

        // リバインドが終了した時の処理を行うローカル関数
        void OnFinished(bool hideMask = true)
        {
            // オペレーションの後処理
            CleanUpOperation();

            // 一時的に無効化したActionを有効化する
            _action.Enable();

            // ブロッキング用マスクを非表示
            if (_mask != null && hideMask)
                _mask.SetActive(false);
        }

        // リバインドのオペレーションを作成し、
        // 各種コールバックの設定を実施し、
        // 開始する
        _rebindOperation = _action
            .PerformInteractiveRebinding(bindingIndex)
            .OnComplete(_ =>
            {
                // リバインドが完了した時の処理
                RefreshDisplay();

                var bindings = _action.bindings;
                var nextBindingIndex = bindingIndex + 1;

                if (nextBindingIndex <= bindings.Count - 1 && bindings[nextBindingIndex].isPartOfComposite)
                {
                    // Composite Bindingの一部なら、次のBindingのリバインドを開始する
                    OnFinished(false);
                    OnStartRebinding(nextBindingIndex);
                }
                else
                {
                    OnFinished();
                }
            })
            .OnCancel(_ =>
            {
                // リバインドがキャンセルされた時の処理
                OnFinished();
            })
            .OnMatchWaitForAnother(0.2f) // 次のリバインドまでの待機時間を設ける
            .Start(); // ここでリバインドを開始する
    }

    // リバインドオペレーションを破棄する
    private void CleanUpOperation()
    {
        // オペレーションを作成したら、Disposeしないとメモリリークする
        _rebindOperation?.Dispose();
        _rebindOperation = null;
    }
}
使用方法はこれまでの例と変わりありません。

例では、次のように移動操作のMove Actionに対して適用するものとします。

実行結果
次のように順番に入力受け付けされるようになりました。

スクリプトの説明
インタラクティブなリバインドが開始されたらBindingのインデックスを取得するところまでは一緒です。

// リバインド対象のBindingIndexを取得
var bindingIndex = _action.GetBindingIndex(
    InputBinding.MaskByGroup(_scheme)
);

// リバインドを開始する
OnStartRebinding(bindingIndex);
Composite Bindingはスキームに含まれないため、上記のコードで内包されるBindingの開始インデックスを取得できます。

リバインドの設定やコールバック処理は以下のように変更しています。

// リバインドのオペレーションを作成し、
// 各種コールバックの設定を実施し、
// 開始する
_rebindOperation = _action
    .PerformInteractiveRebinding(bindingIndex)
    .OnComplete(_ =>
    {
        // リバインドが完了した時の処理
        RefreshDisplay();

        var bindings = _action.bindings;
        var nextBindingIndex = bindingIndex + 1;

        if (
            nextBindingIndex <= bindings.Count - 1 &&
            bindings[nextBindingIndex].isPartOfComposite)
        {
            // Composite Bindingの一部なら、次のBindingのリバインドを開始する
            OnFinished(false);
            OnStartRebinding(nextBindingIndex);
        }
        else
        {
            OnFinished();
        }
    })
    .OnCancel(_ =>
    {
        // リバインドがキャンセルされた時の処理
        OnFinished();
    })
    .OnMatchWaitForAnother(0.2f) // 次のリバインドまでの待機時間を設ける
    .Start(); // ここでリバインドを開始する
次のインデックスのBindingを調べ、それがComposite Bindingに内包されるBindingであれば、次のBindingを開始しています。

ただし、続けてインタラクティブなリバインドを行う場合、前入力が悪さして誤入力されることがあるため、次のコードで0.2秒ほど待機時間を挟んでいます。

.OnMatchWaitForAnother(0.2f) // 次のリバインドまでの待機時間を設ける
OnMatchWaitForAnotherメソッドは、リバインドが成功してから次のリバインドを開始するまでの待機時間を設定するメソッドです。

待機時間は状況に合わせて調整してください。 [6]
参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

キャンセルキーを設ける
ここまで解説した方法では、特定スキームの入力をすべて受け付けるようにしていました。

しかしながら、特定キー（例えばエスケープキー）をキャンセル操作に割り当てたいケースがあるかもしれません。

このようなキャンセル操作は、WithCancelingThroughメソッドにより指定が可能です。

rebindOperation = action
    .PerformInteractiveRebinding(bindingIndex)
    .OnComplete(_ =>
    {
        // リバインドが完了した時の処理
    })
    .OnCancel(_ =>
    {
        // リバインドがキャンセルされた時の処理
    })
    // キャンセルキーを設定する
    .WithCancelingThrough("<Keyboard>/escape")
    .Start(); // ここでリバインドを開始する





ンタラクティブなリバインドの最中にキャンセル入力があればキャンセル扱いとなり、キーの上書きが反映されません。

また、OnCancelコールバックが発火し、OnCompoleteコールバックは発火しません。

参考：Class InputActionRebindingExtensions.RebindingOperation| Input System | 1.5.1

設定情報をセーブ・ロードする
リバインドによって上書きされる情報は、JSONとして読み書きできます。

キーコンフィグの情報をストレージなどに保存しておきたい場合に便利です。



<img src="images/11/11_2/unity-input-system-rebinding-7.png.avif" width="90%" alt="" title="">

<br>


保存用のJSONデータの取得にはSaveBindingOverridesAsJson拡張メソッドを使います。

参考：Class InputActionRebindingExtensions| Input System | 1.5.1

逆にロードしたJSONデータを反映するにはLoadBindingOverridesFromJson拡張メソッドを使います。

参考：Class InputActionRebindingExtensions| Input System | 1.5.1

やり取りする対象のJSONデータは、Input Action Asset単位またはAction単位で可能です。

注意
データの保存方法はゲームやアプリ毎に異なります。状況に合わせて適切に設計する必要があることにご注意ください。

サンプルスクリプト
以下、Input Action Assetの上書き情報を読み書きする例です。

RebindSaveManager.cs
using System.IO;
using UnityEngine;
using UnityEngine.InputSystem;

public class RebindSaveManager : MonoBehaviour
{
    // 対象となるInputActionAsset
    [SerializeField] private InputActionAsset _actionAsset;

    // 上書き情報の保存先
    [SerializeField] private string _savePath = "InputActionOverrides.json";

    // 上書き情報の保存
    public void Save()
    {
        if (_actionAsset == null) return;

        // InputActionAssetの上書き情報の保存
        var json = _actionAsset.SaveBindingOverridesAsJson();

        // ファイルに保存
        var path = Path.Combine(Application.persistentDataPath, _savePath);
        File.WriteAllText(path, json);
    }

    // 上書き情報の読み込み
    public void Load()
    {
        if (_actionAsset == null) return;

        // ファイルから読み込み
        var path = Path.Combine(Application.persistentDataPath, _savePath);
        if (!File.Exists(path)) return;

        var json = File.ReadAllText(path);

        // InputActionAssetの上書き情報を設定
        _actionAsset.LoadBindingOverridesFromJson(json);
    }
}
上記をRebindSaveManager.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチすると使用可能になります。

上書き情報をJSONファイルとして保存するにはSaveメソッド、JSONファイルからロードして上書き情報を適用するにはLoadメソッドを外部から呼び出します。

例では、Save、Loadボタンが押されたときにそれぞれSave、Loadメソッドが呼ばれるようにしました。

ロードされたときは画面の表示も一緒に更新するため、前述のサンプルスクリプトで登場したRefreshDisplayメソッドも呼ぶようにしています。

保存先は、Application.persistentDataPathプロパティが示すディレクトリ直下に保存するようにしました。

実際のパスはプラットフォーム毎に異なります。詳細は以下リファレンスをご確認ください。

参考：Application-persistentDataPath – Unity スクリプトリファレンス

実行結果
リバインドを実施した後にSaveボタンを押すとディスクに上書きデータが保存されます。

Loadボタンを押すと上書きデータがロードされて適用されます。この時、Saveしたときのデータになっていることが確認できます。

保存されたJSONファイルを開くと、次のように最小化されたJSON形式で上書きデータが保存されていることが確認できます。





<img src="images/11/11_2/unity-input-system-rebinding-8.png.avif" width="90%" alt="" title="">

<br>


スクリプトの説明
Input Action Assetから上書き情報を取得してJSONファイルとして保存する処理は以下の通りです。

// 上書き情報の保存
public void Save()
{
    if (_actionAsset == null) return;

    // InputActionAssetの上書き情報の保存
    var json = _actionAsset.SaveBindingOverridesAsJson();

    // ファイルに保存
    var path = Path.Combine(Application.persistentDataPath, _savePath);
    File.WriteAllText(path, json);
}
Application.persistentDataPathプロパティが示すディレクトリ直下にSaveBindingOverridesAsJsonメソッドの結果をそのままテキストファイルとして保存しています。




逆にロードして上書き情報を反映する処理は以下の通りです。

// 上書き情報の読み込み
public void Load()
{
    if (_actionAsset == null) return;

    // ファイルから読み込み
    var path = Path.Combine(Application.persistentDataPath, _savePath);
    if (!File.Exists(path)) return;

    var json = File.ReadAllText(path);

    // InputActionAssetの上書き情報を設定
    _actionAsset.LoadBindingOverridesFromJson(json);
}
ファイルが存在しない場合も考えられるため、File.Existsメソッドで存在チェックしています。


File.Exists(String) メソッド (System.IO)
指定したファイルが存在するかどうかを確認します。
learn.microsoft.com

File.ReadAllText メソッド (System.IO)
テキスト ファイルを開き、そのファイル内のすべてのテキストを文字列に読み取った後、ファイルを閉じます。
learn.microsoft.com
PlayerInput経由で使用する場合
ここまで解説したリバインドは、PlayerInputを使用している環境下でも使える方法です。

例えば以下のようにUnity Event経由でPlayerInputからコールバックを呼び出すコードでも機能します。

PlayerInputReceiveExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerInputReceiveExample : MonoBehaviour
{
    public void OnJump(InputAction.CallbackContext context)
    {
        print("Jump");
    }
}
公式のサンプルシーン
Input Systemパッケージ側でもキーコンフィグを実装した公式サンプルが提供されています。

Package Manager画面からInput Systemパッケージを選択し、「Rebinding UI」に対して「Import」ボタンでインポートすると閲覧できます。




<img src="images/11/11_2/unity-input-system-rebinding-9.png.avif" width="90%" alt="" title="">

<br>

実行すると、本記事で解説したような挙動のインタラクティブなリバインドを行う動作が確認できます。







