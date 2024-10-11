[一つ前に戻る](../5_0.md)

3. Unity機能_その他
     1. [Sound](Sound/Sound0.md)
         + [AudioSource]
         + [AudioMixer]
         + [CRI_Ware]
     
     3. [ScriptableObject](ScriptableObject/0_ScriptableObject.md)

     4. [Timeline]
     








     7. [Shader_Basic](Shader/shader.md)  
       - [C#]  - [HLSL_CG]  - [ShaderGraph]






     8. Shader_Advanced サンプルプロジェクト見てもらう？
       - [Tessellation]   
       - [Geometry]
       - [Liquid]
       - [Ink]
       - [DynamicMesh]
       - [UI]

     9. [データ保存方法](SaveData/0_SaveData.md)
     
     10. 非同期処理
       + [Coroutine]
       + [UniTask_Task](UniTask/UniTask0_0.md)




<br>

11. [DOTS](DOTS/DOTS.md)

<br>



4.  [Asset紹介 (Mesh Baker Free)](https://assetstore.unity.com/packages/tools/modeling/mesh-baker-free-31895?srsltid=AfmBOooKmbb6-xkSJhEceaEVIoH0NwNMoQsw9lH6A3rbPKqn6hrScOaq)

[使い方紹介サイト](https://3dcg-school.pro/unity-asset-mesh-baker/)

Occlusion Culling
Frustum Culling　視錐台  
LOD
Octree
オブジェクトプーリング
バッチ処理
GPUインスタンシング

<br>

---

`Bounds`と`GameObject`の違い

- **Bounds**:
  - `Bounds`は、オブジェクトが占める空間を表すための構造体で、3D空間における位置やサイズを示します。
  - 主に、オブジェクトの衝突判定や描画カリングに使われます。たとえば、`Renderer`や`Collider`から取得されます。
  - `Bounds`自体は、物理的なオブジェクトではなく、あくまでそのオブジェクトが占める空間を定義するものです。

- **GameObject**:
  - `GameObject`は、Unityにおける基本的なオブジェクトの単位です。オブジェクトの位置、回転、スケール、さまざまなコンポーネント（例えば、`Renderer`、`Collider`、`Script`など）を持ちます。
  - `GameObject`は、実際のゲーム内に存在するエンティティであり、視覚的に表示されたり、物理的にインタラクションしたりします。


---


# Boundsとは？

`Bounds`はUnityの構造体で、3D空間内のオブジェクトの軸に平行な境界ボックス（AABB: Axis-Aligned Bounding Box）を表します。この境界ボックスはオブジェクトの位置とサイズを基に決定され、主に以下の用途で使用されます。

- **衝突判定**: 2つの`Bounds`が重なっているかどうかを確認します。
- **可視性判定**: オブジェクトがカメラの視野内にあるかどうかを判断します。
- **位置とサイズの確認**: オブジェクトが占める空間の中心やサイズを取得できます。

## プログラム例

次のプログラム例では、2つのオブジェクトの`Bounds`を取得し、それらが交差しているかどうかを判定します。

```csharp
using UnityEngine;

public class BoundsExample : MonoBehaviour
{
    // シーン内の他のオブジェクトを参照します。
    public GameObject otherObject;

    void Start()
    {
        // このスクリプトがアタッチされたオブジェクトのColliderを取得し、Boundsを取得します。
        Bounds objectBounds = GetComponent<Collider>().bounds;

        // 他のオブジェクトのColliderを取得し、Boundsを取得します。
        Bounds otherBounds = otherObject.GetComponent<Collider>().bounds;

        // 2つのBoundsが交差しているかどうかをチェックします。
        if (objectBounds.Intersects(otherBounds))
        {
            Debug.Log("Objects are intersecting.");
        }
        else
        {
            Debug.Log("Objects are not intersecting.");
        }
    }
}
```

### プログラムの解説

1. **`Bounds`の取得**:
   - `Bounds`は、オブジェクトの`Collider`から取得します。`Collider`は、オブジェクトの形状や物理的な性質を持つコンポーネントであり、`bounds`プロパティを使ってそのオブジェクトの境界ボックスを取得できます。

   ```csharp
   Bounds objectBounds = GetComponent<Collider>().bounds;
   ```

   ここで`GetComponent<Collider>()`は、オブジェクトにアタッチされた`Collider`を取得し、その`bounds`プロパティが`Bounds`を返します。

2. **`Intersects`メソッド**:
   - `Intersects`メソッドは、2つの`Bounds`が重なっているかどうかを判定するためのメソッドです。これにより、2つのオブジェクトが空間内で交差しているかどうかを簡単に確認できます。

   ```csharp
   if (objectBounds.Intersects(otherBounds))
   {
       Debug.Log("Objects are intersecting.");
   }
   ```

   この例では、`objectBounds`と`otherBounds`が交差している場合に「Objects are intersecting.」というメッセージをコンソールに出力します。

3. **可視性判定**:
   - `Bounds`を使ってオブジェクトがカメラの視野内にあるかどうかを判定することもできます。視錐台（Frustum）内に`Bounds`が存在するかを確認するために、`GeometryUtility.CalculateFrustumPlanes`と`GeometryUtility.TestPlanesAABB`メソッドを使用します。

   ```csharp
   Plane[] frustumPlanes = GeometryUtility.CalculateFrustumPlanes(Camera.main);
   if (GeometryUtility.TestPlanesAABB(frustumPlanes, objectBounds))
   {
       Debug.Log("Object is within the camera's frustum.");
   }
   else
   {
       Debug.Log("Object is outside the camera's frustum.");
   }
   ```

   この例では、カメラの視錐台（frustum）を表す平面（`Plane`）の配列を計算し、それに対して`Bounds`が含まれているかをチェックしています。

### まとめ

- **`Bounds`の取得**: オブジェクトの`Collider`から`Bounds`を取得します。
- **衝突判定**: `Intersects`メソッドを使って、2つの`Bounds`が交差しているかを判定できます。
- **可視性判定**: 視錐台内に`Bounds`が含まれているかを確認し、カメラの視野内にオブジェクトがあるかを判定します。

これらの機能は、3Dゲームやシミュレーションにおいて、効率的な衝突判定や可視性チェックを行うために非常に重要です。






---

# 視錐台

カメラの視錐台内にオブジェクトが含まれているかをチェックし、その結果に基づいて描画するかどうかを決定するプログラムの例を見てみます。

<img src="Unity_Frustum1_overview-1.png" width="90%" alt="" title="">



# プログラム例

```csharp
using UnityEngine;

public class FrustumCullingExample : MonoBehaviour
{
    public GameObject[] objectsToRender; // チェック対象のオブジェクトリスト

    void Update()
    {
        // カメラの視錐台を計算
        Plane[] frustumPlanes = GeometryUtility.CalculateFrustumPlanes(Camera.main);

        // 全てのオブジェクトに対して処理を行う
        foreach (GameObject obj in objectsToRender)
        {
            // 各オブジェクトのBoundsを取得
            Bounds bounds = obj.GetComponent<Renderer>().bounds;

            // オブジェクトのBoundsが視錐台内にあるかチェック
            if (GeometryUtility.TestPlanesAABB(frustumPlanes, bounds))
            {
                // 視錐台内にある場合、オブジェクトを表示
                obj.SetActive(true);
            }
            else
            {
                // 視錐台外にある場合、オブジェクトを非表示にする
                obj.SetActive(false);
            }
        }
    }
}
```

# 解説

1. **`objectsToRender`配列**:
   - このスクリプトは、複数のオブジェクトを視錐台内にあるかどうかチェックするために使用します。`objectsToRender`には、チェック対象のオブジェクトを登録しておきます。

   ```csharp
   public GameObject[] objectsToRender;
   ```

2. **`GeometryUtility.CalculateFrustumPlanes`メソッド**:
   - `CalculateFrustumPlanes`は、カメラの視錐台を構成する6つの平面を計算し、それを`Plane`型の配列として返します。この視錐台を使ってオブジェクトの`Bounds`が含まれているかをチェックします。

   ```csharp
   Plane[] frustumPlanes = GeometryUtility.CalculateFrustumPlanes(Camera.main);
   ```

3. **`Renderer`コンポーネントから`Bounds`を取得**:
   - `Renderer`コンポーネントの`bounds`プロパティを使って、オブジェクトの`Bounds`を取得します。`Renderer`は、メッシュなどの描画を担当するコンポーネントです。

   ```csharp
   Bounds bounds = obj.GetComponent<Renderer>().bounds;
   ```

4. **`GeometryUtility.TestPlanesAABB`メソッド**:
   - このメソッドは、視錐台内に`Bounds`があるかどうかを判定します。もし視錐台内に`Bounds`があれば、`true`を返します。

   ```csharp
   if (GeometryUtility.TestPlanesAABB(frustumPlanes, bounds))
   ```

5. **オブジェクトの表示/非表示**:
   - 視錐台内にオブジェクトがあれば、そのオブジェクトを`SetActive(true)`で表示し、視錐台外であれば`SetActive(false)`で非表示にします。これにより、視錐台内にあるオブジェクトだけが描画されます。

   ```csharp
   obj.SetActive(true);
   ```

### このプログラムの用途

このプログラムは、**視錐台カリング**と呼ばれる手法の一例です。視錐台カリングは、カメラの視野内にないオブジェクトを描画しないことで、ゲームのパフォーマンスを向上させるために使用されます。特に大規模なシーンや多くのオブジェクトがあるシーンでは、視錐台カリングを活用することで、描画負荷を大幅に減らすことができます。

この例では、オブジェクトの表示・非表示を`SetActive`メソッドで制御していますが、実際のゲームでは、他のカリング手法（例えばオクルージョンカリングやLOD（レベルオブディテール））と組み合わせて使用されることもあります。




---

#  BoundsとGameObject、視錐台に対する調査の違い

- **Boundsを調べる場合**:
  - `GeometryUtility.TestPlanesAABB`メソッドを使用して、視錐台の平面と`Bounds`を比較します。
  - これにより、その`Bounds`（空間）が視錐台内にあるか、または交差しているかを判定します。
  - `Bounds`を使ったカリングは、オブジェクトが描画されるかどうかを効率的に判断するのに役立ちます。

- **GameObjectを調べる場合**:
  - `GameObject`自体を直接視錐台の中にあるかどうかを調べることはできません。まず`GameObject`の`Renderer`や`Collider`を取得して、それに基づいて`Bounds`を取得し、その`Bounds`を用いて視錐台との比較を行う必要があります。
  - `GameObject`は物理的な存在なので、単体でのカリングは不可能ですが、`Bounds`を通じて間接的にカリングを行います。

### まとめ

- **`Bounds`**は、オブジェクトが占める空間を示す構造体で、主にカリングや衝突判定に使用されます。
- **`GameObject`**は、Unity内での実際のエンティティであり、位置や回転、コンポーネントを持っています。
- 視錐台の判定は、`Bounds`を使って行うため、`GameObject`そのものを直接調べることはできません。`GameObject`から`Bounds`を取得し、その情報を用いて判定します。

このように、`Bounds`と`GameObject`は異なる役割を持っており、視錐台カリングでは`Bounds`を利用することで、効率的に描画対象を決定することができます。





---
(Octreeの構造を使って効率的に空間分割を行い、視錐台内に存在するオブジェクトのみを描画することを目指します。)

以下にその例と解説。

# Octreeの基本的な概念

- **Octree**は、3D空間を8つの等しい部分に再帰的に分割するデータ構造です。各ノードは空間内の部分領域を表し、最小単位（葉ノード）にはオブジェクトが格納されます。
- これにより、広大な空間内でのオブジェクト検索や、特定の範囲内にあるオブジェクトの取得が効率化されます。


# 簡単に書くと

+ Octreeは、3D空間を効率よく管理するためのデータ構造で、特に広範囲にオブジェクトが散らばっている場合に有効です。
+ 各ノードは特定の空間を管理し、その空間内にあるGameObjectをリストとして保持します。
+ 必要に応じてノードはさらに細かいノード（子ノード）に分割され、より細かくオブジェクトを管理します。
+ Bounds情報を使用することで、Octreeを使ったカリング（無駄な描画を避けるための処理）を行い、視野内にあるオブジェクトのみを描画することができます。

この仕組みを使うことで、特に大規模なシーンでの描画パフォーマンスを向上させることが可能です。

# プログラム例

```csharp
using UnityEngine;
using System.Collections.Generic;

public class OctreeNode
{
    public Bounds bounds;
    public List<GameObject> objects;
    public OctreeNode[] children;

    public OctreeNode(Bounds bounds)
    {
        this.bounds = bounds;
        this.objects = new List<GameObject>();
        this.children = null;
    }

    // Octreeの子ノードを作成
    public void Subdivide()
    {
        if (children != null)
            return;

        children = new OctreeNode[8];
        Vector3 size = bounds.size / 2f;
        Vector3 center = bounds.center;

        for (int i = 0; i < 8; i++)
        {
            Vector3 newCenter = center + new Vector3(
                (i & 1) == 0 ? -size.x / 2f : size.x / 2f,
                (i & 2) == 0 ? -size.y / 2f : size.y / 2f,
                (i & 4) == 0 ? -size.z / 2f : size.z / 2f
            );
            children[i] = new OctreeNode(new Bounds(newCenter, size));
        }
    }

    // オブジェクトをOctreeに追加
    public void Insert(GameObject obj)
    {
        if (!bounds.Contains(obj.GetComponent<Renderer>().bounds.min) || !bounds.Contains(obj.GetComponent<Renderer>().bounds.max))
            return;

        if (children == null)
        {
            objects.Add(obj);

            // ノードが満杯になった場合、分割する
            if (objects.Count > 8)
            {
                Subdivide();

                foreach (var existingObj in objects)
                {
                    Insert(existingObj);
                }

                objects.Clear();
            }
        }
        else
        {
            foreach (var child in children)
            {
                child.Insert(obj);
            }
        }
    }

    // 視錐台内のオブジェクトを取得
    public void RetrieveObjectsInFrustum(Plane[] frustumPlanes, List<GameObject> result)
    {
        if (!GeometryUtility.TestPlanesAABB(frustumPlanes, bounds))
            return;

        if (children != null)
        {
            foreach (var child in children)
            {
                child.RetrieveObjectsInFrustum(frustumPlanes, result);
            }
        }
        else
        {
            foreach (var obj in objects)
            {
                if (GeometryUtility.TestPlanesAABB(frustumPlanes, obj.GetComponent<Renderer>().bounds))
                {
                    result.Add(obj);
                }
            }
        }
    }
}

public class OctreeCulling : MonoBehaviour
{
    public GameObject[] objectsToInsert;
    private OctreeNode rootNode;

    void Start()
    {
        // Octreeのルートノードを設定（ここでは空間の全体サイズを指定）
        Bounds sceneBounds = new Bounds(Vector3.zero, new Vector3(100, 100, 100));
        rootNode = new OctreeNode(sceneBounds);

        // オブジェクトをOctreeに挿入
        foreach (var obj in objectsToInsert)
        {
            rootNode.Insert(obj);
        }
    }

    void Update()
    {
        // カメラの視錐台を取得
        Plane[] frustumPlanes = GeometryUtility.CalculateFrustumPlanes(Camera.main);

        // 視錐台内に存在するオブジェクトを取得
        List<GameObject> objectsInFrustum = new List<GameObject>();
        rootNode.RetrieveObjectsInFrustum(frustumPlanes, objectsInFrustum);

        // 全てのオブジェクトを非表示にし、視錐台内に存在するオブジェクトのみ表示
        foreach (var obj in objectsToInsert)
        {
            obj.SetActive(false);
        }

        foreach (var obj in objectsInFrustum)
        {
            obj.SetActive(true);
        }
    }
}
```

# 解説

1. **OctreeNodeクラス**:
   - このクラスは、Octreeの各ノードを表します。各ノードはその領域を表す`Bounds`と、その領域内に含まれる`GameObject`のリストを持っています。また、必要に応じて8つの子ノードを持つことができます。

2. **Subdivideメソッド**:
   - このメソッドは、現在のノードを8つの小さなノードに分割します。ノード内のオブジェクトが一定数を超えた場合に、空間を分割して管理します。

3. **Insertメソッド**:
   - このメソッドは、オブジェクトをOctreeに挿入します。オブジェクトが現在のノードの`Bounds`に完全に収まる場合、そのノードに追加されます。ノードが満杯になると分割され、オブジェクトが適切な子ノードに再挿入されます。

4. **RetrieveObjectsInFrustumメソッド**:
   - このメソッドは、カメラの視錐台に対してノードの`Bounds`をチェックし、その範囲内にあるオブジェクトを取得します。再帰的に子ノードをチェックし、最終的に視錐台内のオブジェクトをリストに追加します。

5. **OctreeCullingクラス**:
   - `OctreeNode`のルートノードを作成し、シーン内のすべてのオブジェクトを挿入します。`Update`メソッドで、視錐台内にあるオブジェクトだけを表示する処理を行います。

# このプログラムの動作

- 起動時に、`objectsToInsert`に指定されたオブジェクトがOctreeに挿入されます。
- 毎フレーム、カメラの視錐台内に存在するオブジェクトをOctreeを用いて効率的に検索し、それ以外のオブジェクトは非表示にします。
- Octreeを使うことで、視錐台カリングを効率的に行い、特に広いシーンや多くのオブジェクトが存在する場合にパフォーマンスを向上させることができます。


このように、Octreeを使用することで、大規模な3Dシーンでのオブジェクト管理が効率的になります。また、視錐台カリングと組み合わせることで、無駄な描画を避け、ゲームのパフォーマンスを最適化できます。