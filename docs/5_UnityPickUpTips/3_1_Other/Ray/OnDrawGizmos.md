# `OnDrawGizmos`について

`OnDrawGizmos`は、Unityエディタ上でシーンの視覚的なデバッグや補助情報を表示するためのツールです。これにより、開発中にオブジェクトの範囲、経路、位置関係などを直感的に把握することができます。

<br>

---

<br>

# 1. **Gizmosとは？**

**Gizmos**は、Unityエディタ内でオブジェクトの状態や関係を視覚的に表現するためのグラフィカル要素です。これらはゲームの実行時には表示されず、あくまでエディタ上でのみ表示されます。主な用途は以下の通りです：

- オブジェクトの範囲やサイズの確認
- ナビゲーションポイントやウェイポイントの表示
- レイキャストやセンサーの視覚化
- デバッグ情報の表示

<br>

---

<br>

# 2. **`OnDrawGizmos`と`OnDrawGizmosSelected`の違い**

- **`OnDrawGizmos`**        : オブジェクトが選択されていなくても常に実行され、Gizmosを描画します。
- **`OnDrawGizmosSelected`**: オブジェクトがエディタ上で選択されている場合にのみ実行され、Gizmosを描画します。

これにより、必要に応じて情報の表示範囲を制御することができます。

<br>

---

<br>

# 3. **`OnDrawGizmos`の基本的な使用方法**

## 3.1. **基本的な構造**

```csharp
using UnityEngine;

public class GizmoExample : MonoBehaviour
{
    void OnDrawGizmos()
    {
        // Gizmosの色を設定
        Gizmos.color = Color.red;
        
        // オブジェクトの位置に球を描画
        Gizmos.DrawSphere(transform.position, 1f);
    }
}
```

## 3.2. **実際の例: レイキャストの視覚化**

先ほどの`RaycastExample1`に`OnDrawGizmos`を追加して、レイキャストをエディタ上で視覚化する方法を紹介します。

```csharp
using UnityEngine;

namespace RaySample
{
    public class RaycastExample1 : MonoBehaviour
    {
        public float rayDistance = 10f;
        public ParticleSystem hitEffect; // ヒットエフェクト用のパーティクルシステムプレハブ

        private RaycastHit lastHit;

        void Update()
        {
            // レイを前方に発射
            Ray ray = new Ray(transform.position, transform.forward);
            RaycastHit hit;

            if (Physics.Raycast(ray, out hit, rayDistance))
            {
                Debug.Log("Hit object: " + hit.collider.name);

                // ヒットした点でエフェクトを表示
                if (hitEffect != null)
                {
                    Instantiate(hitEffect, hit.point, Quaternion.LookRotation(hit.normal));
                }

                // 最後のヒット情報を保存
                lastHit = hit;

                // デバッグ用のレイを赤で表示
                Debug.DrawRay(ray.origin, ray.direction * hit.distance, Color.red);
            }
            else
            {
                // ヒットしなかった場合のデバッグ用のレイを緑で表示
                Debug.DrawRay(ray.origin, ray.direction * rayDistance, Color.green);
            }
        }

        void OnDrawGizmos()
        {
            Gizmos.color = Color.yellow;

            // レイを視覚化
            Gizmos.DrawRay(transform.position, transform.forward * rayDistance);

            // ヒットした点に球を描画
            if (lastHit.collider != null)
            {
                Gizmos.color = Color.red;
                Gizmos.DrawSphere(lastHit.point, 0.2f);
            }
        }
    }
}
```

**解説:**

- `OnDrawGizmos`内で、レイキャストの方向と距離を黄色のレイとして描画します。
- レイがヒットした場合、そのヒットポイントに赤い球を描画します。
- `lastHit`変数を使用して、最後にヒットした情報を保持し、`OnDrawGizmos`で使用しています。

**注意:** `OnDrawGizmos`はゲームの実行中にもエディタ上で表示されますが、ゲームプレイ中のビルド版には影響しません。

<br>

---

<br>

# 4. **Gizmosの描画方法**

Unityでは、`Gizmos`クラスを使用してさまざまな形状を描画できます。以下に主要なメソッドを紹介します。

## 4.1. **基本的な描画メソッド**

| メソッド                     | 説明                                                 |
|-----------------------------|------------------------------------------------------|
| `Gizmos.DrawLine`            | 2点間に線を描画します。                             |
| `Gizmos.DrawWireSphere`      | ワイヤーフレームの球を描画します。                   |
| `Gizmos.DrawSphere`          | 塗りつぶされた球を描画します。                       |
| `Gizmos.DrawWireCube`        | ワイヤーフレームの立方体を描画します。               |
| `Gizmos.DrawCube`            | 塗りつぶされた立方体を描画します。                   |
| `Gizmos.DrawRay`             | レイ（線分）を描画します。                           |
| `Gizmos.DrawIcon`            | 指定した位置にアイコンを描画します。                 |
| `Gizmos.DrawFrustum`         | 視錐台（カメラの視野など）を描画します。             |

## 4.2. **具体的な描画例**

### 4.2.1. **線と球の描画**

```csharp
using UnityEngine;

public class GizmoShapesExample : MonoBehaviour
{
    void OnDrawGizmos()
    {
        // 線を描画
        Gizmos.color = Color.blue;
        Gizmos.DrawLine(transform.position, transform.position + Vector3.up * 5);

        // ワイヤーフレームの球を描画
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(transform.position + Vector3.up * 5, 1f);

        // 塗りつぶされた球を描画
        Gizmos.color = Color.red;
        Gizmos.DrawSphere(transform.position + Vector3.up * 7, 0.5f);
    }
}
```

**結果:**

- 青い線がオブジェクトの位置から上方向に5ユニット描画されます。
- 緑色のワイヤーフレームの球が線の終点に描画されます。
- 赤色の塗りつぶされた球がさらに上に描画されます。

<br>

### 4.2.2. **アイコンの描画**

Unityでは、エディタ用のカスタムアイコンをオブジェクトに描画することもできます。

```csharp
using UnityEngine;

public class GizmoIconExample : MonoBehaviour
{
    public Texture2D iconTexture;

    void OnDrawGizmos()
    {
        if (iconTexture != null)
        {
            Gizmos.DrawIcon(transform.position, "CustomIcon.png", true);
        }
    }
}
```

**注意点:**

- アイコン画像は`Assets/Gizmos`フォルダに配置する必要があります。
- ファイル名は相対パスで指定します（例: `"CustomIcon.png"`）。
- `Gizmos.DrawIcon`の第3引数は、アイコンを常に描画するかどうかを指定します。

<br>


### 4.2.3. **カスタム視錐台の描画**

```csharp
using UnityEngine;

public class GizmoFrustumExample : MonoBehaviour
{
    void OnDrawGizmos()
    {
        Matrix4x4 oldMatrix = Gizmos.matrix;

        // オブジェクトの位置と回転を基準にする
        Gizmos.matrix = transform.localToWorldMatrix;

        Gizmos.color = new Color(1, 0, 0, 0.1f);
        Gizmos.DrawFrustum(Vector3.zero, 60, 10, 1, 1.777f); // 視錐台を描画

        Gizmos.matrix = oldMatrix;
    }
}
```

**解説:**

- `Gizmos.matrix`を使用して、描画するGizmosの基準となる座標系を変更しています。
- `Gizmos.DrawFrustum`はカメラの視野などを視覚化する際に有用です。

<br>

---

<br>


# 5. **`OnDrawGizmosSelected`の使用例**

`OnDrawGizmosSelected`を使用すると、オブジェクトが選択されているときだけGizmosを描画できます。これにより、不要な描画を避け、エディタの視認性を向上させることができます。

```csharp
using UnityEngine;

public class GizmoSelectedExample : MonoBehaviour
{
    void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.cyan;
        Gizmos.DrawWireCube(transform.position, Vector3.one * 2);
    }
}
```

**結果:**

- このスクリプトがアタッチされたオブジェクトを選択すると、オブジェクトの周囲にシアン色のワイヤーフレーム立方体が描画されます。

<br>

---

<br>

# 6. **実践的な応用例**

## 6.1. **センサー範囲の視覚化**

例えば、敵キャラクターがプレイヤーを検知する範囲（視界や追跡範囲）をGizmosで表示することができます。

```csharp
using UnityEngine;

public class EnemySensor : MonoBehaviour
{
    public float viewRadius = 10f;
    [Range(0, 360)]
    public float viewAngle = 90f;

    void OnDrawGizmos()
    {
        // 視界の範囲を円で描画
        Gizmos.color = new Color(1, 0, 0, 0.2f); // 半透明の赤
        Gizmos.DrawSphere(transform.position, viewRadius);

        // 視角を示す線を描画
        Vector3 leftBoundary = Quaternion.Euler(0, -viewAngle / 2, 0) * transform.forward * viewRadius;
        Vector3 rightBoundary = Quaternion.Euler(0, viewAngle / 2, 0) * transform.forward * viewRadius;

        Gizmos.color = Color.red;
        Gizmos.DrawRay(transform.position, leftBoundary);
        Gizmos.DrawRay(transform.position, rightBoundary);
    }
}
```

**解説:**

- `viewRadius`は視界の半径を示し、赤色の半透明の球として描画されます。
- `viewAngle`は視界の角度を示し、左右の境界線として赤色の線が描画されます。

### 6.2. **ウェイポイントの経路表示**

複数のウェイポイントを持つオブジェクトの移動経路をGizmosで表示することも可能です。

```csharp
using UnityEngine;

public class WaypointPath : MonoBehaviour
{
    public Transform[] waypoints;

    void OnDrawGizmos()
    {
        if (waypoints == null || waypoints.Length < 2)
            return;

        Gizmos.color = Color.green;
        for (int i = 0; i < waypoints.Length - 1; i++)
        {
            Gizmos.DrawLine(waypoints[i].position, waypoints[i + 1].position);
        }

        // 最後のウェイポイントと最初のウェイポイントを繋げる（ループ）
        Gizmos.DrawLine(waypoints[waypoints.Length - 1].position, waypoints[0].position);
    }
}
```

**解説:**

- ウェイポイント間を緑色の線で繋ぎ、経路を視覚化します。
- ループを形成するために、最後のウェイポイントと最初のウェイポイントを繋げています。

<br>


# 7. **ベストプラクティス**

- **パフォーマンスを意識する**: `OnDrawGizmos`はエディタ上で毎フレーム実行されるため、重い処理は避けましょう。
- **色や透明度を活用する**: 色や透明度を使い分けて、異なる情報を視覚的に区別しやすくします。
- **適切な描画方法を選ぶ**: 情報の種類に応じて適切なGizmosの描画メソッドを選択します。
- **コメントを追加する**: 何を描画しているのかをコード内にコメントとして残すことで、他の開発者や将来の自分自身にとって理解しやすくなります。

<br>


# 8. **まとめ**

`OnDrawGizmos`と`OnDrawGizmosSelected`は、Unityエディタ内でオブジェクトの状態や関係を視覚的にデバッグ・補助するための非常に有用なツールです。これらを活用することで、開発効率を大幅に向上させることができます。以下に主要なポイントをまとめます：

- **Gizmosはエディタ専用**: ゲーム実行時には表示されず、開発中の視覚的補助として使用されます。
- **描画方法が豊富**: 線、球、立方体、アイコンなど、多様な形状を描画できます。
- **選択状態での描画制御**: `OnDrawGizmosSelected`を使うことで、必要なときだけ情報を表示できます。
- **実践的な応用例が多数**: センサー範囲、ウェイポイント経路、視錐台の表示など、多岐にわたる用途があります。

これらの機能を効果的に活用し、より洗練された開発体験を実現してください。
