サンプルフォルダ

「5_UnityPickUpTips > 1_Other > 15_1_Shader_Mesh > 0_1_Mesh_CS」
参照

## Shaderは
GPU上で動作するプログラムであり、
描画されるオブジェクトの見た目や振る舞いを定義します。  
これは、オブジェクトがどのように見えるか、どのように反応するかを制御します。

## Materialは、
Shaderを使用して実際の描画を行うためのプロパティやパラメータを設定するものです。  
Shaderは描画を行うための指示を与えるだけで、
Materialはその指示に必要な具体的な情報を提供します。  
たとえば、色、テクスチャ、反射率などの情報がMaterialに含まれます。

## MeshFilterは、
Mesh（メッシュ）と呼ばれる3Dオブジェクトの形状を定義するコンポーネントです。  
メッシュは頂点、法線、UVマップなどのジオメトリ情報を保持します。  
MeshFilterはそのメッシュデータを保持し、
それを他のコンポーネント（たとえばMeshRenderer）で描画するための情報を提供します。

## MeshRendererは、
実際にオブジェクトを描画するためのコンポーネントです。  
MeshFilterからメッシュ情報を受け取り、Materialから描画方法を受け取って、オブジェクトを描画します。

これらのコンポーネントと関連付けられた情報（Mesh、Material、Shaderなど）により、
Unity内で3Dオブジェクトを作成し、レンダリングすることが可能になります。



Shaderは描画方法を指定し、  
Materialは具体的な描画に必要な情報を提供し、  
MeshFilterは形状情報を提供し、  
MeshRendererは描画を行います。  


サンプルコード1
```cs
using UnityEngine;

namespace MeshSample {
    public class Mesh1 : MonoBehaviour
    {
        [SerializeField] Material material;

        void Start() {
            // 頂点の位置情報
            Vector3[] vertices = {
                new Vector3(-1f, -1f, 0), //配列内の0番目の要素
                new Vector3(-1f,  1f, 0), //配列内の1番目の要素
                new Vector3( 1f,  1f, 0), //配列内の2番目の要素
                new Vector3( 1f, -1f, 0)  //配列内の3番目の要素
            };

            //三角形を作る頂点の順番情報の指示の仕方　右回り正　左手座標系、右回りの回転で法線が決まる
            int[] triangles = { 0, 1, 2};

            Mesh mesh      = new Mesh();//Meshの入れ物　インスタンス　変数
            mesh.vertices  = vertices;  //頂点　情報　登録
            mesh.triangles = triangles; //三角形情報　登録

            mesh.RecalculateNormals(); //「面の向き」法線計算 (法線ベクトルの情報はmesh.normalsに入ってる)

            MeshFilter meshFilter       = gameObject.GetComponent<MeshFilter>();//ポリゴンの集合体　Mesh情報の登録先
            if (!meshFilter) meshFilter = gameObject.AddComponent<MeshFilter>();//MeshFilterをつける

            MeshRenderer meshRenderer       = gameObject.GetComponent<MeshRenderer>();
            if (!meshRenderer) meshRenderer = gameObject.AddComponent<MeshRenderer>();//MeshRendererをつける

            meshFilter.mesh = mesh;                 //MeshFilterにメッシュを設定
            meshRenderer.sharedMaterial = material; //MeshRendererに表示するマテリアル(材質情報　Shaderから)を設定
        }
    }
}
```


<br>

<br>

---

<br>

<br>

サンプルコード2
```cs
using UnityEngine;


namespace MeshSample
{
    //全体の流れ
    //頂点の位置情報(vertices)と
    //どの頂点で三角形を作るかという情報(triangles)を配列として用意し
    //それをメッシュに渡す
    public class Mesh2 : MonoBehaviour
    {
        [Range(2, 255)]
        [SerializeField] int size;//全体の頂点数 4なら4×4で16個 (1つのメッシュが持てる頂点数の限界65534個)
        [SerializeField] float vertexDistance = 1f;//頂点間の距離
        [SerializeField] Material material;
        [SerializeField] PhysicMaterial physicMaterial;

        void Start() {

            //サイズから配列用意
            Vector3[] vertices = new Vector3[size * size];
            //3の場合下のような位置情報を配列として持つ
            //012
            //345
            //678
            for (int z = 0; z < size; z++) {
                for (int x = 0; x < size; x++) {
                    vertices[z * size + x] = new Vector3(x * vertexDistance, 0, -z * vertexDistance);
                }
            }

            int triangleIndex = 0;
            int[] triangles = new int[(size - 1) * (size - 1) * 6];//すべての三角形の頂点数 2の場合6 　3の場合 24
            //頂点番号　　３つずつ　見て　meshが生成される
            for (int z = 0; z < size - 1; z++) {
                for (int x = 0; x < size - 1; x++) {
                    int a = z * size + x;
                    int b = a + 1;
                    int c = a + size;
                    int d = c + 1;

                    triangles[triangleIndex] = a;
                    triangles[triangleIndex + 1] = b;
                    triangles[triangleIndex + 2] = c;

                    triangles[triangleIndex + 3] = c;
                    triangles[triangleIndex + 4] = b;
                    triangles[triangleIndex + 5] = d;

                    triangleIndex += 6;
                }
            }

            Mesh mesh = new Mesh();
            mesh.vertices  = vertices; //meshに頂点情報(配列)
            mesh.triangles = triangles;//meshに三角形情報(配列)

            mesh.RecalculateNormals();//面

            MeshFilter meshFilter = gameObject.GetComponent<MeshFilter>();
            if (!meshFilter) meshFilter = gameObject.AddComponent<MeshFilter>();

            MeshRenderer meshRenderer = gameObject.GetComponent<MeshRenderer>();
            if (!meshRenderer) meshRenderer = gameObject.AddComponent<MeshRenderer>();

            MeshCollider meshCollider = gameObject.GetComponent<MeshCollider>();
            if (!meshCollider) meshCollider = gameObject.AddComponent<MeshCollider>();

            meshFilter.mesh             = mesh;
            meshRenderer.sharedMaterial = material;

            meshCollider.sharedMesh     = mesh;
            meshCollider.sharedMaterial = physicMaterial;
        }
    }
}
```


<br>

<br>

---

<br>

<br>

サンプルコード3
```cs
using UnityEngine;

//高さを加える
namespace MeshSample
{
    //全体の流れ
    //頂点の位置情報(vertices)と
    //どの頂点で三角形を作るかという情報(triangles)を配列として用意し
    //それをメッシュに渡す
    public class Mesh3 : MonoBehaviour
    {
        [Range(3, 255)]
        [SerializeField] int size;//全体の頂点数 4なら4×4で16個 (1つのメッシュが持てる頂点数の限界65534個)
        [SerializeField] float vertexDistance = 1f;//頂点間の距離
        [SerializeField] Material material;
        [SerializeField] PhysicMaterial physicMaterial;

        [SerializeField] float heightMultiplier = 1f;//高さ

        void Start() {

            //サイズから配列用意
            Vector3[] vertices = new Vector3[size * size];
            //3の場合下のような位置情報を配列として持つ
            //012
            //345
            //678
            for (int z = 0; z < size; z++) {
                for (int x = 0; x < size; x++) {
                    float y = Random.value * heightMultiplier;
                    vertices[z * size + x] = new Vector3(x * vertexDistance, y, -z * vertexDistance);//高さを入れてみる
                    //vertices[z * size + x] = new Vector3(x * vertexDistance, 0, -z * vertexDistance);
                }
            }

            int triangleIndex = 0;
            int[] triangles = new int[(size - 1) * (size - 1) * 6];//すべての三角形の頂点数 　3の場合 24
            //頂点番号　　３つずつ　見て　meshが生成される
            for (int z = 0; z < size - 1; z++) {
                for (int x = 0; x < size - 1; x++) {
                    int a = z * size + x;
                    int b = a + 1;
                    int c = a + size;
                    int d = c + 1;

                    triangles[triangleIndex] = a;
                    triangles[triangleIndex + 1] = b;
                    triangles[triangleIndex + 2] = c;

                    triangles[triangleIndex + 3] = c;
                    triangles[triangleIndex + 4] = b;
                    triangles[triangleIndex + 5] = d;

                    triangleIndex += 6;
                }
            }

            Mesh mesh = new Mesh();
            mesh.vertices  = vertices; //meshに頂点情報(配列)
            mesh.triangles = triangles;//meshに三角形情報(配列)

            mesh.RecalculateNormals();//面

            MeshFilter meshFilter = gameObject.GetComponent<MeshFilter>();
            if (!meshFilter) meshFilter = gameObject.AddComponent<MeshFilter>();

            MeshRenderer meshRenderer = gameObject.GetComponent<MeshRenderer>();
            if (!meshRenderer) meshRenderer = gameObject.AddComponent<MeshRenderer>();

            MeshCollider meshCollider = gameObject.GetComponent<MeshCollider>();
            if (!meshCollider) meshCollider = gameObject.AddComponent<MeshCollider>();

            meshFilter.mesh             = mesh;
            meshRenderer.sharedMaterial = material;

            meshCollider.sharedMesh     = mesh;
            meshCollider.sharedMaterial = physicMaterial;
        }
    }
}
```


<br>

<br>

---

<br>

<br>

サンプルコード4
```cs
using UnityEngine;

//パーリンノイズ
namespace MeshSample
{
    //全体の流れ
    //頂点の位置情報(vertices)と
    //どの頂点で三角形を作るかという情報(triangles)を配列として用意し
    //それをメッシュに渡す
    public class Mesh4 : MonoBehaviour
    {
        [Range(2, 255)]
        [SerializeField] int size;
        [SerializeField] float vertexDistance = 1f;//頂点間の距離
        [SerializeField] Material material;
        [SerializeField] PhysicMaterial physicMaterial;

        [SerializeField] PerlinNoiseProperty[] perlinNoiseProperty = new PerlinNoiseProperty[1];
        [System.Serializable]
        public class PerlinNoiseProperty
        {
            public float heightMultiplier = 1f;
            public float scale = 1f;
            public Vector2 offset;
        }

        void Start() {
            CreateMesh();
        }

        void CreateMesh() {
            Vector3[] vertices = new Vector3[size * size];
            for (int z = 0; z < size; z++) {
                for (int x = 0; x < size; x++) {

                    float sampleX;
                    float sampleZ;
                    float y = 0;
                    foreach (PerlinNoiseProperty p in perlinNoiseProperty) {//後から付け足したプロパティをy座標情報とし加算
                        p.scale = Mathf.Max(0.0001f, p.scale);
                        sampleX = (x + p.offset.x) / p.scale;
                        sampleZ = (z + p.offset.y) / p.scale;
                        y += Mathf.PerlinNoise(sampleX, sampleZ) * p.heightMultiplier;//PerlinNoise = 擬似ランダムパターン(白黒モザイクのやつ)　座標からPerlinNoiseの値取得
                    }

                    vertices[z * size + x] = new Vector3(x * vertexDistance, y, -z * vertexDistance);
                }
            }

            int triangleIndex = 0;
            int[] triangles = new int[(size - 1) * (size - 1) * 6];
            for (int z = 0; z < size - 1; z++) {
                for (int x = 0; x < size - 1; x++) {

                    int a = z * size + x;
                    int b = a + 1;
                    int c = a + size;
                    int d = c + 1;

                    triangles[triangleIndex] = a;
                    triangles[triangleIndex + 1] = b;
                    triangles[triangleIndex + 2] = c;

                    triangles[triangleIndex + 3] = c;
                    triangles[triangleIndex + 4] = b;
                    triangles[triangleIndex + 5] = d;

                    triangleIndex += 6;
                }
            }

            Mesh mesh      = new Mesh();
            mesh.vertices  = vertices;
            mesh.triangles = triangles;

            mesh.RecalculateNormals();

            MeshFilter meshFilter       = gameObject.GetComponent<MeshFilter>();
            if (!meshFilter) meshFilter = gameObject.AddComponent<MeshFilter>();

            MeshRenderer meshRenderer       = gameObject.GetComponent<MeshRenderer>();
            if (!meshRenderer) meshRenderer = gameObject.AddComponent<MeshRenderer>();

            MeshCollider meshCollider       = gameObject.GetComponent<MeshCollider>();
            if (!meshCollider) meshCollider = gameObject.AddComponent<MeshCollider>();

            meshFilter.mesh = mesh;
            meshRenderer.sharedMaterial = material;
            meshCollider.sharedMesh     = mesh;
            meshCollider.sharedMaterial = physicMaterial;
        }

        //インスペクタ上で数値が変更されるごとに自動で呼び出されるメソッドです。
        //size変数をあまり大きくしすぎると処理に時間がかかってしまうので、ほどほどに
        //void OnValidate() {
        //    CreateMesh();
        //}
    }
}
```


<br>

<br>

---

<br>

<br>

サンプルコード5
```cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//Meshに色を付ける
namespace MeshSample
{
    //全体の流れ
    //頂点の位置情報(vertices)と
    //どの頂点で三角形を作るかという情報(triangles)を配列として用意し
    //それをメッシュに渡す
    public class Mesh5 : MonoBehaviour
    {
        [Range(2, 255)]
        [SerializeField] int size;
        [SerializeField] float vertexDistance = 1f;//頂点間の距離
        [SerializeField] Material material;
        [SerializeField] PhysicMaterial physicMaterial;

        [SerializeField] PerlinNoiseProperty[] perlinNoiseProperty = new PerlinNoiseProperty[1];
        [System.Serializable]
        public class PerlinNoiseProperty
        {
            public float heightMultiplier = 1f;
            public float scale = 1f;
            public Vector2 offset;
        }

        [SerializeField] Gradient meshColorGradient;//色のグラデーション設定　ゲージの左端が0%(0.0)、右端が100%(1.0)　　(キーが最大で8個までしか登録できない)

        //地形の最も低い位置と最も高い位置を手動で設定できるように
        [SerializeField] float minHeight;
        [SerializeField] float maxHeight;


        void Start() {
            CreateMesh();
        }

        void CreateMesh() {
            Vector3[] vertices = new Vector3[size * size];
            for (int z = 0; z < size; z++) {
                for (int x = 0; x < size; x++) {

                    float sampleX;
                    float sampleZ;
                    float y = 0;
                    foreach (PerlinNoiseProperty p in perlinNoiseProperty) {//後から付け足したプロパティをy座標情報とし加算
                        p.scale = Mathf.Max(0.0001f, p.scale);
                        sampleX = (x + p.offset.x) / p.scale;
                        sampleZ = (z + p.offset.y) / p.scale;
                        y += Mathf.PerlinNoise(sampleX, sampleZ) * p.heightMultiplier;//PerlinNoise = 擬似ランダムパターン(白黒モザイクのやつ)　座標からPerlinNoiseの値取得
                    }

                    vertices[z * size + x] = new Vector3(x * vertexDistance, y, -z * vertexDistance);
                }
            }

            int triangleIndex = 0;
            int[] triangles = new int[(size - 1) * (size - 1) * 6];
            for (int z = 0; z < size - 1; z++) {
                for (int x = 0; x < size - 1; x++) {

                    int a = z * size + x;
                    int b = a + 1;
                    int c = a + size;
                    int d = c + 1;

                    triangles[triangleIndex] = a;
                    triangles[triangleIndex + 1] = b;
                    triangles[triangleIndex + 2] = c;

                    triangles[triangleIndex + 3] = c;
                    triangles[triangleIndex + 4] = b;
                    triangles[triangleIndex + 5] = d;

                    triangleIndex += 6;
                }
            }


            //テクスチャをメッシュのどの部分に対応させるかを示すもの
            //UVの配列数はメッシュの頂点数と同じ

            //テクスチャの左下部分が(0, 0)、テクスチャの中心が(0.5, 0.5)、テクスチャの右上が(1, 1)とそれぞれ対応
            Vector2[] uvs = new Vector2[size * size];
            for (int z = 0; z < size; z++) {
                for (int x = 0; x < size; x++) {
                    uvs[z * size + x] = new Vector2(x / (float)size, z / (float)size);//サイズが3の場合　(0/3,0/3)   (1/3,0/3)  (2/3,0/3)・・・
                }
            }




            Mesh mesh      = new Mesh();
            mesh.vertices  = vertices;
            mesh.triangles = triangles;
            mesh.uv        = uvs;      //テクスチャのためのUV配列

            mesh.RecalculateNormals();

            MeshFilter meshFilter       = gameObject.GetComponent<MeshFilter>();
            if (!meshFilter) meshFilter = gameObject.AddComponent<MeshFilter>();

            MeshRenderer meshRenderer       = gameObject.GetComponent<MeshRenderer>();
            if (!meshRenderer) meshRenderer = gameObject.AddComponent<MeshRenderer>();

            MeshCollider meshCollider       = gameObject.GetComponent<MeshCollider>();
            if (!meshCollider) meshCollider = gameObject.AddComponent<MeshCollider>();

            meshFilter.mesh = mesh;
            meshRenderer.sharedMaterial = material;
            meshRenderer.sharedMaterial.mainTexture = CreateTexture(vertices);//MeshRendererにテクスチャを設定　　


            meshCollider.sharedMesh     = mesh;
            meshCollider.sharedMaterial = physicMaterial;
  
        }

        //地形の頂点情報を受け取ってテクスチャを返すCreateTextureというメソッドを作成しました。
        //それぞれの頂点のY座標に応じてcolorMap配列に色の情報を格納していきます。
        //Mathf.InverseLerp(a, b, value) は
        //「aを0、bを1とした場合、valueは0～1のどんな値になるか」を調べるメソッドです。
        //たとえばもしMathf.InverseLerp(2, 16, 9)であれば、9は2と16のちょうど中間なので0.5を返します。
        //次の行でその値をmeshColorGradient.Evaluateに渡し、Gradient Editorで設定した色を取得

        Texture2D CreateTexture(Vector3[] vertices) {
            Color[] colorMap = new Color[vertices.Length];//頂点座標分の配列を用意
            for (int i = 0; i < vertices.Length; i++) {
                float percent = Mathf.InverseLerp(minHeight, maxHeight, vertices[i].y);//頂点配列からy座標を取り出し　高さに合わせたパーセンテージを取得
                colorMap[i] = meshColorGradient.Evaluate(percent);//Gradient Editorで設定した色を取得
            }
            Texture2D texture = new Texture2D(size, size);//テクスチャ用意

            texture.SetPixels(colorMap);//テクスチャに　色を割り当てる
            texture.Apply();

            return texture;
        }
        //void OnValidate() {
        //    CreateMesh();
        //}
    }
}
```


<br>

<br>

---

<br>

<br>

サンプルコード6
```cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//頂点数がどんどん増えていくので　専用のシェーダーを使った方がいいかも
namespace MeshSample
{
    //全体の流れ
    //頂点の位置情報(vertices)と
    //どの頂点で三角形を作るかという情報(triangles)を配列として用意し
    //それをメッシュに渡す
    public class Mesh6 : MonoBehaviour
    {
        [Range(2, 255)]
        [SerializeField] int size;
        [SerializeField] float vertexDistance = 1f;//頂点間の距離
        [SerializeField] Material material;
        [SerializeField] PhysicMaterial physicMaterial;

        [SerializeField] PerlinNoiseProperty[] perlinNoiseProperty = new PerlinNoiseProperty[1];
        [System.Serializable]
        public class PerlinNoiseProperty
        {
            public float heightMultiplier = 1f;
            public float scale = 1f;
            public Vector2 offset;
        }

        [SerializeField] Gradient meshColorGradient;

        [SerializeField] float minHeight;
        [SerializeField] float maxHeight;

        [SerializeField] bool blockMode;
        [Range(1, 16)]
        [SerializeField] int textureDetail;

        void Start() {
            CreateMesh();
        }

        void CreateMesh() {
            Vector3[] vertices = new Vector3[size * size];
            for (int z = 0; z < size; z++) {
                for (int x = 0; x < size; x++) {

                    float sampleX;
                    float sampleZ;
                    float y = 0;
                    foreach (PerlinNoiseProperty p in perlinNoiseProperty) {//後から付け足したプロパティをy座標情報とし加算
                        p.scale = Mathf.Max(0.0001f, p.scale);
                        sampleX = (x + p.offset.x) / p.scale;
                        sampleZ = (z + p.offset.y) / p.scale;
                        y += Mathf.PerlinNoise(sampleX, sampleZ) * p.heightMultiplier;//PerlinNoise = 擬似ランダムパターン(白黒モザイクのやつ)　座標からPerlinNoiseの値取得
                    }

                    vertices[z * size + x] = new Vector3(x * vertexDistance, y, -z * vertexDistance);
                }
            }

            int triangleIndex = 0;
            int[] triangles = new int[(size - 1) * (size - 1) * 6];
            for (int z = 0; z < size - 1; z++) {
                for (int x = 0; x < size - 1; x++) {

                    int a = z * size + x;
                    int b = a + 1;
                    int c = a + size;
                    int d = c + 1;

                    triangles[triangleIndex] = a;
                    triangles[triangleIndex + 1] = b;
                    triangles[triangleIndex + 2] = c;

                    triangles[triangleIndex + 3] = c;
                    triangles[triangleIndex + 4] = b;
                    triangles[triangleIndex + 5] = d;

                    triangleIndex += 6;
                }
            }


            //テクスチャをメッシュのどの部分に対応させるかを示すもの
            //UVの配列数はメッシュの頂点数と同じ

            //テクスチャの左下部分が(0, 0)、テクスチャの中心が(0.5, 0.5)、テクスチャの右上が(1, 1)とそれぞれ対応
            Vector2[] uvs = new Vector2[size * size];
            for (int z = 0; z < size; z++) {
                for (int x = 0; x < size; x++) {
                    uvs[z * size + x] = new Vector2(x / (float)size, z / (float)size);//サイズが3の場合　(0/3,0/3)   (1/3,0/3)  (2/3,0/3)・・・
                }
            }




            Mesh mesh      = new Mesh();
            mesh.vertices  = vertices;
            mesh.triangles = triangles;
            mesh.uv        = uvs;      //テクスチャのためのUV配列

            mesh.RecalculateNormals();

            MeshFilter meshFilter       = gameObject.GetComponent<MeshFilter>();
            if (!meshFilter) meshFilter = gameObject.AddComponent<MeshFilter>();

            MeshRenderer meshRenderer       = gameObject.GetComponent<MeshRenderer>();
            if (!meshRenderer) meshRenderer = gameObject.AddComponent<MeshRenderer>();

            MeshCollider meshCollider       = gameObject.GetComponent<MeshCollider>();
            if (!meshCollider) meshCollider = gameObject.AddComponent<MeshCollider>();

            meshFilter.mesh = mesh;
            meshRenderer.sharedMaterial = material;
            meshRenderer.sharedMaterial.mainTexture = CreateTexture(vertices);//MeshRendererにテクスチャを設定　　


            meshCollider.sharedMesh     = mesh;
            meshCollider.sharedMaterial = physicMaterial;
  
        }


        Texture2D CreateTexture(Vector3[] vertices) {
            //解像度をあげてみる
            //textureDetailの値が大きくなるごとにメッシュの頂点を補間する数を多くします。　
            //メッシュの中に　textureDetailという頂点を増やす感じ. 辺2分割するイメージ
            //サイズが3　（頂点数は3*3)　　meshが4つ　で
            //textureDetailが２の場合
            //
            int textureSize = (size - 1) * textureDetail + 1;//増やした後の頂点数 //通常のメッシュの数が2*2 １つのmeshを２分割する場合　辺が４分割　頂点数を数えるならプラス１


            Color[] colorMap = new Color[textureSize * textureSize];//全ての頂点数分の配列を用意　
            for (int z = 0; z < textureSize; z++) {
                for (int x = 0; x < textureSize; x++) {
                    float sampleX;
                    float sampleZ;
                    float y = 0;
                    //それぞれの点でのY座標を求めます
                    foreach (PerlinNoiseProperty p in perlinNoiseProperty) {
                        p.scale = Mathf.Max(0.0001f, p.scale);
                        sampleX = (x / (float)textureDetail + p.offset.x) / p.scale;
                        sampleZ = (z / (float)textureDetail + p.offset.y) / p.scale;
                        y += Mathf.PerlinNoise(sampleX, sampleZ) * p.heightMultiplier;
                    }

                    float percent = Mathf.InverseLerp(minHeight, maxHeight, y);
                    colorMap[z * textureSize + x] = meshColorGradient.Evaluate(percent);//配列の要素として色の割合を保存
                }
            }
            Texture2D texture = new Texture2D(textureSize, textureSize);//テクスチャの要素　１辺の頂点数　


            texture.SetPixels(colorMap);//配列を割り当てる　　[１つ目の要素の頂点の色の割合 ,２つ目の要素の頂点の色の割合 ,３つ目の要素の頂点の色の割合  ,・・・]  
            texture.wrapMode = TextureWrapMode.Clamp; //テクスチャの貼り方を選択。
                                                      //Repeatに設定するとテクスチャを繰り返して隙間なく埋める、
                                                      //Clampにするとテクスチャを引き伸ばしてメッシュの端にピッタリ合わせて貼る
            if (blockMode) texture.filterMode = FilterMode.Point;//テクスチャを3Dのモデルに貼り付けるときにどのように拡大するか
                                                                 //Pointにするとそれぞれのピクセルがブロック状に
            texture.Apply();

            return texture;
        }
        //void OnValidate() {
        //    CreateMesh();
        //}
    }
}

```


このコードはさすがにパフォーマンス的に無理があります。  
たとえばメッシュのsizeが64の場合、実際の頂点数は64×64=4096個。  
textureDetailを4に設定した場合、テクスチャのサンプル数は253×253で64009個にもなります。  
textureDetailが増えるごとにそのおよそ2乗分が増えていくことになるので、  
そのすべてでパーリンノイズを算出して処理していくのはとんでもなくコストがかかります。  
指定したタイミングで1度だけ読み込むとかならいいと思いますが、  
たとえば高解像度のテクスチャを毎フレーム計算したりするのは現実的ではありません。  
というわけで、さすがにもうテクスチャを貼り付けるだけでは間に合わなくなってきました。  
ここまで作っておいてなんですが、ここまでくるとおとなしく専用のシェーダーを用意したほうがよさそうですね。  


<br>

<br>

---

<br>

<br>