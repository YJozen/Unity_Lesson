

#### **5. TexturePainter.shader**
- **役割**:
  - 実際のペイント処理を行うシェーダー。
  - マウス位置やペイント強度に基づいてテクスチャに色を適用。

- **主な機能**:
  - ペイントする色、ブラシの形状、強度、半径などを使用してテクスチャに描画。
  - GPU処理で効率よくペイントを適用。

- **依存関係**:
  - `PaintManager` が `Graphics.Blit` を通じて使用。
  - `MousePainter` を経由してペイントデータを反映。










# サンプルコード3



```shader
Shader "TNTC/TexturePainter"{   

    Properties{
        _PainterColor ("Painter Color", Color) = (0, 0, 0, 0)
    }

    SubShader{
        Cull Off ZWrite Off ZTest Off

        Pass{
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            #include "UnityCG.cginc"

			sampler2D _MainTex;    //ブラシのペイントを適用する基底の画像
            float4 _MainTex_ST;
            
            float3 _PainterPosition;//ペイントの中心座標  塗る位置　レイが判定した位置 3D空間でのブラシの描画位置
            float  _Radius;         //ペイントの半径。
            float  _Hardness;       //ペイントの硬さ（境界のぼやけ具合）。
            float  _Strength;       //ペイントの強度（どれだけはっきり色を塗るか）。
            float4 _PainterColor;   //ペイントする色
            float  _PrepareUV;      //特定の条件下でUV情報を可視化するフラグ

            struct appdata{
                float4 vertex : POSITION; //任意の座標情報
				float2 uv     : TEXCOORD0;//UV座標
            };

            struct v2f{
                float4 vertex   : SV_POSITION;//任意ではない座標情報
                float2 uv       : TEXCOORD0;  //UV座標
                float4 worldPos : TEXCOORD1;  //UV座標
            };

            //ペイントの効果を計算する。中心からの距離に基づいて、ペイントの濃さ(境界のぼやけ具合)（0～1）を決定
            //距離によって　返す値・数字(0~1)を返し　色付けの判断に使う]
            float mask(float3 position, float3 center, float radius, float hardness){
                float m = distance(center, position);               //centerとUV座標との距離を取得
                return 1 - smoothstep(radius * hardness, radius, m);//距離によって 0~1の値を返す
                //軌跡の大きさを計算 smoothstep(a,b,c) は cがa以下の時は0、b以上の時は1、  0～1は補間
                //1 - smoothstep(a,b,c)とすることで補間値を逆転できる　
                //つまり      1 - smoothstep(a,b,c) は  cがa以上の時は1、b以下の時は0、0～1は補間
            }

            //頂点
            v2f vert (appdata v){
                v2f o;
				o.worldPos = mul(unity_ObjectToWorld, v.vertex);//ワールド空間の位置をuv空間に変換する　uvアイランドを再作成　UVに重複する三角形がないことを意味する
                o.uv       = v.uv;
				float4 uv  = float4(0, 0, 0, 1);
                uv.xy      = float2(1, _ProjectionParams.x) * (v.uv.xy * float2( 2, 2 ) - float2(1, 1));//レンダリング投影行列　_ProjectionParams.x　＊  -1~1
                //uv.xy      = (v.uv.xy * 2 - 1) * float2(1, _ProjectionParams.x) ;//_ProjectionParams x は 1.0 または –1.0、反転した射影行列で現在レンダリングしている場合は負の値。
                o.vertex   = uv; 
                return o;
            }

            
            //フラグメント
            fixed4 frag (v2f i) : SV_Target{   
                if(_PrepareUV > 0 ){
                    return float4(0, 0, 1, 1);
                }         

                float4 col = tex2D(_MainTex, i.uv);
                float f    = mask(i.worldPos, _PainterPosition, _Radius, _Hardness);//0~1
                float edge = f * _Strength;
                return lerp(col, _PainterColor, edge);//背景色とブラシの色の間を補間
            }
            ENDCG
        }
    }
}

```




このシェーダーは、テクスチャ上で特定の位置を中心にブラシでペイントするような効果を実現するものです。以下に主要なポイントを解説します：

---

### 1. **プロパティ**
```hlsl
Properties{
    _PainterColor ("Painter Color", Color) = (0, 0, 0, 0)
}
```
- `Properties` セクションではシェーダーで使用するプロパティを定義します。
- `_PainterColor` はペイントする色を指定するためのプロパティです。

---

### 2. **サブシェーダー設定**
```hlsl
Cull Off ZWrite Off ZTest Off
```
- **`Cull Off`**: 両面のポリゴンを描画します。
- **`ZWrite Off`**: 深度バッファへの書き込みを無効にします。
- **`ZTest Off`**: 深度テストを無効にします。
  - これらは、平面やUVにマッピングされたテクスチャを直接操作するために設定されています。

---

### 3. **主要な変数**
- **`_PainterPosition`**: ペイントする中心位置。
- **`_Radius`**: ブラシの半径。
- **`_Hardness`**: ブラシの硬さ（エッジの柔らかさに影響）。
- **`_Strength`**: ペイントの強度。
- **`_PrepareUV`**: UVマップを準備するためのフラグ。

---

### 4. **関数**
#### `mask` 関数
```hlsl
float mask(float3 position, float3 center, float radius, float hardness){
    float m = distance(center, position);
    return 1 - smoothstep(radius * hardness, radius, m);
}
```
- この関数はペイントの影響範囲を決定します。
- 中心 (`center`) からの距離 `m` に基づき、影響値（0~1）を返します。
- `smoothstep` を使用してエッジを滑らかに補間します。

---

### 5. **頂点シェーダー**
```hlsl
v2f vert (appdata v){
    v2f o;
    o.worldPos = mul(unity_ObjectToWorld, v.vertex);
    o.uv       = v.uv;
    float4 uv  = float4(0, 0, 0, 1);
    uv.xy      = float2(1, _ProjectionParams.x) * (v.uv.xy * float2(2, 2) - float2(1, 1));
    o.vertex   = uv;
    return o;
}
```
- 頂点のワールド座標を取得し、UV空間に変換します。
- `unity_ObjectToWorld` はオブジェクト空間からワールド空間への変換行列です。
- `_ProjectionParams.x` を利用して、レンダリングする空間の範囲を設定します。

---

### 6. **フラグメントシェーダー**
```hlsl
fixed4 frag (v2f i) : SV_Target{   
    if(_PrepareUV > 0 ){
        return float4(0, 0, 1, 1);
    }         

    float4 col = tex2D(_MainTex, i.uv);
    float f    = mask(i.worldPos, _PainterPosition, _Radius, _Hardness);
    float edge = f * _Strength;
    return lerp(col, _PainterColor, edge);
}
```
- UV準備モード（`_PrepareUV` > 0）の場合は青色 (`float4(0, 0, 1, 1)`) を返します。
- テクスチャの既存の色（`col`）と、ペイントする色（`_PainterColor`）を `lerp` 関数で補間します。
  - `lerp(a, b, t)` は `a` から `b` への補間を `t` の割合で行う関数です。

---

### 7. **ペイントプロセス**
- ペイントされるピクセルは、`mask` 関数の結果と `lerp` によって柔らかなエッジを持つグラデーションになります。
- `_PrepareUV` フラグが有効であれば、UV領域の準備が行われます。

---

### 8. **改善点と補足**
1. **UV空間の制御**:
   - `v2f.vert` で `_ProjectionParams` を使っていますが、UV変換が独自の投影ロジックを前提としている場合、調整が必要になるかもしれません。
2. **エラー処理**:
   - `tex2D` の座標が不正である場合、アーティファクトが発生する可能性があります。
3. **パフォーマンス**:
   - `mask` 関数内で `distance` を計算する部分は頻繁に使用されるため、場合によっては最適化が必要です（例えば、距離の平方値を使う）。

---

このシェーダーは、特定の位置にペイントするリアルタイム描画アプローチに最適化されています。UV変換の前後や、テクスチャ合成が正しく動作しているかを確認しながら使用してください。










