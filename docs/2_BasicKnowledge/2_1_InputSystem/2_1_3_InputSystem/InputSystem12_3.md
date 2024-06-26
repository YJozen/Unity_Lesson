https://nekojara.city/unity-input-system-local-multiplayer


# Cinemachine使用下で画面分割する

ここまで、Cinemachineを使わない純粋なUnityカメラを用いて画面分割を行っていました。  
Cinemachineを使用した環境下でも画面分割は可能です。



## 複数カメラを独立制御させる仕組み

通常、Cinemachineはシーン上に配置されているすべてのバーチャルカメラから最も優先度の高いものを選択して制御します。  
カメラワークの制御はCinemachine Brainが担っています。

<img src="images/12/12_3/unity-cinemachine-multi-1.png.avif" width="80%" alt="" title="">

<br>

ただし、制御対象のバーチャルカメラは、カメラのCulling Maskで設定されている対象レイヤーのものに限ります。  
(Culling Mask：特定のゲームオブジェクトだけをカメラに映す)

例えば、カメラのCulling MaskにレイヤーP1が設定され、レイヤーP2が設定されていない場合、レイヤーP2のバーチャルカメラは制御の対象外となります。

<img src="images/12/12_3/unity-cinemachine-multi-2.png.avif" width="80%" alt="" title="">

<br>

ここにもう一つのカメラとCinemachine Brainを配置して、Culling MaskにレイヤーP1は設定せず、レイヤーP2を設定すると、こちらはレイヤーP1のバーチャルカメラが制御対象から除外されます。

<img src="images/12/12_3/unity-cinemachine-multi-3.png.avif" width="80%" alt="" title="">

<br>

この仕組みを利用して、Cinemachineで複数カメラを独立制御させます。


複数カメラの設定手順


Cinemachineカメラの設定  
まず、プレイヤーPrefab配下のカメラに`Cinemachine Brain`コンポーネントを追加します。



<img src="images/12/12_1/unity-input-system-local-multiplayer-m7.mp4.gif" width="90%" alt="" title="">

<br>




次に、プレイヤー用の`Cinemachineカメラ（バーチャルカメラ）`を配置します。

ヒエラルキー左上の＋アイコン > Cinemachine > Virtual Cameraより配置できます。


<img src="images/12/12_1/unity-input-system-local-multiplayer-m7.mp4.gif" width="90%" alt="" title="">

<br>


必要に応じて、カメラの追従設定を行います。

例では、FollowとLook At項目にプレイヤーオブジェクトを指定し、BodyにTransposerを指定し、Binding ModeにSimple Follow With World Upを指定して追従させることとします。

<img src="images/12/12_3/unity-input-system-local-multiplayer-17.png.avif" width="90%" alt="" title="">

<br>


## プレイヤー専用レイヤーの定義
各プレイヤー毎のレイヤーを追加します。

例では4人対戦ゲームを想定し、P0、P1、P2、P3の4レイヤーを追加することとします。

<img src="images/12/12_3/unity-input-system-local-multiplayer-18.png.avif" width="90%" alt="" title="">

<br>



プレイヤーインデックスに応じたレイヤーを設定するスクリプトの実装
プレイヤー入室時に割り当てられるプレイヤーインデックスに応じたレイヤーを設定するスクリプトを実装します。

スクリプトの実装例は以下のようになります。

```cs: PlayerCameraLayerUpdater.cs
using System;
using Cinemachine;
using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerCameraLayerUpdater : MonoBehaviour
{
    [SerializeField] private PlayerInput _playerInput;
    [SerializeField] private CinemachineVirtualCamera _cinemachineCamera;

    // プレイヤーインデックスとレイヤーの対応
    [Serializable]
    public struct PlayerLayer
    {
        public int index;
        public int layer;
    }

    [SerializeField] private PlayerLayer[] _playerLayers;

    private int _currentIndex = -1;

    // 初期化
    private void Awake()
    {
        if (_playerInput == null) return;

        // レイヤー更新
        OnIndexUpdated(_playerInput.user.index);
    }

    // 有効化
    private void OnEnable()
    {
        if (PlayerInputManager.instance == null) return;

        // プレイヤーが退室した時のイベントを監視する
        PlayerInputManager.instance.onPlayerLeft += OnPlayerLeft;
    }

    // 無効化
    private void OnDisable()
    {
        if (PlayerInputManager.instance == null) return;

        PlayerInputManager.instance.onPlayerLeft -= OnPlayerLeft;
    }

    // プレイヤーが退室した時に呼ばれる
    private void OnPlayerLeft(PlayerInput playerInput)
    {
        // 他プレイヤーが退室した時はインデックスがずれる可能性があるので
        // レイヤーを更新する
        if (playerInput.user.index >= _playerInput.user.index)
            return;

        // この時、まだインデックスは前のままなので-1する必要がある
        OnIndexUpdated(_playerInput.user.index - 1);
    }

    // プレイヤーインデックスが更新された時に呼ばれる
    private void OnIndexUpdated(int index)
    {
        if (_currentIndex == index) return;

        // インデックスに応じたレイヤー情報取得
        var layerIndex = Array.FindIndex(_playerLayers, x => x.index == index);
        if (layerIndex < 0) return;

        // プレイヤー用のカメラ取得
        var playerCamera = _playerInput.camera;
        if (playerCamera == null) return;

        // カメラのCullingMaskを変更
        // 自身のレイヤーは表示、他プレイヤーのレイヤーは非表示にする
        for (var i = 0; i < _playerLayers.Length; i++)
        {
            var layer = 1 << _playerLayers[i].layer;

            if (i == index)
                playerCamera.cullingMask |= layer;
            else
                playerCamera.cullingMask &= ~layer;
        }

        // Cinemachineカメラのレイヤー変更
        _cinemachineCamera.gameObject.layer = _playerLayers[layerIndex].layer;

        _currentIndex = index;
    }
}
```

上記をPlayerCameraLayerUpdater.csとしてUnityプロジェクトに保存します。

スクリプトの適用
前述のスクリプトをプレイヤーPrefabにアタッチし、インスペクターよりPlayer InputとCinemachineカメラを設定します。

<img src="images/12/12_1/unity-input-system-local-multiplayer-m7.mp4.gif" width="90%" alt="" title="">

<br>


そして、各プレイヤーインデックスとレイヤーの対応テーブルを定義します


<img src="images/12/12_1/unity-input-system-local-multiplayer-m7.mp4.gif" width="90%" alt="" title="">

<br>


<img src="images/12/12_3/unity-input-system-local-multiplayer-19.png.avif" width="90%" alt="" title="">

<br>


例では、レイヤーP0、P1、P2、P3のインデックスがそれぞれ7、8、9、10であるため、上記の設定にしています。


レイヤー値は数値を直接入力する必要がありますが、構造体やProperty Drawerを自作すると選択式でレイヤー値を指定することも可能です。(https://nekojara.city/unity-layer-inspector)



Player Input Manager側のイベント通知設定
上記サンプルスクリプトでは、C#イベント経由で退室通知を受け取るため、Player Input ManagerコンポーネントのNotification Behaviour項目にはInvoke C Shard Eventsを指定してください。

実行結果  
ここまでの手順を成功させると、動画のようにCinemachineが適用された状態でも独立してカメラが制御されることが確認できます。



この時、プレイヤーのUnityカメラのCulling Maskには、自身のレイヤーが設定され、他プレイヤーのレイヤーが未設定になります。




<img src="images/12/12_3/unity-input-system-local-multiplayer-20.png.avif" width="90%" alt="" title="">

<br>

また、Cinemachineカメラのレイヤーには自身に対応するレイヤーが設定されます。


<img src="images/12/12_3/unity-input-system-local-multiplayer-21.png.avif" width="90%" alt="" title="">

<br>


スクリプトの解説
自身のプレイヤーインデックスが更新される時、次の処理でレイヤー情報とカメラの取得を行います。




```cs:
// インデックスに応じたレイヤー情報取得
var layerIndex = Array.FindIndex(_playerLayers, x => x.index == index);
if (layerIndex < 0) return;

// プレイヤー用のカメラ取得
var playerCamera = _playerInput.camera;
if (playerCamera == null) return;
```


次に、自身のカメラのCulling Maskを更新します。この時、他プレイヤーのレイヤーは除外する必要があります。


```cs:
// カメラのCullingMaskを変更
// 自身のレイヤーは表示、他プレイヤーのレイヤーは非表示にする
for (var i = 0; i < _playerLayers.Length; i++)
{
    var layer = 1 << _playerLayers[i].layer;

    if (i == index)
        playerCamera.cullingMask |= layer;
    else
        playerCamera.cullingMask &= ~layer;
}
```

そして、Cinemachineカメラのレイヤーを自身のものに設定します。

```cs:
// Cinemachineカメラのレイヤー変更
_cinemachineCamera.gameObject.layer = _playerLayers[layerIndex].layer;
```

ここまでの処理は、自身が入室した時に行うほか、他プレイヤーが退室した時もインデックスがずれる可能性があるため行います。


```cs:
// 初期化
private void Awake()
{
    if (_playerInput == null) return;

    // レイヤー更新
    OnIndexUpdated(_playerInput.user.index);
}
```



```cs:
// プレイヤーが退室した時に呼ばれる
private void OnPlayerLeft(PlayerInput playerInput)
{
    // 他プレイヤーが退室した時はインデックスがずれる可能性があるので
    // レイヤーを更新する
    if (playerInput.user.index >= _playerInput.user.index)
        return;

    // この時、まだインデックスは前のままなので-1する必要がある
    OnIndexUpdated(_playerInput.user.index - 1);
}
```








