# 【Unity】Input Systemの同時押しを排他制御する

<img src="images/9/9_4/unity-input-system-exclusive-modifier-1.png.avif" width="70%" alt="" title="">

<br>

例えばTabキーを使ったナビゲーションを実装するとき、Tabキー単体では「進む」操作になるが、Shift + Tabキーが押された場合は「戻る」操作となり、「進む」操作は実行されないようにしたい場合を想定します。

通常、Shift + Tabを同時押しするとTabキーが押された時点で「進む」と「戻る」の両方の操作が実行されるかと思います。 

これらを<b><u>排他制御(一度に一つのプロセスだけが、データを操作できるように制御)</u></b>する機能が追加されています。

排他制御の有効化設定は、アプリケーション全体に影響を及ぼすため、注意する必要があります。これが許容できない場合はComposite Bindingを自作する必要があります。

<br>

# 排他制御の設定方法

（アプリケーション全体のInput Actionに対して排他制御が適用されます。既存のプロジェクトなどに適用する場合は、影響範囲に注意してください。一部のボタンのみに対して排他制御をかけたい場合、カスタムComposite Bindingを実装する手順で実現可能です。）

初期設定では排他制御は無効化されています。

有効化するには、トップメニューのEdit > Project Settings…を選択してProject Settingsウィンドウを開き、Input System Package > Enable Input Consumptionにチェックを入れます。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-2.png.avif" width="90%" alt="" title="">

<br>

# Input Actionの設定例
排他制御を検証するための設定例です。

次のようなキー割り当てのActionに対して排他制御を適用してみます。

+ Next   
  Tabキーで反応。Shift + Tabキーでは反応しないようにする。
+ Prev   
  Shift + Tabキーの同時押しで反応するようにする。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-3.png.avif" width="90%" alt="" title="">

<br>

## 入力確認

ここでは、「次へ」「前へ」のActionが実行されたときにログ出力するものとします。  
入力取得はPlayer Inputコンポーネント経由で行うものとします。

以下、取得例です。

GetInputsExample.cs
```cs
using UnityEngine;
using UnityEngine.InputSystem;

public class GetInputsExample : MonoBehaviour
{
    // 「次へ」のAction
    public void OnNext(InputAction.CallbackContext context)
    {
        // ボタンが押された瞬間(performedコールバック)のみ拾う
        if (!context.performed) return;
            
        // ログ出力
        print("次へ");
    }

    // 「前へ」のAction
    public void OnPrev(InputAction.CallbackContext context)
    {
        // ボタンが押された瞬間(performedコールバック)のみ拾う
        if (!context.performed) return;
            
        // ログ出力
        print("前へ");
    }
}
```

上記をGetInputsExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチしておきます。

## Player Inputの設定
前述の確認用スクリプトから入力を取得できるようにするために、Player Input側の設定を行います。

適当なゲームオブジェクトにPlayer Inputコンポーネントをアタッチし、Actions項目に予め作成したInput Actionアセットを、Behaviour項目に<u>Invoke Unity Events</u>を指定します。 


<img src="images/9/9_4/unity-input-system-exclusive-modifier-m3.mp4.gif" width="90%" alt="" title="">

<br>

そして、Events項目の該当するActionにスクリプトのメソッドを登録します。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-m4.png" width="90%" alt="" title="">

<br>

実行すると、排他制御の適用前は、「前へ」操作をしているにも関わらず「次へ」操作が反応してしまっています。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-m5.mp4.gif" width="90%" alt="" title="">

<br>

排他制御を適用すると、「前へ」操作を行なっても「次へ」操作が反応しません。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-m6.mp4.gif" width="70%" alt="" title="">

<br>

<br>

# カスタムComposite Bindingで排他制御を実装する
アプリケーション全体に対して排他制御を実装したくないときなどは、カスタムComposite Bindingを自作して対処することも可能です。

Composite Bindingを用いると、複数の入力を合成したり、ある入力の型を別の型に変換したりすることができます。

あるボタンmodifierが押されている間は入力を流さず、離されている間は入力を流す挙動のComposite Bindingを実装します。


<img src="images/9/9_4/unity-input-system-exclusive-modifier-4.png.avif" width="70%" alt="" title="">

<br>



ボタンの入力値はアナログ値ですが、次のように閾値判定によって押されている／離されているのどちらかを判定できます。  

ボタンの押下状態判定
+ 押されている – 入力値がPress Point以上
+ 離されている – 入力値がPress Point未満

こちらの方法は、一つ目の方法とは異なり、個別のActionに対して排他制御を一つ一つ適用していく必要があります。

## 実装例  
排他制御を行うComposite Bindingの実装例です。

DisallowOneModifierComposite.cs
```cs
using System.ComponentModel;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Layouts;

[DisplayName("Disallow One Modifier")]
public class DisallowOneModifierComposite : InputBindingComposite<float>
{
    // このキーが押されていなければbuttonのActionを実行する
    [InputControl(layout = "Button")] public int modifier;
    
    // 排他制御対象のボタン
    [InputControl(layout = "Button")] public int button;


    /// <summary> 初期化 </summary>
#if UNITY_EDITOR
    [UnityEditor.InitializeOnLoadMethod]
#else
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
#endif

    private static void Initialize()
    {
        // 初回にCompositeBindingを登録する必要がある
        InputSystem.RegisterBindingComposite(typeof(DisallowOneModifierComposite), "DisallowOneModifierComposite");
    }
    
    /// <summary>一方のボタンが押されていない時だけ値を返す</summary>
    public override float ReadValue(ref InputBindingCompositeContext context)
    {
        // modifierのボタンが押されていない時だけbuttonの入力を通す
        if (!context.ReadValueAsButton(modifier))
            return context.ReadValue<float>(button);

        return default;
    }
    
    /// <summary>
    /// 入力値の大きさを取得する
    /// modifier入力の押下判定（Press Pointとの閾値判定）のために実装必須
    /// </summary>
    public override float EvaluateMagnitude(ref InputBindingCompositeContext context)
    {
        return ReadValue(ref context);
    }
}


```
上記スクリプトをUnityプロジェクトに保存するとComposite Bindingが使用可能になります。

このComposite Bindingを排他制御を適用したいAction（例ではNext）に適用します。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-m7.mp4.gif" width="90%" alt="" title="">

<br>

## 実行結果  

(トップメニューのEdit > Project Settings…を選択してProject Settingsウィンドウを開き、Input System Package > Enable Input Consumptionにチェック外しても)  
正しく排他制御されるようになりました。「前へ」操作を行なっても「次へ」操作が反応しません。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-m8.mp4.gif" width="70%" alt="" title="">

<br>

## スクリプトの説明
ボタンの定義。
```cs
// このキーが押されていなければbuttonのActionを実行する
[InputControl(layout = "Button")] public int modifier;

// 排他制御対象のボタン
[InputControl(layout = "Button")] public int button;
```

<br>

modifierの入力が無い時に入力を通す処理は以下部分です。

```cs
// modifierのボタンが押されていない時だけbuttonの入力を通す
if (!context.ReadValueAsButton(modifier))
    return context.ReadValue<float>(button);

return default;
```
context.ReadValueAsButtonメソッドで、指定されたBindingをボタンとみなして押下状態を取得しています。

押されている時にtrueが返されるので、押されている時は入力０を、押されていない時はbuttonのBinding入力を経由するとOKです。



ボタンの押下状態の判定は、「入力値の大きさ」と「Press Pointとの閾値判定」をするため、大きさを返すメソッドEvaluateMagnitudeをオーバーライドして実装する必要があります。 

```cs
public override float EvaluateMagnitude(ref InputBindingCompositeContext context)
{
    return ReadValue(ref context);
}
```

