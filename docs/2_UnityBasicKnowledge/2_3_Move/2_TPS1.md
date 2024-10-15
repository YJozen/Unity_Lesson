
### 4. **TPS（Third-Person Shooter）視点での移動**
TPSスタイルの移動では、カメラの向きを基準にプレイヤーが動くように設計します。これは、キャラクターが常にカメラが向いている方向に進むように制御されます。

<br>

#### TPSスタイル移動のサンプルコード：
```csharp
using UnityEngine;

public class TPSMove : MonoBehaviour
{
    public float speed = 5f;
    public Transform cameraTransform;
    private CharacterController controller;

    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        float moveInput = Input.GetAxis("Horizontal");
        float forwardInput = Input.GetAxis("Vertical");

        Vector3 moveDirection = (cameraTransform.right * moveInput + cameraTransform.forward * forwardInput).normalized;
        moveDirection.y = 0; // Y軸の移動を防ぐ

        controller.Move(moveDirection * speed * Time.deltaTime);
    }
}
```

---

<br>

## 組み合わせの例

### 1. **Transformの移動にTPS視点を追加**
Transform移動をTPSカメラ視点で動かす方法を紹介します。

```csharp
using UnityEngine;

public class TransformTPSMove : MonoBehaviour
{
    public float speed = 5f;
    public Transform cameraTransform;

    void Update()
    {
        float moveInput = Input.GetAxis("Horizontal");
        float forwardInput = Input.GetAxis("Vertical");

        Vector3 moveDirection = (cameraTransform.right * moveInput + cameraTransform.forward * forwardInput).normalized;
        moveDirection.y = 0;

        transform.position += moveDirection * speed * Time.deltaTime;
    }
}
```


カメラの向きに基づく移動を実現。
