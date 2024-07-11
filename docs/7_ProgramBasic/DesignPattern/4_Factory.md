# ファクトリーパターン

## 定義 
インスタンスの生成を、専門のメソッドに委譲するデザインパターンです。  
これにより、クラスのインスタンス化をクライアントから隠蔽・分離し、インターフェースを介して、具体的なクラスの型を指定せずに、オブジェクトを生成することができます。



## 目的
クラスのインスタンス生成に関する責任をクライアントから分離し、インスタンスの生成を一元管理。柔軟で再利用可能なコードを作成する。




## Unityでの実際の使用例
+ Prefab Factory: プレハブを使用してオブジェクトを生成するファクトリー。
+ Asset Factory: アセットを使用してリソースを生成するファクトリー。
+ Character Factory: ゲーム内のキャラクターオブジェクトを生成するファクトリー。
+ Enemy Factory: ゲーム内の敵キャラクターオブジェクトを生成するファクトリー。
+ Item Factory: ゲーム内のアイテムオブジェクトを生成するファクトリー。
+ Weapon Factory: ゲーム内の武器オブジェクトを生成するファクトリー。

<br>

## 利点
+ 柔軟性: 新しいクラスを追加する際に、既存のクライアントコードを変更する必要がない。
+ 分離性: クライアントと具体的な生成方法を分離することで、コードの理解とメンテナンスが容易になる。
+ 再利用性: 生成方法をカプセル化することで、同じ生成ロジックを複数の箇所で再利用できる。

<br>

## 注意点
+ 複雑性の増加: クラス階層とインターフェースの数が増えるため、設計が複雑になる可能性がある。
+ クラスの追加: ファクトリークラスやインターフェースなど、追加のクラスが必要になる。
+ 抽象化のバランス: 過度な抽象化により、理解が難しくなる場合があるため、適切なレベルでの抽象化が求められる。

<br>

## ファクトリーパターンの実装例

<br>
インターフェース:

```cs
public interface IEnemy {
    void Attack();
}
```

<br>
具体的なクラス設定:

```cs
public class Orc : IEnemy {
    public void Attack() {
        Debug.Log("Orc attacks!");
    }
}

public class Troll : IEnemy {
    public void Attack() {
        Debug.Log("Troll attacks!");
    }
}
```

<br>
ファクトリークラス:

```cs
public class EnemyFactory {
    public static IEnemy CreateEnemy(string type) {
        switch (type) {
            case "Orc":
                return new Orc();
            case "Troll":
                return new Troll();
            default:
                throw new ArgumentException("Unknown enemy type");
        }
    }
}
```

<br>
使用例

```cs
public class GameManager : MonoBehaviour {
    void Start() {
        IEnemy orc = EnemyFactory.CreateEnemy("Orc");
        orc.Attack();

        IEnemy troll = EnemyFactory.CreateEnemy("Troll");
        troll.Attack();
    }
}
```
