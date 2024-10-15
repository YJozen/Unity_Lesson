移動方法における**Custom Script**は、ゲームの特定の要件に応じて自由に実装できるため、柔軟性が高いです。  
いくつかの異なる考え方や、具体的な例について記述します。

<br>

# 1. **速度ベクトルを使った移動**

カスタム移動スクリプトの基本的な形は、速度ベクトルを使用して移動する方法です。これは物理エンジンに頼らずにオブジェクトを操作したい場合に有用です。

#### サンプルコード：速度ベクトルを用いた移動

```csharp
using UnityEngine;

public class VelocityBasedMovement : MonoBehaviour {
    public Vector3 velocity;
    public float speed = 5f;

    void Update() {
        // 速度ベクトルに基づいた移動
        transform.position += velocity * speed * Time.deltaTime;
    }
}
```

- **考え方**: 速度ベクトル (`velocity`) を定義して、そのベクトルに基づいてオブジェクトを移動させます。例えば、特定の方向に向かって定速度で動かす場合に適しています。
  
<br>

---

# 2. **補間を使った移動 (Lerp, Slerp)**

補間（`Lerp`や`Slerp`）を使うと、滑らかな移動やアニメーション効果が得られます。これは、オブジェクトを指定した2点間で動かす際に、ゆっくりと変化するようにしたい場合に便利です。

#### サンプルコード：Lerpを使った位置補間

```csharp
using UnityEngine;

public class LerpMovement : MonoBehaviour {
    public Transform targetPosition;
    public float speed = 0.1f;

    void Update() {
        // Lerpを使って現在位置からターゲット位置に移動
        transform.position = Vector3.Lerp(transform.position, targetPosition.position, speed * Time.deltaTime);
    }
}
```

- **考え方**: 線形補間 (`Lerp`) によって、開始位置から終了位置まで滑らかに移動します。Slerpは球面線形補間で、回転のような動きにも使用できます。

---

<br>

# 3. **慣性や滑らかな動きを表現するスクリプト**

慣性や自然な減速をシミュレートする場合、速度や加速度を操作するカスタムスクリプトがよく使われます。これは、特に物理エンジンを使わない場合や、細かいコントロールが必要なときに有効です。

#### サンプルコード：加速・減速を伴う移動

```csharp
using UnityEngine;

public class InertiaMovement : MonoBehaviour {
    public float acceleration = 1f;
    public float deceleration = 0.9f;
    public float maxSpeed = 10f;
    private Vector3 velocity = Vector3.zero;

    void Update() {
        // 入力に基づいて加速
        if (Input.GetKey(KeyCode.W)) {
            velocity += transform.forward * acceleration * Time.deltaTime;
        }

        // 最大速度を制限
        velocity = Vector3.ClampMagnitude(velocity, maxSpeed);

        // 慣性に基づく移動
        transform.position += velocity * Time.deltaTime;

        // 入力がないときに減速
        if (!Input.anyKey) {
            velocity *= deceleration;
        }
    }
}
```

- **考え方**: 速度が徐々に増加する加速度や、キーを離したときに徐々に減速する慣性をシミュレートしています。これは、スムーズな移動体験を提供する際に使われます。


<br>

---

# 4. **Waypoints（経路ポイント）を使った移動**

経路上のポイントを連続して移動させることもよく使われます。ポイント間の移動の制御です。

#### サンプルコード：経路ポイントを使った移動

```csharp
using UnityEngine;

public class WaypointMovement : MonoBehaviour {
    public Transform[] waypoints;
    public float speed = 5f;
    private int currentWaypointIndex = 0;

    void Update() {
        if (waypoints.Length == 0) return;

        // 現在のウェイポイントに向かって移動
        transform.position = Vector3.MoveTowards(transform.position, waypoints[currentWaypointIndex].position, speed * Time.deltaTime);

        // ウェイポイントに到達したかを確認
        if (Vector3.Distance(transform.position, waypoints[currentWaypointIndex].position) < 0.1f) {
            currentWaypointIndex = (currentWaypointIndex + 1) % waypoints.Length; // 次のウェイポイントへ
        }
    }
}
```

- **考え方**: 一連のウェイポイントを設定し、オブジェクトがそのポイント間を順番に移動するようにします。敵パトロールや特定のルートを辿る場合に適しています。

<br>

---

# 5. **キュービックベジェ曲線を使った移動**

ベジェ曲線は、滑らかな曲線上をオブジェクトに移動させる方法です。パスの形状を柔軟に制御でき、アニメーションやモーションパスとしてよく使われます。

#### サンプルコード：ベジェ曲線を使った移動

```csharp
using UnityEngine;

public class BezierCurveMovement : MonoBehaviour {
    public Transform point0, point1, point2, point3;
    public float speed = 0.1f;
    private float t = 0f;

    void Update() {
        // ベジェ曲線の計算
        t += speed * Time.deltaTime;
        t = Mathf.Clamp01(t);

        transform.position = CalculateBezierPoint(t, point0.position, point1.position, point2.position, point3.position);
    }

    Vector3 CalculateBezierPoint(float t, Vector3 p0, Vector3 p1, Vector3 p2, Vector3 p3) {
        float u = 1 - t;
        float tt = t * t;
        float uu = u * u;
        float uuu = uu * u;
        float ttt = tt * t;

        Vector3 p = uuu * p0; // 第一項
        p += 3 * uu * t * p1; // 第二項
        p += 3 * u * tt * p2; // 第三項
        p += ttt * p3; // 第四項

        return p;
    }
}
```

- **考え方**: ベジェ曲線は、指定したコントロールポイントを使って滑らかなカーブを描く移動が可能です。オブジェクトの優雅な移動やアニメーションパスでよく使われます。

<br>

---

# 6. **時間に基づいた移動**

`Time.time`や`Time.deltaTime`を使って時間基準で移動させるスクリプトもあります。フレームレートに依存しない動きを作成するために、時間を基準にすることは重要です。

#### サンプルコード：時間基準の移動

```csharp
using UnityEngine;

public class TimeBasedMovement : MonoBehaviour {
    public float speed = 5f;
    private float startTime;

    void Start() {
        startTime = Time.time; // 開始時刻を取得
    }

    void Update() {
        // 経過時間に基づいて移動
        float t = (Time.time - startTime) * speed;
        transform.position = new Vector3(Mathf.Sin(t), 0.0f, Mathf.Cos(t));
    }
}
```

- **考え方**: `Time.time`や`Time.deltaTime`を使用することで、特定のタイミングで動作を実行する移動を管理できます。例えば、フレームレートに関係なく一定の速度で移動させる場合に使います。

<br>

---

# 7. **ランダムな動き (Perlin Noise)**

カスタムスクリプトでランダムな動きを作成することも可能です。`Perlin Noise`を使用すると、滑らかで予測できない動きが可能になります。

#### サンプルコード：Perlin Noiseを使ったランダムな動き

```csharp
using UnityEngine;

public class PerlinNoiseMovement : MonoBehaviour {
    public float speed = 5f;
    public float scale = 0.1f;

    void Update() {
        // Perlinノイズに基づくランダムな動き
        float x = Mathf.PerlinNoise(Time.time * speed, 0.0f) * 2.0f - 1.0f;
        float z = Mathf.PerlinNoise(0.0f, Time.time

 * speed) * 2.0f - 1.0f;
        transform.position += new Vector3(x, 0, z) * scale;
    }
}
```

- **考え方**: `Perlin Noise`を使うことで、敵やキャラクターの自然なランダムな動きや、環境エフェクトに応用できます。

<br>

<br>

などなど...