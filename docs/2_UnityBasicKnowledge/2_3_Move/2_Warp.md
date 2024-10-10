

### 5. **Warp移動**
Warpは、キャラクターを瞬時に指定した位置に移動させる処理です。敵やプレイヤーが瞬時にワープする場合に使用します。

#### Warp移動のサンプルコード：
```csharp
using UnityEngine;

public class WarpMove : MonoBehaviour
{
    public Transform targetPosition;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // 瞬時にターゲット位置に移動
            transform.position = targetPosition.position;
        }
    }
}
```



### 2. **Rigidbodyの移動にWarp機能を追加**
Rigidbodyの移動を用いつつ、ワープ機能を持たせる例です。

```csharp
using UnityEngine;

public class RigidbodyWarpMove : MonoBehaviour
{
    public float speed = 5f;
    public Transform warpTarget;
    private Rigidbody rb;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        float moveInput = Input.GetAxis("Horizontal");
        rb.velocity = new Vector3(moveInput * speed, rb.velocity.y, 0);

        // Warp
        if (Input.GetKeyDown(KeyCode.Space))
        {
            rb.position = warpTarget.position; // 瞬時にワープ
        }
    }
}
```

- **Warp**: 瞬時に位置を変更する方法。


