### **コマンドバッファ (Command Buffer) とは？**

**コマンドバッファ**は、Unityでカスタムレンダリング操作を行うための機能です。  
GPUに送る描画指示を効率的に管理するための「命令キュー」で、Unityのレンダリングパイプラインを拡張したり、特定のタイミングで特別な処理を挟むのに利用されます。

---

### **基本的な役割**
1. **描画命令の記録**:  
   描画命令やシェーダー操作を一括で記録し、特定のタイミングで実行します。これにより、複雑な描画処理を効率的に管理できます。

2. **レンダリングパイプラインのカスタマイズ**:  
   - 特定のカメラやレンダリングステージに独自の処理を追加できます。
   - 後処理エフェクト、オブジェクトの特殊な描画、マルチパスレンダリングなどに使われます。

3. **パフォーマンス向上**:  
   コマンドを一括でGPUに送ることで、ドローコールのオーバーヘッドを軽減します。

---

### **特徴**
- **遅延実行**:  
  コマンドは即座に実行されず、バッファに記録されて後でまとめて実行されます。

- **自由な挿入タイミング**:  
  特定のレンダリングステージ（例: Before Rendering、After Rendering）に処理を挿入できます。

- **カスタマイズ性**:  
  標準の描画方法では実現できない特殊な処理を、任意に実装可能です。

---

### **基本的な使い方**
以下はUnityでのコマンドバッファの基本的な利用手順です：

#### **1. CommandBufferの作成**
```csharp
using UnityEngine;
using UnityEngine.Rendering;

public class CommandBufferExample : MonoBehaviour
{
    private CommandBuffer commandBuffer;

    void Start()
    {
        // コマンドバッファを生成
        commandBuffer = new CommandBuffer();
        commandBuffer.name = "Custom Command Buffer";

        // 描画命令の記録
        RenderTargetIdentifier cameraTarget = BuiltinRenderTextureType.CameraTarget;
        commandBuffer.ClearRenderTarget(true, true, Color.black); // 画面をクリア
        commandBuffer.SetRenderTarget(cameraTarget);             // 描画先を設定
        commandBuffer.DrawRenderer(GetComponent<Renderer>(), GetComponent<Renderer>().material); // オブジェクトを描画

        // カメラにコマンドバッファを追加
        Camera.main.AddCommandBuffer(CameraEvent.AfterEverything, commandBuffer);
    }

    void OnDestroy()
    {
        // 使用したコマンドバッファを解放
        if (commandBuffer != null)
        {
            Camera.main.RemoveCommandBuffer(CameraEvent.AfterEverything, commandBuffer);
            commandBuffer.Release();
        }
    }
}
```

---

### **主要メソッド**
以下は `CommandBuffer` の主要メソッドです：

#### **描画関連**
- `DrawRenderer`: 特定のオブジェクトを描画する。
- `Blit`: テクスチャをコピー、加工する。ポストプロセス処理などに利用。
- `SetRenderTarget`: 描画先を指定する。

#### **レンダリング制御**
- `ClearRenderTarget`: 描画ターゲットをクリアする。
- `SetGlobalTexture`: シェーダーで使用するテクスチャを設定する。

#### **シェーダー関連**
- `SetGlobalFloat/Vector/Matrix`: グローバル変数を設定する。
- `EnableShaderKeyword`: 特定のシェーダーキーワードを有効にする。

---

### **活用例**
#### **1. 後処理エフェクト**
シーン全体を描画した後にカスタムのエフェクトを追加。
```csharp
commandBuffer.Blit(sourceTexture, destinationTexture, customMaterial);
```

#### **2. 特定オブジェクトの強調表示**
あるオブジェクトだけを特定のマテリアルで再描画。
```csharp
commandBuffer.DrawRenderer(targetRenderer, highlightMaterial);
```

#### **3. 深度やステンシルバッファの操作**
深度バッファに基づいたエフェクト処理（例: 影やアウトライン）。

---

### **主な適用例**
- **カスタムポストプロセスエフェクト**: 通常のカメラエフェクトに独自の処理を追加。
- **描画の高速化**: 描画のバッチ処理でパフォーマンス向上。
- **シーン内の特定エフェクト**: 特定のオブジェクトだけ別の描画方法を適用。
- **シャドウやライトの特殊処理**: 標準のライトシステムを拡張。

---

コマンドバッファは、Unityのレンダリングを深くカスタマイズできる強力なツールです。シェーダーやレンダリングの知識と組み合わせて、ユニークな視覚効果を作り出すことが可能になります。











`Camera.main.AddCommandBuffer` を使用することで、カメラの描画パイプラインにカスタムコマンドを追加しています。この処理は、Unityの**レンダリングパイプライン**の特定のステージで実行されます。そして最終的に、GPUに送られた命令が画面上に描画されます。以下に詳しい流れを解説します。

---

### **1. コマンドバッファの追加**
```csharp
Camera.main.AddCommandBuffer(CameraEvent.AfterEverything, commandBuffer);
```
このコードは、**カメラの描画プロセスの特定のタイミング（`CameraEvent.AfterEverything`）** にカスタムのコマンドバッファを挿入しています。

- **`CameraEvent.AfterEverything`**:
  - これはカメラがすべての通常の描画処理（ジオメトリ、スカイボックス、透過オブジェクト、ポストプロセスなど）を終了した後に実行されるタイミングを指します。
  - このタイミングに追加されたコマンドバッファの処理は、最終的に**画面に描画される直前**に実行されます。

---

### **2. コマンドバッファの命令内容**
```csharp
commandBuffer.ClearRenderTarget(true, true, Color.black); // 画面をクリア
commandBuffer.SetRenderTarget(cameraTarget);             // 描画先を設定
commandBuffer.DrawRenderer(GetComponent<Renderer>(), GetComponent<Renderer>().material); // オブジェクトを描画
```
これにより、以下の手順が記録されます：
1. **`ClearRenderTarget`**:  
   現在の描画ターゲット（カメラのレンダーテクスチャ）を**黒でクリア**します。  
   これは画面を「初期化」する操作に相当します。

2. **`SetRenderTarget`**:  
   カメラの描画先（`BuiltinRenderTextureType.CameraTarget`）を指定します。  
   これにより、GPUに「ここに描画しなさい」という指示がされます。

3. **`DrawRenderer`**:  
   指定した `Renderer` のオブジェクトを指定した `Material` で描画します。  
   この命令が記録されることで、カスタム描画が実行されます。

---

### **3. 実行タイミング**
Unityの内部的なレンダリングプロセスにおいて、以下の順序で描画処理が進みます：

1. **カメラごとの描画プロセス開始**:
   - Unityが各カメラに関連付けられたシーン内のオブジェクトをレンダリングします。

2. **`CameraEvent` タイミングでのコマンドバッファの実行**:
   - `CameraEvent.AfterEverything` は通常の描画処理の最後にあたります。
   - このタイミングで、事前に記録されたコマンドバッファが**GPUに送信され、実行されます**。

3. **画面への描画結果の反映**:
   - GPUで実行されたコマンドの結果が、画面に出力されます。
   - カメラが描画しているレンダーテクスチャ（通常はフレームバッファ）がそのままディスプレイに表示されます。

---

### **4. 実際に確認できる内容**
このコードでは、以下の内容を確認できます：
1. カメラの描画結果がすべて消去され、黒で塗りつぶされます（`ClearRenderTarget` による影響）。
2. アタッチされた `Renderer` が、その `Material` を使用して描画されます。

---

### **補足: 複数のカメラがある場合**
- 上記のコードは `Camera.main` に対してのみコマンドバッファを追加しています。
- 他のカメラには影響しません。
- 複数カメラを使用している場合、ターゲットとなるカメラを明確に指定する必要があります。

---

### **まとめ**
- コマンドバッファは、`CameraEvent` によってカメラの描画パイプラインに挿入され、GPUで最終的に実行されます。
- この例では、`CameraEvent.AfterEverything` で命令が実行され、黒い背景と特定のオブジェクトの描画結果が画面に表示されます。