レイ(Ray)は、3D空間で直線的な視線を発射するために使われ、物体との衝突判定や視線の検出に利用されます。レイは基本的に `Ray` 構造体を使って扱います。

[使用例](Detect/Detect.md)



<br>


# 1. 基本的なレイの使い方

## レイのキャスト
レイを発射して物体との衝突を検出する方法です。以下の例では、レイキャストを使って衝突した物体の情報を取得します。

```csharp
using UnityEngine;

public class RaycastExample : MonoBehaviour
{
    public float rayDistance = 10f;
    // public ParticleSystem hitEffect; // ヒットエフェクト用のパーティクルシステムプレハブ

    void Update()
    {
        // レイを前方に発射
        Ray ray = new Ray(transform.position, transform.forward);
        RaycastHit hit;

        if (Physics.Raycast(ray, out hit, rayDistance))
        {
            Debug.Log("Hit object: " + hit.collider.name);
            // 例: ヒットした点でエフェクトを表示する
            // if (hitEffect != null)
            // {
            //     Instantiate(hitEffect, hit.point, Quaternion.LookRotation(hit.normal));
            // }
            Debug.DrawRay(ray.origin, ray.direction * hit.distance, Color.red);
        }
        else
        {
            // ヒットしなかった場合の処理
            Debug.DrawRay(ray.origin, ray.direction * rayDistance, Color.green);
        }
    }
}
```

この例では、カメラやオブジェクトの前方にレイを発射し、指定した距離で物体に衝突したかどうかを確認しています。`RaycastHit` には衝突した物体の情報（位置、法線、衝突したオブジェクトなど）が含まれます。


<br>


# 2. レイキャストの結果を配列で取得

Unityの `Physics.RaycastAll` メソッドを使うと、レイが複数の物体に衝突する場合に、衝突したすべての物体の情報を配列で取得できます。

```csharp
using UnityEngine;

public class RaycastAllExample : MonoBehaviour
{
    public float rayDistance = 10f;

    void Update()
    {
        // レイを前方に発射
        Ray ray = new Ray(transform.position, transform.forward);
        RaycastHit[] hits = Physics.RaycastAll(ray, rayDistance);

        foreach (RaycastHit hit in hits)
        {
            Debug.Log("Hit object: " + hit.collider.name);
            // 例: ヒットした点でエフェクトを表示する
            Debug.DrawRay(ray.origin, ray.direction * hit.distance, Color.red);
        }
    }
}
```

`Physics.RaycastAll` は、レイが通過したすべての物体との衝突情報を `RaycastHit` の配列で返します。


<br>


# 3. レイキャストにレイヤーマスクを適用

レイキャストを特定のレイヤーの物体に対してのみ行いたい場合は、レイヤーマスクを指定できます。

```csharp
using UnityEngine;

public class RaycastLayerMaskExample : MonoBehaviour
{
    public float rayDistance = 10f;
    public LayerMask layerMask; // 対象レイヤーを指定するためのレイヤーマスク

    void Update()
    {
        // レイを前方に発射
        Ray ray = new Ray(transform.position, transform.forward);
        RaycastHit hit;

        if (Physics.Raycast(ray, out hit, rayDistance, layerMask))
        {
            Debug.Log("Hit object: " + hit.collider.name);
            // 例: ヒットした点でエフェクトを表示する
            Debug.DrawRay(ray.origin, ray.direction * hit.distance, Color.red);
        }
        else
        {
            // ヒットしなかった場合の処理
            Debug.DrawRay(ray.origin, ray.direction * rayDistance, Color.green);
        }
    }
}
```

`layerMask` に設定したレイヤーだけがレイキャストの対象となります。

<br>

# 4. 複数のレイキャストを使った例

複数のレイを使って、広い範囲での衝突を検出することもできます。たとえば、円形の視野を持つレイキャストなどが考えられます。

```csharp
using UnityEngine;

public class MultipleRaycastsExample : MonoBehaviour
{
    public float rayDistance = 10f;
    public float fieldOfView = 45f; // 視野の角度
    public int numberOfRays = 10;    // 発射するレイの数

    void Update()
    {
        float angleStep = fieldOfView / numberOfRays;
        float currentAngle = -fieldOfView / 2;

        for (int i = 0; i < numberOfRays; i++)
        {
            // レイを発射する方向を計算
            Vector3 direction = Quaternion.Euler(0, currentAngle, 0) * transform.forward;
            Ray ray = new Ray(transform.position, direction);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit, rayDistance))
            {
                Debug.Log("Hit object: " + hit.collider.name);
                Debug.DrawRay(ray.origin, ray.direction * hit.distance, Color.red);
            }

            currentAngle += angleStep;
        }
    }
}
```

この例では、視野の範囲にわたって複数のレイを発射し、それぞれのレイが物体に衝突したかどうかを確認しています。


<br>



<br>


# まとめ

- **基本的なレイキャスト**: `Physics.Raycast` を使用して単一のレイで物体との衝突を検出します。
- **複数のレイキャスト**: `Physics.RaycastAll` を使用して複数の衝突情報を取得します。
- **レイヤーマスク**: `Physics.Raycast` で特定のレイヤーに対するレイキャストを行います。
- **複数レイの視覚化**: `Debug.DrawRay` を使ってレイの発射方向を視覚化します。

これらの方法を活用して、さまざまなレイキャストのシナリオを実現できます。

<br>

---

<br>

[使用例_サンプルプログラム](Detect/Detect.md)

[OnDrawGizmosについて](OnDrawGizmos.md)

[Debugについて](Debug.md)