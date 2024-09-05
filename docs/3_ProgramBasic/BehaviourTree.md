以下は、`Behaviour Tree`と`Blackboard`を実装するための各ファイルの説明と、`AIController.cs`の内容を少し増やした解説です。

## ファイル構成
```
BehaviourTree/
    BTNode.cs
    Selector.cs
    Sequence.cs
    TaskNode.cs
Blackboard/
    Blackboard.cs
AIController.cs
```

## 各ファイルの説明

### 1. `BTNode.cs`
**説明**:  
`BTNode`は、Behaviour Treeの基本ユニットである「ノード」を表現する抽象クラスです。全てのBehaviour Treeノードは、このクラスを継承して、`Execute`メソッドを実装する必要があります。`Execute`メソッドは、ノードが成功したか失敗したかを示す`bool`値を返します。

**内容**:
```csharp
namespace BehaviourTree
{
    public abstract class BTNode
    {
        public abstract bool Execute();
    }
}
```

### 2. `Selector.cs`
**説明**:  
`Selector`ノードは、複数の子ノードを持ち、子ノードを順に実行します。子ノードのうち一つでも成功したら、`Selector`ノード全体が成功と見なされます。全ての子ノードが失敗した場合、`Selector`ノードも失敗と見なされます。

**内容**:
```csharp
namespace BehaviourTree
{
    public class Selector : BTNode
    {
        private BTNode[] nodes;
        public Selector(params BTNode[] nodes)
        {
            this.nodes = nodes;
        }

        public override bool Execute()
        {
            foreach (var node in nodes)
            {
                if (node.Execute())
                    return true;
            }
            return false;
        }
    }
}
```

### 3. `Sequence.cs`
**説明**:  
`Sequence`ノードは、複数の子ノードを持ち、子ノードを順に実行します。全ての子ノードが成功した場合、`Sequence`ノード全体が成功と見なされます。もし一つでも子ノードが失敗したら、`Sequence`ノードも失敗と見なされます。

**内容**:
```csharp
namespace BehaviourTree
{
    public class Sequence : BTNode
    {
        private BTNode[] nodes;
        public Sequence(params BTNode[] nodes)
        {
            this.nodes = nodes;
        }

        public override bool Execute()
        {
            foreach (var node in nodes)
            {
                if (!node.Execute())
                    return false;
            }
            return true;
        }
    }
}
```

### 4. `TaskNode.cs`
**説明**:  
`TaskNode`は、具体的な処理を実行するためのノードです。このノードは、`Func<bool>`型のデリゲートを受け取り、それを`Execute`メソッドで呼び出すことで、タスクを実行します。タスクの結果は、成功なら`true`、失敗なら`false`として返されます。

**内容**:
```csharp
namespace BehaviourTree
{
    public class TaskNode : BTNode
    {
        private Func<bool> task;
        public TaskNode(Func<bool> task)
        {
            this.task = task;
        }

        public override bool Execute()
        {
            return task.Invoke();
        }
    }
}
```

### 5. `Blackboard.cs`
**説明**:  
`Blackboard`は、AIの「知識ベース」として機能するクラスで、AIエージェントが共有するデータを格納します。`Dictionary`を用いてデータをキーと値のペアで保存し、必要なときに他のクラスやノードがデータにアクセスできます。これにより、各ノードが共通のデータに基づいて動作を決定できます。

**内容**:
```csharp
namespace BlackboardSystem
{
    public class Blackboard
    {
        private Dictionary<string, object> data = new Dictionary<string, object>();

        public void SetData<T>(string key, T value)
        {
            data[key] = value;
        }

        public T GetData<T>(string key)
        {
            return (T)data[key];
        }
    }
}
```

### 6. `AIController.cs`
**説明**:  
`AIController`は、ゲーム内のAIキャラクターにBehaviour TreeとBlackboardを使用して動作を制御するためのスクリプトです。`Blackboard`インスタンスを持ち、`Behaviour Tree`のノードを構築して、特定の条件やタスクを設定します。このクラスでは、キャラクターがどのように行動するかを定義し、ゲーム内でのAIの動作を実行します。

**内容**:
```csharp
using UnityEngine;
using BehaviourTree;  // Behaviour Treeのクラスを使用
using BlackboardSystem;  // Blackboardクラスを使用

public class AIController : MonoBehaviour
{
    private Blackboard blackboard;
    private BTNode behaviourTree;

    void Start()
    {
        // Blackboardの初期化
        blackboard = new Blackboard();
        blackboard.SetData("Health", 50);
        blackboard.SetData("IsEnemyNear", false);

        // Behaviour Treeの構築
        behaviourTree = new Selector(
            new Sequence(
                new TaskNode(() => blackboard.GetData<int>("Health") <= 70),
                new TaskNode(() => Heal())
            ),
            new TaskNode(() => EngageEnemy())
        );

        // Behaviour Treeの実行
        behaviourTree.Execute();
    }

    bool Heal()
    {
        // 回復行動の処理
        Debug.Log("Healing...");
        blackboard.SetData("Health", blackboard.GetData<int>("Health") + 20);
        return true;
    }

    bool EngageEnemy()
    {
        // 敵との戦闘処理
        if (blackboard.GetData<bool>("IsEnemyNear"))
        {
            Debug.Log("Engaging Enemy...");
            return true;
        }
        return false;
    }

    void Update()
    {
        // 定期的にBehaviour Treeを評価
        behaviourTree.Execute();
    }
}
```

**追加の解説**:
- `Start`メソッド内で、Blackboardに初期データを設定しています。例えば、`Health`の値を50に設定し、`IsEnemyNear`を`false`に設定しています。
- `Heal`メソッドと`EngageEnemy`メソッドは、それぞれキャラクターが回復するか、敵と戦闘を行うかを決定します。これらのメソッドは`TaskNode`でラップされ、Behaviour Tree内で使用されています。
- `Update`メソッド内で、毎フレームBehaviour Treeが再評価され、状況に応じて適切な行動を取ります。

<br>

<hr>

<hr>

<br>

以下に、テキストベースのダイアグラムを作成しました。この図は、各クラスの関係性と階層構造を示しています。

```
+----------------+     uses     +-------------------+
|  AIController  |<-------------|    Blackboard     |
+----------------+              +-------------------+
        |
        | uses
        |
        v
+----------------+
|     BTNode     |
+----------------+
        ^
        |
   +----+----+----+
   |         |    |
+--------+ +----------+ +----------+
|Selector| | Sequence | | TaskNode |
+--------+ +----------+ +----------+



Legend:
+-------+    +-----------+
| Class | or | Interface |
+-------+    +-----------+


<------------- : Uses/Depends on


      ^
      | : Inherits from
```

この図では:

1. `AIController`が`Blackboard`と`BTNode`を使用しています。
2. `Selector`、`Sequence`、`TaskNode`は全て`BTNode`を継承しています。
3. `Selector`と`Sequence`は複数の`BTNode`を含むことができます（子ノード）。

この図は、プログラムの主要なコンポーネント間の関係を視覚化しています。`AIController`がどのようにBehaviour TreeとBlackboardを使用して、AIの動作を制御しているかが分かります。
