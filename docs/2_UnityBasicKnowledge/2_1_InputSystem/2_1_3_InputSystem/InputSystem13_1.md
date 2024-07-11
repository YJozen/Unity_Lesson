【Unity】Input SystemのControl Pathの基本構造と使い方

https://nekojara.city/unity-input-system-control-path

Input Systemでは、キーボードのボタンやマウス移動量、ゲームパッドのスティックといったControlの情報はControl Pathという文字列として扱われます。

例えば、Input Action Assetの編集でActionのBindingに割り当てる入力先がControl Pathです。

<img src="images/13/13_1/unity-input-system-control-path-1.png.avif" width="80%" alt="" title="">

<br>

普段はドロップダウン形式で選択するUIですが、右側にある小さな「T」ボタンをクリックすると、実際のControl Pathの文字列として編集可能になります。

<img src="images/13/13_1/unity-input-system-control-path-2.png.avif" width="80%" alt="" title="">

<br>




Controlの基本的な仕組み
Input Systemでは、ゲームパッドやキーボード、これらに付いているボタン類などを全てControlとして管理します。

Controlは次のような階層構造として管理されます。


<img src="images/13/13_1/unity-input-system-control-path-3.png.avif" width="80%" alt="" title="">

<br>


スクリプト中からはInputControl継承クラスとして扱われます。


階層化されたControlはスラッシュ「/」区切りのパスとして表現されます。




<img src="images/13/13_1/unity-input-system-control-path-4.png.avif" width="80%" alt="" title="">

<br>



Control Pathの基本構文
Control単体は次のような文字列で表現されます。

<layoutName>{usageName}controlName#(displayName)
指定するものが4つありますが、すべてを指定する必要はなく、最低限どれか1つ指定すればよいです。基本的に数あるControlのどれを使うかを検索するために使われるものです。

また、階層化されたControlはスラッシュ「/」区切りで指定します。




control/control/...
layoutNameには、「Keyboard」「Gamepad」などのレイアウト名（Controlの型）を指定します。他にも、後述する子階層のControlで「Button」「Axis」などの名前も指定できます。

レイアウト名は「<」と「>」で囲んで指定します。

参考：Layouts | Input System | 1.5.1

usageNameには、「Submit」や「Back」など、予めControlに割り当てられているusages名を指定します。例えば、Escキーには「Back」と「Cancel」、Enterキーには「Submit」がusageとして予め割り当てられています。

usage名は「{」と「}」で囲んで指定します。




controlNameには、具体的なControl名を指定します。例えばゲームパッドの「DualShock4GamepadHID」やEnterキーの「enter」などといった名前です。

displayNameには、Controlの表示名を指定します。例えばキーボードのEnterキーの「Enter」などが該当します。

displayNameは「#(」と「)」で囲んで指定します。

# 構文の例
具体的なControl Pathの例をいくつか示します。



+ <Gamepad>/rightTrigger
「Gamepad」というLayout名のControl配下の「rightTrigger」という名前のControl
ゲームパッドの右トリガーを表す
DualShock4GamepadHID/buttonEast
「DualShock4GamepadHID」という名前のControl配下の「buttonEast」という名前のControl
DUALSHOCK 4コントローラーの〇ボタンを表す
<Gamepad>/leftStick/left
「Gamepad」というLayout名のControl配下の「leftStick」という名前のControl配下の「left」という名前のControl
ゲームパッドの左スティックの左入力を表す
<Gamepad>/<Button>
「Gamepad」というLayout名のControl配下の「Button」というLayout名のControl
ゲームパッドのボタン全体が対象となる
<Keyboard>/#(Enter)
「Keyboard」というLayout名のControl配下の「Enter」という表示名のControl
キーボードのEnterキーを表す

# ワイルドカード表記
Control Pathには、「全て」を表すControlをアスタリスク「*」として指定可能です。

+ <Gamepad\>/\*  
「Gamepad」というLayout名のControl配下の「全て」のControl
+ \*/{Submit}
「全て」のControl配下の「Submit」というusage名のControl
スクリプトからControl Pathを扱う
スクリプトではControl Pathは文字列（string型）として扱います。

シリアライズするフィールドに[InputControl]属性を付加すると、インスペクター上からControl Pathを編集するための専用UIに置き換わります。



<img src="images/13/13_1/unity-input-system-control-path-5.png.avif" width="80%" alt="" title="">

<br>



サンプルスクリプト
以下、インスペクターから指定されたControl Pathをログ出力するサンプルスクリプトです。


```
ControlPathExample.cs
using UnityEngine;
using UnityEngine.InputSystem.Layouts;

public class ControlPathExample : MonoBehaviour
{
    // InputControl属性を付加し、Control PathのUIに置き換える
    [SerializeField, InputControl] private string _controlPath;

    private void Start()
    {
        print($"Control Path: {_controlPath}");
    }
}
```

上記をControlPathExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりControl Pathを設定してください。


ゲームを実行すると、インスペクターから指定されたControl Pathの文字列がログ出力されるようになります。




<img src="images/13/13_1/unity-input-system-control-path-6.png.avif" width="80%" alt="" title="">

<br>



Control Pathの構文を解析する
Control Pathはstring型の文字列として管理されますが、構文を解析することも可能です。

構文解析には、InputControlPath.Parseメソッドを用います。

public static IEnumerable<InputControlPath.ParsedPathComponent> Parse(string path)
参考：Class InputControlPath| Input System | 1.5.1

解析結果は、InputControlPath.ParsedPathComponent構造体のコレクションとして返されます。コレクションの各要素は、上層からパスで区切られたControl情報です。

参考：Struct InputControlPath.ParsedPathComponent| Input System | 1.5.1

サンプルスクリプト
以下、指定されたControl Path文字列を解析してログ出力する例です

```cs:
using System;
using System.Text;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Layouts;

public class ParseExample : MonoBehaviour
{
    // インスペクターから指定されるControl Path
    [SerializeField, InputControl] private string _controlPath;

    private void Start()
    {
        var sb = new StringBuilder();
        
        print($"「{_controlPath}」のパース結果");

        // Control Pathをパースして、各要素（フィールド）をログ出力
        foreach (var path in InputControlPath.Parse(_controlPath))
        {
            // 各要素（フィールド）をログ出力
            sb.AppendLine($"layout: {path.layout}");
            foreach (var usage in path.usages)
            {
                sb.AppendLine($" usage: {usage}");
            }

            sb.AppendLine($"name: {path.name}");
            sb.AppendLine($"displayName: {path.displayName}");

            Debug.Log(sb.ToString());

            sb.Clear();
        }
    }
}
```

上記をParseExample.csという名前で保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりControl Pathを設定すると機能するようになります。

実行結果
例えば、「<Gamepad>/dpad/down」というControl Pathが指定されると、以下のような結果になります。



<img src="images/13/13_1/unity-input-system-control-path-7.png.avif" width="80%" alt="" title="">

<br>




上から順にLayout名が「Gamepad」のControl、名前がdpadのControl、名前がdownのControlという順番のコレクションがInputControlPath.Parseメソッドから返されていることが確認できます。

Control Pathから実際のControlを取得する
実際にActionなどとしてボタンやスティックなど各種Controlから入力を受け取るためには、Control Pathから実際のControlを取得する必要があります。

このようなControlはプログラム上ではInputControl継承クラスとして扱われます。

例えばボタンはButtonControl、スティックはStickControl、キーボードのキーはKeyControlという派生クラスとして実装されます。

単一のControlはInputSystem.FindControlメソッドから取得できます。

public static InputControl FindControl(string path)
参考：Class InputSystem| Input System | 1.5.1

サンプルスクリプト
以下、与えられたControl PathからInputControlインスタンスを取得し、内容をログ出力する例です。取得に失敗したらその旨のメッセージを出力します。


```cs:
using System.Text;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Layouts;

public class InputControlExample : MonoBehaviour
{
    [SerializeField, InputControl] private string _controlPath;

    private void Start()
    {
        // Control PathからInputControlを取得
        var control = InputSystem.FindControl(_controlPath);
        if (control == null)
        {
            // コントローラーなどが接続されていないとnullになり失敗する
            print("InputControlの取得に失敗しました");
            return;
        }

        // InputControlの各種プロパティをログ出力
        var sb = new StringBuilder();
        sb.AppendLine($"Control Path: {_controlPath}");
        sb.AppendLine($"Type: {control.GetType()}");
        sb.AppendLine($"name: {control.name}");
        sb.AppendLine($"displayName: {control.displayName}");
        sb.AppendLine($"shortDisplayName: {control.shortDisplayName}");
        sb.AppendLine($"path: {control.path}");
        sb.AppendLine($"layout: {control.layout}");
        sb.AppendLine($"device: {control.device}");
        sb.AppendLine($"parent: {control.parent}");
        sb.AppendLine("children:");
        foreach (var child in control.children)
        {
            sb.AppendLine($" - {child}");
        }

        sb.AppendLine("usages:");
        foreach (var usage in control.usages)
        {
            sb.AppendLine($" - {usage}");
        }

        sb.AppendLine("aliases:");
        foreach (var alias in control.aliases)
        {
            sb.AppendLine($" - {alias}");
        }

        Debug.Log(sb.ToString());
    }
}
```

上記をInputControlExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチすると機能します。

予めインスペクターよりControl Pathを設定してください。

実行結果
Control Pathに「<Keyboard>/enter」が指定されると、EnterキーのInputControlが得られ、その内容がログ出力されます。




<img src="images/13/13_1/unity-input-system-control-path-8.png.avif" width="80%" alt="" title="">

<br>





レイアウトが「Key」だったり、親Controlが「Keyboard」だったり、usageに「Submit」が存在していたりといった情報が確認できます。

試しにControl Pathに親の「<Keyboard>」を指定してみると、次のような結果が得られます。





<img src="images/13/13_1/unity-input-system-control-path-9.png.avif" width="80%" alt="" title="">

<br>


親Controlが存在しない代わりに、子Controlとして各種キーが大量に存在していることが確認できます。





複数のControlを取得する
前述の例では、単一のInputControlのみ取得していました。

しかし、実際にはControl Pathから複数のInputControlが得られるケースもあり得ます。例えばワイルドカードが指定されたControl Pathなどです。

これはInputSystem.FindControlsメソッドで取得できます。

public static InputControlList<InputControl> FindControls(string path)
public static InputControlList<TControl> FindControls<TControl>(string path)
    where TControl : InputControl
テンプレート引数TControlを指定することで、得られるControlの型を制限できます。例えば、キーボードのキーに限定したい場合はKeyControl型を指定すれば良いです。

参考：Class InputSystem| Input System | 1.5.1

サンプルスクリプト
以下、指定されたControl Pathから複数のControlを列挙し、その内容をログ出力する例です。


```
using System.Text;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Layouts;

public class InputControlsExample : MonoBehaviour
{
    [SerializeField, InputControl] private string _controlPath;

    private void Start()
    {
        // Control Pathから複数のInputControlを取得
        var controls = InputSystem.FindControls(_controlPath);
        
        print($"Control Path: {_controlPath}");
        
        var sb = new StringBuilder();

        for (var i = 0; i < controls.Count; i++)
        {
            var control = controls[i];
            
            // InputControlの各種プロパティをログ出力
            sb.AppendLine($"Control[{i}]:");
            sb.AppendLine($" Type: {control.GetType()}");
            sb.AppendLine($" name: {control.name}");
            sb.AppendLine($" displayName: {control.displayName}");
            sb.AppendLine($" shortDisplayName: {control.shortDisplayName}");
            sb.AppendLine($" path: {control.path}");
            sb.AppendLine($" layout: {control.layout}");
            sb.AppendLine($" device: {control.device}");
            sb.AppendLine($" parent: {control.parent}");
            sb.AppendLine(" children:");
            foreach (var child in control.children)
            {
                sb.AppendLine($"  - {child}");
            }

            sb.AppendLine(" usages:");
            foreach (var usage in control.usages)
            {
                sb.AppendLine($"  - {usage}");
            }

            sb.AppendLine(" aliases:");
            foreach (var alias in control.aliases)
            {
                sb.AppendLine($"  - {alias}");
            }

            Debug.Log(sb.ToString());
            sb.Clear();
        }
    }
}
```


上記をInputControlsExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりControl Pathを設定します。

実行結果
例えば、「*/{Submit}」というControl Pathが指定されると、全てのデバイス直下の「Submit」というusageを持っているControlが列挙されます。





<img src="images/13/13_1/unity-input-system-control-path-10.png.avif" width="80%" alt="" title="">

<br>



例ではキーボードとXboxコントローラーのSubmitボタンが得られていますが、他にもSubmitとなり得る候補は存在します。あくまでも接続され使用可能になっているControlのみが対象になっている点が特徴です。

