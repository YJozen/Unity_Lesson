# Input Systemを使用し、キーボードとマウスの入力を検知する

## 1. キーボードのAキーが押されているかどうかを判定する例

適当なゲームオブジェクトにアタッチして実行確認してください。  
Aキーの押下状態がログ出力されます。

KeyboardExample.cs
```cs

using UnityEngine;
using UnityEngine.InputSystem;

public class KeyboardExample : MonoBehaviour
{
    private void Update()
    {
        var keyboardCurrent = Keyboard.current;// 現在のキーボード情報

        if (keyboardCurrent == null)// キーボード接続チェック // キーボードが接続されていないと // Keyboard.currentがnullになる  
        {            
            return;
        }
            
        var aKey = keyboardCurrent.aKey; // Aキーの入力状態取得

        if (aKey.wasPressedThisFrame) // Aキーが押された瞬間かどうか
        {
            Debug.Log("Aキーが押された！");
        }
            
        if (aKey.wasReleasedThisFrame) // Aキーが離された瞬間かどうか
        {
            Debug.Log("Aキーが離された！");
        }

        if (aKey.isPressed) // Aキーが押されているかどうか
        {
            Debug.Log("Aキーが押されている！");
        }
    }
}
```


[その他のキーの取得](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.5/api/UnityEngine.InputSystem.Keyboard.html "その他のキーの取得")



---

## 2. マウスのボタンとカーソル位置を取得してログ出力する例

適当なゲームオブジェクトにアタッチして実行確認してください。
左ボタンがクリックされたら、カーソル座標と共にメッセージ出力されます。

KeyboardExample.cs
```cs

using UnityEngine;
using UnityEngine.InputSystem;

public class KeyboardExample : MonoBehaviour
{
    private void Update()
    {
        var mouseCurrent = Mouse.current;// 現在のマウス情報

        if (mouseCurrent == null) // マウス接続チェック // マウスが接続されていないと // Mouse.currentがnullになる
        {      
            return;
        }
    
        var cursorPosition = mouseCurrent.position.ReadValue(); // マウスカーソル位置取得       
        var mouseLeftButton = mouseCurrent.leftButton;     // 左ボタンの入力状態取得
        
        if (mouseLeftButton.wasPressedThisFrame) // 左ボタンが押された瞬間かどうか
        {
            Debug.Log($"左ボタンが押された！ {cursorPosition}");
        }
        
        if (mouseLeftButton.wasReleasedThisFrame)// 左ボタンが離された瞬間かどうか
        {
            Debug.Log($"左ボタンが離された！{cursorPosition}");
        }
        
        if (mouseLeftButton.isPressed)// 左ボタンが押されているかどうか
        {
            Debug.Log($"左ボタンが押されている！{cursorPosition}");
        }
    }
}
```

[マウス情報について](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.5/api/UnityEngine.InputSystem.Mouse.html "その他、マウス情報について")


<br>
