**InputSystem 2**

既存のComposite Bindingでは物足りない場合、Composite Bindingを自作することも可能です。






Composite Bindingはステートレス
カスタムComposite Bindingを実装する際の注意点として、Composite Bindingはステートレスでなければならないという決まりがあります。

参考：Input Bindings | Input System | 1.6.3

例えば、Composite Bindingインスタンスの中で状態変数を持つような実装をしてはいけません。

もしこのような状態変数を持った振る舞いを実現したい場合はInteractionを使用する、または併用する方が適しているかもしれません。



サンプルスクリプト
以上を踏まえたカスタムComposite Bindingの実装例です。2つのボタン入力を判定し、どちらか片方のボタンのみが押されている間だけそのボタンの入力値を返します。



```cs:

using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Layouts;

public class XorComposite : InputBindingComposite<float>
{
    // ボタン1
    [InputControl(layout = "Button")] public int button1 = 0;

    // ボタン2
    [InputControl(layout = "Button")] public int button2 = 0;


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
        InputSystem.RegisterBindingComposite<XorComposite>(nameof(XorComposite));
    }

    /// <summary>
    /// どちらか一方のボタンが押されている場合のみ、押されているボタンの入力値を返す
    /// </summary>
    public override float ReadValue(ref InputBindingCompositeContext context)
    {
        // ボタンの押下状態取得
        var button1Pressed = context.ReadValueAsButton(button1);
        var button2Pressed = context.ReadValueAsButton(button2);

        // どちらか片方のボタンが押されている場合のみ、
        // 押されているボタンの入力値を返す
        if (button1Pressed ^ button2Pressed)
            return context.ReadValue<float>(button1Pressed ? button1 : button2);

        return 0;
    }

    /// <summary>
    /// 入力値を返す
    /// </summary>
    public override float EvaluateMagnitude(ref InputBindingCompositeContext context)
    {
        return ReadValue(ref context);
    }
}

```


上記をXorComposite.csという名前でUnityプロジェクトに保存すると、カスタムComposite BindingとしてInput Action側で使えるようになります。

例えば適当なAction右の＋アイコンをクリックすると、メニューに追加されていることが確認できます。


<img src="images/9/9_1/unity-input-system-composite-binding-24.png.avif" width="50%" alt="" title="">

<br>





その後、各Bindingを指定してください。例では数字の「1」と「2」キーを対象としました。



<img src="images/9/9_1/unity-input-system-composite-binding-25.png.avif" width="50%" alt="" title="">

<br>



検証用スクリプト（必要ならば）
以下、カスタムComposite Bindingの入力値を受け取る検証用スクリプトです。

```cs:CustomExample.cs

using UnityEngine;
using UnityEngine.InputSystem;

public class CustomExample : MonoBehaviour
{
    [SerializeField] private InputActionReference _actionRef;

    private void OnDestroy()
    {
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

    private void Update()
    {
        print("入力値: " + _actionRef.action.ReadValue<float>());
    }
}


```


上記をCustomExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりカスタムComposite Bindingを設定したActionを指定してください。




<img src="images/9/9_1/unity-input-system-composite-binding-26.png.avif" width="50%" alt="" title="">

<br>


実行結果
指定された2つのボタンのうち、どちらか片方のボタンが押されたときのみ入力値が出力されるようになりました。


どちらのボタンも押していない、または両方のボタンを押した時は入力値を出力しません。




スクリプトの説明



カスタムComposite Bindingの基本形
次のようにInputBindingComposite<T>継承クラスを実装します。

public class MyCustomComposite : InputBindingComposite<float>
このクラスでは、次のようにReadValueメソッドの実装が必須です。

public override float ReadValue(ref InputBindingCompositeContext context)
{
    // TODO : Bindingの値を合成して返す
    return 0;
}
また、Interactionでのボタンの押された判定や長押し判定など、ボタンの押下状態を判定するのに入力値の大きさを用います。

これらを動作させるためには、EvaluateMagnitudeメソッドの実装も必要です。

public override float EvaluateMagnitude(ref InputBindingCompositeContext context)
{
    // 入力値の大きさを返す
    return ReadValue(ref context);
}
そして、合成元となるBindingは、次のようにInputControl属性を指定したpublicなint型フィールドとして定義します。

// ボタン1
[InputControl(layout = "Button")] public int button1 = 0;

// ボタン2
[InputControl(layout = "Button")] public int button2 = 0;
参考：Class InputControlAttribute| Input System | 1.6.3

また、これだけではInput System側にカスタムComposite Bindingが登録されないため、次の処理で登録する必要があります。

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
        InputSystem.RegisterBindingComposite<XorComposite>(nameof(XorComposite));
    }
エディタ時と実行時で登録処理を行うInitializeメソッドの呼び出し方法を分けています。

エディタ時ではUnityエディタが読み込まれたとき、実行時ではシーンの読み込み前にそれぞれInitializeメソッドを呼び、カスタムComposite Bindingの登録処理を行っています。

参考：Unity – Scripting API: InitializeOnLoadMethodAttribute

参考：Unity – Scripting API: RuntimeInitializeLoadType.BeforeSceneLoad

Composite Bindingの登録はInputSystem.RegisterBindingCompositeメソッドにて行います。

public static void RegisterBindingComposite(Type type, string name);
public static void RegisterBindingComposite<T>(string name = null);
Composite Bindingのクラスの型と名前をそれぞれ指定して登録します。

参考：Class InputSystem| Input System | 1.6.3







スクリプトの説明


カスタムComposite Bindingの値を合成する処理では、どちらか一方のボタンが押されている間のみ入力値を流すようにするため、2つのボタンの押下状態の排他的論理和を取っています。




```cs:
/// <summary>
/// どちらか一方のボタンが押されている場合のみ、押されているボタンの入力値を返す
/// </summary>
public override float ReadValue(ref InputBindingCompositeContext context)
{
    // ボタンの押下状態取得
    var button1Pressed = context.ReadValueAsButton(button1);
    var button2Pressed = context.ReadValueAsButton(button2);

    // どちらか片方のボタンが押されている場合のみ、
    // 押されているボタンの入力値を返す
    if (button1Pressed ^ button2Pressed)
        return context.ReadValue<float>(button1Pressed ? button1 : button2);

    return 0;
}

```

そして、この排他的論理和が真の時のみ押されているボタン側の入力値を返しています。それ以外は常に0です。


Composite Bindingの各種ボタン入力を判定したい場合


Composite Bindingを使用した際にあり得るケースとして、例えばWASDキーによる移動Actionがあり、なおかつWキーが押されたことを個別で判定したいケースを考えます。

この場合は、Composite Bindingとは別にWキー専用のActionを作るのが望ましいです。




<img src="images/9/9_1/unity-input-system-composite-binding-26.png.avif" width="50%" alt="" title="">

<br>



Input Actionからコールバックで受け取る時にどのボタンの入力なのかの判定も可能ですが、次のようなコードにしてしまうと正しく処理できません。

悪い例

private void OnMove(InputAction.CallbackContext context)
{
    if (context.control.name == "w")
    {
        // 上キーが押された処理など
    }
}
理由は、複数の方向キーが同時に押された場合に意図しない判定になるためです。


これは、例えば対象ActionのAction TypeにValueが指定されている場合などに起こります。Valueが指定されると値が変化された瞬間にコールバックが発火するため、離されたボタンが認識されたり、押されたボタンが認識されたりとまちまちです。

他にも、個別のControlをチェックすることによりInput Actionの持つ柔軟性が失われてしまう、スクリプトにデバイス固有の判定ロジックが入ってしまうなど数々の副作用を引き起こすため避けるべきです。