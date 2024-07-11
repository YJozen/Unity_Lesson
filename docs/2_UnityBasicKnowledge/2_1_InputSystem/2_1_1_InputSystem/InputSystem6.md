**InputSystem 1**

# 「PlayerInput」コンポーネントで「Action」のアセットを管理してスクリプトから操作しやすくする
## 1.Player Inputコンポーネント

Player Inputは、  
Input Systemの入力を「仲介」するコンポーネントで、「Action」の入力をスクリプト側に通知します

<img src="images/6/unity-input-system-player-input-1.png.avif" width="50%" alt="" title="">

<br>

---
## 2.Player Inputの利用

動かす対象をSphereとして書いていきます

<img src="images/6/unity-input-system-player-input-2.png" width="50%" alt="" title="">

<br>

動かす対象のオブジェクトにPlayer Inputコンポーネントをアタッチ  
アタッチすると、次のようなPlayer Inputプロパティがインスペクターに表示されます

<img src="images/6/unity-input-system-player-input-3.png" width="50%" alt="" title="">

<br>

Actions項目にInput Actionアセットを指定。
(Input ActionはCreate Actions…ボタンから新規作成することも可能)  
上の写真の中で特に重要な設定は「Actions」と「Behavior」です。

「Behavior」の設定によって参照元のスクリプトのコードが異なります。
後ほど、それぞれの設定における使い方について、例を示しながら解説していきます。

+ Actions  
Input Actionアセットを指定

+ Default Scheme  
デフォルトで使用するスキームを指定します。(どういったデバイスを使うか)  
`<Any>`が指定された場合は、使用するスキームが自動的に決定  
設定しておく必要がある。（種類の追加設定は左上のAll Control SchemesからAddして下さい）  

<img src="images/6/unity-input-system-player-input-4.jpg.avif" width="50%" alt="" title="">

<br>


+ Auto-Switch  
使用中のスキームが使用不可になったとき、別のスキームに切り替えるかどうかの設定

+ Defualt Map  
Input ActionアセットのAction　Mapsの箇所

+ UI Input Module  
UIをPlayer Input経由で操作させたい場合に使用

+ Camera  
プレイヤーに関連付けるカメラを指定します。複数プレイヤーの画面分割をするときに使います。

+ Behavior  
スクリプト側に通知する方法を次の４種類から指定
    - Send Messages - Component.SendMessageメソッドを使ってスクリプトに通知
    - Broadcast Messages - Component.BroadcastMessageメソッドを使ってスクリプトに通知
    - Invoke Unity Events - UnityEventを通じて通知します。
    - Invoke C Sharp Events - C#のデリゲートを通じて通知します。

---
## 3.Behavior  に　Send Messages／Broadcast Messagesを設定した場合

Moveアクションの通知を受け取って、オブジェクトを移動させるサンプルスクリプト

SendMessageExample.cs
```cs

using UnityEngine;
using UnityEngine.InputSystem;

public class SendMessageExample : MonoBehaviour
{
    private Vector3 _velocity;

    // 通知を受け取るメソッド名は「On + Action名」である必要がある
    private void OnMove(InputValue value)
    {
        // MoveActionの入力値を取得
        var axis = value.Get<Vector2>();

        // 移動速度を保持
        _velocity = new Vector3(axis.x, 0, axis.y);
    }

    private void Update()
    {
        // オブジェクト移動
        transform.position += _velocity * Time.deltaTime;
    }
}
```

上記スクリプトをSendMessageExample.csという名前で保存し、プレイヤーオブジェクトにアタッチします。

また、Player InputコンポーネントのBehaviorをSend MessagesまたはBroadcast Messagesに設定。

Send Messagesを設定した場合は、Player Inputがアタッチされているオブジェクトにアタッチする必要があります。

Broadcast Messagesを設定した場合は、Player Inputがアタッチされているオブジェクトまたはその子オブジェクトにアタッチする必要があります。

---
Player Inputから通知を受け取るためには、「On + Action名」という名前のメソッドを定義する必要があります。

---
## 4.Invoke Unity Eventsを設定した場合

UnityEventExample.cs
```cs
    using UnityEngine;
    using UnityEngine.InputSystem;

    public class UnityEventExample : MonoBehaviour
    {
        private Vector3 _velocity;

        // 先ほどと違いメソッド名は何でもOKだが、 publicにする必要がある
        // Events項目が出現するため、該当するイベントの＋ボタンより通知を受け取るスクリプトのメソッドを指定
        public void OnMove(InputAction.CallbackContext context)
        {
            // MoveActionの入力値を取得
            var axis = context.ReadValue<Vector2>();

            // 移動速度を保持
            _velocity = new Vector3(axis.x, 0, axis.y);
        }

        private void Update()
        {
            // オブジェクト移動
            transform.position += _velocity * Time.deltaTime;
        }
    }

```
Events項目が出現するため、該当するイベントの＋ボタンより通知を受け取るスクリプトのメソッドを指定して下さい

---
## 5.Invoke C Sharp Eventsを設定した場合


+ 書き方１ -  onActionTriggeredを使用する方法  

Input System全体でトリガーされるすべてのアクションをキャッチするための方法です。すべてのアクションを一つのコールバックで処理したい場合に便利

CSharpEventExample.cs
```cs

    using UnityEngine;
    using UnityEngine.InputSystem;

    [RequireComponent(typeof(PlayerInput))]
    public class CSharpEventExample : MonoBehaviour
    {
        private PlayerInput _playerInput;
        private Vector3 _velocity;

        private void Awake()
        {
            _playerInput = GetComponent<PlayerInput>();
        }

        private void OnEnable()
        {
            if (_playerInput == null) return;

            // デリゲート登録  onActionTriggeredプロパティに追加
            _playerInput.onActionTriggered += OnMove;
        }
        private void OnDisable()
        {
            if (_playerInput == null) return;

            // デリゲート登録解除
            _playerInput.onActionTriggered -= OnMove;
        }


        private void OnMove(InputAction.CallbackContext context)
        {
            // Move以外は処理しない
            if (context.action.name != "Move")
                return;

            // MoveActionの入力値を取得
            var axis = context.ReadValue<Vector2>();

            // 移動速度を保持
            _velocity = new Vector3(axis.x, 0, axis.y);
        }


        private void Update()
        {
            // オブジェクト移動
            transform.position += _velocity * Time.deltaTime;
        }
    }
```


+ 書き方2 - アクションごとにコールバックを設定する方法

特定のアクションに対して直接コールバックを設定

```cs
    using UnityEngine;
    using UnityEngine.InputSystem;

    public class InputHandler : MonoBehaviour
    {
        PlayerInput playerInput 
        InputAction jumpAction;

        private void Awake()
        {
            playerInput = GetComponent<PlayerInput>();
            jumpAction  = playerInput.actions["Jump"];
            jumpAction.performed += OnJump;
        }

        private void OnDestroy()
        {
            jumpAction.performed -= OnJump;
        }

        private void OnJump(InputAction.CallbackContext context)
        {
            // ジャンプアクションがトリガーされたときの処理
        }
    }

```
