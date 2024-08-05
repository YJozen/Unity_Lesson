**InputSystem 2**

# 【Unity】Input SystemのComposite Bindingで入力値を合成する

プレイヤーをWASDキーや十字キーで移動させる際、4つのボタンに方向を割り当てて最終的にスティックのような2軸入力（Vector2型の値など）を求めたいケースがあります。

Composite Bindingを使うと、ベクトルに変換する処理をInput System側で行えるようになり、複数ボタン入力から移動方向を計算するコードを書かなくてもよくなります。


<img src="images/9/9_0/unity-input-system-composite-binding-2.png.avif" width="80%" alt="" title="">

<br>

参照元からは１つのBindingのみが存在しているように見えます。 
Composite Bindingには、次のようなものが予め用意されています。

+ 1D axis – 2つのボタンを1軸の値にする
+ 2D vector – 4つのボタンを2次元ベクトルにする
+ 3D vector – 6つのボタンを3次元ベクトルにする
+ One Modifier – あるボタンが押されている間だけ、指定のBindingが入力されたことにする
+ Two Modifiers – ある2つのボタンが押されている間だけ、指定のBindingが入力されたことにする

（上記だけでは物足りない場合、独自のComposite Bindingを実装して適用することも可能です。）


## Composite Bindingの適用方法

ActionにComposite Bindingを適用する方法を見ていきます。

例では、MoveというActionに対してWASDキーの4方向のComposite Bindingを適用します。

Actionの定義方法はいくつかありますが、ここではInput Action Assetを新規作成し、PlayerというMapの下にMoveという名前のActionを作成します。

<img src="images/9/9_0/unity-input-system-composite-binding-3.png.avif" width="80%" alt="" title="">

<br>

次に、連続した2軸入力として受け取るため、Action TypeをValueにし、Control TypeをVector 2に設定します。

<img src="images/9/9_0/unity-input-system-composite-binding-4.png.avif" width="80%" alt="" title="">

<br>

Action Typeに設定したValueは、入力値が変化するたびに入力（performedコールバック）を通知する設定です。

Control Typeに設定するVector 2は、Action自体が受け付ける入力値の型を表します。2軸入力なのでVector 2を指定しています。



Actionを新規追加した場合は、空のBindingが追加されるため、これを削除しておきます。そして、Actionの右の＋アイコンからAdd Up\Down\Left\Right Compositeを選択します。


<img src="images/9/9_0/unity-input-system-composite-binding-m3.mp4.gif" width="80%" alt="" title="">

<br>


次に、Composite Binding下のそれぞれの方向のBindingを選択し、Path項目をクリックし、該当のキーを指定します。

例では、ListenボタンをクリックしてからWASDなどのキーを入力して選択しています。

<img src="images/9/9_0/unity-input-system-composite-binding-m4.mp4.gif" width="80%" alt="" title="">

<br>


ここまで設定し終えたら、忘れずにSave AssetボタンをクリックしてInput Action Assetの内容を保存しておきます


## Composite Bindingの入力を受け取るスクリプト
上記で設定した2軸のAction入力値を受け取ってログ出力する例です

GetMoveExample.cs
```cs

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

そしてインスペクターにて、Actionを指定すると、入力値をログ出力するようになります。


<img src="images/9/9_0/unity-input-system-composite-binding-6.png.avif" width="80%" alt="" title="">

<br>

実行確認すると、Composite Bindingで設定した4方向ボタンを入力すると、入力値が変化した瞬間にコンソールにログ出力されます。  
複数方向のボタンが同時に入力された場合は、その合算したベクトル値となります。

複数の方向ボタンが押されたときの挙動は、Composite BindingのMode項目から設定できます。

<img src="images/9/9_0/unity-input-system-composite-binding-7.png.avif" width="80%" alt="" title="">

<br>


## スクリプトの説明  
Composite Bindingより得られた入力値を取得するために、次のようにperformed、canceledコールバックに登録しています。

```cs
private void Awake()
{
    // 値が変化した瞬間をコールバックで取得する
    _actionRef.action.performed += OnMove;
    _actionRef.action.canceled += OnMove;
}
```

これにより、入力値が変化した瞬間にOnMoveメソッドが呼ばれるようになります。

OnMoveメソッドでは、次のように引数contextに対してReadValue<Vector2>メソッドを呼び出すことで2軸入力値を取得してログ出力しています。

```cs
private void OnMove(InputAction.CallbackContext context)
{
    // 受け取った入力値をログ出力
    print(context.ReadValue<Vector2>());
}
```


## 各Composite Bindingの説明
既に提供されているComposite Bindingについて紹介します。

#### ・1D axis
プラス方向とマイナス方向の2入力から1軸入力に合成するComposite Binding。

該当ActionのControl TypeがAxisなどの1軸入力型の場合に使用可能になります。

<img src="images/9/9_0/unity-input-system-composite-binding-8.png.avif" width="80%" alt="" title="">

<br>

Action右の＋アイコンよりAdd Positive\Negative Bindingを選択すると追加されます。

<img src="images/9/9_0/unity-input-system-composite-binding-9.png.avif" width="80%" alt="" title="">

<br>


設定項目について。
+ Min Value – 取り得る入力の最小値。
+ Max Value – 取り得る入力の最大値。
+ Which Side Wins – ボタンが同時に押された時に、どちら側の入力値を使うかどうか。
+ Neither – 0を返す。
+ Positive – プラス方向の入力値を返す。
+ Negative – マイナス方向の入力値を返す。


<img src="images/9/9_0/unity-input-system-composite-binding-10.png.avif" width="80%" alt="" title="">

<br>


#### ・2D vector
上下左右の4入力を2軸入力に合成するComposite Binding。

Control TypeがVector 2の時に使用可能。

<img src="images/9/9_0/unity-input-system-composite-binding-11.png.avif" width="80%" alt="" title="">

<br>


追加は、Action右の＋アイコンから表示されるAdd Up\Down\Left\Right Bindingから行えます。

<img src="images/9/9_0/unity-input-system-composite-binding-12.png.avif" width="80%" alt="" title="">

<br>


設定項目について。
+ Mode – 4方向の入力値の処理方法を指定。
+ Analog – 各軸の入力値をそのまま加減算。
+ Ditigal Normalized – 入力値の大きさを1に正規化（ただし入力値が(0, 0)ならそのまま(0, 0)を返す）
+ Digital – 各軸単位で閾値Press Pointを基準に-1、0、1のどれかにスナップさせる。

<img src="images/9/9_0/unity-input-system-composite-binding-13.png.avif" width="80%" alt="" title="">

<br>



#### ・3D vector
上下左右前後の6入力を3軸入力に合成するComposite Binding。
Control TypeがVector 3の時に使用できます。


<img src="images/9/9_0/unity-input-system-composite-binding-14.png.avif" width="80%" alt="" title="">

<br>

追加は、該当Action右の＋アイコンからAdd Up\Down\Left\Right\Forward\Backward Compositeを選択することで行います。


<img src="images/9/9_0/unity-input-system-composite-binding-15.png.avif" width="80%" alt="" title="">

<br>

設定項目について。

+ Mode – 6方向の入力値の処理方法を指定。
+ Analog – 各軸の入力値をそのまま加減算。
+ Ditigal Normalized – 入力値の大きさを1に正規化（ただし入力値が(0, 0, 0)ならそのまま(0, 0, 0)を返す）
+ Digital – 各軸単位で閾値Press Pointを基準に-1、0、1のどれかにスナップさせる。


<img src="images/9/9_0/unity-input-system-composite-binding-16.png.avif" width="80%" alt="" title="">

<br>

#### ・One Modifier
あるボタン（Modifier）が押されている時だけ指定されたBindingの入力を流すComposite Bindingです。複数キーの同時押しによるショートカットキー操作や、ドラッグ操作などを実現できます。

このComposite Bindingは、Action TypeやControl Typeの設定によらず使用可能です。

追加は、Add Binding With One Modifierから行います。

<img src="images/9/9_0/unity-input-system-composite-binding-17.png.avif" width="80%" alt="" title="">

<br>

すると、次のようなBindingが追加されます。

<img src="images/9/9_0/unity-input-system-composite-binding-18.png.avif" width="80%" alt="" title="">

<br>

それぞれ次のような意味を持ちます。

+ Modifier – 修飾子となるボタン入力。このボタン入力がある間、もう一方のBinding側の値が流れる。
+ Binding – Modifierに指定されたボタンが押されている間に受け取る入力。
+ Composite Bindingの設定項目では、Override Modifiers Need To Be Pressed First項目の有効・無効を指定できます。


<img src="images/9/9_0/unity-input-system-composite-binding-19.png.avif" width="80%" alt="" title="">

<br>


これは、主にショートカットなどで用いられるボタン押下の順序によって押された判定にするかどうかを指定する項目です。

この項目のチェックが外れている場合（初期値）、その挙動は次のProject SettingsのInput System PackageのEnabled Input Consumption項目の挙動によって決まります。

<img src="images/9/9_0/unity-input-system-composite-binding-20.png.avif" width="80%" alt="" title="">

<br>


これは、ショートカットの修飾子（Ctrl、Shiftキーなど）を最初に押す必要があるかどうかの設定で、この項目にチェックが入っていると、Modifier→Bindingの順にボタンを押さないと入力が得られなくなります。

例えば「Ctrl」＋「C」などのショートカットで最初に「Ctrl」キーが押された時だけ反応し、逆に「C」から押された時は反応しないようにしたい場合に役立ちます。

チェックが付いていないと、どちらのキーから先に押されても反応するようになります。

この設定はアプリケーション全体に影響を及ぼすため、取り扱いには注意してください。

Override Modifiers Need To Be Pressed First項目にチェックが付いている場合は、Project Settings の Input System PackageのEnabled Input Consumption項目の設定にかかわらず、常にどちらのキーから先に押されても反応するようになります

<br>

#### ・Two Modifiers
ある2つのボタン（Modifier1、Modifier2）が押されている時だけ指定されたBindingの入力を流すComposite Binding。3ボタンの同時押しを実現したい場合に使えます。

追加はAdd Binding With Two Modfiersから行います

<img src="images/9/9_0/unity-input-system-composite-binding-21.png.avif" width="80%" alt="" title="">

<br>


追加すると、3つのBinding（Modifier1、Modifier2、Binding）が指定できます。

<img src="images/9/9_0/unity-input-system-composite-binding-22.png.avif" width="80%" alt="" title="">

<br>

Composite Bindingの設定項目は、One Modifierと同様Override Modifiers Need To Be Pressed Firstのみ。


<img src="images/9/9_0/unity-input-system-composite-binding-23.png.avif" width="80%" alt="" title="">

<br>


設定項目の意味と挙動もOne Modifierと一緒です

