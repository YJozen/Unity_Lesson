カメラが対象物（例えばプレイヤーやオブジェクト）の周りを回転する方法は、**オービットカメラ**（またはターゲットオービット）と呼ばれます。カメラ自体が移動せずに、特定のオブジェクトを中心に円軌道で回転する動きを実装する方法について説明します。

## オービットカメラの実装方法

### ステップ 1: ターゲットを設定
まず、カメラが回転するターゲットを指定します。このターゲットはカメラの中心となるオブジェクト（例えばプレイヤー）です。

### ステップ 2: カメラの位置と回転を計算
カメラの位置をターゲットの周りに設定し、ユーザーのマウス入力やキー入力に基づいて回転させます。ここでは `Transform.RotateAround()` メソッドを使用して、カメラをターゲットの周りで回転させます。

### ステップ 3: 実装例

次に、カメラが対象物を中心に回転するスクリプトを示します。

```csharp
using UnityEngine;

public class OrbitCamera : MonoBehaviour
{
    public Transform target;  // カメラが周回する対象
    public float distance = 5.0f;  // ターゲットとの距離
    public float xSpeed = 360.0f;  // 水平方向の回転速度
    public float ySpeed = 360.0f;  // 垂直方向の回転速度
    public float yMinLimit = -20f; // 垂直方向の最小角度
    public float yMaxLimit = 80f;  // 垂直方向の最大角度

    private float x = 0.0f;
    private float y = 0.0f;

    void Start()
    {
        // カメラの初期角度を設定
        Vector3 angles = transform.eulerAngles;
        x = angles.y;
        y = angles.x;
    }

    void LateUpdate()
    {
        // マウスの入力を取得
        if (target && Input.GetMouseButton(0))  // 右クリックで回転操作
        {
            x += Input.GetAxis("Mouse X") * xSpeed * Time.deltaTime;
            y -= Input.GetAxis("Mouse Y") * ySpeed * Time.deltaTime;

            // 垂直方向の角度を制限
            y = Mathf.Clamp(y, yMinLimit, yMaxLimit);

            // カメラの位置と回転を設定
            Quaternion rotation = Quaternion.Euler(y, x, 0);
            Vector3 position = rotation * new Vector3(0.0f, 0.0f, -distance) + target.position;

            transform.rotation = rotation;
            transform.position = position;
        }
    }
}
```

### スクリプトの説明:
1. **ターゲット (target)**: カメラが回転する中心となるオブジェクト（例えば、プレイヤー）。
2. **距離 (distance)**: カメラがターゲットからどれくらい離れているかを設定します。
3. **回転速度 (xSpeed, ySpeed)**: マウスの動きに応じてカメラを回転させる速度を指定します。
4. **垂直方向の角度制限 (yMinLimit, yMaxLimit)**: 垂直方向（上下）の回転角度の範囲を制限するための設定です。カメラがターゲットの真下や真上に行き過ぎるのを防ぎます。
5. **LateUpdate()**: 毎フレーム、カメラの位置と回転を計算して更新します。マウスの右ボタンを押している間にカメラを回転させます。
6. **`Quaternion.Euler(y, x, 0)`**: カメラの回転を計算するための四元数を生成します。
7. **`RotateAround()`** メソッドは使用していませんが、カメラの位置を手動で計算しています。`target.position`を基準にした円軌道を計算して、カメラをその位置に移動させています。

### ステップ 4: Unityでの設定

1. 上記のスクリプトを `OrbitCamera.cs` という名前で保存します。
2. カメラにこのスクリプトをアタッチします。
3. Unityエディタ内で、スクリプトの `target` フィールドにカメラが回転するオブジェクト（プレイヤーなど）を設定します。

これにより、マウスの右クリックを押しながら動かすと、カメラがターゲットの周りを回転するようになります。

### その他の補足:
- スクロールホイールで `distance` を変更することで、ズームイン・ズームアウトを追加することもできます。
- `RotateAround()` を使用する方法もありますが、`Quaternion` と位置ベクトルを使った方法はより柔軟です。