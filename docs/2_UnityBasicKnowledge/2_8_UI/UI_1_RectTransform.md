

<img src="images/unity-rect-transform-corners-5.png.avif" width="90%" alt="" title="">

<br>

<img src="images/unity-rect-transform-corners-9.png.avif" width="90%" alt="" title="">

<br>

---

<br>

# `RectTransform` 

`RectTransform` は、UI 要素の位置、サイズ、回転を制御するために使用される Unity のコンポーネントです。通常の `Transform` コンポーネントは 3D オブジェクトに使用されますが、`RectTransform` は UI 要素（例えば、ボタン、画像、テキストなど）に使用され、UI のレイアウトに特化しています。

<br>

## `RectTransform` の主なプロパティ

| プロパティ名         | 型              | 説明                                                                                                                                                 | 使用例                                                                                                                                         |
|----------------------|-----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| `anchoredPosition`    | `Vector2`       | 親 `RectTransform` に対するローカル位置を設定または取得。                                                                                         | `rectTransform.anchoredPosition = new Vector2(100, 200);`                                                                                   |
| `sizeDelta`           | `Vector2`       | `RectTransform` の幅と高さを設定または取得。                                                                                                       | `rectTransform.sizeDelta = new Vector2(200, 100);`                                                                                          |
| `anchorMin`           | `Vector2`       | `RectTransform` の左下隅のアンカーを指定。0,0 が親の左下、1,1 が親の右上。                                                                        | `rectTransform.anchorMin = new Vector2(0, 0);`                                                                                             |
| `anchorMax`           | `Vector2`       | `RectTransform` の右上隅のアンカーを指定。                                                                                                        | `rectTransform.anchorMax = new Vector2(1, 1);`                                                                                             |
| `pivot`               | `Vector2`       | `RectTransform` の基準点を設定。0,0 が左下隅、1,1 が右上隅。                                                                                   | `rectTransform.pivot = new Vector2(0.5f, 0.5f);`                                                                                          |
| `rotation`            | `Quaternion`    | `RectTransform` の回転を設定または取得。                                                                                                          | `rectTransform.rotation = Quaternion.Euler(0, 0, 45);`                                                                                   |

<br>

<br>

---

<br>

<br>

# スクリーンポジション（Screen Position）について

スクリーンポジションは、ワールド空間の座標をスクリーン（画面上）の座標に変換したものです。UI 要素は通常、スクリーン座標系（ピクセル単位）で配置されますが、ゲームオブジェクトや 3D オブジェクトはワールド座標系で位置を持っています。これを Unity の `Camera` クラスを使って変換します。

- **ワールド座標**: ゲームオブジェクトがシーン内で持っている位置。
- **スクリーン座標**: ゲームオブジェクトが画面上でどこに描画されるかを決定する座標。

<br>

## `Camera.WorldToScreenPoint` と `Camera.ScreenToWorldPoint`

- `WorldToScreenPoint`: ワールド座標をスクリーン座標に変換します。
- `ScreenToWorldPoint`: スクリーン座標をワールド座標に変換します。

これらを使うことで、例えばワールド内のキャラクターの位置を画面上に表示するUI（例えば、HPバー）に変換することができます。

<br>

---

<br>

# 使い方の例

## 1. `RectTransform` を使った UI の位置調整

以下のコードは、`RectTransform` を使って UI 要素（例えばボタン）を画面上で特定の位置に配置する方法です。

```csharp
using UnityEngine;

public class UIPositioning : MonoBehaviour
{
    public RectTransform rectTransform;

    void Start()
    {
        // RectTransform の位置を (100, 200) に設定
        rectTransform.anchoredPosition = new Vector2(100, 200);
        
        // サイズを変更
        rectTransform.sizeDelta = new Vector2(200, 100);
        
        // アンカーを画面の左下に設定
        rectTransform.anchorMin = new Vector2(0, 0);
        rectTransform.anchorMax = new Vector2(0, 0);
    }
}
```

上記のコードでは、`rectTransform` の位置を (100, 200) に設定し、サイズを `200x100` に変更しています。アンカーは左下隅に設定されています。


<br>

## 2. ワールド座標からスクリーン座標への変換

次に、ワールド座標をスクリーン座標に変換する方法を見てみましょう。例えば、ゲームオブジェクトの位置を画面上の位置に変換して表示する場合です。

```csharp
using UnityEngine;

public class WorldToScreenExample : MonoBehaviour
{
    public Camera mainCamera;

    void Update()
    {
        // ゲームオブジェクトのワールド座標をスクリーン座標に変換
        Vector3 screenPos = mainCamera.WorldToScreenPoint(transform.position);
        
        // スクリーン座標をコンソールに表示
        Debug.Log("スクリーン座標: " + screenPos);
    }
}
```

このコードでは、ゲームオブジェクト（`transform.position`）の位置をスクリーン座標に変換し、コンソールにその位置を表示しています。これにより、ゲームオブジェクトが画面上のどこに描画されるかを知ることができます。

<br>

## 3. スクリーン座標からワールド座標への変換

逆に、スクリーン座標をワールド座標に変換する例です。これを使うことで、UI 要素の位置をワールド空間の位置に変換することができます。

```csharp
using UnityEngine;

public class ScreenToWorldExample : MonoBehaviour
{
    public Camera mainCamera;

    void Update()
    {
        // マウスのスクリーン座標をワールド座標に変換
        Vector3 worldPos = mainCamera.ScreenToWorldPoint(Input.mousePosition);
        
        // ワールド座標をコンソールに表示
        Debug.Log("ワールド座標: " + worldPos);
    }
}
```

このコードでは、マウスの位置（スクリーン座標）をワールド座標に変換し、その位置をコンソールに表示しています。

<br>

---

---

<br>

# 関連する技術・単語

1. **アンカー（Anchor）**:   
`RectTransform` のアンカーは、UI 要素が親要素に対してどの位置で固定されるかを決定します。アンカーが `(0, 0)` に設定されていれば、UI 要素は親の左下隅に固定されます。
   
2. **ピボット（Pivot）**:   
`RectTransform` のピボットは、UI 要素の回転やスケーリングの基準点となる位置です。ピボットの位置によって、UI 要素の位置やサイズが変わります。

3. **スクリーン座標系（Screen Space）**:   
スクリーン座標系は、画面上でのピクセル単位の座標系です。ワールド座標系はシーン内の位置を表しますが、スクリーン座標系は画面上での位置を表します。

4. **ワールド座標系（World Space）**:   
ワールド座標系は、シーン内での絶対的な位置を表します。`Camera.WorldToScreenPoint` や `Camera.ScreenToWorldPoint` を使って、ワールド座標とスクリーン座標を相互に変換できます。

5. **Canvas**:   
Unity の UI システムでは、すべての UI 要素は `Canvas` 内に配置されます。`Canvas` はスクリーン座標系とワールド座標系をつなぐ役割も果たします。

---


<br>

<br>



<br>

<br>


