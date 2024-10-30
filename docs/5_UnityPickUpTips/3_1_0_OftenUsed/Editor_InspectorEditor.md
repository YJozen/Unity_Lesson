# Editor拡張の例

<br>

Unityのエディターでボタンや機能を追加したり、インスペクターに新しい要素を追加するには、Unityの**Editorスクリプト**や**カスタムエディター**機能を使います。

<br>

---


# 1. **エディタースクリプトのセットアップ**

Unityエディターでカスタムツールを追加するためには、`UnityEditor`名前空間を使います。  
Editorスクリプトは通常、`Editor`フォルダに入れておきます。

```csharp
using UnityEditor;
using UnityEngine;

public class CustomEditorWindow : EditorWindow
{
    [MenuItem("Window/Custom Tool")]
    public static void ShowWindow()
    {
        GetWindow<CustomEditorWindow>("Custom Tool");
    }

    private void OnGUI()
    {
        if (GUILayout.Button("Press me"))
        {
            Debug.Log("Button Pressed!");
        }
    }
}
```

このスクリプトを実行すると、**「Window > Custom Tool」**に新しいウィンドウが追加され、ボタンをクリックするとメッセージが表示されます。

<br>

# 2_1. **インスペクターにボタンを追加**

インスペクターに独自のボタンを追加したい場合、**カスタムエディター**を使います。  
 `CustomEditor`属性を使い、特定のスクリプトのエディターを拡張します。

```csharp
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(MyScript))]
public class MyScriptEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        MyScript myScript = (MyScript)target;
        if (GUILayout.Button("Execute Action"))
        {
            myScript.PerformAction(); // 実行する関数
        }
    }
}
```

ここでは、`MyScript`スクリプトに対してカスタムエディターを作成し、ボタンが表示されるようにしています。

<br>

# 2_2. **GameObjectをインスタンス化してみる**

`MyObjectSpawner.cs`

```csharp
using UnityEngine;

public class MyObjectSpawner : MonoBehaviour
{
    public GameObject prefab; // スポーンするオブジェクトのPrefab
    public Vector3 spawnPosition; // スポーン位置

    // オブジェクトをスポーンするメソッド
    public void SpawnObject()
    {
        if (prefab != null)
        {
            Instantiate(prefab, spawnPosition, Quaternion.identity);
        }
        else
        {
            Debug.LogWarning("Prefabが指定されていません！");
        }
    }
}
```

<br>

`MyObjectSpawnerEditor.cs`

```cs
#if UNITY_EDITOR
using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(MyObjectSpawner))]
public class MyObjectSpawnerEditor : Editor
{
    public override void OnInspectorGUI()
    {
        // 通常のインスペクター要素を描画
        DrawDefaultInspector();

        // スポーナーオブジェクトを参照
        MyObjectSpawner spawner = (MyObjectSpawner)target;

        // スポーンボタンを追加
        if (GUILayout.Button("Spawn Object"))
        {
            spawner.SpawnObject();
        }

        // スポーン位置をランダムに生成するボタン
        if (GUILayout.Button("Randomize Position"))
        {
            spawner.spawnPosition = new Vector3(
                Random.Range(-10f, 10f),
                Random.Range(0f, 5f),
                Random.Range(-10f, 10f)
            );
        }
    }
}
#endif

```

<br>

# 3. **URLを表示してGitHubページに飛ばす**

インスペクターにURLボタンを追加して、クリックすると指定のURLに飛ぶ機能を追加できます。

```csharp
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(MyScript))]
public class JumpURLEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();
        
        if (GUILayout.Button("Visit Unity_Lesson Page"))
        {
            Application.OpenURL("https://yjozen.github.io/Unity_Lesson/");
        }
    }
}
```


<br>

# 4. **サブウィンドウの作成**

特定のプロジェクトで使える便利なサブウィンドウを作成できます。たとえば、特定のオブジェクトにクイックアクセスするためのウィンドウを作成してみましょう。

```csharp
using UnityEditor;
using UnityEngine;

public class QuickAccessWindow : EditorWindow
{
    [MenuItem("Window/Quick Access")]
    public static void ShowWindow()
    {
        GetWindow<QuickAccessWindow>("Quick Access");
    }

    private void OnGUI()
    {
        if (GUILayout.Button("Select Player"))
        {
            var player = GameObject.Find("Player");
            Selection.activeGameObject = player;
        }
    }
}
```

<br>

# 5. **EditorPrefsで設定の保存**

エディターツールに保存機能を持たせ、Unityを再起動しても設定が残るようにするには、`EditorPrefs`を使用します。

```csharp
public class SettingsWindow : EditorWindow
{
    private string mySetting;

    [MenuItem("Window/Settings")]
    public static void ShowWindow()
    {
        GetWindow<SettingsWindow>("Settings");
    }

    private void OnGUI()
    {
        mySetting = EditorGUILayout.TextField("My Setting", mySetting);

        if (GUILayout.Button("Save Setting"))
        {
            EditorPrefs.SetString("mySetting", mySetting);
        }

        if (GUILayout.Button("Load Setting"))
        {
            //もしキーが存在していればその保存された値を返し、存在しない場合は指定したデフォルト値 "Default Value" を返します。
            mySetting = EditorPrefs.GetString("mySetting", "Default Value");
        }

        if (GUILayout.Button("Reset"))
        {
            mySetting = EditorPrefs.DeleteKey("mySetting");
        }
    }
}
```


<br>

# 6. **シーンビューにボックスやスフィアを描画**

`OnDrawGizmos`を使って、シーンビュー上で簡単な視覚ガイドを描画できます。以下のコードでは、オブジェクトの周囲にシーン上でのみ表示されるボックスとスフィアを描画します。

```csharp
private void OnDrawGizmos() {
    Gizmos.color = Color.yellow;
    Gizmos.DrawWireCube(transform.position, new Vector3(1, 1, 1));  // ボックス描画
    Gizmos.color = Color.red;
    Gizmos.DrawWireSphere(transform.position, 1f); // スフィア描画
}
```

このようなガイドは、オブジェクトの当たり判定や範囲を視覚的に確認するのに便利です。

<br>

# 7. **シーンビュー上にインタラクティブなGUIボタンの追加**

シーンビューにボタンを追加して、特定の操作を行うインタラクティブなインターフェイスを作成できます。以下の例では、クリック時にオブジェクトを移動させるボタンを表示します。

`SceneEditorSample.cs`

```cs
#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(SceneEditorSampleComponent))]
public class SceneEditorSample : Editor
{
    private void OnSceneGUI()
    {
        Transform targetTransform = (target as MonoBehaviour).transform;
        
        // ラベルの表示
        Handles.Label(targetTransform.position + Vector3.up * 2f, "Move Up", 
            new GUIStyle() { normal = { textColor = Color.cyan } });

        // ボタンの表示と処理
        Handles.color = Color.red;
        if (Handles.Button(targetTransform.position + Vector3.up * 1.5f, 
            Quaternion.identity, 0.5f, 0.5f, Handles.SphereHandleCap))
        {
            // 移動処理
            Undo.RecordObject(targetTransform, "Move Up");
            targetTransform.position += Vector3.up * 2f;
        }
    }
}


#endif
```

<br>

`SceneEditorSampleComponent.cs`

```csharp
using UnityEngine;
using UnityEditor;

public class SceneEditorSampleComponent : MonoBehaviour
{

}
```



このコードでは、シーンビューにボタンが描画され、押すとオブジェクトが上に移動します。

<br>

# 8. **シーンビュー上に距離や角度を表示**

`Handles`を使って、オブジェクト間の距離や角度を計測し、シーンビューに表示することもできます。

```csharp
#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(SceneEditorSampleComponent))]
public class SceneEditorSample : Editor
{
    private void OnSceneGUI()
    {
        Transform targetTransform = (target as MonoBehaviour).transform;
        
        // ラベルの表示
        Handles.Label(targetTransform.position + Vector3.up * 2f, "Move Up", 
            new GUIStyle() { normal = { textColor = Color.cyan } });

        // ボタンの表示と処理
        Handles.color = Color.red;
        if (Handles.Button(targetTransform.position + Vector3.up * 1.5f, 
            Quaternion.identity, 0.5f, 0.5f, Handles.SphereHandleCap))
        {
            // 移動処理
            Undo.RecordObject(targetTransform, "Move Up");
            targetTransform.position += Vector3.up * 2f;
        }
    }
}


#endif
```


<br>

`OtherObject.cs`

```cs
using UnityEngine;

public class OtherObject : MonoBehaviour
{

}

```


この例では、別のオブジェクト(OtherObjectをアタッチしたObject)との距離を表示し、シーンビュー上で距離を可視化します。

<br>

# 9. **プロジェクト内で使用するショートカットボタン**

`MenuItem`属性を使ってショートカット機能を作成することも可能です。たとえば、エディター上で選択したオブジェクトを特定の位置に移動させるショートカットボタンを作成できます。

```csharp
#if UNITY_EDITOR
public class ShortcutActions : MonoBehaviour
{
    [MenuItem("Tools/Move to Origin")]
    private static void MoveToOrigin()
    {
        if (Selection.activeTransform != null)
        {
            Selection.activeTransform.position = Vector3.zero;
        }
    }
}
#endif
```

このスクリプトは、「Tools > Move to Origin」にショートカットを追加し、選択したオブジェクトを原点に移動します。

<br>

---


---

<br>

### その他（外部サイト）

<a href="https://gametukurikata.com/customize/sceneview/handles" target="_blank">UnityのHandleを使用してシーンビューのオブジェクトを操作する</a>

<a href="https://zenn.dev/dolphiiiin/articles/3dc6a44170a8f1" target="_blank">便利なUnitのEditor拡張まとめ</a>

<a href="https://yotiky.hatenablog.com/entry/unity_editorextension-tips" target="_blank">Unity - Editor 拡張のチートシート</a>





---