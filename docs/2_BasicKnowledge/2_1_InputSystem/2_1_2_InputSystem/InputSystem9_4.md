**InputSystem 2**


# 【Unity】Input Systemの同時押しを排他制御する




<img src="images/9/9_4/unity-input-system-exclusive-modifier-1.png.avif" width="50%" alt="" title="">

<br>


Input Systemでボタンの同時押しと片方押しを排他制御する方法の解説記事です。

例えばTabキーを使ったナビゲーションを実装するとき、Tabキー単体では「進む」操作になるが、Shift + Tabキーが押された場合は「戻る」操作となり、「進む」操作は実行されないようにしたい場合を想定します。

しかし、通常はShift + Tabを同時押しするとTabキーが押された時点で「進む」と「戻る」の両方の操作が実行されてしまいます。 [1]
Input System 1.4.0以降ではこれらを排他制御する機能が追加されています。また、それ未満のバージョンでもComposite Bindingを自作すれば回避可能です。

排他制御の実現方法
Input System 1.4.0以降 – 排他制御の有効化設定で対応可能
Input System 1.3.0以前 – カスタムComposite Bindingを実装して対応可能
前者の排他制御の有効化設定はアプリケーション全体に影響を及ぼすため、注意する必要があります。これが許容できない場合は後者のComposite Bindingを自作する方法となります。

本記事では、このようなボタン操作の排他制御をInput Systemで実現する方法について解説します。バージョンによって手順が異なるため、この辺の差異も含めて解説します。






# 排他制御の設定方法
Input System 1.4.0以降で可能ですが、バージョンによって手順が異なります。それぞれ使用バージョンに合った手順を実施してください。

Input System 1.3.0以前では本手順は実施不可なので、カスタムComposite Bindingを実装する手順へ進んでください。

注意
本手順はアプリケーション全体のInput Actionに対して排他制御が適用されます。既存のプロジェクトなどに適用する場合は影響範囲にご注意ください。一部のボタンのみに対して排他制御をかけたい場合、カスタムComposite Bindingを実装する手順で実現可能です。

 Input System 1.4.4以降
初期設定では排他制御は無効化されています。

有効化するには、トップメニューのEdit > Project Settings…を選択してProject Settingsウィンドウを開き、Input System Package > Enable Input Consumptionにチェックを入れます。



# Input Actionの設定例
排他制御を検証するための設定例を示します。本手順はあくまでも例のため、必須ではありません。

Input Actionの定義
本記事では、次のようなキー割り当てのActionに対して排他制御を適用することを例として解説を進めます。

Next – Tabキーで反応する。ただしShift + Tabキーでは反応しない。
Prev – Shift + Tabキーの同時押しで反応する。



<img src="images/9/9_4/unity-input-system-exclusive-modifier-3.png.avif" width="50%" alt="" title="">

<br>

確認用スクリプトの実装
ここでは、「次へ」「前へ」のActionが実行されたときにログ出力するものとします。入力取得はPlayer Inputコンポーネント経由で行うものとします。

以下、取得例です。



```cs:GetInputsExample.cs

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







# Player Inputの設定
前述の確認用スクリプトから入力を取得できるようにするために、Player Input側の設定を行います。

適当なゲームオブジェクトにPlayer Inputコンポーネントをアタッチし、Actions項目に予め作成したInput Actionアセットを、Behaviour項目にInvoke Unity Eventsを指定します。 


<img src="images/9/9_4/unity-input-system-exclusive-modifier-m3.mp4.gif" width="50%" alt="" title="">

<br>

そして、Events項目の該当するActionにスクリプトのメソッドを登録します。

<img src="images/9/9_4/unity-input-system-exclusive-modifier-m4.png" width="50%" alt="" title="">

<br>

実行結果
排他制御の適用前は、以下のように「前へ」操作をしているにも関わらず「次へ」操作が反応してしまっています。



<img src="images/9/9_4/unity-input-system-exclusive-modifier-m5.mp4.gif" width="50%" alt="" title="">

<br>

排他制御を適用すると、「前へ」操作を行なっても「次へ」操作が反応しません。


<img src="images/9/9_4/unity-input-system-exclusive-modifier-m6.mp4.gif" width="50%" alt="" title="">

<br>



# カスタムComposite Bindingで排他制御を実装する
Input System 1.3.0以前を使用している場合や、アプリケーション全体に対して排他制御を実装したくないときは、カスタムComposite Bindingを自作して対処することも可能です。

Composite Bindingを用いると、複数の入力を合成したり、ある入力の型を別の型に変換したりすることができます。

次のようにあるボタンmodifierが押されている間は入力を流さず、離されている間は入力を流す挙動のComposite Bindingを実装すれば良いです。


<img src="images/9/9_4/unity-input-system-exclusive-modifier-4.png.avif" width="50%" alt="" title="">

<br>



ボタンの入力値はアナログ値ですが、次のように閾値判定によって押されている／離されているのどちらかを判定できます。 [3]
ボタンの押下状態判定
+ 押されている – 入力値がPress Point以上
+ 離されている – 入力値がPress Point未満


こちらの方法は、一つ目の方法とは異なり、個別のActionに対して排他制御を一つ一つ適用していく必要があります。

実装例
以下、排他制御を行うComposite Bindingの実装例です。


```cs:DisallowOneModifierComposite.cs

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

    /// <summary>
    /// 初期化
    /// </summary>
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
    
    /// <summary>
    /// 一方のボタンが押されていない時だけ値を返す
    /// </summary>
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



<img src="images/9/9_4/unity-input-system-exclusive-modifier-m7.mp4.gif" width="50%" alt="" title="">

<br>


実行結果
こちらも正しく排他制御されるようになりました。「前へ」操作を行なっても「次へ」操作が反応しません。


<img src="images/9/9_4/unity-input-system-exclusive-modifier-m8.mp4.gif" width="50%" alt="" title="">

<br>

スクリプトの説明
ボタンの定義は以下で行なっています。

```cs:
// このキーが押されていなければbuttonのActionを実行する
[InputControl(layout = "Button")] public int modifier;

// 排他制御対象のボタン
[InputControl(layout = "Button")] public int button;
```

modifierの入力が無い時に入力を通す処理は以下部分です。
```cs:
// modifierのボタンが押されていない時だけbuttonの入力を通す
if (!context.ReadValueAsButton(modifier))
    return context.ReadValue<float>(button);

return default;
```
context.ReadValueAsButtonメソッドで、指定されたBindingをボタンとみなして押下状態を取得しています。

押されている時にtrueが返されるので、押されている時は入力０を、押されていない時はbuttonのBinding入力をバイパスするとOKです。



ボタンの押下状態の判定は、入力値の大きさとPress Pointとの閾値判定をするため、大きさを返すメソッドEvaluateMagnitudeをオーバーライドして実装する必要があります。 

```cs:
public override float EvaluateMagnitude(ref InputBindingCompositeContext context)
{
    return ReadValue(ref context);
}
```

