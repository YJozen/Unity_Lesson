**InputSystem 2**

# 【Unity】Input Systemで同時押しを実現する

Input Systemを使用している環境で、ボタンの同時押しや押しながら操作などを実現する方法の紹介です。

このような操作は、Button with one modifierやButton with two modifiersを用いるとスマートに実現できます。

これらは、あるボタンが押されている間のみ入力値を返す振る舞いをします。




<img src="images/9/9_3/unity-input-system-modifier-1.png.avif" width="50%" alt="" title="">

<br>



# Button with one modifierの使い方
ある１つのボタンが押されている間だけ、あるBindingの入力値を返すComposite Bindingです。

Composite Bindingとは、複数の操作をまとめて一つのBindingとして扱うもので、ほかにもいくつか種類が存在します。

参考：Input Bindings | Input System | 1.2.0

Button with one modifierを用いると、次のような操作を実現できます。

+ ２ボタン同時押し
+ ドラッグ操作

具体的な実装例も紹介していきます。


# ２ボタン同時押しの実装例
マウスの左右ボタンの同時押しを実現する例です。

Input Action側の設定
該当するActionにButton with one modifierというComposite Bindingを追加して設定します。

Button with one modifierの追加は、Actionの右側の＋アイコンからAdd Binding With One Modifierを選択して行います。


<img src="images/9/9_3/unity-input-system-modifier-2.jpg.avif" width="50%" alt="" title="">

<br>


追加すると、次の２つのBindingが子階層に追加されます。

+ Modifier  
もう一方のBindingの入力値を取得するために押されている必要があるボタンのBinding
+ Binding  
Modifierのボタンが押されている間だけ入力値を返すBinding

設定までの流れは以下動画のようになります。

<img src="images/9/9_3/unity-input-system-modifier-m1.mp4.gif" width="50%" alt="" title="">

<br>

例では次の構成にしました。


<img src="images/9/9_3/unity-input-system-modifier-3.jpg.avif" width="50%" alt="" title="">

<br>

設定したら、Save Assetボタンをクリックして設定内容を保存します。


<img src="images/9/9_3/unity-input-system-modifier-4.jpg.avif" width="50%" alt="" title="">

<br>


MapとAction名の設定は重要です。この名前をもとにスクリプトなどがActionに対する入力取得を行いますので、間違いないようにしてください。名前が違うとコンパイルエラーや実行時エラーになる可能性があります。




入力を取得するスクリプト  
Actionの入力値をログ出力するサンプルスクリプトです。コード生成されたInput Actionクラスを参照することを前提としています。



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

注意  
Input Actionが生成するスクリプトのクラス名と、スクリプト側のInput Actionのクラス名が合っていないとコンパイルエラーとなりますのでご注意ください。

実行結果





<img src="images/9/9_3/unity-input-system-modifier-m2.mp4.gif" width="50%" alt="" title="">

<br>




# ドラッグ操作の実装例
マウスの左ボタンを押している間だけ移動量を返すようにする例です。

Input Action側の設定
Button with one modifierを使い、ActionとModifier、Bindingを次の設定にします。



 <table>
    <tr>
      <td>Action > Action Type</td>
      <td>Value</td>
    </tr>
    <tr>
      <td>Action > Control Type</td>
      <td>Vector 2</td>
    </tr>
    <tr>
      <td>Modifier</td>
      <td>Left Button [Mouse]</td>
    </tr>
    <tr>
      <td>Binding</td>
      <td>Delta [Mouse]</td>
    </tr>
 </table>



<img src="images/9/9_3/unity-input-system-modifier-m3.mp4.gif" width="50%" alt="" title="">

<br>

入力を取得するスクリプト
ドラッグActionの入力値をログ出力するサンプルです。



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


実行結果


<img src="images/9/9_3/unity-input-system-modifier-m4.mp4.gif" width="50%" alt="" title="">

<br>



# Button with two modifiersの使い方
ある２つのボタンが押されている間だけBindingの入力を返すComposite Bindingです。３つ同時押しや、マウスの左右ボタンでドラッグさせたい場合に役立ちます。

Bindingの追加は、Add Binding With Tow Modifiersから行います。


<img src="images/9/9_3/unity-input-system-modifier-5.jpg.avif" width="50%" alt="" title="">

<br>

追加すると、２つのModifierとBindingが追加されるため、それぞれ設定してください。

<img src="images/9/9_3/unity-input-system-modifier-6.jpg.avif" width="50%" alt="" title="">

<br>











