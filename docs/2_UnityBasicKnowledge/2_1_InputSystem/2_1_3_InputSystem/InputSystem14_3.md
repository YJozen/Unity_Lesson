【Unity】Input Systemの仮想カーソルをローカルマルチで扱う方法
2024年4月24日

https://nekojara.city/unity-input-system-multiple-virtual-mice

こじゃら
ローカルマルチで複数プレイヤーが仮想カーソルで選択する画面を作りたい場合どうすればいいの？

このは
Input System提供のVirtual MouseとPlayer Inputを組み合わせて実現できるわ。

Input Systemでは仮想カーソル用のコンポーネントVirtual Mouseが提供されていますが、ローカルマルチなど複数プレイヤーがそれぞれカーソルを操作する場面では少し工夫が必要です。

やや面倒ですが、プレイヤー毎にVirtual MouseとPlayer Inputをシーンに配置して、操作対象を紐づける設定をスクリプト側から行えば実現可能です。

また、動画の例の様にカーソルをUIとして画面に配置する場合、いくつか運用の制約があり注意が必要です。

本記事では、この注意点含めローカルマルチでプレイヤー毎の仮想カーソルを動かす方法について解説します。

 動作環境
Unity 2023.2.16f1
Input System 1.7.1
スポンサーリンク


目次 非表示
前提条件
実現方法の概要
実装手順
Input Action Assetの準備
Event System側の設定
プレイヤー用のPrefab準備
カーソルPrefabの準備
Player Input Managerの設定
カーソル管理用スクリプトの実装
実装例
スクリプトの適用
実行結果
スクリプトの説明
UI Scale ModeがScale With Screen Sizeの場合の対処
スケール補正用のProcessorの実装
スケール補正を適用するスクリプトの実装
スクリプトの適用
実行結果
スクリプトの説明
さいごに
関連記事
参考サイト
前提条件
事前にInput Systemがインストールされ、有効化されているものとします。

導入手順は以下記事で解説しています。


【Unity】Input Systemの使い方入門
Unity公式の新しい入力システムパッケージInput Systemの入門者向け記事です。 本記事では、Input Systemパッケージのインストール方法から、最低限使えるようにするところまでを解説していきます。 また…
2021年11月29日
また、本記事を読み進めるにあたり、仮想カーソルおよびローカルマルチの基本的な使い方を押さえておくと理解がスムーズです。

より詳細な使い方は以下記事で解説しています。


【Unity】Input Systemからマウスカーソルを操作する
Input Systemでは、マウスカーソルをゲームパッドなどから操作可能にするVirtual Mouseコンポーネントが提供されています。 これを用いると、次のようにゲームパッドのスティックなどでカーソル移動やクリック…
2023年5月26日

【Unity】Input Systemでローカルマルチを実装する
Input Systemでは、PCなどに複数のゲームパッドを繋いでゲームをプレイするローカルマルチプレイヤーに対応しています。 これは、Player InputおよびPlayer Input Managerコンポーネント…
2023年6月2日
本記事では、次のようにUnity UIで画面上に配置されているボタンに対し、複数の仮想カーソルからクリックできるようにするところを目指します。 [1]

EventSystemにStandalone Input Moduleがアタッチされている場合、そのままではInput Systemの入力を取得できない（旧Inputの入力を取得する設定になる）ので、Replace with InputSystemUIInputModuleボタンからコンポーネントを置き換えてください。

また、仮想カーソルを使用するにあたっては、CanvasのCanvas ScalerコンポーネントのUI Scale ModeにConstant Pixel Sizeが指定されていることが前提となります。


もしUI Scale ModeにScale With Screen Sizeを指定する場合、クリック位置のずれ問題が発生するため、ずれ解消のための特殊な手順が必要です。本記事では、この解消方法含めた手順を順を追って解説します。

実現方法の概要
まず、仮想カーソルを複数プレイヤーから操作するために必要な実装方法の概要を示します。

Input Systemでの仮想カーソルの実現は、Virtual Mouseコンポーネント（プログラム上ではVirtualMouseInputクラス）で実現できます。

OSカーソルを直接動かすハードウェアカーソルモードと、UI画像などをカーソルに見立てて動かすソフトウェアカーソルモードの2種類が存在しますが、複数カーソルを扱う場合は後者となります。

通常はカーソルとなるUI画像をCanvas上に配置して、ここにVirtual Mouseをアタッチしておけば良いでしょう


仮想カーソルUIとVirtual Mouse
Virtual Mouseがゲームパッドなどからの入力を受け取るには、Virtual Mouse側のInput Actionの設定が必要になります。


仮想カーソルを動かすために必要なAction
単一の仮想カーソルを動かす場合はInput Actionの設定だけで良いですが、複数プレイヤーにカーソルを用意して動かすためにはPlayer Inputコンポーネントからの入力をVirtual Mouse側に指定する必要があります。 [2]
これは、Virtual MouseのInput ActionにPlayer Input内部が管理しているInput Actionを指定すれば良いです。


プレイヤーの入退室に応じて動的にプレイヤー数が変わる場合、Player Input ManagerコンポーネントからPrefabを生成して管理する運用方法があります。

参考：Class PlayerInputManager| Input System | 1.7.0

例えば、プレイヤーがあるコントローラーのボタンを押したら、プレイヤーをシーンに配置して入室させるといったことが可能です。

本記事では、この追加されたプレイヤーのPlayer Inputに基づいて仮想カーソル配置してActionを紐づける処理をスクリプトで実装して対応することとします。


入室時のスクリプト処理
実装手順
前述の仕組みを実現するための手順を解説していきます。

Input Action Assetの準備
仮想カーソルからの入力を定義するためのInput Action Assetを準備します。これは後述する仮想カーソルの入力として使います。

本記事では、「Game」という名前のInput Action Assetを新規作成するものとします。

また、「Player」というMapを作成し、そのMap内に仮想カーソル移動入力の「Move」、左ボタン入力の「LeftButton」という名前のActionを定義するものとします。

そして、各Actionに対してBinding（実際の入力割り当て）を定義します。ここでは、次のような操作を設定するものとします。

設定するBinding
キーボード
Move – WASDキー
LeftButton – スペースキー
ゲームパッド
Move – 左スティック
LeftButton – Southボタン
また、各種ActionのAction TypeとControl Typeは以下のように設定してください。

Actionの設定内容
Move
Action Type – Value
Control Type – Vector 2
LeftButton
Action Type – Button

Event System側の設定
EventSystemにアタッチされているInput System UI Input ModuleコンポーネントのPointer BehaviourにAll Pointers As Isを指定します。


これは、複数のポインター入力を統合などの処理をせずそのまま独立したポインターとして扱う設定です。

参考：UI support | Input System | 1.7.0

注意
Pointer BehaviourがAll Pointers As Isになっていない場合、ポインターの統合処理が行われ複数の仮想カーソルのクリック位置を正常に処理できなくなるためご注意ください。

プレイヤー用のPrefab準備
各プレイヤー毎の入力の受け皿となるオブジェクト用のPrefabを作成します。本記事では、仮想カーソルの画像やVirtual Mouseコンポーネントは別で作成して配置するものとします。

まず、適当なゲームオブジェクトを作成し、Player Inputコンポーネントをアタッチします。オブジェクト名は「PlayerInput」としました。

そして、Player InputのActionsに先ほど作成したInput Action Assetを指定し、BegaviourにInvoke Unity Eventsを指定します。 [3]
最終的に以下の様な設定になっていれば良いです。


ここまで終わったらゲームオブジェクトをPrefab化しておきます。

カーソルPrefabの準備
続いて表示用のカーソルUIのPrefabを作成します。例では、次の1Pと2P用のスプライトを使用することとします。


このカーソル画像はUnity UIのImageとして扱うため、Import SettingsのTexture TypeをSprite (2D an UI)に設定しておいてください。


続いて、カーソルPrefabを作成していきます。ここでは、Canvas配下にImageオブジェクトを配置し、前述のカーソルスプライトを適用するものとします。

また、カーソル自身のRaycast Targetが有効になっているとクリックの妨げになってしまうため無効化します。


注意
Raycast Targetの無効化を忘れると、カーソル画像自身に妨げられてクリックが反応しなくなる不都合が発生する可能性があるのでご注意ください。

そして、アンカーを左下に設定し、Pivotをクリックが反応して欲しい位置に調整します。例では、カーソル先端がクリック位置になるようにPivotを調整しています。


仮想カーソル化するためのVirtual Mouseコンポーネントを追加し、Cursor GraphicとCursor Transformにそれぞれカーソル自身のImageとTransformを指定します。Cursor ModeはSoftware Cursorのままとしてください。


本記事では、カーソル自身もPrefab化するため、Prefab化して分かりやすい名前にしておきます。例では「Cursor_1P」としました。

もしプレイヤー毎に表示するカーソルを変えたい場合は、必要なカーソルPrefabを同様に作成しておきます。例では、2P用のカーソルを複製して画像のみ差し替えることとします。

Player Input Managerの設定
ローカルマルチで複数プレイヤーの入退室を管理するために、Player Input Managerコンポーネントがアタッチされたゲームオブジェクトをシーンに配置します。

例では、「PlayerInputManager」という名前のオブジェクトを配置してコンポーネントを追加することとします。

そして、Player Input Managerコンポーネントをインスペクターから設定します。以下の通り設定してください。

Notification Behaviour – Invoke Unity Events
Join Behaviour – Join Players When Button Is Pressed（ボタンが押されたデバイスで参加する挙動）
Player Prefab – 前述の手順で作成したプレイヤーPrefab（Player Inputコンポーネントをアタッチしたもの）

カーソル管理用スクリプトの実装
プレイヤーが入室したときに仮想カーソルを配置して必要なActionを紐づけるスクリプトを実装します。これはPlayer Inputの入力をVirtual Mouseに渡す役割を持ちます。

実装例
以下実装例です。

VirtualMouseManager.cs
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.UI;

public class VirtualMouseManager : MonoBehaviour
{
    // カーソルの親オブジェクト
    [SerializeField] private RectTransform _root;

    // プレイヤーのカーソルPrefab一覧
    [SerializeField] private VirtualMouseInput[] _cursorPrefabs;

    // カーソル移動Action名
    [SerializeField] private string _moveActionName = "Move";

    // カーソル左クリックAction名
    [SerializeField] private string _leftButtonActionName = "LeftButton";

    // 生成されたカーソル一覧
    private readonly List<VirtualMouseInput> _cursors = new();

    // プレイヤーの参加時に呼び出される
    public void OnPlayerJoined(PlayerInput playerInput)
    {
        print($"プレイヤー#{playerInput.playerIndex}が参加しました");

        // インデックスのチェック
        var playerIndex = playerInput.playerIndex;
        if (playerIndex < 0 || playerIndex >= _cursorPrefabs.Length)
        {
            Debug.LogError("参加できるプレイヤー数を超えています");
            return;
        }

        // カーソルの生成
        var cursor = Instantiate(_cursorPrefabs[playerIndex], _root);
        cursor.name = $"Cursor#{playerIndex}";

        // カーソルを管理リストに追加
        _cursors.Add(cursor);

        // InputActionの取得
        var actions = playerInput.actions;

        var moveAction = actions.FindAction(_moveActionName);
        var leftButtonAction = actions.FindAction(_leftButtonActionName);

        // ActionPropertyの設定
        if (moveAction != null)
            cursor.stickAction = new InputActionProperty(moveAction);
        if (leftButtonAction != null)
            cursor.leftButtonAction = new InputActionProperty(leftButtonAction);
    }

    // プレイヤーの離脱時に呼び出される
    public void OnPlayerLeft(PlayerInput playerInput)
    {
        print($"プレイヤー#{playerInput.playerIndex}が離脱しました");

        // カーソルを管理リストから削除
        var playerIndex = playerInput.playerIndex;

        // 生成されたカーソル取得
        var cursor = _cursors.Find(c => c != null && c.name == $"Cursor#{playerIndex}");
        if (cursor == null) return;

        // カーソルの削除
        _cursors.Remove(cursor);
        Destroy(cursor.gameObject);
    }
}
スクリプトの適用
上記スクリプトをVirtualMouseManager.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチします。インスペクターより以下の項目を設定してください。

Root – カーソルを配置する親オブジェクト
Cursor Prefabs – プレイヤー毎のカーソルPrefab（必要なプレイヤー数だけ登録）
Move Action Name – カーソル移動Action名
Left Button Action Name – クリックAction名
Action名は例の通りのActionをInput Action Assetに定義している場合は初期設定のままで問題ありません。


最後に、Player Input ManagerのEventsに上記スクリプトのメソッドを登録します。Player Joined EventにVirtualMouseManager.OnPlayerJoinedメソッドを、Player Left EventにVirtualMouseManager.OnPlayerLeftメソッドを登録してください。


注意
この手順を忘れると、Player Input Managerからの入退室通知を受け取れなくなるためご注意ください。

また、インスペクターから指定するメソッドは、必ず引数を個別指定しない方（メニュー上側）を選択してください。下側に表示されるメソッドはPlayer Inputのインスタンスをインスペクターから手動指定する設定なので引数から正しくPlayer Inputを受け取れません。


実行結果
ボタンを押したコントローラーにプレイヤーが割り当てられ、入室と同時にカーソルが表示されてUIを操作可能になります。

今回はサンプルのため、敢えて初期位置の指定処理は入れていませんが、仮想カーソルのアンカー位置をInstantiate値またはその後にスクリプトから調整すれば実現可能です。

また、この例ではCanvas ScalerのUI Scale ModeがConstant Pixel Sizeでないとクリック位置がずれてしまう現象に遭遇します。この対処法は後述します。

スクリプトの説明
仮想カーソルの配置先のオブジェクト階層やPrefab、Player Inputから受け取るAction名は以下フィールドとして定義しています。

// カーソルの親オブジェクト
[SerializeField] private RectTransform _root;

// プレイヤーのカーソルPrefab一覧
[SerializeField] private VirtualMouseInput[] _cursorPrefabs;

// カーソル移動Action名
[SerializeField] private string _moveActionName = "Move";

// カーソル左クリックAction名
[SerializeField] private string _leftButtonActionName = "LeftButton";
そして、Prefabから生成された仮想カーソルオブジェクトは、以下のリストとして管理します。これはプレイヤー退室時に破棄できるようにするためです。

// 生成されたカーソル一覧
private readonly List<VirtualMouseInput> _cursors = new();
プレイヤー入室の検知は次のメソッドで行います。

// プレイヤーの参加時に呼び出される
public void OnPlayerJoined(PlayerInput playerInput)
{
    print($"プレイヤー#{playerInput.playerIndex}が参加しました");
入室を検知したら、プレイヤーインデックスを取得し、インデックスに応じた仮想カーソルをPrefabからInstantiateします。

// インデックスのチェック
var playerIndex = playerInput.playerIndex;
if (playerIndex < 0 || playerIndex >= _cursorPrefabs.Length)
{
    Debug.LogError("参加できるプレイヤー数を超えています");
    return;
}

// カーソルの生成
var cursor = Instantiate(_cursorPrefabs[playerIndex], _root);
cursor.name = $"Cursor#{playerIndex}";
例では念のためインデックスの範囲チェックを行ってからPrefab生成処理に進んでいます。もしここでカーソル生成位置を独自指定したい場合、Instantiateの第2引数に位置を指定すれば良いです。

カーソル生成が済んだら、管理リストに追加しておきます。

// カーソルを管理リストに追加
_cursors.Add(cursor);
生成した仮想カーソルにPlayer InputのAction入力を渡すため、まずPlayer Inputの各種必要なActionを取得します。

// InputActionの取得
var actions = playerInput.actions;

var moveAction = actions.FindAction(_moveActionName);
var leftButtonAction = actions.FindAction(_leftButtonActionName);
PlayerInputクラスが保持するActionはactionsプロパティから取得できます。

そして、このプロパティからFindActionメソッドで指定した名前のActionを取得しています。

参考：Class InputActionAsset| Input System | 1.7.0

Actionを取得出来たら、仮想カーソルコンポーネントのVirtualMouseInputインスタンスの各種Actionに前述のPlayerInputのActionを指定して完了です。

// ActionPropertyの設定
if (moveAction != null)
    cursor.stickAction = new InputActionProperty(moveAction);
if (leftButtonAction != null)
    cursor.leftButtonAction = new InputActionProperty(leftButtonAction);
VirtualMouseInputクラスが要求するActionの型はInputActionProperty構造体なので、InputActionPropertyインスタンス経由で渡しています。

参考：Struct InputActionProperty| Input System | 1.7.0


【Unity】Actionの指定を便利にするInputActionPropertyの使い方
Input SystemのActionをスクリプトから扱う際、インスペクターからActionを指定する方法は主に次の2通りが考えられます。 両者はそれぞれデータの持ち方が別ですが、InputActionProperty構…
2023年5月2日
プレイヤー退室時には、以下メソッドが呼ばれます。

// プレイヤーの離脱時に呼び出される
public void OnPlayerLeft(PlayerInput playerInput)
{
    print($"プレイヤー#{playerInput.playerIndex}が離脱しました");
例では名前検索で管理リストから対象となる仮想カーソルを取得し、オブジェクト毎削除しています。

// カーソルを管理リストから削除
var playerIndex = playerInput.playerIndex;

// 生成されたカーソル取得
var cursor = _cursors.Find(c => c != null && c.name == $"Cursor#{playerIndex}");
if (cursor == null) return;

// カーソルの削除
_cursors.Remove(cursor);
Destroy(cursor.gameObject);
UI Scale ModeがScale With Screen Sizeの場合の対処
Canvas ScalerのUI Scale ModeにScale With Screen Sizeを指定している場合、次のようにクリック位置がずれてしまう問題が発生します。

これは、Virtual Mouse側がカーソル位置をスクリーン座標として処理しているためです。

この位置ずれの問題を解決したい場合、ハック的な方法になりますが、次のような手順で回避できる可能性があります。

位置ずれの解消手順
クリック位置を補正するカスタムProcessorを実装する
上記ProcessorをInputSystemUIInputModuleのpoint（Input Action）に適用するスクリプトを実装する
Canvasのサイズが変わったら、上記Processorのパラメータを更新する処理を実装
ただし、開発するゲームやアプリの設計によっては別の対処法が必要な可能性もありますので、ご自身のプログラムの作りをよく確認の上、作業を進めてください。

スケール補正用のProcessorの実装
ポインタ位置の座標を補正するためのProcessorを実装します。

以下実装例です。

VirtualMouseScaler.cs
using UnityEngine;
using UnityEngine.InputSystem;

#if UNITY_EDITOR
using UnityEditor;

[InitializeOnLoad]
#endif
public class VirtualMouseScaler : InputProcessor<Vector2>
{
    // 位置補正のスケール値(Processorのパラメータ)
    public float scale = 1;

    private const string ProcessorName = nameof(VirtualMouseScaler);

#if UNITY_EDITOR
    static VirtualMouseScaler() => Initialize();
#endif

    // Processorの登録処理
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Initialize()
    {
        // 重複登録すると、Input ActionのProcessor一覧に正しく表示されない事があるため、
        // 重複チェックを行う
        if (InputSystem.TryGetProcessor(ProcessorName) == null)
            InputSystem.RegisterProcessor<VirtualMouseScaler>(ProcessorName);
    }

    // 独自のProcessorの処理定義
    public override Vector2 Process(Vector2 value, InputControl control)
    {
        // VirtualMouseの場合のみ、座標系問題が発生するためProcessorを適用する
        if (control.device.name.StartsWith("VirtualMouse"))
            value *= scale;

        return value;
    }
}
上記をVirtualMouseScaler.csという名前で保存しておきます。これでVirtualMouseScalerという名前のProcessorが使用可能になります。

スケール補正を適用するスクリプトの実装
ポインタ位置に前述のProcessorを適用するスクリプトを実装します。

以下実装例です。

SoftwareCursorPositionAdjuster.cs
using System;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.UI;

public class SoftwareCursorPositionAdjuster : MonoBehaviour
{
    // InputSystemUIInputModuleへの参照
    [SerializeField] private InputSystemUIInputModule _inputSystemUIInputModule;
    
    // Canvasへの参照
    [SerializeField] private Canvas _canvas;

    private float _lastScaleFactor = 1;

    // 現在のCanvasスケール
    private float CurrentScale => _canvas.scaleFactor;

    private void Start()
    {
        // InputSystemUIInputModuleとCanvasが指定されていなければ、自動で取得する
        // 参照はインスペクター上で設定することが推奨される
        if (_inputSystemUIInputModule == null)
        {
            var modules =
                FindObjectsByType<InputSystemUIInputModule>(FindObjectsInactive.Include, FindObjectsSortMode.None);
            if (modules.Length > 0) _inputSystemUIInputModule = modules[0];
        }

        if (_canvas == null)
        {
            var canvases = FindObjectsByType<Canvas>(FindObjectsInactive.Include, FindObjectsSortMode.None);
            if (canvases.Length > 0) _canvas = canvases[0];
        }
    }

    // Canvasのスケールを監視して、VirtualMouseの座標を補正する
    private void Update()
    {
        // Canvasのスケール取得
        var scale = CurrentScale;

        // スケールが変化した時のみ、以降の処理を実行
        if (Math.Abs(scale - _lastScaleFactor) == 0) return;

        // VirtualMouseInputのカーソルのスケールを変更するProcessorを適用
        _inputSystemUIInputModule.point.action.ApplyBindingOverride(new InputBinding
        {
            overrideProcessors = $"VirtualMouseScaler(scale={scale})"
        });

        _lastScaleFactor = scale;
    }
}
上記をSoftwareCursorPositionAdjuster.csという名前で保存しておきます。

スクリプトの適用
前述のSoftwareCursorPositionAdjusterスクリプトを適当なゲームオブジェクトにアタッチします。例ではCanvasオブジェクトにアタッチするものとします。


実行結果
位置ずれなく正しくカーソル位置が判定できるようになりました。

途中でCanvasサイズを変更していますが、変更後のサイズにも追従できていることも確認できました。

スクリプトの説明
ポインタ位置を補正するInput SystemのProcessorは、以下クラスとして実装しています。

#if UNITY_EDITOR
using UnityEditor;

[InitializeOnLoad]
#endif
public class VirtualMouseScaler : InputProcessor<Vector2>
{
Unityエディタ時でも動作するように[InitializeOnLoad]属性を付加しています。

参考：起動時エディタースクリプト実行 – Unity マニュアル

実装したProcessorはそのままではInput System側が認識できないため、以下処理で登録を行っています。

#if UNITY_EDITOR
    static VirtualMouseScaler() => Initialize();
#endif

    // Processorの登録処理
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Initialize()
    {
        // 重複登録すると、Input ActionのProcessor一覧に正しく表示されない事があるため、
        // 重複チェックを行う
        if (InputSystem.TryGetProcessor(ProcessorName) == null)
            InputSystem.RegisterProcessor<VirtualMouseScaler>(ProcessorName);
    }
参考：Processors | Input System | 1.7.0

参考：Class InputSystem| Input System | 1.7.0


【Unity】Input SystemのProcessorで入力値を加工する
Input SystemのProcessor機能の使い方についての解説記事です。 Processorを使うと、次のように入力値に対する加工が可能になります。 ProcessorはInput Actionの機能の一つです。…
2022年4月11日
そして、実際にポインタ位置を補正する処理は以下部分です。

// 独自のProcessorの処理定義
public override Vector2 Process(Vector2 value, InputControl control)
{
    // VirtualMouseの場合のみ、座標系問題が発生するためProcessorを適用する
    if (control.device.name.StartsWith("VirtualMouse"))
        value *= scale;

    return value;
}
得られた入力のデバイス名が「VirtualMouse」から始まる場合だけスケールを掛けるようにしています。これは、他の入力処理にまで適用してしまうと、今度は元のカーソルのクリック位置がずれてしまうためです。

メモ
同じデバイスが追加されると、末尾に番号が割り当てられて区別されます。

仮想カーソルの場合、「VirtualMouse」という名前のデバイスとして追加されるため、2番目以降のデバイスは「VirtualMouse1」「VirtualMouse2」などとなります。


複数のデバイス名を正しく判定するため、名前が「VirtualMouse」から始まるデバイス名という条件でチェックしています。

実際のCanvasサイズからProcessorにスケール補正値を渡す処理はSoftwareCursorPositionAdjuster.csの以下部分です。

// Canvasのスケールを監視して、VirtualMouseの座標を補正する
private void Update()
{
    // Canvasのスケール取得
    var scale = CurrentScale;

    // スケールが変化した時のみ、以降の処理を実行
    if (Math.Abs(scale - _lastScaleFactor) == 0) return;

    // VirtualMouseInputのカーソルのスケールを変更するProcessorを適用
    _inputSystemUIInputModule.point.action.ApplyBindingOverride(new InputBinding
    {
        overrideProcessors = $"VirtualMouseScaler(scale={scale})"
    });

    _lastScaleFactor = scale;
}
Updateイベントの中でスケールの変化をチェックし、スケールファクターが変わった時だけInputSystemUIInputModuleのカーソル位置（スクリーン座標）であるpointプロパティに設定をオーバーライドする形でProcessorを適用しています。

参考：Class InputSystemUIInputModule| Input System | 1.7.0

参考：Class InputActionRebindingExtensions| Input System | 1.7.0


【Unity】Input Actionをスクリプトから動的に編集する方法
Input SystemのActionをスクリプトから動的に構築したり変更する方法の解説記事です。 これを実践すると、次のようなことが実現できるようになります。 Input Systemでキャラクターの移動やジャンプ操作…
2023年3月28日
さいごに
Input Systemの仮想カーソルであるVirtual Mouseをローカルマルチに対応させるためには、Player Input側のActionをVirtual Mouse側に動的に紐づけるのが肝となります。

本記事ではプレイヤーと仮想カーソルのオブジェクトを分けて管理する方法を提案しましたが、必ずしもこの設計である必要はなく、最終的にActionの紐づけが出来れば良いです。

また、Canvas ScalerでScale With Screen Sizeを設定している場合は、仮想カーソルのポインタ位置（スクリーン座標）をキャンバス内の座標に変換する処理が必要になります。

