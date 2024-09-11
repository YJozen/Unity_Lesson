# Input Actionをスクリプトから動的に編集する方法②



## Input Action Assetのセーブ・ロード
スクリプトなどで編集したInput Action Assetの内容はJSONにシリアライズしたり、逆にJSONからデシリアライズできます。

<img src="images/11/11_1/unity-input-system-actions-runtime-16.png.avif" width="70%" alt="" title="">

<br>

これにより、Input Action Assetをファイルなどから読み書き可能になります。

JSONへのシリアライズ（JSONへの変換）にはInputActionAsset.ToJsonメソッドを使います。
```cs:
InputActionAsset inputActionAsset = ScriptableObject.CreateInstance<InputActionAsset>();

・・・（中略）・・・

// JSONにシリアライズ
string json = inputActionAsset.ToJson();
```

JSONからのデシリアライズ（JSONからの読み込み）メソッドは、InputActionAsset.FromJson、InputActionAsset.LoadFromJsonメソッドの2種類があります。

InputActionAsset.FromJsonメソッドはJSONから新しいInputActionAssetインスタンスを生成します。
```cs:
// Input Action Assetの内容が格納されたJSON
string json;

・・・（中略）・・・

// JSONからインスタンス生成
InputActionAsset inputActionAsset = InputActionAsset.FromJson(json);

// ロード後は有効化する必要がある
inputActionAsset.Enable();
```


InputActionAsset.LoadFromJsonメソッドは既存のInputActionAssetインスタンスを使いまわして内容をロードします。

```cs:
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
```


JsonUtilityクラスを使用したJSONのシリアライズ・デシリアライズでは正しく動作しませんのでご注意ください。



## Input Action AssetをJSONとして読み書きするサンプルです。

```cs:JsonExample.cs
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
```

Aキーが押されたら保存、Bキーが押されたらロードする処理になっています。

保存場所はインスペクターから参照できる変数に格納するようにしているため、ロード前にここを編集するとキーアサインを自由に変更できます。

実行結果
Aキーを押すと、インスペクターのJson項目にシリアライズされたJSONが出力されるようになります。




この時、Jsonの内容を編集してからBキーを押すとインスペクターで編集されたJSONが読み込まれて適用されます。

上記動画では、保存のAキーをCキーに変更してからロードさせる挙動を実演しています。

スクリプトの説明
保存キーが押されたときは、以下処理でJSONにシリアライズしています。
```cs:
// Input Action Assetの内容をJSONに保存
_json = _inputActionAsset.ToJson();
```
ロードキーが押されたときに、JSONからデシリアライズして読み込む処理は以下部分です。

```cs:
// 登録済みのコールバックを登録解除
_inputActionAsset["Save"].performed -= OnSave;
_inputActionAsset["Load"].performed -= OnLoad;

// JSONを既存のInputActionAssetインスタンスに反映
_inputActionAsset.LoadFromJson(_json);

// コールバック再登録
_inputActionAsset["Save"].performed += OnSave;
_inputActionAsset["Load"].performed += OnLoad;
```


インスタンス破棄前にコールバックの登録を解除し、その後にLoadFromJsonメソッドでJSONからのロードを行っています。

この後、各種コールバックの再登録を行います。

ロード後はそのままではActionが無効化されてキー入力を受け取れない状態のため、以下で有効化する必要があります。

```cs:
// 読み込み後はInputActionAssetを有効化する必要がある
_inputActionAsset.Enable();
```


Input Action Assetの実態
Unityプロジェクト等で保存されているInput Action Asset（拡張子が.inputactionsのファイル）も中身はJSONとして管理されています。
```cs:
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
```
InputActionAsset.ToJsonメソッドが出力するJSONと同じ構造です。


## Actionの一部を上書きする
ここまでInput ActionやInput Action Assetに対してスクリプトから編集する方法を解説してきました。

しかしながら、キーコンフィグやマウス感度調整などの機能を実装する場合は「上書き」を使って内容を編集する方法が適しています。

理由は次のような特徴を備えているためです。

上書き機能の特徴
既存のAction内容とは別に「上書き」情報として管理される
上書き内容をセーブ・ロードする専用メソッドが存在する
これらの操作用メソッドは、InputActionRebindingExtensionsクラスのメソッド群として提供されています。


## Bindingの上書き
指定されたActionのControl PathやInteraction、Processorなどを上書きしたい場合、次のようなにInputActionに対してApplyBindingOverrideメソッドを実行します。
```cs:
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
```

InputBindingインスタンス指定で上書き内容を指定する場合は、次のフィールドに内容を格納することに注意してください。

Control Path – overridePath（pathではない）
Interaction – overrideInteractions（interactionsではない）
Processor – overrideProcessors（processorsではない）



サンプルスクリプト
以下、指定された名前のActionを上書きするサンプルです。
```cs:OverrideExample.cs
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
```

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

## スクリプトの説明
これまでの例ではスクリプトからInput Action Assetインスタンスを生成するコードを示していましたが、今回はインスペクターから予め指定する方法を取っています。

```cs:
// UnityプロジェクトのInput Action Assetを指定しておく
[SerializeField] private InputActionAsset _inputActionAsset;
```

Actionに対する上書き処理は、以下部分で行っています。

```cs:
// Actionの内容を上書き
_targetAction.ApplyBindingOverride(new InputBinding
{
    overridePath = "<Keyboard>/B", // Bキーに変更
    overrideInteractions = "hold", // 長押しInteraction付加
    overrideProcessors = "scale(factor=3)", // スケールを3倍にするProcessor付加
});
```

Control Pathを変更し、InteractionとProcessorを追加しています。既存のものは削除されません。

## 上書き内容のセーブ・ロード
上書きしたBindingの内容をキーコンフィグなどとしてセーブ・ロードできるようにしたい場合は、専用のメソッドを使います。

こちらは、上書き内容のみをJSONとしてシリアライズ・デシリアライズする機能です。

<img src="images/11/11_1/unity-input-system-actions-runtime-19.png.avif" width="70%" alt="" title="">

<br>

上書き内容をJSONとして取得するにはSaveBindingOverridesAsJson拡張メソッドを使用します。


```cs:
// 上書き対象Action
InputAction jumpAction = new InputAction("Jump");

・・・（中略）・・・

// 上書き内容をJSONとして抽出
string json = jumpAction.SaveBindingOverridesAsJson();
```


逆に上書き情報のJSONをActionに反映したい場合は、LoadBindingOverridesFromJson拡張メソッドを使います。

```cs:
// 上書き内容が格納されたJSON
string json;

・・・（中略）・・・

// 上書き内容をJSONから反映
jumpAction.LoadBindingOverridesFromJson(json);
```

## サンプルスクリプト
指定されたActionの上書き内容を読み書きするサンプルです。
```cs:OverrideJsonExample.cs
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
```

「Target」という名前のActionに対して内容の上書きを行います。

<img src="images/11/11_1/unity-input-system-actions-runtime-20.png.avif" width="70%" alt="" title="">

<br>

上記をOverrideJsonExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチした後、次のような名前を含むActionを定義したInput Action Assetを作成します。

<img src="images/11/11_1/unity-input-system-actions-runtime-21.png.avif" width="70%" alt="" title="">

<br>

その後、インスペクターより上記Input Action Assetをセットすると機能するようになります。


<img src="images/11/11_1/unity-input-system-actions-runtime-22.png.avif" width="70%" alt="" title="">

<br>

上記の通りの設定にしないとサンプルは正しく動作しませんのでご注意ください。

実行結果
対象のAction（名前がTarget）がAキーの長押しで反応するように設定が上書きされます。



その後、上書き内容をJSONとして保存し、上書き対象のActionキーをBに書き換えた後ロードさせています。

そのため、ロード後はBキー長押しで反応するようになっています。

## スクリプトの説明
まず、デモを実行するのに必要なActionを名前で検索して取得しています。
```cs:
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
```

検索に失敗したらnullが変えるので、その場合は続行不可として処理を中断しています。

以下処理で名前がTargetのActionに対して上書きを行っています。
```cs:
// Actionの内容を上書き
_targetAction.ApplyBindingOverride(new InputBinding
{
    overridePath = "<Keyboard>/A", // Aキーに変更
    overrideInteractions = "hold", // 長押しInteraction付加
    overrideProcessors = "scale(factor=3)", // 入力値を3倍にするProcessor付加
});
```
Control PathをAキーに上書きし、Interactionを長押しに、Processorで入力値を3倍にする効果を付加しています。

保存キー（例では1キー）が押されたとき、以下処理でフィールドにJSONとして上書き内容を保存しています。


```cs:
// 保存Action
private void OnSave(InputAction.CallbackContext context)
{
    Debug.Log("JSON保存");

    // 上書き内容をJSONとして保存
    _json = _targetAction.SaveBindingOverridesAsJson();
}
```

ロードキー（例では2キー）が押されたとき、保存された上書き内容をロードする処理は以下部分です。

```cs:
// 読み込みAction
private void OnLoad(InputAction.CallbackContext context)
{
    Debug.Log("JSONロード");

    if (string.IsNullOrEmpty(_json))
        return;

    // 上書き内容をJSONからロード
    _targetAction.LoadBindingOverridesFromJson(_json);
}
```
Input Action自体のロードとは異なり、こちらは改めてActionを有効化する必要がありません。


Input Action Asset自体のセーブ・ロードを実行したときの挙動
InputActionAssetインスタンスに対してToJsonメソッドで内容をシリアライズしたとき、上書き内容は無視されます。

検証用スクリプト
以下、Input Action AssetのActionに対して上書きした後、Input Action Assetと上書き内容をそれぞれJSONとして保存するスクリプトです。

```cs:OverrideToJsonExample.cs
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
```

例ではJumpというActionをAキーで反応するように定義し、その後Bキーに上書きしています。

実行結果
ToJsonメソッドでシリアライズされたJSONでは、上書き前のAキーが出力されています。

一方、SaveBindingOverridesAsJsonメソッドでシリアライズされた上書き内容のJSONでは、Bキーが出力されています。

<img src="images/11/11_1/unity-input-system-actions-runtime-23.png.avif" width="70%" alt="" title="">

<br>

それぞれの内容が排他的に出力されていることが確認できます。



# さいごに
Input Actionにはスクリプトから内容を変更するメソッドが公開されています。しかし、InteractionやProcessorの変更など一部制限がある操作もあります。

また、キーコンフィグなどの実装では上書き機能を用いると実装がスムーズです。

本記事では原理の解説に絞るため、キーコンフィグの具体的な実装方法は割愛させていただきました。これは別記事で改めて投稿させていただきます。





