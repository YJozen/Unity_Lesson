# Input SystemのProcessorを自作する

ここまで紹介したProcessorは、Input Systemパッケージ側で用意されているものですが、独自のProcessorを自作して適用することも可能です。

## 自作の流れ
1. InputProcessor<T>継承クラスをスクリプトで定義
2. 初期化時、InputSystemにProcessorを登録する処理を実装
3. Processorの処理を実装


## スクリプトの実装例
Vector2型の入力値を加工する（ずらす）自作Processorを実装したものです。

Vector2DValueShiftProcessor.cs
```cs

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

<img src="images/8/8_2/unity-input-system-processor-20.png.avif" width="80%" alt="" title="">

## スクリプトの解説
独自のProcessorは、次のコードのように、InputSystem<T>クラスを継承して実装します。

```cs
public class Vector2DValueShiftProcessor : InputProcessor<Vector2>
```
InputProcessor<T>はProcessorを表す基底クラスです。


Processorのプロパティとして編集可能なパラメータは、publicフィールドとして定義する必要があります。
```cs
// publicでなければプロパティに表示されない
// Vector2のような型はエラー、プリミティブ型かEnum型のフィールドである必要がある
public float shiftX;
public float shiftY;
```

実際に値を加工する処理は、以下の部分となります。
```cs
// 独自のProcessorの処理定義
public override Vector2 Process(Vector2 value, InputControl control)
{
    return value + new Vector2(shiftX, shiftY);
}
```

InputSystemへのProcessorの登録は、次の処理で行っています。
```cs
// Processorの登録処理
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
static void Initialize()
{
    // 重複登録すると、Input ActionのProcessor一覧に正しく表示されない事があるため、
    // 重複チェックを行う
    if (InputSystem.TryGetProcessor(ProcessorName) == null)
        InputSystem.RegisterProcessor<Vector2DValueShiftProcessor>(ProcessorName);
}
```


## 自作Processorにエディタ拡張を適用する

次のようなスクリプトをEditorフォルダ配下に置くことで適用できます。
```cs
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
```
この例の場合、以下のようなスライダーの見た目に変更されます。

<img src="images/8/8_2/unity-input-system-processor-21.png.avif" width="80%" alt="" title="">


---


### 自作Processorを実装する際の注意点

#### ・パラメータはpublic、かつプリミティブ型かEnum型のみ
通常のシリアライザのようにprivateフィールドに[SerializeField]属性を付けても有効化されません。

また、プリミティブ型（int、floatなど）かEnum型でなければならないという制約があるため、Vector2型などそれ以外の型をフィールドとして持たせてしまうと次のようなエラーが出てしまいます。
```
ArgumentException: Don't know how to convert PrimitiveValue to 'Object'
Parameter name: type
```
#### ・Processorの重複登録を行うと、メニューに表示されなくなる
重複チェックを行わず、以下のような形で登録処理を実装すると、UnityEditorから再生したとき等にProcessorの重複登録が発生してしまうことがあります。
```cs
[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
static void Initialize()
{
    InputSystem.RegisterProcessor<Vector2DValueShiftProcessor>(ProcessorName);
}
```
もしメニューに表示されなくなった場合は、UnityEditorを再起動するか、Processorを定義しているスクリプトを再インポートし直せば復活する場合があります。




