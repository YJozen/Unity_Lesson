**InputSystem 1**

##  1.「Action」をMapというアセットとして管理する

「Action」たちを管理しやすいようにMapという形をとる
![](images/5/unity-input-system-actions-1.png.avif "")

<br>

PlayerMap(Player階層)のMoveというActionを使って!などとスクリプトに指示する
![](images/5/unity-input-system-actions-2.png.avif "")

<br>

Actionの中には、どの入力デバイスを参照するかといったキーバインド情報（Binding）が格納されており、マウスやキーボードやGamepadなどをスクリプトで判別しなくても、Actionに設定されたデバイスからの入力を受け取ることができます。
![](images/5/unity-input-system-actions-3.png.avif "")


---
## 2.Input Actionsアセットを作成し、使ってみよう
メニューのAssets > Create > Input Actionsの順に選択
![](images/5/unity-input-system-actions-4.png.avif "")


GameInputsなど適当な名前をつけてInput Actionsアセットを作成

![](images/5/unity-input-system-actions-5.jpg.avif "")


作成したInput Actionsアセットをダブルクリックし、Input Actionsの編集ウィンドウを開く
![](images/5/unity-input-system-actions-6.jpg.avif "")


左上のActions Maps右の＋ボタンをクリックし、Action Map名(例として「Player」)を入力。
![](images/5/unity-input-system-actions-7.jpg.avif "")

例として、移動の「Action」として「Move」と、ジャンプの「Action」として「Jump」を設定していきます
![](images/5/unity-input-system-actions-8.jpg.avif "")


新しいActionの追加は、Actions右上の＋ボタンから行います。「Jump」を追加して下さい
![](images/5/unity-input-system-actions-9.jpg.avif "")


次は、作成したそれぞれの「Action」の挙動を設定です
例えば、移動操作なら「2軸の入力値」、ジャンプ操作なら「ボタンの押下状態」を知る必要があります
![](images/5/unity-input-system-actions-10_1.jpg.avif "")
+ Action - Actionの基本的な振る舞いを設定します。入力値の種類やスクリプトから扱う型などの設定があります。
+ Interactions - 長押しやダブルクリックなどの通知を設定します。
+ Processors - デッドゾーンや値の正規化、反転などの演算処理を設定します。

・移動操作の設定例  
Action > Action Type項目をValueに設定
Action > Control Type項目をVector2
![](images/5/unity-input-system-actions-10_2.png "")

・ジャンプ操作の設定例  
Action > Action Type項目はButton
![](images/5/unity-input-system-actions-11.jpg.avif "")

作成した「Action」にキーバインド情報を設定していきます
![](images/5/unity-input-system-actions-12.jpg.avif "")

BindingはActionの右にある＋アイコンから複数追加できます
![](images/5/unity-input-system-actions-13.jpg.avif "")

・移動操作の設定例
例として、ゲームパッドの左スティック入力は、  
Binding Properties > Binding > Path項目にGamepad > LeftStickで設定  
もしくは、  
Path選択リストの左のListenボタンをクリックしてから実際にコントローラー入力をすると、該当するパスが即座に一覧出てくるので、それを選択
![](images/5/unity-input-system-actions-14_2.png "")

さらにキーボード入力も追加してみましょう  
Action右の＋アイコンからAdd Up\Down\Left\Right Compositeを選択
![](images/5/unity-input-system-actions-14_3.png "")

４方向それぞれに対して、パスを設定してください
![](images/5/unity-input-system-actions-14_4.png "")

・ジャンプ操作の設定例
ジャンプに関しても同じ要領です
![](images/5/unity-input-system-actions-14_5.png "")

※忘れずにSave Assetボタンをクリックして設定を保存(Auto-Saveにチェックでも可)  
![](images/5/unity-input-system-actions-15.jpg.avif "")

---
## 3.Input Actionsアセットの使用

試しに、シーン上に配置されたボールを操作できるようにしていきます
![](images/5/unity-input-system-actions-16.jpg.avif "")

Input Actionのソースコードを生成していきます。  
作成したInput Actionsアセットを選択し、Generate C# Classにチェックを入れます。  
すると、
+ 保存するスクリプトファイル名（C# Class File）
+ クラス名（C# Class Name）
+ 名前空間（C# Class Namespace）  
の設定項目が出現するため、必要に応じて設定し、Applyボタンをクリック。  
![](images/5/unity-input-system-actions-17.jpg.avif "")

保存に成功すると、指定したパスにスクリプトが追加されます。
![](images/5/unity-input-system-actions-18.jpg.avif "")



先述のInput Actionクラスから入力を取得し、ボールを操作するスクリプトを実装します。  
PlayerMover.csなどとスクリプトを作成し、ボールを動かしてみて下さい。

```cs:PlayerMover.cs
    using System;
    using UnityEngine;
    using UnityEngine.InputSystem;

    [RequireComponent(typeof(Rigidbody))]
    public class PlayerMover : MonoBehaviour
    {
        [SerializeField] private float _moveForce = 5;
        [SerializeField] private float _jumpForce = 5;

        private Rigidbody _rigidbody;
        private GameInputs _gameInputs;
        private Vector2 _moveInputValue;

        private void Awake()
        {
            _rigidbody = GetComponent<Rigidbody>();
     
            _gameInputs = new GameInputs();// Actionスクリプトのインスタンス生成

            // Actionイベント登録
            _gameInputs.Player.Move.started   += OnMove;
            _gameInputs.Player.Move.performed += OnMove;
            _gameInputs.Player.Move.canceled  += OnMove;
            _gameInputs.Player.Jump.performed += OnJump;

            // Input Actionを機能させるために、有効化
            _gameInputs.Enable();
        }

        private void OnDestroy()
        {
            // 自身でインスタンス化したActionクラスはIDisposableを実装しているので、
            // 必ずDisposeする必要がある
            _gameInputs?.Dispose();
        }

        private void OnMove(InputAction.CallbackContext context)
        {
            // Moveアクションの入力取得
            _moveInputValue = context.ReadValue<Vector2>();
        }

        private void OnJump(InputAction.CallbackContext context)
        {
            // ジャンプする力を与える
            _rigidbody.AddForce(Vector3.up * _jumpForce, ForceMode.Impulse);
        }

        private void FixedUpdate()
        {
            // 移動方向の力を与える
            _rigidbody.AddForce(new Vector3(
                _moveInputValue.x,
                0,
                _moveInputValue.y
            ) * _moveForce);
        }
    }
```



