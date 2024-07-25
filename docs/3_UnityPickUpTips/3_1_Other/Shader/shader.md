# Shader

基本的にはC#からいじる方法、HLSLやCG言語で書く方法、Shader Graphを使用する方法が色々あります。

使用したい目的や表現のShader記事を検索してヒットすれば、それを模倣すればいいと思いますが、ある程度意味を理解したい場合は勉強してみましょう

<br>

# 参考0  

公式Youtube    
シェーダを書けるプログラマになろう #1  
https://www.youtube.com/watch?v=wUx_Y9BgC7k


[上記に関するスライド等](https://drive.google.com/drive/folders/1ag0gMAOHYUzGGLT-Oar-vHUnkxp9Rg6u)

<br>

# 参考1

そろそろShaderをやる  
https://zenn.dev/kento_o

Unity ShaderGraph CookBook
https://zenn.dev/r_ngtm/books/shadergraph-cookbook  
https://zenn.dev/r_ngtm

<br>

# 参考2

第1章 Unityではじめるプロシージャルモデリング   
第2章 ComputeShader入門  
第3章 群のシミュレーションのGPU実装   
第4章 格子法による流体シミュレーション   
第5章 SPH法による流体シミュレーション   
第6章 ジオメトリシェーダーで草を生やす  
第7章 雰囲気で始めるMarchingCubes入門   
第8章 MCMCで行う3次元空間サンプリング   
第9章 MultiPlanePerspectiveProjection   


サンプル
[https://github.com/IndieVisualLab/UnityGraphicsProgramming?tab=readme-ov-file](https://github.com/IndieVisualLab/UnityGraphicsProgramming?tab=readme-ov-file)


Document
[https://github.com/IndieVisualLab/UnityGraphicsProgrammingSeries?tab=readme-ov-file](https://github.com/IndieVisualLab/UnityGraphicsProgrammingSeries?tab=readme-ov-file)

<br>

<br>


# Unityでは基本VertexとFragmentをいじる
基本的にはUnityのShaderでは、**Vertex Shader**と**Fragment Shader**の2つを主に使用します。この2つは、シェーダープログラムの主要な部分を構成し、それぞれ異なる役割を果たします。

<br>

# UnityにおけるShader記述方法

Unityでは、シェーダーを記述する方法として**ShaderLab**という高レベルのスクリプト言語が使用されます。ShaderLabは、HLSL（High-Level Shading Language）コードを含むことができます。

<br>



# サンプル

この例は、基本的なテクスチャマッピングシェーダーの流れを示しています。Vertex Shaderで頂点を処理し、Fragment Shaderでテクスチャから色をサンプリングして出力しています。


```csharp
Shader "Custom/MyShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            sampler2D _MainTex;

            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
            };

            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            float4 frag (v2f i) : SV_Target
            {
                float4 texColor = tex2D(_MainTex, i.uv);
                return texColor;
            }
            ENDCG
        }
    }
}
```

<br>

# Vertex Shader

- **役割**: 頂点の位置や属性（法線、UV座標など）を処理します。
- **主な機能**:
  - モデル空間からビュー空間、そしてクリップ空間への頂点の変換。
  - ライティング計算のための頂点ごとの法線変換。
  - テクスチャ座標やその他の頂点属性の計算と伝達。
- **コード例**:
  ```glsl
  // HLSL for Unity's vertex shader
  struct appdata
  {
      float4 vertex : POSITION;
      float3 normal : NORMAL;
      float2 uv : TEXCOORD0;
  };

  struct v2f
  {
      float2 uv : TEXCOORD0;
      float4 pos : SV_POSITION;
  };

  v2f vert (appdata v)
  {
      v2f o;
      o.pos = UnityObjectToClipPos(v.vertex);
      o.uv = v.uv;
      return o;
  }
  ```

<br>

# Fragment Shader (Pixel Shader)

- **役割**: 各ピクセルの色を計算します。
- **主な機能**:
  - テクスチャからの色のサンプリング。
  - ライティング計算（ディフューズ、スペキュラ、陰影処理など）。
  - その他のピクセルごとのエフェクト（例えば、ノーマルマッピング、パララックスマッピングなど）。
- **コード例**:
  ```glsl
  // HLSL for Unity's fragment shader
  sampler2D _MainTex;
  float4 _MainTex_ST;

  struct v2f
  {
      float2 uv : TEXCOORD0;
      float4 pos : SV_POSITION;
  };

  float4 frag (v2f i) : SV_Target
  {
      float4 texColor = tex2D(_MainTex, i.uv);
      return texColor;
  }
  ```

# Pipelineの流れ

1. **頂点データの入力**:
   - モデルの頂点データが頂点シェーダーに渡されます。
2. **頂点シェーダーの処理**:
   - 各頂点の位置がクリップ空間に変換され、頂点属性が計算されます。
3. **ラスタライゼーション**:
   - 変換された頂点からプリミティブ（トライアングル、ライン、ポイントなど）が生成され、ピクセルごとのデータに分割されます。
4. **フラグメントシェーダーの処理**:
   - 各ピクセルの色が計算され、テクスチャやライティングが適用されます。
5. **フレームバッファへの出力**:
   - 計算されたピクセルの色が最終的に画面に描画されます。

<br>

# サンプルプログラムの詳細

下記シェーダーは、`Shader`構文を使って定義され、`Custom/MyVertexShader`という名前が付けられています。`Properties`ブロックと`SubShader`ブロックを持ち、頂点シェーダー（Vertex Shader）とフラグメントシェーダー（Fragment Shader）を含んでいます。

```csharp
Shader "Custom/MyVertexShader"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            // ここでVertex Shaderとして使用する関数を指定
            #pragma vertex vert
            #pragma fragment frag

            // サンプラー変数の宣言
            sampler2D _MainTex;

            // 頂点データの構造体
            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            // Vertex ShaderからFragment Shaderに渡されるデータの構造体
            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
            };

            // Vertex Shaderの関数
            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            // Fragment Shaderの関数
            float4 frag (v2f i) : SV_Target
            {
                float4 texColor = tex2D(_MainTex, i.uv);
                return texColor;
            }
            ENDCG
        }
    }
}
```

### 詳細解説

1. **Shader "Custom/MyVertexShader"**:
   - シェーダーの名前を定義しています。これはUnityエディター内でシェーダーを識別するための名前です。

2. **Properties**:
   - シェーダーのプロパティを定義するブロックです。このシェーダーでは、2Dテクスチャ `_MainTex` を宣言しています。

    ```csharp
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
    }
    ```

    - `_MainTex ("Texture", 2D) = "white" {}`: `_MainTex`という名前の2Dテクスチャプロパティを宣言しています。デフォルト値は白（"white"）です。

3. **SubShader**:
   - シェーダーの主要な部分を定義するブロックです。`SubShader`ブロックには、シェーダーパスを定義する`Pass`ブロックが含まれています。

    ```csharp
    SubShader
    {
        Pass
        {
            CGPROGRAM
            // ここでVertex Shaderとして使用する関数を指定
            #pragma vertex vert
            #pragma fragment frag

            // サンプラー変数の宣言
            sampler2D _MainTex;

            // 頂点データの構造体
            struct appdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            // Vertex ShaderからFragment Shaderに渡されるデータの構造体
            struct v2f
            {
                float2 uv : TEXCOORD0;
                float4 pos : SV_POSITION;
            };

            // Vertex Shaderの関数
            v2f vert (appdata v)
            {
                v2f o;
                o.pos = UnityObjectToClipPos(v.vertex);
                o.uv = v.uv;
                return o;
            }

            // Fragment Shaderの関数
            float4 frag (v2f i) : SV_Target
            {
                float4 texColor = tex2D(_MainTex, i.uv);
                return texColor;
            }
            ENDCG
        }
    }
    ```

4. **CGPROGRAM**:
   - シェーダーコードの開始を示します。このブロック内にCg/HLSLコードを書きます。

5. **#pragma vertex vert**:
   - Vertex Shaderとして使用する関数 `vert` を指定します。

6. **#pragma fragment frag**:
   - Fragment Shaderとして使用する関数 `frag` を指定します。

7. **sampler2D _MainTex**:
   - サンプラー変数 `_MainTex` を宣言します。この変数はテクスチャをサンプリングするために使用されます。

8. **構造体 `appdata` と `v2f`**:
   - `appdata`構造体は、頂点データを表します。`vertex`フィールドは頂点位置、`uv`フィールドはテクスチャ座標を含みます。
   - `v2f`構造体は、Vertex ShaderからFragment Shaderに渡されるデータを表します。`uv`フィールドはテクスチャ座標、`pos`フィールドはクリップ空間の頂点位置を含みます。

    ```csharp
    struct appdata
    {
        float4 vertex : POSITION;
        float2 uv : TEXCOORD0;
    };

    struct v2f
    {
        float2 uv : TEXCOORD0;
        float4 pos : SV_POSITION;
    };
    ```

9. **Vertex Shader 関数 `vert`**:
   - `appdata`構造体を入力とし、`v2f`構造体を出力します。
   - `UnityObjectToClipPos(v.vertex)`関数を使って、頂点位置をオブジェクト空間からクリップ空間に変換します。
   - 入力頂点データのUV座標をそのまま出力します。

    ```csharp
    v2f vert (appdata v)
    {
        v2f o;
        o.pos = UnityObjectToClipPos(v.vertex);
        o.uv = v.uv;
        return o;
    }
    ```

10. **Fragment Shader 関数 `frag`**:
    - `v2f`構造体を入力とし、色値を出力します。
    - `tex2D(_MainTex, i.uv)`関数を使って、テクスチャ `_MainTex` からサンプリングした色を取得します。

    ```csharp
    float4 frag (v2f i) : SV_Target
    {
        float4 texColor = tex2D(_MainTex, i.uv);
        return texColor;
    }
    ```

11. **ENDCG**:
    - Cgプログラムの終了を示します。

### まとめ

このシェーダーは、テクスチャマッピングされたオブジェクトをレンダリングするシンプルなシェーダーです。  
頂点シェーダーで頂点の位置とUV座標を計算し、フラグメントシェーダーでテクスチャから色をサンプリングして出力します。  


<br>

# その他のシェーダータイプ

高度なシェーダーでは、**Geometry Shader**や**Compute Shader**なども使用されることがありますが、基本的なシェーダーの理解としては、Vertex ShaderとFragment Shaderをしっかりと押さえておくことが重要です。

<br>


