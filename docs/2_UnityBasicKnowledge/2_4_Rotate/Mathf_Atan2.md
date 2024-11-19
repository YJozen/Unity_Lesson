
配布プロジェクト
「2_UnityBasicKnowledge > 04_Rotation > Atan2」

サンプルコード

```cs
using UnityEngine;
using TMPro;

public class Vector2Angle : MonoBehaviour
{
    [Header("Object Settings")]
    public Transform obj; // 回転させる対象のオブジェクト
    public TextMeshProUGUI tmp_text; // 角度を表示するテキスト

    [Header("Movement Settings")]
    public float rotationSpeed = 0.3f; // 回転のスピード
    public float radius = 4f; // 回転半径

    private float currentAngle = 0f; // 現在の角度

    void Update()
    {
        // 角度を進める
        currentAngle += rotationSpeed * Time.deltaTime;

        // オブジェクトの位置を角度に基づいて更新
        obj.position = CalculatePositionFromAngle(currentAngle, radius);

        // オブジェクトの位置から角度を計算
        float angle = CalculateAngleFromPosition(obj.position);

        // 角度を小数点第一位まで四捨五入
        float roundedAngle = Mathf.Round(angle * 10f) / 10f;

        // テキストに角度を表示
        tmp_text.text = $"{roundedAngle}";
    }

    /// <summary>
    /// 指定された角度（度）から、回転半径に基づいた位置を計算します。
    /// </summary>
    /// <param name="angle">角度（度）</param>
    /// <param name="radius">回転半径</param>
    /// <returns>計算された位置</returns>
    Vector3 CalculatePositionFromAngle(float angle, float radius)
    {
        float angleInRadians = angle * Mathf.Deg2Rad; // 度からラジアンに変換
        float x = Mathf.Cos(angleInRadians); // x座標
        float z = Mathf.Sin(angleInRadians); // z座標

        // y座標は固定で0、xとzの位置に基づいてオブジェクトを配置
        return new Vector3(x, 0f, z) * radius;
    }

    /// <summary>
    /// 与えられた位置から、その位置の角度を計算します。
    /// </summary>
    /// <param name="position">オブジェクトの位置</param>
    /// <returns>計算された角度（度）</returns>
    float CalculateAngleFromPosition(Vector3 position)
    {
        // atanを使って、x軸に対する角度（度）を計算
        return Mathf.Atan(position.z/position.x) * Mathf.Rad2Deg;
        // atan2を使って、x軸に対する角度（度）を計算
        // return Mathf.Atan2(position.z, position.x) * Mathf.Rad2Deg;
    }
}


```


このスクリプトは、指定されたオブジェクトを円軌道に沿って回転させ、その角度をUIテキストで表示するものです。主に`Transform`の位置を更新して、回転に関する角度を計算し、それを画面上に表示します。コードの動作と各部分の詳細を説明します。

### クラス全体の構成
- **`obj`**: 回転させる対象のオブジェクトを指定します。
- **`tmp_text`**: 角度を表示するUIの`TextMeshProUGUI`コンポーネントを指定します。
- **`rotationSpeed`**: オブジェクトの回転スピードを設定するパラメータです。回転の速さはこの値に基づいて決まります。
- **`radius`**: オブジェクトが円軌道で移動する際の半径です。
- **`currentAngle`**: 現在の回転角度を保持する変数です。

### `Update()` メソッド
このメソッドは毎フレーム呼ばれ、オブジェクトを回転させ、角度を計算し、その結果をUIに反映させます。

1. **角度の更新**:
   ```csharp
   currentAngle += rotationSpeed * Time.deltaTime;
   ```
   - `rotationSpeed`は回転速度（1秒間に回転する角度）で、`Time.deltaTime`（前フレームとの時間差）を掛けることで、フレームレートに依存せず一定の速度で回転します。

2. **オブジェクトの位置の更新**:
   ```csharp
   obj.position = CalculatePositionFromAngle(currentAngle, radius);
   ```
   - 現在の角度`currentAngle`と回転半径`radius`を基に、オブジェクトの新しい位置を計算します。
   
3. **オブジェクトの位置から角度を計算**:
   ```csharp
   float angle = CalculateAngleFromPosition(obj.position);
   ```
   - `obj.position`（オブジェクトの現在位置）から、その位置が表す角度を計算します。この角度をUIに表示するために使用します。

4. **角度の表示**:
   ```csharp
   float roundedAngle = Mathf.Round(angle * 10f) / 10f;
   tmp_text.text = $"{roundedAngle}";
   ```
   - `angle`を小数点第一位まで四捨五入して、`tmp_text`に表示します。

### `CalculatePositionFromAngle(float angle, float radius)` メソッド
このメソッドは、指定された角度と回転半径に基づいて、オブジェクトが円軌道上のどこに位置するかを計算します。

```csharp
float angleInRadians = angle * Mathf.Deg2Rad;
float x = Mathf.Cos(angleInRadians); // x座標
float z = Mathf.Sin(angleInRadians); // z座標
return new Vector3(x, 0f, z) * radius;
```
- **`angleInRadians`**: 角度は度単位で指定されていますが、三角関数ではラジアン単位を使用します。`Mathf.Deg2Rad`は度からラジアンに変換するための定数です。
- **`x` と `z` の計算**:
   - `Mathf.Cos(angleInRadians)` は、円の半径と角度に基づいてx座標を計算します。
   - `Mathf.Sin(angleInRadians)` は、円の半径と角度に基づいてz座標を計算します。
- `y`座標は固定で0とし、2D平面（x, z平面）上での位置を返します。
- 最後に、計算した位置を`radius`（半径）でスケーリングして、指定された回転半径に合わせます。

### `CalculateAngleFromPosition(Vector3 position)` メソッド
このメソッドは、指定された位置から角度を計算します。

```csharp
return Mathf.Atan(position.z / position.x) * Mathf.Rad2Deg;
```
- `Mathf.Atan(position.z / position.x)`は、x軸とz軸の比率から角度を求める方法です。これにより、座標系に基づいてオブジェクトがx軸に対してどれくらい回転しているかを求めます。
- `Mathf.Rad2Deg`はラジアンから度に変換するための定数です。

### コメントアウトされた `Mathf.Atan2` の使用
- もう一つの方法として`Mathf.Atan2`を使う方法もあります。この方法は、`x`と`z`の値がどちらも負の値を取る場合にも正しい角度を計算できるため、より安定した結果を得ることができます。

```csharp
return Mathf.Atan2(position.z, position.x) * Mathf.Rad2Deg;
```
- `Mathf.Atan2`は、`x`と`z`の両方の座標を引数に取り、正確な角度を計算します。この方法が一般的に推奨されます。

### まとめ
このスクリプトは、指定されたオブジェクトを円軌道上で回転させ、その角度を計算してUIに表示するという動作を行います。`rotationSpeed`と`radius`を調整することで、回転の速さや円軌道の大きさを変更できます。また、`Mathf.Atan2`や`Mathf.Cos`、`Mathf.Sin`などを用いて、円形の動きと角度の計算を行っています。


<br>

<br>

---

<br>

<br>

+ [Mathf.Atan2などのMathf](../../5_UnityPickUpTips/3_1_3_Other/Mathf.md)
+ [Mathf.Atan2などの様々な角度の求め方の例](../../5_UnityPickUpTips/3_1_3_Other/様々な角度の求め方.md)

<br>


<br>

<br>

<br>