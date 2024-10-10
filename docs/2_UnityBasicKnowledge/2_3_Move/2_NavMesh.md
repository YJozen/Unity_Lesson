NavMeshは、Unityの強力なパスファインディングシステムで、ゲーム内のエージェントが自動で障害物を避けながら目的地に到達するために使用されます。教材では、NavMeshの基本的な使い方から応用例までを解説し、サンプルコードを通じて学べる内容にします。

## NavMeshに関する教材構成案

### 1. **NavMeshの基本概念**
NavMesh（Navigation Mesh）は、シーンの地形上に設計された移動可能な領域を示します。これにより、キャラクターは特定の範囲内で移動可能であり、障害物を回避しながら目的地に向かいます。

- **Bake**: NavMeshを生成するプロセスです。地形や障害物を元に、移動可能な領域を自動で作成します。
- **NavMesh Agent**: キャラクターやオブジェクトに取り付けるコンポーネントで、NavMesh上でのパスファインディングを行います。

---

### 2. **基本的なNavMeshのセットアップ方法**
#### ステップ 1: NavMeshの作成
1. シーン内の地形に「NavMesh」データを適用するには、Unityエディタで`Window > AI > Navigation`を開きます。
2. NavMeshを使用したい地形オブジェクトに`Static`オプションを適用し、`Bake`を実行して移動可能な領域を作成します。

#### ステップ 2: NavMesh Agentの設定
1. 移動するキャラクターに`NavMesh Agent`コンポーネントを追加します。
2. `Destination`プロパティに目的地を設定することで、キャラクターは自動でその位置まで移動します。

---

### 3. **サンプルプログラム：NavMesh Agentを使った移動**
NavMesh Agentを用いてキャラクターを指定した目的地まで自動で移動させる基本的なサンプルプログラムです。

```csharp
using UnityEngine;
using UnityEngine.AI;

public class NavMeshMovement : MonoBehaviour
{
    public Transform target; // 目的地となるターゲットのTransform
    private NavMeshAgent agent;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>(); // NavMesh Agentの取得
    }

    void Update()
    {
        agent.SetDestination(target.position); // ターゲットの位置まで自動で移動
    }
}
```

#### 解説:
- **NavMesh Agent**は、`SetDestination`メソッドでターゲットの位置に向かって自動的に移動します。
- `NavMeshAgent`は自動的に最適なルートを計算し、障害物を避けながら移動します。

---

### 4. **応用：クリックで動かすキャラクターの実装**
マウスでクリックした場所にキャラクターを移動させる方法です。プレイヤーがインタラクティブにキャラクターを操作できるようになります。

#### サンプルプログラム：
```csharp
using UnityEngine;
using UnityEngine.AI;

public class ClickToMove : MonoBehaviour
{
    private NavMeshAgent agent;
    private Camera cam;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();
        cam = Camera.main;
    }

    void Update()
    {
        if (Input.GetMouseButtonDown(0)) // 左クリックで目的地を設定
        {
            Ray ray = cam.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
                agent.SetDestination(hit.point); // クリックした地点まで移動
            }
        }
    }
}
```

#### 解説:
- `Raycast`を使用して、クリックした位置を取得し、NavMesh Agentにその座標を設定することで移動を開始します。
- クリック位置が地形上にあり、NavMesh内の有効なポイントであれば、キャラクターはその地点に移動します。

---

### 5. **NavMeshのカスタマイズ**
NavMeshの設定をカスタマイズして、移動の挙動を調整します。`NavMesh Agent`には、次のようなプロパティが用意されています。

- **Speed**: エージェントの移動速度。
- **Angular Speed**: 回転速度。
- **Stopping Distance**: 目的地に到達した際に停止する距離。
- **Auto Braking**: 目的地に近づくときに自動で減速するかどうか。

#### 例: スピードや停止距離をカスタマイズ
```csharp
using UnityEngine;
using UnityEngine.AI;

public class CustomNavMeshAgent : MonoBehaviour
{
    public Transform target;
    private NavMeshAgent agent;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();
        agent.speed = 6f; // 移動速度のカスタマイズ
        agent.stoppingDistance = 1f; // 目的地の手前1mで停止
        agent.angularSpeed = 120f; // 回転速度のカスタマイズ
    }

    void Update()
    {
        agent.SetDestination(target.position);
    }
}
```

#### 解説:
- `speed`や`stoppingDistance`の変更により、エージェントの動きが柔軟にカスタマイズできます。
- 目的地に近づいたときにスムーズに減速したり、到着後の挙動もコントロールできます。

---

### 6. **複雑なシーンでのNavMesh利用**
NavMeshは複雑な地形やマップでも利用可能です。橋や坂、複数階層の構造物を含むシーンでは、以下の方法を考慮してNavMeshを生成できます。

- **NavMesh Link**: 階段や橋のような複数の高さを移動する場合に使用。
- **NavMesh Obstacle**: 移動をブロックするオブジェクトに設定し、キャラクターがそのオブジェクトを避けて移動できるようにする。

---

### 7. **応用例：複数エージェントの管理**
複数のキャラクターが同時にNavMeshを使用して移動する場合のサンプルです。キャラクター同士がぶつからないように、NavMeshの衝突回避が自動で処理されます。

#### サンプルプログラム：
```csharp
using UnityEngine;
using UnityEngine.AI;

public class MultipleAgents : MonoBehaviour
{
    public Transform[] targets;
    private NavMeshAgent[] agents;

    void Start()
    {
        agents = FindObjectsOfType<NavMeshAgent>(); // シーン内の全てのNavMesh Agentを取得
    }

    void Update()
    {
        for (int i = 0; i < agents.Length; i++)
        {
            agents[i].SetDestination(targets[i % targets.Length].position); // 各エージェントに異なる目的地を設定
        }
    }
}
```

#### 解説:
- シーン内に複数のNavMeshエージェントを配置し、それぞれ異なる目的地に向かわせます。
- `NavMeshAgent`のコリジョン回避機能により、エージェント同士が衝突することなく移動します。

---

### 8. **NavMesh + TPS（Third Person Shooter）**
NavMeshとTPS視点を組み合わせて、プレイヤーが自由に動ける環境を提供します。

#### サンプルプログラム：
```csharp
using UnityEngine;
using UnityEngine.AI;

public class TPSNavMeshMove : MonoBehaviour
{
    public Camera playerCamera;
    private NavMeshAgent agent;

    void Start()
    {
        agent = GetComponent<NavMeshAgent>();
    }

    void Update()
    {
        // TPS風のカメラ移動
        if (Input.GetMouseButtonDown(0))
        {
            Ray ray = playerCamera.ScreenPointToRay(Input.mousePosition);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit))
            {
                agent.SetDestination(hit.point);
            }
        }
    }
}
```

#### 解説:
- プレイヤーのカメラからマウスクリックした地点をRaycastで検出し、その場所にNavMesh Agentが移動します。
- TPS視点により、キャラクターが画面に対してどの位置に移動するかをインタラクティブに操作できます。

---

## まとめ
この教材では、NavMeshの基本から応用までをカバーしました。`NavMesh Agent`の活用方法、マウスクリックでの移動、複数エージェントの管理、カスタマイズ可能なパラメータ、そしてTPS視

点との組み合わせまで、さまざまな応用が可能です。