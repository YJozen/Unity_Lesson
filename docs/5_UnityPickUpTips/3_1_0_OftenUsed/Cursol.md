カーソルが邪魔になったり、画面外にカーソルが出てしまうなどの解決方法をいくつか紹介

<br>

# 1. カーソルを画面中央に固定する
画面上でマウスカーソルを動かしてカメラ操作をする際に、カーソルが邪魔になる場合や、画面外に行かないようにするには、カーソルを非表示にして中央に固定し、相対的なマウス移動量を使ってカメラを操作する方法があります。

#### サンプルコード



```csharp
using UnityEngine;

public class CameraController : MonoBehaviour
{
    public float sensitivity = 300f;
    private float rotationX = 0f;
    private float rotationY = 0f;

    void Start()
    {
        // カーソルを非表示にしてロックする
        Cursor.lockState = CursorLockMode.Locked;
        Cursor.visible = false;
    }

    void Update()
    {
        // マウスの移動量を取得
        float mouseX = Input.GetAxis("Mouse X") * sensitivity * Time.deltaTime;
        float mouseY = Input.GetAxis("Mouse Y") * sensitivity * Time.deltaTime;

        // カメラの回転を計算
        rotationY += mouseX;
        rotationX -= mouseY;
        rotationX = Mathf.Clamp(rotationX, -90f, 90f); // カメラの上下制限

        // カメラの回転を適用
        transform.localRotation = Quaternion.Euler(rotationX, rotationY, 0f);

        // ESCキーを押したらカーソルロックを解除
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }
    }
}
```

#### 説明
- **Cursor.lockState**: `CursorLockMode.Locked`に設定すると、カーソルが画面の中央に固定され、マウスの移動量が相対的に扱われます。
- **Cursor.visible**: `false`に設定することで、カーソルが見えなくなります。
- **Input.GetAxis("Mouse X") / Input.GetAxis("Mouse Y")**: マウスの相対的な移動量を取得します。

このコードでは、`ESC`キーを押すことでカーソルロックを解除し、カーソルを再び表示することができます。

<br>

# 2. カーソルを画面内に制限する
カーソルを表示したまま、画面外に出ないように制限することも可能です。

#### サンプルコード

```csharp
using UnityEngine;

public class CursorBoundaries : MonoBehaviour
{
    void Start()
    {
        // カーソルを画面内に制限
        Cursor.lockState = CursorLockMode.Confined;
    }

    void Update()
    {
        // ESCキーで制限解除
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Cursor.lockState = CursorLockMode.None;
        }
    }
}
```

#### 説明
- **CursorLockMode.Confined**: カーソルが画面内に制限され、画面外に出なくなります。ただし、カーソル自体は表示されたままになります。


<br>


### 3. カメラ操作とカーソル制御の切り替え
あるタイミングでカーソルをロックしてカメラ操作に集中し、別のタイミングでカーソル操作に切り替えるといった方法もあります。

#### サンプルコード

```csharp
using UnityEngine;

public class ToggleCursorLock : MonoBehaviour
{
    private bool isLocked = true;

    void Start()
    {
        ToggleCursorLockState();
    }

    void Update()
    {
        // スペースキーでカーソルロックを切り替え
        if (Input.GetKeyDown(KeyCode.Space))
        {
            isLocked = !isLocked;
            ToggleCursorLockState();
        }
    }

    void ToggleCursorLockState()
    {
        if (isLocked)
        {
            Cursor.lockState = CursorLockMode.Locked;
            Cursor.visible = false;
        }
        else
        {
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }
    }
}
```

#### 説明
- スペースキーを押すと、カーソルのロック状態を切り替えます。ロックしている時はカメラ操作に集中し、解除した時は通常のカーソル操作が可能です。


<br>


---

### まとめ
- **CursorLockMode.Locked**: カーソルを非表示にして、中央に固定。カメラの自由な回転などに使う。
- **CursorLockMode.Confined**: カーソルが画面内に制限され、画面外に行かなくなる。
- **Cursor.visible**: `false`でカーソルを非表示、`true`で表示する。

```cs
using UnityEngine;

namespace Often
{
    public class CursorCtrl : MonoBehaviour
    {
        void Start() {
            Cursor.visible = false;
            Cursor.lockState = CursorLockMode.Locked;
        }

        void Update() {
            if (Input.GetKeyDown(KeyCode.Escape)) {
                Cursor.visible = true;
                Cursor.lockState = CursorLockMode.None;
            }
            if (Input.GetMouseButtonDown(0)) {
                Cursor.visible = false;
                Cursor.lockState = CursorLockMode.Locked;
            }
        }
    }
}
```


[対象物のまわりを回るカメラ](CameraOrbit.md)