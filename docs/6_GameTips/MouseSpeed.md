マウスの速さに基づいてポイントを加算するためには、前回のマウスの位置と現在のマウスの位置を比較して、移動の速さを計算する必要があります。以下にその具体的な方法を示します。

### スクリプトの例

以下のスクリプトは、マウスの移動速度に基づいてポイントを加算する基本的な方法を示しています。

```csharp
using UnityEngine;

public class MouseSpeedPoints : MonoBehaviour
{
    public float pointsMultiplier = 1f; // マウスの速度に基づくポイントの乗数
    private Vector3 lastMousePosition;
    private float totalPoints = 0f;

    void Start()
    {
        // 初期マウス位置の設定
        lastMousePosition = Input.mousePosition;
    }

    void Update()
    {
        // 現在のマウス位置
        Vector3 currentMousePosition = Input.mousePosition;

        // マウスの移動量を計算
        float distanceMoved = Vector3.Distance(lastMousePosition, currentMousePosition);

        // マウスの移動速度に基づいてポイントを加算
        float pointsEarned = distanceMoved * pointsMultiplier;
        totalPoints += pointsEarned;

        // デバッグ用の表示
        Debug.Log($"Points Earned: {pointsEarned}, Total Points: {totalPoints}");

        // 現在のマウス位置を次回のフレームのために記録
        lastMousePosition = currentMousePosition;
    }
}
```

### 解説

1. **`lastMousePosition`**: 前回のフレームでのマウスの位置を保存します。これにより、現在のマウスの位置との距離を計算できます。

2. **`Update()` メソッド**: 毎フレーム呼び出され、現在のマウスの位置と前回の位置の距離を計算します。

3. **`Vector3.Distance()`**: 現在のマウス位置と前回の位置の間の距離を計算します。これがマウスの移動量です。

4. **ポイントの加算**: `distanceMoved` に `pointsMultiplier` を掛けて、得られるポイントを計算し、`totalPoints` に加算します。

5. **`lastMousePosition` の更新**: 現在のマウス位置を次回のフレームでの参照用に保存します。

### 注意点

- **ポイントの調整**: `pointsMultiplier` を調整して、ポイントの加算の度合いをコントロールできます。

- **フレームレート依存**: `Update()` はフレームごとに呼び出されるため、フレームレートが異なるとポイントの増加に差が出る可能性があります。これを補正するためには、`Time.deltaTime` を使ってフレームレートの影響を減らすこともできます。

- **速度のスムージング**: `distanceMoved` の計算に `Time.deltaTime` を掛けることで、マウスの速度をスムージングしてより安定した結果を得ることもできます。

```csharp
float distanceMoved = Vector3.Distance(lastMousePosition, currentMousePosition) / Time.deltaTime;
```

この方法を使うことで、マウスの移動速度に応じて動的にポイントを加算することができます。

<br>

-----

<br>

マウスの速さ（移動速度）を取得することは可能です。具体的には、フレームごとのマウスの位置の変化量を計算し、それを時間で割ることで速度を求めます。

### コード例:
以下のコードは、マウスの速さを取得し、`Debug.Log`で表示する例です。

```csharp
using UnityEngine;

public class MouseSpeedTracker : MonoBehaviour
{
    private Vector3 _lastMousePosition;
    private float _mouseSpeed;

    void Start()
    {
        // 最初のフレームのマウス位置を記録
        _lastMousePosition = Input.mousePosition;
    }

    void Update()
    {
        // 現在のマウス位置を取得
        Vector3 currentMousePosition = Input.mousePosition;

        // マウスの速さを計算 (単位: ピクセル/秒)
        _mouseSpeed = (currentMousePosition - _lastMousePosition).magnitude / Time.deltaTime;

        // マウス位置の更新
        _lastMousePosition = currentMousePosition;

        // マウスの速さを出力
        Debug.Log("Mouse Speed: " + _mouseSpeed + " pixels/second");
    }
}
```

### 解説:
- `Input.mousePosition`でマウスの現在のスクリーン座標を取得します。
- 前回のフレームのマウス位置との距離を計算し、それを`Time.deltaTime`で割ることで、マウスの速さ（ピクセル/秒）を求めます。
- `.magnitude`は、ベクトルの長さ（つまり、移動距離）を取得します。

この方法で、マウスの動きの速さをリアルタイムで取得し、様々な応用に利用することができます。