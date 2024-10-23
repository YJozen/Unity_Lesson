# 1. Boundsの基本

**Bounds**は、3D空間におけるオブジェクトの大きさや位置を表すための境界ボックス（Bounding Box）です。通常、`Bounds`は中心点とサイズ（幅、高さ、奥行き）によって定義されます。

主に以下のように使用されます。

- **可視範囲の判定**: オブジェクトがカメラに映るかどうかを判断する際に、Boundsを使用して視界内に存在するかを判定できます。
- **オブジェクトの衝突判定**: コリジョンを処理する際に、Boundsを利用して、オブジェクト同士が接触しているかどうかを判断します。

<br>

# 2. Boundsとコリジョン

コリジョン判定において、Boundsは以下のように利用されます。

## 2.1. 衝突の最初のフィルタリング

コリジョンシステムは、実際の物理計算を行う前に、オブジェクトのBoundsを使用して初期フィルタリングを行います。これにより、次のようなメリットがあります。

- **パフォーマンスの向上**: Boundsが重ならない場合、そのオブジェクト同士は衝突しないため、物理計算を省略できます。これにより、計算負荷が大幅に軽減されます。

- **簡易判定**: Boundsのオーバーラップをチェックすることで、実際のコリジョンの前に簡易的な衝突判定が行われます。これにより、複雑な形状のMesh Colliderを使わなくても、簡易的な形状（Box、Sphereなど）でオーバーラップを判定できます。

<br>

## 2.2. Colliderの形状とBounds

Colliderは、オブジェクトの形状に基づいてBoundsを生成します。  
たとえば、Box Colliderはその形状に合わせたBoundsを持ち、Sphere Colliderも同様です。これにより、次のことが可能になります。

- **形状の適切なサイズと位置を保持**: 各Colliderは自動的にBoundsを計算するため、オブジェクトが移動する際にもBoundsが自動的に更新されます。

- **可視性の管理**: Boundsを利用してオブジェクトがカメラに映るかどうかを判定する際に、Colliderの形状を考慮した適切なBoundsが必要です。

<br>

# 3. Boundsの使用方法

## 3.1
Unityでは、`Collider`や`Renderer`クラスが`bounds`プロパティを持っています。これを使用して、オブジェクトの境界ボックスを取得することができます。

以下に例を示します。

```csharp
void Update()
{
    // GameObjectのRendererからBoundsを取得
    Bounds bounds = GetComponent<Renderer>().bounds;
    
    // Boundsの中心位置を取得
    Vector3 center = bounds.center;

    // Boundsのサイズを取得
    Vector3 size = bounds.size;

    Debug.Log("Center: " + center + ", Size: " + size);
}
```

<br>

## 3.2

`Bounds`を使用して当たり判定を行う場合、特定のオブジェクトとの衝突や接触を直接判別することはできませんが、オブジェクトの境界を比較することで、重なりや交差を確認することが可能です。  
`Bounds`クラスを使用して、2つのオブジェクトの境界が重なっているかどうかを判断できます。

<br>

## `Bounds`を使った当たり判定の基本

`Bounds`は3D空間でのオブジェクトの範囲を表すクラスで、中心点、サイズ、最小・最大の座標を持っています。これを使って、他のオブジェクトとの重なりを確認することができます。

<br>

## 例: `Bounds`を使用してオブジェクトの重なりを確認する

特定のオブジェクトと自分自身のオブジェクトが重なっているかどうかを判別するサンプルコード。

```csharp
using UnityEngine;

public class BoundsChecker : MonoBehaviour
{
    // チェック対象のオブジェクト
    public GameObject targetObject;

    void Update()
    {
        // 自分自身のBoundsを取得。自分自身の`Collider`の境界を取得
        Bounds myBounds = GetComponent<Collider>().bounds;

        // チェック対象のオブジェクトのBounds(境界)を取得
        Bounds targetBounds = targetObject.GetComponent<Collider>().bounds;

        // Boundsが重なっているかをチェック
        if (myBounds.Intersects(targetBounds))
        {
            Debug.Log("オブジェクトが重なっています: " + targetObject.name);
        }
    }
}
```

<br>

# 注意点

1. **精度**: `Bounds`は、オブジェクトの形状が単純である場合（例えば、立方体や球体）にはうまく機能しますが、複雑な形状のオブジェクトに対しては、境界ボックスが正確にオブジェクトの形状を表現しないことがあります。

2. **トリガーと物理**: `Bounds`を使った当たり判定は物理エンジンの動作とは独立しているため、衝突の反応を伴わない点に注意が必要です。物理的な応答が必要な場合は、`OnCollisionEnter`や`OnTriggerEnter`を使用することが推奨されます。

