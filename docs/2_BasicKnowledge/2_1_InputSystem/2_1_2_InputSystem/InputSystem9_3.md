**InputSystem 2**

# 【Unity】Input Systemで同時押しを実現する

ボタンの同時押しや押しながら操作。このような操作は、Button with one modifierやButton with two modifiersを用いると良いかと思います。

これらは、あるボタンが押されている間のみ入力値を返します。

<img src="images/9/9_3/unity-input-system-modifier-1.png.avif" width="70%" alt="" title="">

<br>

# Button with one modifierの使い方
ある１つのボタンが押されている間だけ、あるBindingの入力値を返すComposite Bindingです。(Composite Bindingとは、複数の操作をまとめて一つのBindingとして扱うものです。)

Button with one modifierを用いて、下記の具体的な実装例を見ていきます。

+ ２ボタン同時押し
+ ドラッグ操作


## ・２ボタン同時押しの実装例
マウスの左右ボタンの同時押しを実現する例です。

該当するActionの右側の＋アイコンから、Button with one modifierを選択して、Composite Bindingを追加します。

<img src="images/9/9_3/unity-input-system-modifier-2.jpg.avif" width="90%" alt="" title="">

<br>

追加すると、次の２つのBindingが子階層に追加されます。

  + Modifier  
  もう一方のBindingの入力値を取得するために、押されている必要があるボタンのBinding
  + Binding  
  Modifierのボタンが押されている間だけ入力値を返すBinding

<img src="images/9/9_3/unity-input-system-modifier-m1.mp4.gif" width="90%" alt="" title="">

<br>

例では次の構成にしました。

<img src="images/9/9_3/unity-input-system-modifier-3.jpg.avif" width="70%" alt="" title="">

<br>

設定したら、Save Assetボタンをクリックして設定内容を保存します。

<img src="images/9/9_3/unity-input-system-modifier-4.jpg.avif" width="50%" alt="" title="">

<br>

(MapとAction名の設定は重要です。この名前をもとにスクリプトなどがActionに対する入力取得を行いますので、間違いないようにしてください。名前が違うとコンパイルエラーや実行時エラーになる可能性があります。)

<br>

### 入力を取得するスクリプトの例  
Actionの入力値をログ出力するサンプルスクリプトです。コード生成されたInput Actionクラスを参照することを前提としたものになります。
`PressTwoButtons`というクラス名は、各々作成したコード由来のクラス名に変更し、使用して下さい


```cs:PressTwoButtonsExample.cs

using UnityEngine;
using UnityEngine.InputSystem;

public class PressTwoButtonsExample : MonoBehaviour
{
    private PressTwoButtons _inputActions;
    
    private void Awake()
    {
        // Input Actionの初期化
        _inputActions = new PressTwoButtons();
        _inputActions.Player.LeftRight.performed += OnLeftRight;
        _inputActions.Enable();
    }

    private void OnLeftRight(InputAction.CallbackContext context)
    {
        print("左右ボタンが同時に押された！");
    }
}
```
このスクリプトをPressTwoButtonsExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチすると動きます。

(Input Actionが生成するスクリプトのクラス名と、スクリプト側のInput Actionのクラス名が合っていないとコンパイルエラーとなりますので注意してください。)

実行結果

<img src="images/9/9_3/unity-input-system-modifier-m2.mp4.gif" width="90%" alt="" title="">

<br>

## ・ドラッグ操作の実装例
マウスの左ボタンを押している間だけ移動量を返すようにする例です。  
Button with one modifierを使い、ActionとModifier、Bindingを次の設定にします。

 <table>
    <tr>
      <td><b>Action > Action Type</b></td>
      <td>Value</td>
    </tr>
    <tr>
      <td><b>Action > Control Type</b></td>
      <td>Vector 2</td>
    </tr>
    <tr>
      <td><b>Modifier</b></td>
      <td>Left Button [Mouse]</td>
    </tr>
    <tr>
      <td><b>Binding</b></td>
      <td>Delta [Mouse]</td>
    </tr>
 </table>

<img src="images/9/9_3/unity-input-system-modifier-m3.mp4.gif" width="90%" alt="" title="">

<br>

### 入力を取得するスクリプトの例
ドラッグActionの入力値をログ出力。
先ほどと同様、変数_inputActionsのクラス名は、自分で生成したInputActionAssetのコードのクラス名に変更して下さい。

```cs:MouseDragExample.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class MouseDragExample : MonoBehaviour
{
    private MouseDrag _inputActions;

    private void Awake()
    {
        // Input Actionの初期化
        _inputActions = new MouseDrag();
        _inputActions.UI.Drag.performed += OnDrag;
        _inputActions.Enable();
    }

    private void OnDrag(InputAction.CallbackContext context)
    {
        // マウスドラッグの移動量取得
        var dragValue = context.ReadValue<Vector2>();

        print($"マウスドラッグ : {dragValue}");
    }
}
```

<img src="images/9/9_3/unity-input-system-modifier-m4.mp4.gif" width="90%" alt="" title="">

<br>



# Button with two modifiersの使い方
ある２つのボタンが押されている間だけBindingの入力を返すComposite Bindingです。  
３つ同時押しや、マウスの左右ボタンでドラッグさせたい場合に役立ちます。

Bindingの追加は、Add Binding With Tow Modifiersから行います。

<img src="images/9/9_3/unity-input-system-modifier-5.jpg.avif" width="70%" alt="" title="">

<br>

追加すると、２つのModifierとBindingが追加されるため、それぞれ設定してください。

<img src="images/9/9_3/unity-input-system-modifier-6.jpg.avif" width="70%" alt="" title="">

<br>











