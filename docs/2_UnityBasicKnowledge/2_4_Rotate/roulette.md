ルーレットのような回転するオブジェクトを「回転させて徐々に減速し、最終的に停止させる」場合、次の要素が必要です：

1. **回転の開始**: 一定の速度で回転させる。
2. **減速**: 回転速度を徐々に減少させ、自然に止まるようにする。
3. **停止**: 特定の範囲で止まるように制御する（ルーレットの目が停止する場所を決定する）。

<br>

## アプローチ

回転を制御するために、減速を**線形減速**や**Ease out（徐々に遅くなる）**といった方法で実現します。このような回転は、`Rigidbody` を使用して物理的に回転させても良いですが、ルーレットのような滑らかな回転には、`transform.Rotate`と補間関数（Lerp）を使った回転制御が一般的です。

<br>

## サンプルコード

次に、簡単なルーレットのサンプルコードを示します。このコードでは、ルーレットが高速で回転し始め、徐々に減速して特定のポイントで停止します。

```csharp
using UnityEngine;

public class RouletteSpinner : MonoBehaviour
{
    public float initialSpeed = 500f;   // 初期の回転速度
    public float deceleration = 50f;    // 減速率
    public float stopThreshold = 0.1f;  // 回転を停止させる閾値（これ以下の速度になったら止まる）
    
    private float currentSpeed;
    private bool isSpinning = false;

    void Start() {
        // ルーレットの回転速度を初期化
        currentSpeed = initialSpeed;
    }

    void Update() {
        if (isSpinning) {
            // 回転する
            transform.Rotate(Vector3.forward, -currentSpeed * Time.deltaTime);

            // 徐々に減速させる
            currentSpeed -= deceleration * Time.deltaTime;

            // 回転が停止閾値を下回ったら停止させる
            if (currentSpeed <= stopThreshold) {
                currentSpeed = 0f;
                isSpinning = false;
                Debug.Log("Roulette stopped.");
                // ここで停止後の処理を行う（例えば、どの目に止まったか判定する）
            }
        }

        // スペースキーで回転を開始
        if (Input.GetKeyDown(KeyCode.Space) && !isSpinning) {
            StartSpin();
        }
    }

    // 回転を開始するメソッド
    void StartSpin() {
        isSpinning = true;
        currentSpeed = initialSpeed;  // 初期速度で再び回転を開始
        Debug.Log("Roulette started spinning.");
    }
}
```

### 説明

1. **初期速度 (`initialSpeed`)**: ルーレットが最初に回転を開始する速度です。例えば、500度/秒で回転を開始します。
2. **減速率 (`deceleration`)**: 回転速度を毎フレームごとに減速するための値です。`deceleration`が大きいほど、回転は早く止まります。
3. **停止閾値 (`stopThreshold`)**: 回転がこの閾値以下になると、完全に停止します。回転速度が小さくなりすぎたら、見た目上も回転していないようにするための基準です。
4. **`StartSpin()`**: 回転を開始するメソッドです。スペースキーを押すと回転が始まります。新たに回転させたい場合に、このメソッドを呼び出します。
5. **`transform.Rotate(Vector3.up, speed * Time.deltaTime)`**: 毎フレームごとに回転を行います。回転速度に `Time.deltaTime` を掛けることで、フレームレートに依存しない回転が実現します。

<br>

---

<br>

### 改善ポイント

#### 1. 回転が停止するポイントの調整
このサンプルコードでは、回転が自然に停止しますが、ルーレットの場合、特定の目（スロット）に停止する必要があります。これを実現するには、最後に停止したい角度に近づける補正処理が必要です。

以下のコードは、ルーレットの停止位置を調整するための修正例です。

```csharp
void Update() {
    if (isSpinning) {
        // 通常の回転
        transform.Rotate(Vector3.up, currentSpeed * Time.deltaTime);

        // 減速処理
        currentSpeed -= deceleration * Time.deltaTime;

        // 徐々に回転を停止させる
        if (currentSpeed <= stopThreshold) {
            currentSpeed = 0f;
            isSpinning = false;
            Debug.Log("Roulette stopped.");

            // 最終的な角度に補正（例: ルーレットが360度を超えない範囲に調整）
            float finalAngle = Mathf.Round(transform.eulerAngles.y / 30f) * 30f; // 30度ごとに停止させる
            transform.eulerAngles = new Vector3(0, finalAngle, 0);
            Debug.Log("Stopped at angle: " + finalAngle);
        }
    }

    // スペースキーで回転を開始
    if (Input.GetKeyDown(KeyCode.Space) && !isSpinning) {
        StartSpin();
    }
}
```

<br>

#### 2. `Rigidbody`を使用した物理ベースの回転

物理的なルーレットをシミュレートしたい場合、`Rigidbody` を使用し、`AddTorque` を使って回転力を加え、摩擦 (`angularDrag`) を設定する方法もあります。この方法では、回転力が自然に減少して、よりリアルな物理的な動作を実現できます。

```csharp
using UnityEngine;

public class RouletteWithRigidbody : MonoBehaviour
{
    public float initialTorque = 500f;
    public float angularDrag = 2f;  // 摩擦
    private Rigidbody rb;

    void Start() {
        rb = GetComponent<Rigidbody>();
        rb.maxAngularVelocity = initialTorque;  // 回転の最大速度を設定
        rb.angularDrag = angularDrag;  // 摩擦を設定
    }

    void Update() {
        // スペースキーで回転を開始
        if (Input.GetKeyDown(KeyCode.Space)) {
            StartSpin();
        }
    }

    void StartSpin() {
        rb.angularVelocity = Vector3.zero;  // 以前の回転をリセット
        rb.AddTorque(Vector3.up * initialTorque, ForceMode.Impulse);  // 初期の回転力を与える
    }
}
```

#### 説明
- **`AddTorque(Vector3.up * initialTorque, ForceMode.Impulse)`**: これでルーレットが一瞬の力で高速回転を開始します。`ForceMode.Impulse`は、瞬間的な力を与えるためのモードです。
- **`rb.angularDrag`**: これで回転速度を自然に減速させ、ルーレットが摩擦により徐々に止まります。

---

### まとめ

ルーレットの回転には、いくつかの方法がありますが、次のように状況に応じて使い分けるのが良いでしょう：
- **`transform.Rotate`を使用する方法**: シンプルでコントロールしやすく、簡単に徐々に回転を減速させたい場合に適しています。
- **物理ベースの`AddTorque`を使う方法**: 物理演算に基づいたリアルな回転シミュレーションが可能です。摩擦や慣性も考慮した回転を実現できます。

各方法を組み合わせて、目的に応じた回転処理を行うのが効果的です。


[ルーレットの停止判定例](roulette_judge.md)