<img src="images/" width="90%" alt="" title="">


Unityの**Canvas**は、UI要素を画面上に表示するための基盤として使用されるコンポーネントで、特にユーザーインターフェースを構築する際に重要です。

Canvasを使うことで、画面解像度やサイズに対応したスケーリングや配置が可能になります。



以下、Canvasの仕組みや種類、設定項目、使い方について詳しく説明します。

<br>

# 1. **Canvasの仕組みと役割**
- **Canvasコンポーネント**は、画面上のUI要素（テキスト、ボタン、画像など）を管理するための基礎です。

- Canvasを利用してUI要素を表示するには、Canvasオブジェクトを作成し、その子オブジェクトとしてボタンやテキストなどのUI要素（GameObject）を追加します。この構造にすることで、UI要素がCanvasに従い、画面全体やビューポートに対して適切に表示されるようになります

- Canvasには複数の設定項目があり、それぞれの設定によってレンダリング順が変わります。

<br>

# 2. **Canvasの種類**
Canvasには、以下の3つのレンダリングモードがあり、各モードによってUIの表示方法や制御方法が異なります。

## a. **Screen Space - Overlay（スクリーンスペース・オーバーレイ）**
- **UIが常に画面の最前面に表示**され、シーン内のカメラの影響を受けません。
- 解像度やアスペクト比に関係なく、画面サイズに合わせてUIが自動でスケーリングされます。
- **通常のUI（メニュー、HUDなど）** を表示するのに最適です。

## b. **Screen Space - Camera（スクリーンスペース・カメラ）**
- UIは特定のカメラによってレンダリングされます。Canvasをリンクさせるカメラを指定する必要があります。
- カメラの位置や向きによって影響を受けるため、奥行きのあるUIやUIエフェクトが必要な場合に使用されます。
- UIの配置はカメラのビューポートに基づき、画面サイズに応じてスケールや位置が変わります。

## c. **World Space（ワールドスペース）**
- UI要素が3Dオブジェクトとして扱われ、シーン内の他のオブジェクトと同様に、座標とスケールを自由に設定できます。
- 3D空間内での位置や回転が可能で、たとえばゲーム内の看板やインタラクティブな3DオブジェクトとしてUIを配置したい場合に最適です。
- カメラからの距離や角度の影響を受け、視点に応じてUIの見え方が変化します。

<br>

# 3. **Canvasの設定項目**
Canvasにはいくつかの重要な設定があり、それぞれの設定がUIの描画方法やパフォーマンスに影響します。

## a. **Render Mode**
- **Overlay、Camera、World**のいずれかを選択し、UIがどのように表示されるかを決定します。

## b. **Canvas Scaler**
- Canvasのスケーリング方法を設定し、異なる解像度に対応します。
  - **Constant Pixel Size**: 常に同じピクセル数で表示。解像度が変わっても、UIのサイズは一定。
  - **Scale with Screen Size**: 画面サイズに合わせてスケール。指定した解像度基準で自動的にスケールされます。
  - **Constant Physical Size**: 実際の物理サイズ（インチ）を基準にスケールし、デバイスのDPIに対応します。

## c. **Additional Shader Channels**
- 必要な追加のシェーダーチャンネルを設定するオプションです。たとえば、**Normal**や**Tangent**などを選択することで、よりリッチなグラフィックス表現が可能です。

## d. **Sorting LayerとOrder in Layer**
- Canvasが描画される**順序**を指定し、重なり順を調整します。
- **複数のCanvas**がある場合、この順序を変更することでUIが上に描画されるか、下に描画されるかを管理できます。

# 4. **Canvasを使用した基本的なUIの作成**
以下は、簡単なボタンをCanvas上に配置するコード例です。

```csharp
using UnityEngine;
using UnityEngine.UI;

public class UIButtonExample : MonoBehaviour
{
    void Start()
    {
        // Canvasの作成
        GameObject canvasObj = new GameObject("Canvas");
        Canvas canvas = canvasObj.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        
        // Canvas Scalerの設定
        CanvasScaler scaler = canvasObj.AddComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1920, 1080);

        // ボタンの作成
        GameObject buttonObj = new GameObject("Button");
        buttonObj.transform.SetParent(canvasObj.transform);
        
        // ボタンにRectTransformとImageを追加
        RectTransform rectTransform = buttonObj.AddComponent<RectTransform>();
        rectTransform.sizeDelta = new Vector2(160, 60);
        Button button = buttonObj.AddComponent<Button>();

        // ボタンにテキストを追加
        GameObject textObj = new GameObject("ButtonText");
        textObj.transform.SetParent(buttonObj.transform);
        Text text = textObj.AddComponent<Text>();
        text.text = "Click Me";
        text.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        text.alignment = TextAnchor.MiddleCenter;
        text.rectTransform.sizeDelta = rectTransform.sizeDelta;
    }
}
```

<br>

# 5. **関連技術・概念**
- **RectTransform**: Canvas上のUI要素を配置するためのコンポーネントで、UIの位置やサイズを制御します。
- **Anchors（アンカー）**: RectTransformでUIを親オブジェクトに対して相対的に配置し、画面サイズの変化に応じたリサイズを可能にします。
- **Pivot（ピボット）**: UI要素の中心位置を設定するプロパティで、要素の回転やスケーリングの基準になります。

<br>

# 6. **Canvasにおけるパフォーマンスの考慮点**
- **Canvasの分割**: 動的に変更されるUI要素を別のCanvasに分けることで、再描画の負荷を低減できます。
- **Batching（バッチ処理）**: UI要素をまとめて描画することで、処理負荷を軽減します。Canvasが頻繁に更新される場合、過剰な再描画を防ぐためにバッチ処理を活用します。
  
Canvasは、画面上でのインターフェースの描画や操作性に重要な役割を果たし、UIの位置や見栄えを管理する上で非常に重要なコンポーネントです。