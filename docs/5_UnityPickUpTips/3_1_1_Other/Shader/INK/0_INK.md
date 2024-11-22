サンプルプログラム

「5_UnityPickUpTips　> 1_Other　> 15_1_Shader_Mesh > 1_3_INK 」参照

<br>

<br>

# 全体の流れ


① **`MousePainter.cs`** がインクを塗る位置や色、大きさ、強さを決定し、**`PaintManager.cs`** に渡す。  
② **`PaintManager.cs`** が受け取った情報を基に、**`Paintable.cs`** がアタッチされたオブジェクトのテクスチャに対して、`CommandBuffer` と`shader`を使用し、描画処理を実行  
③ **`Paintable.shadergraph`** が、描画されたテクスチャを元にオブジェクトの最終的な見た目を決定し、**`MeshRenderer`** がそのビジュアルを表示。

<br>

<br>

## 1. **`MousePainter.cs` でインクを塗る位置とパラメータを決める**
   - `MousePainter.cs` は、ユーザーのマウスの位置（`hit.point`）やインタラクションを処理します。
   - ユーザーがどこにインクを塗るのか、どんな色、サイズ、強さでペイントするのかを決め、それらの情報（ペイントする位置、色、大きさ、強さなど）を `PaintManager.cs` に渡します。

## 2. **`PaintManager.cs` でペイントの処理を行う**
   - `PaintManager.cs` は、実際にペイント処理を行うクラスです。
   - `MousePainter.cs` から受け取ったインクの位置・色・サイズ・強さなどの情報を基に、`Paintable.cs` から取得したテクスチャ（`maskRenderTexture` や `supportTexture` など）に対して描画を行います。
   - `CommandBuffer` を使って、ペイントする対象のテクスチャに対して描画処理を実行します。
     - `TexturePainter.shader` や `ExtendIslands.shader` が使われ、インクを塗る際のシェーダー処理が行われます。
     - `CommandBuffer` は、この描画処理を効率的に行うために、複数の描画命令を一度に実行します。

## 3. **`Paintable.shadergraph` で最終的な見た目を決定**
   - `Paintable.shadergraph` で作成された `Material` が、最終的にオブジェクトの見た目を決定します。
   - `Paintable.shadergraph` は、ペイントされたテクスチャ（ `maskRenderTexture` ・ `supportTexture`・`uvIslandsRenderTexture`、`extendIslandsRenderTexture` ）を使って、オブジェクトのビジュアルを計算します。
     - 具体的には、テクスチャ情報に基づいて色や質感を変更し、`MeshRenderer` を通じて最終的な描画が行われます。
   - これにより、インクが塗られた場所やその色、テクスチャが反映された見た目がオブジェクトに表示されます。

<br>

---

<br>

##  **TexturePainter.shader** と **ExtendIslands.shader** の役割

### **TexturePainter.shader**
このシェーダーは、ペイントするための実際の処理を担当します。  
例えば、マウスの位置に基づいて、指定した半径内で色を塗る処理を行います。

- **入力**:   
`PainterPosition`（ペイントする位置）  
`Radius`（塗る範囲の半径）  
`Strength`（塗る強度）  
`PainterColor`（塗る色）  
など

- **出力**:   
塗られるオブジェクトのテクスチャを更新（色を加える）

<br>

### **ExtendIslands.shader**
このシェーダーは、ペイントされたエリアを拡張するためのシェーダーです。  
例えば、ペイントの境界をスムーズにするためや、ペイントが施されているエリアの周囲を拡張するために使います。

- **入力**:   
`UVIslands`（ペイント済みの領域）  
`OffsetUV`（拡張する距離）

- **出力**:  
拡張されたペイント範囲を持つ新しいテクスチャ

<br>
 
###  `PaintManager.cs`の**Graphics.ExecuteCommandBuffer(command)** での描画命令

最終的に、`Graphics.ExecuteCommandBuffer(command)` で描画処理が実行されます。このコマンドバッファは、どのオブジェクトに対してどのような描画処理を行うかを指示するために使われます。

- **コマンドバッファの作成**:  
 `Graphics.ExecuteCommandBuffer` に渡すコマンドバッファ (`command`) は、描画対象（`Paintable.shadergraph` を適用したオブジェクトのマテリアル）に対してペイントやテクスチャの変更を行うための命令を含みます。
  
  例えば、`TexturePainter.shader` や `ExtendIslands.shader` で処理を行い、ペイントが施されたテクスチャを更新する命令が `command` に追加されます。これにより、指定したマテリアルに対してその命令が実行され、最終的に描画されます。












