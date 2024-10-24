#  **OnCollision～ と OnTrigger～ **

**OnCollision**と**OnTrigger**は、Unityにおける二つの異なる当たり判定システムです。主な違いは以下の通りです。








- **OnCollision～**:  
オブジェクトが物理的に衝突した際に呼ばれるメソッド。剛体（`Rigidbody`）が必要で、物理挙動の影響を受けます。

- **OnTrigger～**:  
オブジェクトが「衝突した」としても物理的な反応（反発、停止）はなく、単に当たり判定が検知されたことを知らせるためのメソッド。通常、`Collider`の「Is Trigger」オプションを有効にして使用します。

<br>

<br>

# **OnCollision～ メソッド（物理的な衝突）**

<img src="images/collision.png" width="90%" alt="" title="">


オブジェクト同士が物理的に衝突したときに呼ばれるメソッドです。主な使用メソッドは以下です。

- **OnCollisionEnter**: 衝突が始まった瞬間に呼ばれる。
- **OnCollisionStay**: 衝突が続いている間、毎フレーム呼ばれる。
- **OnCollisionExit**: 衝突が終了したときに呼ばれる。

これらは、`Collision`クラスを通じて衝突の詳細情報を取得します。

```csharp
void OnCollisionEnter(Collision collision)
{
    // 衝突したオブジェクトの名前を出力
    Debug.Log("Collided with: " + collision.gameObject.name);
    
    // 衝突の位置や法線ベクトル
    foreach (ContactPoint contact in collision.contacts)
    {
        Debug.Log("Contact point: " + contact.point);
        Debug.Log("Contact normal: " + contact.normal);
    }
}
```

**`Collision`クラス**には以下のプロパティがあります。

- `collision.gameObject`: 衝突した相手のゲームオブジェクト。
- `collision.contacts`: 衝突点情報の配列（`ContactPoint[]`）。衝突の位置や面の法線ベクトルを取得。
- `collision.relativeVelocity`: 衝突した際の速度差を示すベクトル。


<br>

<br>

# **OnTrigger～ メソッド（トリガー検知）**

<img src="images/OnTriggerExit実行.gif" width="90%" alt="" title="">

`OnTrigger～`メソッドは、物理的な衝突ではなく、当たり判定の領域に入ったか出たかを検知するためのものです。通常、`Collider`の「Is Trigger」オプションを有効にして使用します。`Rigidbody`は必須ではありませんが、`Rigidbody`を持つオブジェクト間で使うのが一般的です。

- **OnTriggerEnter**: トリガー領域に入った時に呼ばれる。
- **OnTriggerStay**: トリガー領域にいる間、毎フレーム呼ばれる。
- **OnTriggerExit**: トリガー領域から出た時に呼ばれる。

```csharp
void OnTriggerEnter(Collider other)
{
    // トリガーに入ったオブジェクトの名前を出力
    Debug.Log("Triggered by: " + other.gameObject.name);
}
```

**`Collider`クラス**には以下のプロパティがあります。

- `other.gameObject`: トリガー領域に入ったオブジェクト。
- `other.transform`: トリガー領域に入ったオブジェクトのトランスフォーム情報。



---
