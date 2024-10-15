### 1. **Transformによる移動**
Transformによる移動は、直接オブジェクトの位置を操作するため、非常にシンプルで、物理演算は考慮されません。  
簡単なスクリプトで位置を更新できます。

#### 基本サンプルコード：
```csharp
using UnityEngine;

public class TransformMove : MonoBehaviour
{
    public float speed = 5f;

    void Update()
    {
        // 水平移動
        float moveInput = Input.GetAxis("Horizontal");
        transform.position += new Vector3(moveInput, 0, 0) * speed * Time.deltaTime;
    }
}
```

#### 特徴：
- **長所**: シンプルでカスタマイズが簡単。
- **短所**: 物理エンジンを無視するため、衝突処理や滑らかな動きが難しい。

基本的な移動方法で、シンプルだが物理的な衝突は考慮されない。