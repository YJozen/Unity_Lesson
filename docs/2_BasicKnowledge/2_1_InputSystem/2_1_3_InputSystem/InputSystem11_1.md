
<link rel="stylesheet" href="/sample.css">

# Input Actionをスクリプトから動的に編集する方法

https://nekojara.city/unity-input-system-actions-runtime

+ [Actionを作成する](#actionを作成する)

<hr>

## スクリプトから動的に編集する例
+ キーアサインを変更
+ マウス感度などの調整機能の実装
+ キーコンフィグ機能（リバインド）の実装

Input Systemでキャラクターの移動やジャンプ操作などを扱う時は、Actionという単位で管理します。この Actionを動的に作成したり変更したり削除したりもできます。

<img src="images/11/11_1/unity-input-system-actions-runtime-1.png.avif" width="70%" alt="" title="">

<br>

<br>

キーコンフィグを実装したい場合は、Actionの上書き機能を使うのが適しています。 (変更とは少し異なる機能です。)

<img src="images/11/11_1/unity-input-system-actions-runtime-2.png.avif" width="70%" alt="" title="">

上書き機能を使うことで、上書きしたデータのみをJSONとして保存したり、読み込んで適用したりできるようになります。

<br>

# Actionを作成する
Input SystemのActionはスクリプトからはInputActionクラスとして扱われます。

InputActionクラスは、「一つのActionを表すクラス」で、次のような情報を指定してインスタンス生成できます。

指定できる情報
+ Action名
+ Action Type（Value、Button、Pass Throughなど）
+ Bindingのパス
+ Interaction（長押し、ダブルタップなど）
+ Processor（スケールやデッドゾーンなど）
+ 種類の制限（Button、Keyboardのみ受け付けるなど）

以下はインスタンス生成する最低限のコードの例です。


```cs:
// Input Actionを生成する
InputAction inputAction = new InputAction(
    "TestAction",           // Action名
    InputActionType.Button, // Action Type
    "<Keyboard>/A"          // BindingのControl Path
);
```
「TestAction」という名前のActionを生成しています。  
キーボードのAキーが押された瞬間に入力が得られます。

<img src="images/11/11_1/unity-input-system-actions-runtime-3.png.avif" width="70%" alt="" title="">

<br>

<br>

ProcessorやInteractionも含めると次のようになります。
```cs:
// Input Actionを生成する
InputAction inputAction = new InputAction(
    "TestAction",           // Action名
    InputActionType.Button, // Action Type
    "<Keyboard>/A",         // BindingのControl Path
    "hold",                 // Interaction
    "scale(factor=2.5)",    // Processor
    "Button"                // 種類の制限
);
```
InteractionやProcessorなどは文字列として指定します。  
「名前(引数1=値1,引数2=値2,引数3=値3)」などという文字列形式で指定します。

<img src="images/11/11_1/unity-input-system-actions-runtime-4.png.avif" width="70%" alt="" title="">

<br>

その他、文字列指定の形式
+ <a href="https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/manual/Processors.html" target="_blank">Processor</a>
+ <a href="https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/manual/Interactions.html" target="_blank">Interaction</a>

<br>

スクリプトから動的にActionを生成し、ボタン入力があったらログを出力するサンプル。

```cs:
using UnityEngine;
using UnityEngine.InputSystem;

public class CreateInputActionExample : MonoBehaviour
{
    // 作成したActionはインスペクターから表示できるようにしておく
    [SerializeField] private InputAction _inputAction;

    private void Awake()
    {
        // Input Actionの生成
        _inputAction = new InputAction(
            "TestAction",           // Action名
            InputActionType.Button, // Action Type
            "<Keyboard>/A",         // BindingのControl Path
            "hold",                 // Interaction
            "scale(factor=2.5)",    // Processor
            "Button"                // 種類の制限
        );

        // performedコールバックを受け取るように設定
        _inputAction.performed += OnReadAction;

        // 入力の受け取りを有効化する必要がある
        _inputAction.Enable();
    }

    private void OnDestroy()
    {
        // 終了時にActionを無効化する
        _inputAction?.Disable();
    }

    // TestActionのperformedコールバック
    private void OnReadAction(InputAction.CallbackContext context)
    {
        // 受け取った値をログ出力
        Debug.Log($"入力値 : {context.ReadValue<float>()}");
    }
}

```
上記をCreateInputActionExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチすると機能します。

Aキーを長押しすると、入力値がログ出力されるようになります。

長押しして反応する理由　→　Interactionに”hold”を指定したため  
得られる入力値は2.5。　→ 入力値に、指定の値を掛けるProcessorのscaleを指定したため  

上記スクリプトのInput Action項目をダブルクリックすると、指定された内容で初期化されていることが確認できます。

<img src="images/11/11_1/unity-input-system-actions-runtime-6.png.avif" width="70%" alt="" title="">

<br>

# Input Action Assetの作成
Input Actionの定義そのものはInput Action Assetとして保存されます。このアセット自体もスクリプトから作成できます。

Input Action Assetは、複数のActionをまとめた複数のMapで構成されます。

<img src="images/11/11_1/unity-input-system-actions-runtime-7.png.avif" width="70%" alt="" title="">

<br>

スクリプトからはInputActionAssetクラスとして扱います。

InputActionAssetクラスはScriptableObject継承クラスなので、スクリプトから作成するときは次のようにScriptableObject.CreateInstanceメソッド経由でインスタンス化します。
```cs:
// Input Action Assetインスタンスを生成
InputActionAsset inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();
```

作成したInput Action Assetに対して、MapやActionを追加・削除・編集ができます。
```cs:
// 「Player」というMapを追加
InputActionMap playerMap = inputActionAsset.AddActionMap("Player");

// 「Jump」というActionをPlayer Mapに追加
InputAction jumpAction = playerMap.AddAction(
    "Jump",
    InputActionType.Button,
    "<Keyboard>/A"
);
```
<br>

Input Action Assetをスクリプトから作成する例です。
```cs:CreateInputActionAssetExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class CreateInputActionAssetExample : MonoBehaviour
{
    private InputActionAsset _inputActionAsset;

    // 初期化
    private void Awake()
    {
        // Input Action Assetを作成
        _inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();

        // 「Player」というMapを追加
        var playerMap = _inputActionAsset.AddActionMap("Player");

        // 「Jump」というActionをPlayer Mapに追加
        var jumpAction = playerMap.AddAction(
            "Jump",
            InputActionType.Button,
            "<Keyboard>/Space"
        );

        // Jump Actionのperformedコールバックだけ拾う
        jumpAction.performed += OnJump;

        // Input Action Asset全体のActionを有効化する
        _inputActionAsset.Enable();
    }

    // 後処理
    private void OnDisable()
    {
        // Input Action Assetの破棄
        if (_inputActionAsset != null)
            Destroy(_inputActionAsset);
    }

    // Jump Actionコールバック
    private void OnJump(InputAction.CallbackContext context)
    {
        // ログ出力
        print("Jump");
    }
}
```

新しくInput Action Assetを作成し、「Player」という名前のMapを作成し、その下に「Jump」というActionを追加しています。


<img src="images/11/11_1/unity-input-system-actions-runtime-8.png.avif" width="70%" alt="" title="">

<br>

上記スクリプトをCreateInputActionAssetExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチすると機能するようになります。

スペースキーが押されるたびに「Jump」というログを出力します。

<br>

## スクリプトの説明
初期化の次の部分でInput Action Assetを作成してMapとActionを追加しています。
```cs:
// Input Action Assetを作成
_inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();

// 「Player」というMapを追加
var playerMap = _inputActionAsset.AddActionMap("Player");

// 「Jump」というActionをPlayer Mapに追加
var jumpAction = playerMap.AddAction(
    "Jump",
    InputActionType.Button,
    "<Keyboard>/Space"
);
```

生成されたInputActionAssetインスタンスに対してEnableメソッドを実行すると、Input Action Assetに登録されているAction全体を有効化できます。

```cs:
// Input Action Asset全体のActionを有効化する
_inputActionAsset.Enable();
```
Enableメソッドを実行しないとActionが有効化されず、入力を受け取れなくなるためご注意ください。

<br>






# ActionにBindingを追加する
インスタンスとして生成されたInputActionは、後からスクリプトより編集できます。

Actionに後からBindingを追加したり、Composite Binding を追加したりできます。

# Bindingの追加
次のようにInputActionインスタンスに対してAddBindingメソッドを呼び出す形で追加できます。

```cs:
InputAction inputAction;

・・・（中略）・・・

// スペースキーがPathのBindingを追加する
inputAction.AddBinding("<Keyboard>/Space");
```

<img src="images/11/11_1/unity-input-system-actions-runtime-10.png.avif" width="70%" alt="" title="">

<br>


これは、以下のようにいくつかオーバーロードされた拡張メソッドとして定義されています。
```
public static InputActionSetupExtensions.BindingSyntax AddBinding(
    this InputAction action,
    string path,
    string interactions = null,
    string processors = null,
    string groups = null
);
```

```
public static InputActionSetupExtensions.BindingSyntax AddBinding(
    this InputAction action,
    InputBinding binding = default(InputBinding)
);
```

```
public static InputActionSetupExtensions.BindingSyntax AddBinding(
    this InputAction action,
    InputControl control
);
```

InteractionやProcessorなども一緒に追加できます。

戻り値として、Bindingを編集するためのシンタックスが返されます。このシンタックスに対して様々な操作を施すことが可能です。

Composite Bindingの追加
ActionにはBindingのほかComposite Bindingも追加できます。次のようにAddCompositeBindingメソッドを呼び出す形で行います。

```
InputAction inputAction;

・・・（中略）・・・

inputAction.AddCompositeBinding("Axis")
    .With("Negative", "<Keyboard>/LeftArrow")
    .With("Positive", "<Keyboard>/RightArrow");
```


<img src="images/11/11_1/unity-input-system-actions-runtime-11.png.avif" width="70%" alt="" title="">

<br>

例はAxisというComposite Binding（1軸入力）を追加し、パラメータとして負方向ボタン（Negative）に左矢印キー、正方向ボタン（Positive）に右矢印キーをメソッドチェーンで追加しています。

AddCompositeBindingメソッドは次のような拡張メソッドとして定義されています。

```cs:
public static InputActionSetupExtensions.CompositeSyntax AddCompositeBinding(
    this InputAction action,
    string composite,
    string interactions = null,
    string processors = null
);
```

AddBindingメソッド同様、こちらもInteractionやProcessorも同時に指定できます。

戻り値はComposite Binding編集用のシンタックスで、これに対してComposite Bindingのパラメータを設定できます。

サンプルスクリプト
WASDキー入力のComposite Bindingをスクリプトから追加するサンプルスクリプトです。

```cs:AddCompositeBindingExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class AddCompositeBindingExample : MonoBehaviour
{
    // 作成したActionはインスペクターから表示できるようにしておく
    [SerializeField] private InputAction _moveAction;

    private void Awake()
    {
        // Input Actionの生成
        _moveAction = new InputAction(
            "Move", // Action名
            InputActionType.Value // 連続値なのでValue
        );

        // Composite Bindingの追加
        // WASDを2軸入力として受け取れるようにする
        _moveAction.AddCompositeBinding("2DVector")
            .With("Up", "<Keyboard>/W")
            .With("Down", "<Keyboard>/S")
            .With("Left", "<Keyboard>/A")
            .With("Right", "<Keyboard>/D");

        // performedコールバックを受け取るように設定
        _moveAction.performed += OnMove;
        _moveAction.canceled += OnMove;

        // 入力の受け取りを有効化する必要がある
        _moveAction.Enable();
    }

    private void OnDestroy()
    {
        // 終了時にActionを無効化する
        _moveAction?.Disable();
    }

    // Move Actionの入力値受け取りコールバック
    // 入力値が変化したときに呼ばれる
    private void OnMove(InputAction.CallbackContext context)
    {
        // 受け取った値をログ出力
        Debug.Log($"入力値 : {context.ReadValue<Vector2>()}");
    }
}
```

次のような内容のActionをスクリプトから生成します。

<img src="images/11/11_1/unity-input-system-actions-runtime-12.png.avif" width="70%" alt="" title="">

<br>



上記スクリプトをAddCompositeBindingExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチすると機能するようになります。

実行すると、WASDキーで2軸入力を取得出来ていることを確認出来ました。

インスペクター上では2DVectorとしてComposite Bindingが設定されていることが確認できます。

<img src="images/11/11_1/unity-input-system-actions-runtime-13.png.avif" width="70%" alt="" title="">

<br>

## スクリプトについて
Composite Bindingを追加している処理は以下部分です。

// Composite Bindingの追加
// WASDを2軸入力として受け取れるようにする
_moveAction.AddCompositeBinding("2DVector")
    .With("Up", "<Keyboard>/W")
    .With("Down", "<Keyboard>/S")
    .With("Left", "<Keyboard>/A")
    .With("Right", "<Keyboard>/D");
WASDキーなどの4ボタン入力を2軸入力にまとめるComposite Bindingは「2DVector」という名前のため、AddCompositeBindingメソッドの引数に文字列「2DVector」を指定しています。

参考：Input Bindings | Input System | 1.5.1

そして、得られたシンタックスに対してメソッドチェーンで各方向のパラメータに対するControl Pathを指定しています。

これにより、次のコードでVector2型の2軸入力として入力値を受け取れるようになります。

// Move Actionの入力値受け取りコールバック
// 入力値が変化したときに呼ばれる
private void OnMove(InputAction.CallbackContext context)
{
    // 受け取った値をログ出力
    Debug.Log($"入力値 : {context.ReadValue<Vector2>()}");
}
ActionにInteractionやProcessorを追加したい場合
Input Systemでは、ActionやBindingに対してInteractionやProcessorを設定できます。

ただし、Action自体 [5] に対して後からInteractionやProcessorを追加する手段はInput System 1.5.0時点では提供されていません。

Actionに追加されている個別のBindingに対しては、後述の手順により後からInteractionやProcessorを追加可能です。

ActionのBindingを編集する
予め作成したActionのBinding対して、後からControl Pathを変更したり、InteractionやProcessorを追加したりできます。

編集できる内容
Nameを指定する
Control Pathを指定する
Interactionを追加する
Processorを追加する
InteractionとProcessorについては追加しかできない点にご注意ください。

名前を編集する
Actionに登録される各Bindingには、名前を設定することが可能です。

これは、後述するBindingの編集の際、ActionからBindingを検索して取得する際に使用できます。



<img src="images/11/11_1/unity-input-system-actions-runtime-14.png.avif" width="70%" alt="" title="">

<br>

次のようにAddBindingメソッドなどに対してメソッドチェーンで指定できます。 [6]
InputAction action = new InputAction("Test", InputActionType.Button);

・・・（中略）・・・

// 「NameA」という名前をBindingに指定
action.AddBinding("<Keyboard>/A")
    .WithName("NameA");

// 「NameB」という名前をBindingに指定
action.AddBinding("<Keyboard>/B")
    .WithName("NameB");
参考：Struct InputActionSetupExtensions.BindingSyntax| Input System | 1.5.1

Control Path、Interaction、Processorを編集する
例えば、AまたはBキーが押されたらperformedが発火する「Jump」というActionに対して、次のような変更を加えることを考えます。

BキーをCキーに変更する（Control Pathの変更）
長押しでperformed発火とする（Hold Interactionの追加）
入力値を3倍にする（Scale Processorの追加）



<img src="images/11/11_1/unity-input-system-actions-runtime-15.png.avif" width="70%" alt="" title="">

<br>



これをコードにすると次のようになります。

InputAction action = new InputAction("Jump", InputActionType.Button);

・・・（中略）・・・

// Bindingの変更
action.ChangeBinding(1)                  // インデックス1のBinding取得
    .WithPath("<Keyboard>/C")            // Cキーに変更
    .WithInteraction("hold")             // 長押しInteraction追加
    .WithProcessor("scale(factor=2.5)"); // Scale Processor追加
Actionに登録されているBindingにアクセスするためには、ChangeBinding拡張メソッドを使用します。

public static InputActionSetupExtensions.BindingSyntax ChangeBinding(
    this InputAction action,
    int index
);
引数には、Bindingに対する0始まりのインデックスを指定します。

戻り値は、Binding編集用のシンタックスです。

参考：Class InputActionSetupExtensions| Input System | 1.5.1

なお、ChangeBindingには名前指定で取得するオーバーロードされたメソッドなども用意されています。

public static InputActionSetupExtensions.BindingSyntax ChangeBinding(
    this InputAction action,
    string name
);
状況に応じて使い分けると良いでしょう。

必要な方は上記公式リファレンスをご確認ください。

サンプルスクリプト
以下、予め生成されたActionに対してControl Pathを変更し、InteractionとProcessorを追加する例です。

ChangeBindingExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class ChangeBindingExample : MonoBehaviour
{
    // 作成したActionはインスペクターから表示できるようにしておく
    [SerializeField] private InputAction _jumpAction;

    private void Awake()
    {
        // Input Actionの生成
        _jumpAction = new InputAction(
            "Jump",
            InputActionType.Button
        );

        // Bindingを追加
        // A、Bキーで反応する
        _jumpAction.AddBinding("<Keyboard>/A");
        _jumpAction.AddBinding("<Keyboard>/B");

        // Bキー（インデックス1）のBindingを編集
        _jumpAction.ChangeBinding(1) // インデックス1のBinding取得
            .WithPath("<Keyboard>/C") // Cキーに変更
            .WithInteraction("hold") // 長押しInteraction追加
            .WithProcessor("scale(factor=2.5)"); // 入力値を2.5倍にする

        // performedコールバックを受け取るように設定
        _jumpAction.performed += OnJump;

        // 入力の受け取りを有効化する必要がある
        _jumpAction.Enable();
    }

    // Jump Actionのperformedコールバック
    private void OnJump(InputAction.CallbackContext context)
    {
        Debug.Log($"入力値 : {context.ReadValue<float>()}");
    }
}
最初にA、BキーのBindingを追加し、後からBキーのBindingだけ編集しています。

上記スクリプトをChangeBindingExample.csという名前で保存し、適当なゲームオブジェクトにアタッチすると機能します。

実行結果
BキーのBindingがCキーに変更され、長押ししないと反応しないようになりました。また、入力値が2.5倍されています。


Bindingを削除する
予め追加されたBindingを削除したい場合も、ChangeBindingメソッドなどで得られるシンタックスを使います。 [7]
Binding削除にはシンタックスのEraseメソッドを使います。

// Input Actionを生成する
InputAction action = new InputAction(
    "TestAction",
    InputActionType.Button,
    "<Keyboard>/0"
);

・・・（中略）・・・

// インデックス0のBindingを削除
action.ChangeBinding(0).Erase();
参考：Struct InputActionSetupExtensions.BindingSyntax| Input System | 1.5.1

Input Action Assetのセーブ・ロード
スクリプトなどで編集したInput Action Assetの内容はJSONにシリアライズしたり、逆にJSONからデシリアライズできます。




<img src="images/11/11_1/unity-input-system-actions-runtime-16.png.avif" width="70%" alt="" title="">

<br>

これにより、Input Action Assetをファイルなどから読み書き可能になります。

JSONへのシリアライズ（JSONへの変換）にはInputActionAsset.ToJsonメソッドを使います。

InputActionAsset inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();

・・・（中略）・・・

// JSONにシリアライズ
string json = inputActionAsset.ToJson();
参考：Class InputActionAsset| Input System | 1.5.1

JSONからのデシリアライズ（JSONからの読み込み）メソッドは、InputActionAsset.FromJson、InputActionAsset.LoadFromJsonメソッドの2種類があります。

InputActionAsset.FromJsonメソッドはJSONから新しいInputActionAssetインスタンスを生成します。

// Input Action Assetの内容が格納されたJSON
string json;

・・・（中略）・・・

// JSONからインスタンス生成
InputActionAsset inputActionAsset = InputActionAsset.FromJson(json);

// ロード後は有効化する必要がある
inputActionAsset.Enable();
InputActionAsset.LoadFromJsonメソッドは既存のInputActionAssetインスタンスを使いまわして内容をロードします。

// 予めInputActionAssetインスタンスを生成
InputActionAsset inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();

// Input Action Assetの内容が格納されたJSON
string json;

・・・（中略）・・・

// JSONからロード
// インスタンスはそのまま使いまわす
inputActionAsset.LoadFromJson(json);

// ロード後は有効化する必要がある
inputActionAsset.Enable();




注意
JsonUtilityクラスを使用したJSONのシリアライズ・デシリアライズでは正しく動作しませんのでご注意ください。


サンプルスクリプト
Input Action AssetをJSONとして読み書きするサンプルです。

JsonExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class JsonExample : MonoBehaviour
{
    private InputActionAsset _inputActionAsset;

    // Input Action Assetの内容が格納されるJSON
    // この変数を保存場所代わりとする
    // インスペクターから自由に編集できるようにする
    [SerializeField] private string _json;

    private void Awake()
    {
        // Input Action Assetを作成
        _inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();

        // 「UI」というMapを追加
        var uiMap = _inputActionAsset.AddActionMap("UI");

        // 「Save」というActionをUI Mapに追加
        uiMap.AddAction(
            "Save",
            InputActionType.Button,
            "<Keyboard>/A" // Aキーで保存
        );

        // 「Load」というActionをUI Mapに追加
        uiMap.AddAction(
            "Load",
            InputActionType.Button,
            "<Keyboard>/B" // Bキーでロード
        );

        // コールバック登録
        _inputActionAsset["Save"].performed += OnSave;
        _inputActionAsset["Load"].performed += OnLoad;

        // 入力を受け付けるようにする
        _inputActionAsset.Enable();
    }

    // 後処理
    private void OnDestroy()
    {
        if (_inputActionAsset != null)
            Destroy(_inputActionAsset);
    }

    // 保存Action
    private void OnSave(InputAction.CallbackContext context)
    {
        Debug.Log("JSON保存");

        // Input Action Assetの内容をJSONに保存
        _json = _inputActionAsset.ToJson();
    }

    // 読み込みAction
    private void OnLoad(InputAction.CallbackContext context)
    {
        Debug.Log("JSONロード");

        // 念のため空チェック
        if (string.IsNullOrEmpty(_json))
            return;

        // 登録済みのコールバックを登録解除
        _inputActionAsset["Save"].performed -= OnSave;
        _inputActionAsset["Load"].performed -= OnLoad;

        // JSONを既存のInputActionAssetインスタンスに反映
        _inputActionAsset.LoadFromJson(_json);

        // コールバック再登録
        _inputActionAsset["Save"].performed += OnSave;
        _inputActionAsset["Load"].performed += OnLoad;

        // 読み込み後はInputActionAssetを有効化する必要がある
        _inputActionAsset.Enable();
    }
}
Aキーが押されたら保存、Bキーが押されたらロードする処理になっています。

保存場所はインスペクターから参照できる変数に格納するようにしているため、ロード前にここを編集するとキーアサインを自由に変更できます。

実行結果
Aキーを押すと、インスペクターのJson項目にシリアライズされたJSONが出力されるようになります。




この時、Jsonの内容を編集してからBキーを押すとインスペクターで編集されたJSONが読み込まれて適用されます。

上記動画では、保存のAキーをCキーに変更してからロードさせる挙動を実演しています。

スクリプトの説明
保存キーが押されたときは、以下処理でJSONにシリアライズしています。

// Input Action Assetの内容をJSONに保存
_json = _inputActionAsset.ToJson();
ロードキーが押されたときに、JSONからデシリアライズして読み込む処理は以下部分です。

// 登録済みのコールバックを登録解除
_inputActionAsset["Save"].performed -= OnSave;
_inputActionAsset["Load"].performed -= OnLoad;

// JSONを既存のInputActionAssetインスタンスに反映
_inputActionAsset.LoadFromJson(_json);

// コールバック再登録
_inputActionAsset["Save"].performed += OnSave;
_inputActionAsset["Load"].performed += OnLoad;
インスタンス破棄前にコールバックの登録を解除し、その後にLoadFromJsonメソッドでJSONからのロードを行っています。

この後、各種コールバックの再登録を行います。

ロード後はそのままではActionが無効化されてキー入力を受け取れない状態のため、以下で有効化する必要があります。

// 読み込み後はInputActionAssetを有効化する必要がある
_inputActionAsset.Enable();
Input Action Assetの実態
Unityプロジェクト等で保存されているInput Action Asset（拡張子が.inputactionsのファイル）も中身はJSONとして管理されています。

{
    "name": "AddCompositeBindingExample",
    "maps": [
        {
            "name": "UI",
            "id": "6af07cd4-5bde-4e92-9751-4c99d4ed17e1",
            "actions": [
                {
                    "name": "W",
                    "type": "Button",
                    "id": "64b88232-ab9e-42e2-9233-902b5fded87f",
                    "expectedControlType": "Button",
                    "processors": "",
                    "interactions": "",
                    "initialStateCheck": false
                },
                {
                    "name": "S",
                    "type": "Button",
                    "id": "8f21bdef-4db6-4583-b649-fdf07464ee36",
                    "expectedControlType": "Button",
                    "processors": "",
                    "interactions": "",
                    "initialStateCheck": false
                },

・・・（以下省略）・・・
InputActionAsset.ToJsonメソッドが出力するJSONと同じ構造です。

Actionの一部を上書きする
ここまでInput ActionやInput Action Assetに対してスクリプトから編集する方法を解説してきました。

しかしながら、キーコンフィグやマウス感度調整などの機能を実装する場合は「上書き」を使って内容を編集する方法が適しています。

理由は次のような特徴を備えているためです。

上書き機能の特徴
既存のAction内容とは別に「上書き」情報として管理される
上書き内容をセーブ・ロードする専用メソッドが存在する
これらの操作用メソッドは、InputActionRebindingExtensionsクラスのメソッド群として提供されています。

参考：Class InputActionRebindingExtensions| Input System | 1.5.1

Bindingの上書き
指定されたActionのControl PathやInteraction、Processorなどを上書きしたい場合、次のようなにInputActionに対してApplyBindingOverrideメソッドを実行します。

// 元はスペースキーで反応するAction
InputAction action = new InputAction(
    "Jump",
    InputActionType.Button,
    "<Keyboard>/Space"
);

・・・（中略）・・・

// Aキーで反応するように設定を上書き
action.ApplyBindingOverride("<Keyboard>/A");

// InputBindingで上書き指定することも可能
// InteractionやProcessorも一緒に上書きできる
action.ApplyBindingOverride(new InputBinding
{
    overridePath = "<Keyboard>/B",
    overrideInteractions = "hold",
    overrideProcessors = "scale(factor=3)"
});
InputBindingインスタンス指定で上書き内容を指定する場合は、次のフィールドに内容を格納することに注意してください。

Control Path – overridePath（pathではない）
Interaction – overrideInteractions（interactionsではない）
Processor – overrideProcessors（processorsではない）
参考：Class InputActionRebindingExtensions| Input System | 1.5.1

サンプルスクリプト
以下、指定された名前のActionを上書きするサンプルです。

OverrideExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class OverrideExample : MonoBehaviour
{
    // UnityプロジェクトのInput Action Assetを指定しておく
    [SerializeField] private InputActionAsset _inputActionAsset;
    
    // 上書き対象のAction名
    [SerializeField] private string _targetActionName = "Jump";

    private InputAction _targetAction;

    // 初期化
    private void Awake()
    {
        // Nullチェック
        if (_inputActionAsset == null)
            return;

        // 指定された名前のAction取得
        _targetAction = _inputActionAsset.FindAction(_targetActionName);
        if (_targetAction == null)
            return;

        // Actionの内容を上書き
        _targetAction.ApplyBindingOverride(new InputBinding
        {
            overridePath = "<Keyboard>/B", // Bキーに変更
            overrideInteractions = "hold", // 長押しInteraction付加
            overrideProcessors = "scale(factor=3)", // スケールを3倍にするProcessor付加
        });

        // コールバック登録
        _targetAction.performed += OnJump;

        // 入力受け付けを有効化
        _inputActionAsset.Enable();
    }

    // 後処理
    private void OnDestroy()
    {
        if (_targetAction != null)
        {
            // Actionの破棄
            _targetAction.performed -= OnJump;
            _targetAction.Dispose();
        }
    }

    // performedコールバック
    private void OnJump(InputAction.CallbackContext context)
    {
        // 入力値をログ出力
        Debug.Log($"Jump : {context.ReadValue<float>()}");
    }
}
上記を使いたい場合は、OverrideExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターより必要項目を設定してください。

Input Action Asset項目にUnityプロジェクトで管理されているアセットへの参照、Target Nameに上書き操作したいAction名を設定します。

例では以下のようなInput Action AssetとAction名を設定することとします。




<img src="images/11/11_1/unity-input-system-actions-runtime-17.png.avif" width="70%" alt="" title="">

<br>


<img src="images/11/11_1/unity-input-system-actions-runtime-18.png.avif" width="70%" alt="" title="">

<br>

検証のため、Input Action Assetの該当Actionには、Interactionにはダブルタップを表すMulti Tap Interactionを追加しています。

実行結果
Control PathがBキーに変更され、長押しInteractionが追加されていることが確認できました。また、Scale Processorの追加により入力値が3倍されています。



上書き前ではMulti Tap Interactionが追加されていましたが、こちらも機能しています。なお、上書き前のControl Pathは反応しなくなっています。

スクリプトの説明
これまでの例ではスクリプトからInput Action Assetインスタンスを生成するコードを示していましたが、今回はインスペクターから予め指定する方法を取っています。

// UnityプロジェクトのInput Action Assetを指定しておく
[SerializeField] private InputActionAsset _inputActionAsset;
Actionに対する上書き処理は、以下部分で行っています。

// Actionの内容を上書き
_targetAction.ApplyBindingOverride(new InputBinding
{
    overridePath = "<Keyboard>/B", // Bキーに変更
    overrideInteractions = "hold", // 長押しInteraction付加
    overrideProcessors = "scale(factor=3)", // スケールを3倍にするProcessor付加
});
Control Pathを変更し、InteractionとProcessorを追加しています。既存のものは削除されません。

上書き内容のセーブ・ロード
上書きしたBindingの内容をキーコンフィグなどとしてセーブ・ロードできるようにしたい場合は、専用のメソッドを使います。

こちらは、上書き内容のみをJSONとしてシリアライズ・デシリアライズする機能です。



<img src="images/11/11_1/unity-input-system-actions-runtime-19.png.avif" width="70%" alt="" title="">

<br>

上書き内容をJSONとして取得するにはSaveBindingOverridesAsJson拡張メソッドを使用します。

// 上書き対象Action
InputAction jumpAction = new InputAction("Jump");

・・・（中略）・・・

// 上書き内容をJSONとして抽出
string json = jumpAction.SaveBindingOverridesAsJson();
参考：Class InputActionRebindingExtensions| Input System | 1.5.1

逆に上書き情報のJSONをActionに反映したい場合は、LoadBindingOverridesFromJson拡張メソッドを使います。

// 上書き内容が格納されたJSON
string json;

・・・（中略）・・・

// 上書き内容をJSONから反映
jumpAction.LoadBindingOverridesFromJson(json);
サンプルスクリプト
指定されたActionの上書き内容を読み書きするサンプルです。

OverrideJsonExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class OverrideJsonExample : MonoBehaviour
{
    // UnityプロジェクトのInput Action Assetを指定しておく
    [SerializeField] private InputActionAsset _inputActionAsset;

    // 上書き内容が保存されるJSON
    [SerializeField, TextArea] private string _json;

    private InputAction _saveAction;
    private InputAction _loadAction;
    private InputAction _targetAction;

    // 初期化
    private void Awake()
    {
        // Nullチェック
        if (_inputActionAsset == null)
            return;

        // 「Save」という名前のAction取得
        _saveAction = _inputActionAsset.FindAction("Save");
        if (_saveAction == null)
            return;

        // 「Load」という名前のAction取得
        _loadAction = _inputActionAsset.FindAction("Load");
        if (_loadAction == null)
            return;

        // 「Target」という名前のAction取得
        _targetAction = _inputActionAsset.FindAction("Target");
        if (_targetAction == null)
            return;

        // Actionの内容を上書き
        _targetAction.ApplyBindingOverride(new InputBinding
        {
            overridePath = "<Keyboard>/A", // Aキーに変更
            overrideInteractions = "hold", // 長押しInteraction付加
            overrideProcessors = "scale(factor=3)", // 入力値を3倍にするProcessor付加
        });

        // コールバック登録
        _saveAction.performed += OnSave;
        _loadAction.performed += OnLoad;
        _targetAction.performed += OnTarget;

        // 入力受け付けを有効化
        _inputActionAsset.Enable();
    }

    // 後処理
    private void OnDestroy()
    {
        // 各Actionのコールバックの登録解除
        if (_saveAction != null)
            _saveAction.performed -= OnSave;
        if (_loadAction != null)
            _loadAction.performed -= OnLoad;
        if (_targetAction != null)
            _targetAction.performed -= OnTarget;
    }

    // 保存Action
    private void OnSave(InputAction.CallbackContext context)
    {
        Debug.Log("JSON保存");

        // 上書き内容をJSONとして保存
        _json = _targetAction.SaveBindingOverridesAsJson();
    }

    // 読み込みAction
    private void OnLoad(InputAction.CallbackContext context)
    {
        Debug.Log("JSONロード");

        if (string.IsNullOrEmpty(_json))
            return;

        // 上書き内容をJSONからロード
        _targetAction.LoadBindingOverridesFromJson(_json);
    }

    // 上書き対象Action
    private void OnTarget(InputAction.CallbackContext context)
    {
        Debug.Log("上書き対象Actionが実行された！");
    }
}
「Target」という名前のActionに対して内容の上書きを行います。





<img src="images/11/11_1/unity-input-system-actions-runtime-20.png.avif" width="70%" alt="" title="">

<br>

上記をOverrideJsonExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチした後、次のような名前を含むActionを定義したInput Action Assetを作成します。


<img src="images/11/11_1/unity-input-system-actions-runtime-21.png.avif" width="70%" alt="" title="">

<br>


その後、インスペクターより上記Input Action Assetをセットすると機能するようになります。


<img src="images/11/11_1/unity-input-system-actions-runtime-22.png.avif" width="70%" alt="" title="">

<br>


注意
上記の通りの設定にしないとサンプルは正しく動作しませんのでご注意ください。

実行結果
対象のAction（名前がTarget）がAキーの長押しで反応するように設定が上書きされています。



その後、上書き内容をJSONとして保存し、上書き対象のActionキーをBに書き換えた後ロードさせています。

そのため、ロード後はBキー長押しで反応するようになっています。

スクリプトの説明
まず、デモを実行するのに必要なActionを名前で検索して取得しています。

// 「Save」という名前のAction取得
_saveAction = _inputActionAsset.FindAction("Save");
if (_saveAction == null)
    return;

// 「Load」という名前のAction取得
_loadAction = _inputActionAsset.FindAction("Load");
if (_loadAction == null)
    return;

// 「Target」という名前のAction取得
_targetAction = _inputActionAsset.FindAction("Target");
if (_targetAction == null)
    return;
検索に失敗したらnullが変えるので、その場合は続行不可として処理を中断しています。

以下処理で名前がTargetのActionに対して上書きを行っています。

// Actionの内容を上書き
_targetAction.ApplyBindingOverride(new InputBinding
{
    overridePath = "<Keyboard>/A", // Aキーに変更
    overrideInteractions = "hold", // 長押しInteraction付加
    overrideProcessors = "scale(factor=3)", // 入力値を3倍にするProcessor付加
});
Control PathをAキーに上書きし、Interactionを長押しに、Processorで入力値を3倍にする効果を付加しています。

保存キー（例では1キー）が押されたとき、以下処理でフィールドにJSONとして上書き内容を保存しています。

// 保存Action
private void OnSave(InputAction.CallbackContext context)
{
    Debug.Log("JSON保存");

    // 上書き内容をJSONとして保存
    _json = _targetAction.SaveBindingOverridesAsJson();
}
ロードキー（例では2キー）が押されたとき、保存された上書き内容をロードする処理は以下部分です。

// 読み込みAction
private void OnLoad(InputAction.CallbackContext context)
{
    Debug.Log("JSONロード");

    if (string.IsNullOrEmpty(_json))
        return;

    // 上書き内容をJSONからロード
    _targetAction.LoadBindingOverridesFromJson(_json);
}
Input Action自体のロードとは異なり、こちらは改めてActionを有効化する必要がありません。

参考：Class InputActionRebindingExtensions| Input System | 1.5.1

Input Action Asset自体のセーブ・ロードを実行したときの挙動
InputActionAssetインスタンスに対してToJsonメソッドで内容をシリアライズしたとき、上書き内容は無視されます。

検証用スクリプト
以下、Input Action AssetのActionに対して上書きした後、Input Action Assetと上書き内容をそれぞれJSONとして保存するスクリプトです。

OverrideToJsonExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class OverrideToJsonExample : MonoBehaviour
{
    private InputActionAsset _inputActionAsset;

    // Input Action AssetのJSON
    [SerializeField, TextArea(3, 100)] private string _json;

    // 上書き内容が保存されるJSON
    [SerializeField, TextArea] private string _jsonOverride;

    // 初期化
    private void Awake()
    {
        // Input Action Assetを作成
        _inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();

        // 「Player」というMapを追加
        var playerMap = _inputActionAsset.AddActionMap("Player");

        // 「Jump」というActionをPlayer Mapに追加
        var jumpAction = playerMap.AddAction(
            "Jump",
            InputActionType.Button,
            "<Keyboard>/A" // Aキーでジャンプ
        );
        
        // 「Jump」というActionのControl PathをBキーに上書き
        jumpAction.ApplyBindingOverride("<Keyboard>/B");
        
        // Input Action Assetの内容をJSONとして保存
        _json = _inputActionAsset.ToJson();
        
        // 上書き内容をJSONとして保存
        _jsonOverride = _inputActionAsset.SaveBindingOverridesAsJson();
    }

    // 後処理
    private void OnDestroy()
    {
        if (_inputActionAsset != null)
            Destroy(_inputActionAsset);
    }
}
例ではJumpというActionをAキーで反応するように定義し、その後Bキーに上書きしています。

実行結果
ToJsonメソッドでシリアライズされたJSONでは、上書き前のAキーが出力されています。

一方、SaveBindingOverridesAsJsonメソッドでシリアライズされた上書き内容のJSONでは、Bキーが出力されています。





<img src="images/11/11_1/unity-input-system-actions-runtime-23.png.avif" width="70%" alt="" title="">

<br>


それぞれの内容が排他的に出力されていることが確認できます。









