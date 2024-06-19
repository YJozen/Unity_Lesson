**InputSystem 2**


複数キー操作の合成
【Unity】Input SystemのComposite Bindingで入力値を合成する

プレイヤーをWASDキーや十字キーで移動させる際、4つのボタンに方向を割り当てて最終的に移動ベクトル（Vector2型の値など）を求めたいケースがあります。

これは、複数のBindingの入力を合成して一つの入力値にしたり、入力値の型を変換したりするComposite Bindingを用いると楽です。


他にも次のようなことが実現できます。

Composite Bindingで出来ること
キーボードの矢印キーやゲームパッドの十字ボタン入力を2軸入力に合成する
ゲームパッドのLRキーを1軸の入力値に合成する
ボタンの同時押しを判定する
独自のカスタム合成を実装する

## Composite Bindingの仕組み

Composite Bindingを用いることで、複数のBindingを合成して1つのBindingとして模倣することが出来ます。

<img src="images/9/9_0/unity-input-system-composite-binding-2.png.avif" width="50%" alt="" title="">

<br>



そのため、参照元からは１つのBindingのみが存在しているように見えます。 
Composite Bindingには、次のようなものが予め用意されています。

+ 1D axis – 2つのボタンを1軸の値にする
+ 2D vector – 4つのボタンを2次元ベクトルにする
+ 3D vector – 6つのボタンを3次元ベクトルにする
+ One Modifier – あるボタンが押されている間だけ、指定のBindingが入力されたことにする
+ Two Modifiers – ある2つのボタンが押されている間だけ、指定のBindingが入力されたことにする

上記だけでは物足りない場合、独自のComposite Bindingを実装して適用することも可能です。


## Composite Bindingの適用方法


ここからは、実際のActionにComposite Bindingを適用する方法を解説していきます。

例では、MoveというActionに対してWASDキーの4方向のComposite Bindingを適用するものとします。

Actionの定義方法はいくつかありますが、ここではInput Action Assetを新規作成し、PlayerというMapの下にMoveという名前のActionを作成します。





<img src="images/9/9_0/unity-input-system-composite-binding-3.png.avif" width="50%" alt="" title="">

<br>


次に、連続した2軸入力として受け取るため、Action TypeをValueにし、Control TypeをVector 2に設定します。



<img src="images/9/9_0/unity-input-system-composite-binding-4.png.avif" width="50%" alt="" title="">

<br>

Action Typeに設定するValueは、入力値が変化するたびに入力（performedコールバック）を通知する設定です。

Control Typeに設定するVector 2は、Action自体が受け付ける入力値の型を表します。2軸入力なのでVector 2を指定しています。



Actionを新規追加した場合は空のBindingが追加されるため、これを削除しておきます。そして、Actionの右の＋アイコンからAdd Up\Down\Left\Right Compositeを選択します。


<img src="images/9/9_0/unity-input-system-composite-binding-m3.mp4.gif" width="50%" alt="" title="">

<br>





そして、Composite Binding下のそれぞれの方向のBindingを選択し、Path項目をクリックし、該当のキーを指定します。

例では、ListenボタンをクリックしてからWASDなどのキーを入力して選択しています。

<img src="images/9/9_0/unity-input-system-composite-binding-m4.mp4.gif" width="50%" alt="" title="">

<br>


ここまで設定し終えたら、忘れずにSave AssetボタンをクリックしてInput Action Assetの内容を保存しておきます






Composite Bindingの入力を受け取るスクリプト
上記で設定した2軸のAction入力値を受け取ってログ出力する例です


```cs:GetMoveExample.cs

using UnityEngine;
using UnityEngine.InputSystem;

public class GetMoveExample : MonoBehaviour
{
    // 2軸入力を受け取る想定のAction
    [SerializeField] private InputActionReference _actionRef;

    private void Awake()
    {
        // 値が変化した瞬間をコールバックで取得する
        _actionRef.action.performed += OnMove;
        _actionRef.action.canceled += OnMove;
    }

    private void OnDestroy()
    {
        _actionRef.action.performed -= OnMove;
        _actionRef.action.canceled -= OnMove;

        _actionRef.action.Dispose();
    }

    private void OnEnable()
    {
        _actionRef.action.Enable();
    }

    private void OnDisable()
    {
        _actionRef.action.Disable();
    }

    private void OnMove(InputAction.CallbackContext context)
    {
        // 受け取った入力値をログ出力
        print(context.ReadValue<Vector2>());
    }
}

```




上記をGetMoveExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチします。

そして、インスペクターより前述のComposite Bindingを設定したActionを指定すると、入力値をログ出力するようになります。


<img src="images/9/9_0/unity-input-system-composite-binding-6.png.avif" width="50%" alt="" title="">

<br>

実行確認すると、Composite Bindingで設定した4方向ボタンを入力すると、入力値が変化した瞬間にコンソールにログ出力されます。

複数方向のボタンが同時に入力された場合は、その合算したベクトル値となります。

複数の方向ボタンが押されたときの挙動は、Composite BindingのMode項目から設定できます。



https://nekojara.city/unity-input-system-composite-binding


---
4.

