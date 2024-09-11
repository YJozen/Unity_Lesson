
<link rel="stylesheet" href="/sample.css">

# Input Actionをスクリプトから動的に編集する方法①

https://nekojara.city/unity-input-system-actions-runtime

+ [Actionを作成する](#actionを作成する)
+




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

本記事では、このようなInput Actionの内容をスクリプトから動的に作成・変更する方法を解説します。











<br>

# Actionの作成
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


```cs
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
```cs
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


<br>

# サンプルスクリプト


スクリプトから動的にActionを生成し、ボタン入力があったらログを出力するサンプル。

```cs
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

<img src="images/11/11_1/unity-input-system-actions-runtime-5.png.avif" width="70%" alt="" title="">


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
```cs
// Input Action Assetインスタンスを生成
InputActionAsset inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();
```

作成したInput Action Assetに対して、MapやActionを追加・削除・編集ができます。
```cs
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

CreateInputActionAssetExample.cs
```cs
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
```cs
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

```cs
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

```cs
InputAction inputAction;

・・・（中略）・・・

// スペースキーがPathのBindingを追加する
inputAction.AddBinding("<Keyboard>/Space");
```

<img src="images/11/11_1/unity-input-system-actions-runtime-10.png.avif" width="70%" alt="" title="">

<br>


これは、以下のようにいくつかオーバーロードされた拡張メソッドとして定義されています。
```cs
public static InputActionSetupExtensions.BindingSyntax AddBinding(
    this InputAction action,
    string path,
    string interactions = null,
    string processors = null,
    string groups = null
);
```

```cs
public static InputActionSetupExtensions.BindingSyntax AddBinding(
    this InputAction action,
    InputBinding binding = default(InputBinding)
);
```

```cs
public static InputActionSetupExtensions.BindingSyntax AddBinding(
    this InputAction action,
    InputControl control
);
```

InteractionやProcessorなども一緒に追加できます。

戻り値として、Bindingを編集するためのシンタックスが返されます。このシンタックスに対して様々な操作を施すことが可能です。

Composite Bindingの追加
ActionにはBindingのほかComposite Bindingも追加できます。次のようにAddCompositeBindingメソッドを呼び出す形で行います。

```cs
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

```cs
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

AddCompositeBindingExample.cs
```cs
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

# 実行結果
BキーのBindingがCキーに変更され、長押ししないと反応しないようになりました。また、入力値が2.5倍されています。


<br>

# Bindingを削除する
予め追加されたBindingを削除したい場合も、ChangeBindingメソッドなどで得られるシンタックスを使います。 [7]
Binding削除にはシンタックスのEraseメソッドを使います。

```cs
// Input Actionを生成する
InputAction action = new InputAction(
    "TestAction",
    InputActionType.Button,
    "<Keyboard>/0"
);

・・・（中略）・・・

// インデックス0のBindingを削除
action.ChangeBinding(0).Erase();
```

参考：Struct InputActionSetupExtensions.BindingSyntax| Input System | 1.5.1







