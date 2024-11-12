<head>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>


大まかなイメージ

<div class="mermaid">

graph TD
    A[Textの入力：<br>ユーザーが入力する文字列] -->|入力文字列| B[TextMeshProComponent：<br>描画するテキストの管理]
    B -->|フォントや色などの指定| C[TextMeshProFontAsset：<br>フォントやアトラス情報の保持]
    C -->|文字の形状データ要求| D[OTF/TTF FontAsset：<br>フォントの基本データ]
    C -->|グリフ画像の参照| E[TextMeshProFontAtlas：<br>グリフ（文字画像）の集合]
    D -->|グリフ形状データの提供| E
    E -->|指定文字のグリフ情報| F[グリフ情報の取得：<br>各文字の形状データ取得]
    F -->|UV座標の計算| G[UVマッピングの設定<br>テクスチャの位置設定]
    G -->|頂点情報とUV座標| H[Mesh生成<br>文字列全体のメッシュ構築]
    H -->|生成されたMesh| I[MeshFilterComponent<br>メッシュの保持]
    I -->|メッシュデータを提供| J[MeshRendererComponent<br>メッシュの描画処理]
    J -->|最終的な描画結果| K[描画<br>テキストをシーンに表示]

    E -. グリフ画像（アトラス） -.-> F
    G -. UVマップ -.-> E

</div>


### 各ステップの詳細

1. **Textの入力**  
   - **概要**：ユーザーが入力した文字列が `TextMeshProComponent` に渡されます。
   - **例**：ユーザーが「Hello World」を入力。

2. **TextMeshProComponent**  
   - **役割**：テキストの内容やフォント設定を管理し、描画の指示を出します。
   - **渡されるデータ**：フォント、色、サイズなどの情報が含まれる。

3. **TextMeshProFontAsset**  
   - **役割**：フォントやグリフ情報のアセットを保持し、描画に必要なデータを参照します。
   - **渡されるデータ**：テキストに対応する `OTF/TTF FontAsset`（フォントファイル）と `TextMeshProFontAtlas`（グリフ画像の集合）。

4. **OTF/TTF FontAsset**  
   - **役割**：ベクターデータで定義された文字形状を持つフォントファイルです。
   - **渡されるデータ**：指定された文字のベクターデータ（形状）。

5. **TextMeshProFontAtlas**  
   - **役割**：フォントのグリフ（各文字の形状）を画像化したテクスチャ（アトラス）です。
   - **渡されるデータ**：テキスト中の各文字に対応するグリフのビットマップ画像。

6. **グリフ情報の取得**  
   - **役割**：指定された文字ごとに、アトラスからグリフのビジュアル情報を取得します。
   - **渡されるデータ**：各文字の形状データ（頂点やUVマッピングの元データ）。

7. **UVマッピングの設定**  
   - **役割**：アトラス内のグリフ画像に対するUV座標を設定し、各文字が正しく表示されるための位置情報を指定します。
   - **渡されるデータ**：各グリフの位置を指定するUV座標。

8. **Mesh生成**  
   - **役割**：UVマッピングを基に、文字列全体の形状データを表すMeshを生成します。
   - **渡されるデータ**：生成された Mesh データ（頂点座標、インデックス、UV情報）。

9. **MeshFilterComponent**  
   - **役割**：生成された Mesh を保持し、描画のために `MeshRendererComponent` に渡します。
   - **渡されるデータ**：メッシュデータを保持。

10. **MeshRendererComponent**  
    - **役割**：メッシュデータを受け取り、シーンにテキストを描画する処理を行います。
    - **渡されるデータ**：シーンのレンダラーにメッシュを送り描画を実行。

11. **描画**  
    - **概要**：最終的にテキストが指定されたフォント、サイズ、色でシーンに表示されます。