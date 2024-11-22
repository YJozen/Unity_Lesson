

#### **4. ExtendIslands.shader**
- **役割**:
  - UVアイランド（UV座標に基づく分離領域）の境界を広げて、テクスチャのピクセルを埋める。
  - 境界に近いピクセルの色を利用して、周囲を補完。

- **主な機能**:
  - ペイント処理時に、UVアイランド外でも滑らかに色が広がるようにする。
  - ペイントエフェクトの「にじみ」や「ぼかし」を実現。

- **依存関係**:
  - `PaintManager` から呼び出される可能性がある（例: ペイント結果を後処理で拡張）。

---


# サンプルコード4

```shader
Shader "TNTC/ExtendIslands"{
    Properties{
        _MainTex   ("Texture", 2D) = "white" {}           //元となるテクスチャ。
        _UVIslands ("Texture UVIsalnds", 2D) = "white" {} //UVアイランド情報を含むテクスチャ。
        _OffsetUV  ("UVOffset", float) = 1                //UVのオフセット量。テクスチャ座標の拡張を調整
    }

    SubShader{
        Tags { "RenderType"="Opaque" }
        LOD 100

        Pass{
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #pragma target 3.0

            #include "UnityCG.cginc"

            struct appdata{
                float4 vertex : POSITION;
                float2 uv     : TEXCOORD0;
            };

            struct v2f{
                float2 uv     : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };


            //変数宣言
            sampler2D _MainTex;
            float4    _MainTex_ST;
            float4    _MainTex_TexelSize;
            float     _OffsetUV;
            sampler2D _UVIslands;

            //頂点
            v2f vert (appdata v){
                v2f o;
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.uv     = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            //フラグメント
            fixed4 frag (v2f i) : SV_Target{
                float2 offsets[8] = {float2(-_OffsetUV, 0), float2(_OffsetUV, 0), float2(0, _OffsetUV), float2(0, -_OffsetUV), float2(-_OffsetUV, _OffsetUV), float2(_OffsetUV, _OffsetUV), float2(_OffsetUV, -_OffsetUV), float2(-_OffsetUV, -_OffsetUV)};//UV座標を8方向にオフセットさせるためのベクトル
				float2 uv         = i.uv;
				float4 color      = tex2D(_MainTex, uv);
				float4 island     = tex2D(_UVIslands, uv);

                if(island.z < 1){
                    float4 extendedColor = color;
                    for	(int i = 0; i < offsets.Length; i++){
                        float2 currentUV      = uv + offsets[i] * _MainTex_TexelSize.xy;
                        float4 offsettedColor = tex2D(_MainTex, currentUV);
                        extendedColor         = max(offsettedColor, extendedColor);//最大値（max関数）を使用して、新しいピクセル色を拡張。
                    }
                    color = extendedColor;
                }
				return color;
            }
            ENDCG
        }
    }
}

```





このシェーダーは、UVアイランドの境界を拡張するために設計されています。特定の条件でテクスチャを周囲から取得して補間し、境界を滑らかにするような効果を持っています。以下に、コードの主要なポイントと改善点を解説します。

---

### 1. **プロパティ**
```hlsl
Properties{
    _MainTex   ("Texture", 2D) = "white" {}
    _UVIslands ("Texture UVIslands", 2D) = "white" {}
    _OffsetUV  ("UVOffset", float) = 1
}
```
- **`_MainTex`**: 主に描画するテクスチャ。
- **`_UVIslands`**: UVアイランドを表すマスクテクスチャ（おそらくZチャンネルに情報が格納されている）。
- **`_OffsetUV`**: UV座標のオフセット値（ピクセル単位でのオフセット距離）。

---

### 2. **サブシェーダー設定**
```hlsl
Tags { "RenderType"="Opaque" }
LOD 100
```
- **`RenderType="Opaque"`**: 描画タイプを不透明に設定。
- **`LOD 100`**: シェーダーのレベルオブディテール (LOD) を100に設定。

---

### 3. **主要な変数**
```hlsl
float2 offsets[8] = { ... }
```
- 近隣のピクセル（8方向）のオフセット値を計算します。
- `_MainTex_TexelSize.xy` を掛けることで、テクスチャのピクセルサイズに基づいた正確なオフセットを計算。

```hlsl
float4 color = tex2D(_MainTex, uv);
float4 island = tex2D(_UVIslands, uv);
```
- **`color`**: 現在のUV座標での `_MainTex` の色。
- **`island`**: `_UVIslands` テクスチャから取得したデータ。`island.z` を使用して条件分岐を行います。

---

### 4. **条件分岐**
```hlsl
if(island.z < 1){
    float4 extendedColor = color;
    for (int i = 0; i < offsets.Length; i++){
        float2 currentUV = uv + offsets[i] * _MainTex_TexelSize.xy;
        float4 offsettedColor = tex2D(_MainTex, currentUV);
        extendedColor = max(offsettedColor, extendedColor);
    }
    color = extendedColor;
}
```
- **条件**: `island.z < 1` の場合、境界ピクセルとして処理。
- **処理内容**: 
  - 周囲8ピクセルの色を取得。
  - `max` 関数を使って最も強い（明るい）色を選択。
  - 最終的な `color` を更新。

---

### 5. **頂点シェーダー**
```hlsl
v2f vert (appdata v){
    v2f o;
    o.vertex = UnityObjectToClipPos(v.vertex);
    o.uv     = TRANSFORM_TEX(v.uv, _MainTex);
    return o;
}
```
- **`UnityObjectToClipPos`**: 頂点のオブジェクト空間座標をクリップ空間に変換。
- **`TRANSFORM_TEX`**: UV座標をテクスチャのスケールとオフセットに基づいて変換。

---

### 6. **フラグメントシェーダー**
```hlsl
fixed4 frag (v2f i) : SV_Target{
    ...
    return color;
}
```
- 最終的なピクセルの色（`color`）を返します。

---

### 7. **改善点**
1. **パフォーマンス最適化**:
   - ループ内のテクスチャフェッチ（`tex2D`）は負荷が高いです。8方向すべてを計算せず、必要最小限の方向だけを考慮するロジックを検討するとよいでしょう。
2. **条件分岐の整理**:
   - 境界判定（`island.z < 1`）を複数条件で拡張可能にする（例: 複数チャンネルでの境界処理）。
3. **カラー計算の柔軟性**:
   - 現在は単純に `max` を取っていますが、グラデーションやブレンドを加えることでより自然な見た目を実現できます。

---

### 8. **用途と応用例**
- **UVアイランド境界の拡張**: 境界ピクセルに対して近隣ピクセルの色を適用することで、境界を拡張・補間する用途に使えます。
- **エッジ処理**: テクスチャのエッジを滑らかにすることで、アーティファクトを軽減できます。
- **マスクベースの操作**: `_UVIslands` を別の操作マスクとして使用することで、多用途な効果を実現可能です。

---

### 9. **動作確認ポイント**
- `_UVIslands` テクスチャのZチャンネルが適切に設定されているか確認。
- `_OffsetUV` と `_MainTex_TexelSize.xy` のスケーリングが適切に機能しているか確認。

---

このシェーダーは、特にUVアイランド境界の制御や補間に役立ちます。テクスチャ処理が多いため、高解像度のテクスチャで使用する場合は適切な最適化が必要です。













