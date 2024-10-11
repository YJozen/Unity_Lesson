
### 3. **CharacterControllerによる移動**
`CharacterController`は、キャラクターの移動を制御する専用のコンポーネントで、物理エンジンの影響を軽減しながら衝突や地形の反応を処理できます。

#### 基本サンプルコード：
```csharp
using UnityEngine;

public class CharacterControllerMove : MonoBehaviour
{
    public float speed = 5f;
    private CharacterController controller;

    void Start()
    {
        controller = GetComponent<CharacterController>();
    }

    void Update()
    {
        float moveInput = Input.GetAxis("Horizontal");
        Vector3 move = transform.right * moveInput * speed * Time.deltaTime;

        // Moveを使用してキャラクターを移動
        controller.Move(move);
    }
}
```

#### 特徴：
- **長所**: 衝突処理が簡単で、柔軟に地形に反応できる。
- **短所**: 重力や他の物理効果は手動で処理する必要がある。

---

衝突や地形対応がしやすく、移動に特化したコントローラー。