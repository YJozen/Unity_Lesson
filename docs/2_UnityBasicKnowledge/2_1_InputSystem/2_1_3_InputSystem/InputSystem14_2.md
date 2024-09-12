【Unity】UI操作をInput Systemのローカルマルチに対応させる
2024年4月12日

https://nekojara.city/unity-input-system-local-multiplayer-ui



複数コントローラーを接続したローカルマルチの環境で、UIを個別のコントローラーで操作する方法の解説記事です。

次のように、プレイヤー毎に割り当てられたゲームパッドなどでUIを選択したり決定したりする操作をさせることを想定します。

操作対象のUIは、例えば1P用、2P用で排他的に操作したり、共存させたりする事が可能です。

本記事では、このような複数プレイヤーによるUI操作をInput Systemで実現する方法を解説していきます。



前提条件
事前にInput Systemパッケージがインストールされ、有効化されているものとします。

ここまでの手順が分からない方は、以下記事を参考にセットアップを済ませてください。


【Unity】Input Systemの使い方入門
Unity公式の新しい入力システムパッケージInput Systemの入門者向け記事です。 本記事では、Input Systemパッケージのインストール方法から、最低限使えるようにするところまでを解説していきます。 また…
2021年11月29日
また、本記事ではUnity UIで構築されたUIに対してマルチプレイの操作を適用していくものとします。


UI操作の実現方法の概要
実際の手順に入る前に、ローカルマルチでUI操作を実現するための概要について触れておきます。

通常のUI操作ではEvent Systemコンポーネントを使用しますが、ローカルマルチの場合はMultiplayer Event Systemコンポーネントを使用します。

参考：Class MultiplayerEventSystem| Input System | 1.7.0

Multiplayer Event Systemコンポーネントはプレイヤーの分だけシーンに存在させます。


シングルプレイヤーの場合

複数プレイヤーの場合
Event Systemとセットで必要になるInput System UI Input Moduleコンポーネントもプレイヤー数だけ存在します。

Multiplayer Event Systemコンポーネントでは、各プレイヤー毎に操作対象のUIを割り当てることできます。これにより、例えば1P側が2P用のUIを操作しないように排他制御できます。

設定手順
ここから先は、実際にマルチプレイヤー操作を適用していく手順を解説していきます。

Event Systemの削除
もしシーン上にEventSystemオブジェクト（Event Systemコンポーネントがアタッチされているオブジェクト）があれば、それを削除します。

UIのイベント処理は、最終的にMultiplayer Event Systemコンポーネントが担います。

Multiplayer Event Systemの配置
各プレイヤー毎の入力に基づいたイベント処理を行うために、Multiplayer Event Systemコンポーネントをプレイヤー分だけシーンに配置していきます。

例では、1Pと2Pの2プレイヤーが存在することを想定して解説します。 [1]
まず、適当なゲームオブジェクトをシーンに配置します。ここでは「MultiplayerEventSystem_P1」とします。

作成したゲームオブジェクトにMultiplayer Event Systemコンポーネントを追加します。

インスペクターからMultiplayer Event Systemコンポーネントの「Add Default Input Modules」ボタンをクリックしてStandard Input Moduleコンポーネントを追加し、更にStandard Input Moduleコンポーネントの「Replace with InputSystemUIInputModule」ボタンをクリックしてInput System UI Input Moduleコンポーネントに置き換えます。

注意
「Add Default Input Modules」ボタンをクリックして追加しただけでは、Input System UI Input Moduleコンポーネントは追加されません。

この操作を忘れると、Input Systemを通じたUI操作が一切できなくなる（旧Inputを使用する挙動になる）のでご注意ください。


最終的に、次のようにMultiplayer Event SystemとInput System UI Input Moduleコンポーネントが追加されている状態になっていれば良いです。


Player Inputの設定
複数プレイヤーの入力を管理するために、Player Inputコンポーネントをシーンに配置します。これにより、各プレイヤーにデバイス [2] を割り当てることが出来るようになります。

参考：The PlayerInput component | Input System | 1.7.0

例では、先ほど作成したMultiplayerEventSystem_P1オブジェクトにアタッチすることとします。

インスペクターからPlayer InputコンポーネントのActions項目にUI操作に使用するInput Action Assetを指定します。

Input Action Assetは自作しても良いですが、例ではInput Systemデフォルトの定義ファイルを指定することとします。

プロジェクトウィンドウのPackages/Input System/InputSystem/Plugins/PlayerInputフォルダ配下のDefaultInputActionsをドラッグ＆ドロップで指定します。

また、Default Map項目をUIに設定します。

更に、UI Input Module項目に、前述のInput System UI Input Moduleコンポーネントを指定します。

これによって、Player Input側がどのMultiplayer Event Systemかを認識できるようになります。

参考：The PlayerInput component | Input System | 1.7.0

プレイヤー分のMultiplayer Event Systemの配置
ここまで解説したコンポーネントをプレイヤー分だけシーンに配置します。基本的にオブジェクトをコピーして配置するだけで問題ありません。

例では1つのゲームオブジェクトに必要なコンポーネントを全て追加しているため、それをコピーして「MultiplayerEventSystem_P2」と名付けることとします。

最終的に、以下のようにプレイヤー毎のオブジェクトが配置されている状態になっていればよいです。


最初の選択要素の設定
各プレイヤーのMultiplayer Event SystemコンポーネントのFirst Selected項目に、初期状態の選択要素を指定します。

UIの操作対象の指定
必要に応じて操作対象のUIのルートオブジェクトをPlayer Root項目に指定します。

メモ
Player Root項目が未指定の場合、全てのUI要素が操作対象となります。例では、1Pと2Pが互いのUIを操作できる状態になります。

コントローラーの準備
ここまで解説した手順で実際に複数プレイヤーで操作するために、予めプレイヤーの数だけのデバイスが接続された状態にしておく必要があります。

例では、キーボード＆マウス、ゲームパッドが接続された状態とします。

メモ
現在接続中のデバイスは、UnityトップメニューのWindow > Analysis > Input Debugger項目からInput Debugウィンドウを開き、その中のDevicesツリーから確認できます。


注意
プレイヤー分のデバイスが接続され、使用可能な状態にならないと本記事の例を正しく実行できないため、ご注意ください。

実行結果
プレイヤー毎に割り当てられたコントローラーでUIを独立して操作できるようになりました。

Multiplayer Event SystemコンポーネントのPlayer Root項目にプレイヤー毎のUIルートオブジェクトが設定されていることで、互いのUIが操作できないようになっています。

もし、一つのコントローラーで複数プレイヤーのUIを同時に動かせてしまう場合、プレイヤー分のデバイスが認識されていない可能性が高いため、デバイスの接続状態をInput Debugger等で確認してください。

動的にプレイヤーが追加される場合
プレイヤーの数が決まっておらず、後からプレイヤーが追加されるケースでの適用例です。

動的なプレイヤー管理には、通常はPlayer Input Managerコンポーネントを使います。これは、例えば入力があったコントローラーにプレイヤーを割り当てるといった挙動を実現します。

参考：The Player Input Manager component | Input System | 1.7.0


【Unity】Input Systemでローカルマルチを実装する
Input Systemでは、PCなどに複数のゲームパッドを繋いでゲームをプレイするローカルマルチプレイヤーに対応しています。 これは、Player InputおよびPlayer Input Managerコンポーネント…
2023年6月2日
ただし、実行時にMultiplayer Event SystemコンポーネントのFirst SelectedやPlayer Root項目の設定を行う必要があるため、スクリプトでの対処が必要になります。

Prefabの作成
前述のMultiplayer Event SystemコンポーネントがアタッチされたオブジェクトをPrefab化します。これは、後述する手順でプレイヤーを動的にシーンに配置するためです。

例では、「MultiplayerEventSystem_P1」オブジェクトをPrefab化して「MultiplayerEventSystem」と名前変更し、シーンに配置済みのものを全て削除することとします。

Player Input Managerの配置
シーンにPlayer Input Managerコンポーネントを配置します。例では、「PlayerInputManager」という名前のゲームオブジェクトを作成し、ここにコンポーネントを追加することとします。

そして、予め作成したプレイヤーのPrefabをPlayer Input ManagerコンポーネントのPrefab項目に指定します。

Multiplayer Event Systemを設定するためのスクリプト実装
プレイヤーが追加されたときにMultiplayer Event Systemを初期化するためのスクリプトを実装します。

以下実装例です。

LocalMultiUISetup.cs
```cs
using System;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.UI;

public class LocalMultiUISetup : MonoBehaviour
{
    [SerializeField] private PlayerInputManager _playerInputManager;

    // プレイヤー毎のUI情報
    [Serializable]
    private struct PlayerUIInfo
    {
        public GameObject playerRoot;
        public GameObject firstSelected;
    }

    [SerializeField] private PlayerUIInfo[] _playerUIInfo;

    // 入室イベントの登録・解除
    private void Awake() => _playerInputManager.onPlayerJoined += OnPlayerJoined;
    private void OnDestroy() => _playerInputManager.onPlayerJoined -= OnPlayerJoined;

    // プレイヤーが入室したときの処理
    private void OnPlayerJoined(PlayerInput playerInput)
    {
        // Multiplayer Event Systemを取得
        if (!playerInput.TryGetComponent(out MultiplayerEventSystem eventSystem))
        {
            // Multiplayer Event Systemがアタッチされていない場合は追加
            eventSystem = playerInput.gameObject.AddComponent<MultiplayerEventSystem>();
        }

        // プレイヤー情報を取得
        if (playerInput.playerIndex >= _playerUIInfo.Length)
        {
            Debug.LogError("割り当て可能なプレイヤー情報がありません。");
            return;
        }

        var playerUiInfo = _playerUIInfo[playerInput.playerIndex];

        // UI情報を設定
        eventSystem.playerRoot = playerUiInfo.playerRoot;
        eventSystem.firstSelectedGameObject = playerUiInfo.firstSelected;
    }
}
```
上記をLocalMultiUISetup.csという名前でUnityプロジェクトに保存します。

そして、適当なゲームオブジェクトにアタッチし、インスペクターから以下項目を設定してください。

Player Input Manager – 先ほど追加したPlayer Input Managerコンポーネントを指定
Player UI Info – プレイヤー毎のMultiplayer Event Systemに設定する項目
例では、PlayerInputManagerオブジェクトにそのまま追加して設定することとします。

実行結果
Multiplayer Event Systemオブジェクトが動的に追加された場合でも正しく操作可能になりました。

前述のサンプルスクリプトのPlayer UI Info項目に指定した内容がMultiplayer Event Systemに反映されていれば成功です。


スクリプトの説明
プレイヤー入室の検知は、以下コードで行っています。

// 入室イベントの登録・解除
private void Awake() => _playerInputManager.onPlayerJoined += OnPlayerJoined;
private void OnDestroy() => _playerInputManager.onPlayerJoined -= OnPlayerJoined;
PlayerInputManager.onPlayerJoinedイベントに対して購読および購読解除を行っています。

参考：Class PlayerInputManager| Input System | 1.7.0

イベントを受け取った際の実際の処理は以下部分です。

// プレイヤーが入室したときの処理
private void OnPlayerJoined(PlayerInput playerInput)
{
    // Multiplayer Event Systemを取得
    if (!playerInput.TryGetComponent(out MultiplayerEventSystem eventSystem))
    {
        // Multiplayer Event Systemがアタッチされていない場合は追加
        eventSystem = playerInput.gameObject.AddComponent<MultiplayerEventSystem>();
    }
引数には追加されたプレイヤーのPlayer Inputコンポーネントが渡されるため、Player Inputが属するゲームオブジェクトからMultiplayer Event Systemコンポーネントを取得し、無ければ追加しています。

また、PlayerInput.playerIndexプロパティから、追加されたプレイヤーの0始まりのインデックスが得られるため、範囲チェックしてから該当する初期化情報を決定しています。

// プレイヤー情報を取得
if (playerInput.playerIndex >= _playerUIInfo.Length)
{
    Debug.LogError("割り当て可能なプレイヤー情報がありません。");
    return;
}

var playerUiInfo = _playerUIInfo[playerInput.playerIndex];
参考：Class PlayerInput| Input System | 1.7.0

そして、実際にMultiplayer Event Systemに設定する処理は以下部分です。

// UI情報を設定
eventSystem.playerRoot = playerUiInfo.playerRoot;
eventSystem.firstSelectedGameObject = playerUiInfo.firstSelected;
さいごに
Input Systemを通じてUnity UIを複数コントローラーから独立して操作させるためには、Event SystemではなくMultiplayer Event Systemをプレイヤー毎に割り当てて設定する必要があります。

動的にプレイヤーを追加する場合は、Multiplayer Event Systemをランタイムで設定するためのスクリプトを実装することで実現可能です。

これを応用すれば、例えば複数の仮想カーソルを独立して操作させるといったことも可能です。