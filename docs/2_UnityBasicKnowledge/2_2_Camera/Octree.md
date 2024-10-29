# Octree

Octreeを使った効率化は、大規模なシーンや多くのオブジェクトを効率的に管理・描画する際に非常に有効です。特に、プレイヤーの周りに存在するオブジェクトだけを描画し、それ以外の領域を描画しないことで、パフォーマンスを向上させることができます。

**Octreeの基本的な考え方**  
Octreeは、空間を再帰的に8つの領域に分割し、必要に応じて詳細な領域まで細分化してオブジェクトを格納するデータ構造です。プレイヤーが動いた際に、プレイヤーの視界や描画範囲に入るオブジェクトだけを描画することができるため、描画負荷が軽減されます。

<br>

---

<br>

## Octreeを使った効率化プログラムの実装

### 1. **Octreeの基本構造**
まず、Octreeの基本的な構造を定義し、各ノードにオブジェクトを格納します。オブジェクトの位置に基づいて、Octree内の適切なノードに分配します。

### 2. **プレイヤーの位置に基づく描画**
次に、プレイヤーの位置に基づいて、プレイヤー周辺の領域に含まれるオブジェクトだけを描画します。

### **サンプルコード**

以下のコードは、Octreeを利用してプレイヤーの周りのオブジェクトだけを効率的に描画する例です。

```csharp
using UnityEngine;
using System.Collections.Generic;

public class OctreeNode
{
    private const int MAX_OBJECTS = 10;   // ノードに格納できる最大オブジェクト数
    private const int MAX_DEPTH = 5;      // Octreeの最大深度

    private Bounds bounds;                // ノードの範囲
    private List<GameObject> objects;     // ノード内に格納されるオブジェクト
    private OctreeNode[] children;        // 子ノード
    private int depth;                    // 現在の深度

    // コンストラクタ
    public OctreeNode(Bounds bounds, int depth)
    {
        this.bounds = bounds;
        this.depth = depth;
        objects = new List<GameObject>();
        children = null;
    }

    // オブジェクトをOctreeに追加
    public void Insert(GameObject obj)
    {
        // オブジェクトがこのノードの範囲外であれば無視
        if (!bounds.Contains(obj.transform.position))
        {
            return;
        }

        // 子ノードが存在する場合、再帰的に追加
        if (children != null)
        {
            int index = GetChildIndex(obj.transform.position);
            children[index].Insert(obj);
            return;
        }

        // オブジェクトをこのノードに追加
        objects.Add(obj);

        // 最大オブジェクト数を超えた場合、ノードを分割
        if (objects.Count > MAX_OBJECTS && depth < MAX_DEPTH)
        {
            Subdivide();

            // 既存のオブジェクトを子ノードに再分配
            for (int i = objects.Count - 1; i >= 0; i--)
            {
                int index = GetChildIndex(objects[i].transform.position);
                children[index].Insert(objects[i]);
                objects.RemoveAt(i);
            }
        }
    }

    // ノードの分割
    private void Subdivide()
    {
        children = new OctreeNode[8];

        Vector3 size = bounds.size / 2f;
        Vector3 center = bounds.center;

        for (int i = 0; i < 8; i++)
        {
            Vector3 newCenter = center + new Vector3(
                (i & 1) == 0 ? -size.x / 2 : size.x / 2,
                (i & 2) == 0 ? -size.y / 2 : size.y / 2,
                (i & 4) == 0 ? -size.z / 2 : size.z / 2
            );

            Bounds childBounds = new Bounds(newCenter, size);
            children[i] = new OctreeNode(childBounds, depth + 1);
        }
    }

    // プレイヤーの周りのオブジェクトだけを取得
    public void GetObjectsInRange(Bounds range, List<GameObject> result)
    {
        // 範囲がノードと交差していない場合、処理をスキップ
        if (!bounds.Intersects(range))
        {
            return;
        }

        // 子ノードが存在する場合、再帰的に探索
        if (children != null)
        {
            foreach (var child in children)
            {
                child.GetObjectsInRange(range, result);
            }
        }
        else
        {
            // 現在のノード内のオブジェクトを追加
            foreach (var obj in objects)
            {
                if (range.Contains(obj.transform.position))
                {
                    result.Add(obj);
                }
            }
        }
    }

    // オブジェクトの位置に基づいて子ノードのインデックスを取得
    private int GetChildIndex(Vector3 position)
    {
        int index = 0;
        if (position.x > bounds.center.x) index |= 1;
        if (position.y > bounds.center.y) index |= 2;
        if (position.z > bounds.center.z) index |= 4;
        return index;
    }
}

```

```cs

public class OctreeManager : MonoBehaviour
{
    public GameObject player;     // プレイヤーへの参照
    public float viewDistance = 50f;  // プレイヤーの描画範囲
    private OctreeNode rootNode;  // Octreeのルートノード

    void Start()
    {
        // Octreeのルートノードをシーン全体に合わせて作成
        Bounds sceneBounds = new Bounds(Vector3.zero, new Vector3(200, 200, 200));
        rootNode = new OctreeNode(sceneBounds, 0);

        // シーン内の全オブジェクトを取得し、Octreeに追加
        foreach (var obj in FindObjectsOfType<GameObject>())
        {
            rootNode.Insert(obj);
        }
    }

    void Update()
    {
        // プレイヤーの周りのオブジェクトを取得
        Bounds playerRange = new Bounds(player.transform.position, Vector3.one * viewDistance);
        List<GameObject> visibleObjects = new List<GameObject>();
        rootNode.GetObjectsInRange(playerRange, visibleObjects);

        // 取得したオブジェクトだけを描画
        foreach (var obj in visibleObjects)
        {
            obj.SetActive(true);
        }
    }
}
```

---

### **解説**

#### 1. **Octree構造**
- `OctreeNode`: Octreeの各ノードを表します。ノードは、指定された空間範囲（`Bounds`）とその中に格納されるオブジェクトリストを持ちます。必要に応じて、ノードは8つの子ノードに分割されます。
- `Insert`: オブジェクトをノードに挿入します。最大オブジェクト数を超えた場合、自動的にノードが分割され、オブジェクトが適切な子ノードに再分配されます。

#### 2. **プレイヤーの周囲のオブジェクトを取得**
- `GetObjectsInRange`: プレイヤーの位置と描画範囲（`Bounds`）に基づいて、Octree内から対象範囲に含まれるオブジェクトを再帰的に取得します。

#### 3. **オブジェクトの描画**
- プレイヤーの周りに存在するオブジェクトだけをリストに追加し、それらのオブジェクトのみをアクティブにします。

---

### **パフォーマンスの利点**
- **広大なシーンでの効率的な描画**: Octreeを使うことで、広大なシーン内でプレイヤーが視認できる範囲のオブジェクトだけを描画するため、無駄な計算や描画を削減できます。
- **大規模シーンの管理**: 多数のオブジェクトが存在するシーンでも、Octreeを使って効率的にオブジェクトを管理し、パフォーマンスを向上させることが可能です。

---

### **拡張**
- このOctreeの基本構造を利用して、プレイヤーのカメラ視野やLODシステムと連動させることも可能です。