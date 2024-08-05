デコレーターパターン

デコるのデコ　

## 定義: 
デオブジェクトに追加機能を動的に付加するためのデザインパターンです。このパターンは、基本機能を持つオブジェクトを「装飾」し、追加機能を持つ新しいオブジェクトを作成することで、元のクラスを変更せずに機能を拡張する方法を提供します。


## 目的:
基本機能を変更せずにオブジェクトの振る舞いを拡張する。  
デコレータパターンの主な目的は、クラスの機能を拡張するために継承を使用するのではなく、コンポジションを使用することです。これにより、動的に機能を追加・削除でき、コードの柔軟性と再利用性を高めることができます。  
機能の追加: クラスの機能を継承なしで動的に拡張する。  
柔軟性   : 元のクラスを変更することなく、機能を追加・変更できる。

## 使用例
UIコンポーネント      : UnityのUIシステムで、装飾的な要素を追加するために使用されることがあります。
ゲームオブジェクトの装飾: 特定の機能を持つゲームオブジェクトに、追加の機能を動的に付加するために使用されます。

## 利点
柔軟性      : オブジェクトの振る舞いを動的に変更できる。基本機能を変更することなく、新しい機能を追加できる。
再利用性     : デコレータクラスを組み合わせて、新しい振る舞いを作成できる。追加機能を個別のデコレーターとして定義し、異なるオブジェクトに適用できる。
単一責任の原則: クラスが1つの機能に特化し、機能追加が必要な場合はデコレータを使う。各デコレーターが特定の機能追加を担当することで、クラスの責任を分離できる。



## 欠点
デコレータを多用すると、コードが複雑になり追跡が困難になる場合がある。



## 構造
+ コンポーネント（Component）: 追加機能を提供するための基本となるオブジェクトのインターフェースまたは抽象クラス。
+ 具体コンポーネント（Concrete Component）: 基本機能を実装するクラス。
+ デコレータ（Decorator）: コンポーネントインターフェースを実装または拡張する抽象クラス。基本コンポーネントへの参照を保持し、そのメソッドを拡張する。
+ 具体デコレータ（Concrete Decorator）: デコレータクラスを拡張し、追加機能を実装するクラス。

## デコレーターパターンの実装例
Unityでデコレーターを使用してプレイヤーの能力を拡張する例を示します。
GameManager.csに関しては適当なGameObjectにアタッチしてください。

<br>
インターフェース

```cs
public interface IPlayer {
    void Attack();
}
```
基本となるプレイヤーの動作を定義するインターフェースを作成。  
プレイヤーが持つべき基本的な動作を定義します。  



<br>
具体的なプレイヤークラス

```cs
public class BasicPlayer : IPlayer {
    public void Attack() {
        Debug.Log("Player attacks!");
    }
}
```
IPlayerインターフェースを実装する基本的なプレイヤークラス。  



<br>
デコレータークラス

```cs
public abstract class PlayerDecorator : IPlayer {
    protected IPlayer decoratedPlayer;

    public PlayerDecorator(IPlayer player) {
        this.decoratedPlayer = player;
    }

    public virtual void Attack() {
        decoratedPlayer.Attack();
    }
}
```
デコレータの基本クラスを定義します。  
このクラスは、IPlayerインターフェースを実装し、他のIPlayerオブジェクトをラップします。

<br>

「ラップする（wrap）」  
プログラミングにおいて特定のオブジェクトを他のオブジェクトで包み込むこと。  
これにより、元のオブジェクトの機能を拡張したり、変更したり、追加の機能を提供することができます。  
デコレータパターンでは、基本となるオブジェクトをデコレータオブジェクトで包み込み（ラップし）、新しい機能を提供します。

<br>

decoratedPlayerは、ラップされるIPlayerオブジェクトです。  
PlayerDecoratorクラスはIPlayerインターフェースを実装し、コンストラクターでラップするプレイヤーオブジェクトを受け取ります。  
Attackメソッドは、ラップされているプレイヤーオブジェクトのAttackメソッドを呼び出します。




<br>
具体的なデコレータクラス

```cs
public class FireAttackDecorator : PlayerDecorator {
    public FireAttackDecorator(IPlayer player) : base(player) { }

    public override void Attack() {
        base.Attack();
        AddFireAttack();
    }

    private void AddFireAttack() {
        Debug.Log("Player attacks with fire!");
    }
}

public class IceAttackDecorator : PlayerDecorator {
    public IceAttackDecorator(IPlayer player) : base(player) { }

    public override void Attack() {
        base.Attack();
        AddIceAttack();
    }

    private void AddIceAttack() {
        Debug.Log("Player attacks with ice!");
    }
}
```
基本的なプレイヤーの攻撃に新しい攻撃方法を追加する具体的なデコレータクラスを作成します。  
BasicPlayerオブジェクトをデコレータで包み込みます。  
これにより、新しい機能を追加します。上記の例では、FireAttackDecoratorクラスで火の攻撃を追加しています。


FireAttackDecoratorは、PlayerDecoratorを継承しています。  
コンストラクタで、ラップする対象を受け取ります。（あとでBasicPlayerを渡します）
Attackメソッドをオーバーライドし、まず基本のAttackメソッドを呼び出し）、その後に火の攻撃を追加しています。

<br>
使用例

```cs
public class GameManager : MonoBehaviour {
    void Start() {
        IPlayer basicPlayer   = new BasicPlayer();
        IPlayer firePlayer    = new FireAttackDecorator(basicPlayer);
        IPlayer iceFirePlayer = new IceAttackDecorator(firePlayer);

        basicPlayer.Attack();   // Output: "Player attacks!"
        firePlayer.Attack();    // Output: "Player attacks!" followed by "Player attacks with fire!"
        iceFirePlayer.Attack(); // Output: "Player attacks!" followed by "Player attacks with fire!" and "Player attacks with ice!"
    }
}
```

デコレータパターンを実際に使用する例です。  
`basicPlayer`は、単純なプレイヤーオブジェクトです。
`firePlayer`は、`basicPlayer`をラップし、火の攻撃を追加したプレイヤーオブジェクトです。  
`iceFirePlayer`は、`firePlayer`をラップし、火の攻撃と氷の攻撃を追加したプレイヤーオブジェクトです。  

デコレータパターンを使用すると、基本クラスを変更せずに新しい機能を追加することができます。この例では、プレイヤーの攻撃に火や氷の攻撃を動的に追加しました。このパターンを使用することで、コードの柔軟性と再利用性を高めることができます。