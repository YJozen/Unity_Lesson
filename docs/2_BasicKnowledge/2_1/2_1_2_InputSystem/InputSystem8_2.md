**InputSystem 2**

# Input SystemのProcessorを自作する

ここまで紹介したProcessorは、Input Systemパッケージ側で用意されているものですが、独自のProcessorを自作して適用することも可能です。

## 自作の流れ
1. InputProcessor<T>継承クラスをスクリプトで定義
2. 初期化時、InputSystemにProcessorを登録する処理を実装
3. Processorの処理を実装


## スクリプトの実装例

```cs:Vector2DValueShiftProcessor.cs

using UnityEngine;
using UnityEngine.InputSystem;

#if UNITY_EDITOR
using UnityEditor;
#endif

#if UNITY_EDITOR
[InitializeOnLoad]
#endif
public class Vector2DValueShiftProcessor : InputProcessor<Vector2>
{
    // publicでなければプロパティに表示されない
    // Vector2のような型はエラー、プリミティブ型かEnum型のフィールドである必要がある
    public float shiftX;
    public float shiftY;

    private const string ProcessorName = "Vector2DValueShift";

#if UNITY_EDITOR
    static Vector2DValueShiftProcessor() => Initialize();
#endif

    // Processorの登録処理
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Initialize()
    {
        // 重複登録すると、Input ActionのProcessor一覧に正しく表示されない事があるため、
        // 重複チェックを行う
        if (InputSystem.TryGetProcessor(ProcessorName) == null)
            InputSystem.RegisterProcessor<Vector2DValueShiftProcessor>(ProcessorName);
    }

    // 独自のProcessorの処理定義
    public override Vector2 Process(Vector2 value, InputControl control)
    {
        return value + new Vector2(shiftX, shiftY);
    }
}

```
上記スクリプトをVector2DValueShiftProcessor.csなどの名前でUnityプロジェクトに保存すれば、新しいProcessorとして機能するようになります。
![](images/8/8_2/unity-input-system-processor-20.png.avif "")


スクリプトの解説
例で示したサンプルは、Vector2型の入力値を加工する自作Processorを実装したものです。

独自のProcessorは、次のコードのように、InputSystem<T>クラスを継承して実装します。

public class Vector2DValueShiftProcessor : InputProcessor<Vector2>
InputProcessor<T>はProcessorを表す基底クラスです。

参考：Class InputProcessor| Input System | 1.3.0

Processorのプロパティとして編集可能なパラメータは、publicフィールドとして定義する必要があります。

// publicでなければプロパティに表示されない
// Vector2のような型はエラー、プリミティブ型かEnum型のフィールドである必要がある
public float shiftX;
public float shiftY;
実際に値を加工する処理は、以下の部分となります。

// 独自のProcessorの処理定義
public override Vector2 Process(Vector2 value, InputControl control)
{
    return value + new Vector2(shiftX, shiftY);
}
InputSystemへのProcessorの登録は、次の処理で行っています。

// Processorの登録処理
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
static void Initialize()
{
    // 重複登録すると、Input ActionのProcessor一覧に正しく表示されない事があるため、
    // 重複チェックを行う
    if (InputSystem.TryGetProcessor(ProcessorName) == null)
        InputSystem.RegisterProcessor<Vector2DValueShiftProcessor>(ProcessorName);
}
これらの処理は公式リファレンスに則っていますが、一部処理を変更しています。理由は、Processorの重複登録が行われるとProcessorメニューの選択項目に表示されなくなる現象が発生するためです。（後述します）

自作Processorにエディタ拡張を適用する
次のようなスクリプトをEditorフォルダ配下に置くことで適用できます。

#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;
using UnityEngine.InputSystem.Editor;

public class Vector2ValueShiftProcessorEditor : InputParameterEditor<Vector2DValueShiftProcessor>
{
    private GUIContent m_SliderLabelX = new GUIContent("Shift X By");
    private GUIContent m_SliderLabelY = new GUIContent("Shift Y By");

    // protectedにする必要あり
    protected override void OnEnable()
    {
    }

    public override void OnGUI()
    {
        target.shiftX = EditorGUILayout.Slider(m_SliderLabelX, target.shiftX, -10, 10);
        target.shiftY = EditorGUILayout.Slider(m_SliderLabelY, target.shiftY, -10, 10);
    }
}
#endif
この例の場合、以下のようなスライダーの見た目に変更されます。

![](images/8/8_2/unity-input-system-processor-21.png.avif "")

自作Processorを実装する際の注意点
Processorを独自実装するにあたり、いくつか嵌った点がありましたので、軽くまとめます。

パラメータはpublic、かつプリミティブ型かEnum型のみ
通常のシリアライザのようにprivateフィールドに[SerializeField]属性を付けても有効化されません。

また、プリミティブ型（int、floatなど）かEnum型でなければならないという制約があるため、Vector2型などそれ以外の型をフィールドとして持たせてしまうと次のようなエラーが出てしまいます。

ArgumentException: Don't know how to convert PrimitiveValue to 'Object'
Parameter name: type
Processorの重複登録を行うと、メニューに表示されなくなる
以下のような形で登録処理を実装すると、UnityEditorから再生したとき等にProcessorの重複登録が発生してしまうことがあります。

[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
static void Initialize()
{
    InputSystem.RegisterProcessor<Vector2DValueShiftProcessor>(ProcessorName);
}
この問題は、以下Issueでも報告されています。

参考：New Input System processors not appearing always – Unity Forum

Input System 1.3.0でもこの問題が発生するため、本記事ではやむを得ず重複チェックを行うことで回避しています。

もしメニューに表示されなくなった場合は、UnityEditorを再起動するか、Processorを定義しているスクリプトを再インポートし直せば復活する場合があります。

InputParameterEditor.OnEnable()メソッドはprotected
公式リファレンスのエディタ拡張サンプルでは、アクセス修飾子がpublicになっていますが、実装上はprotectedが正解です。publicのままではエラーが出てしまう状況です。

スクリプトリファレンスでもprotectedとなっているので、こちらに合わせると問題なく動くようになります。