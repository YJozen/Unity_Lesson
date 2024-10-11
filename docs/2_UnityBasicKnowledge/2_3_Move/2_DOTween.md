
---

### 6. **DOTweenによる移動**
`DOTween`は、スムーズなアニメーションや移動を簡単に実装できる強力なツールです。プレイヤーが特定の座標まで滑らかに移動する場合に活用できます。

#### DOTween移動のサンプルコード：
```csharp
using UnityEngine;
using DG.Tweening;

public class DOTweenMove : MonoBehaviour
{
    public Transform targetPosition;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // DOTweenを使用して滑らかに移動
            transform.DOMove(targetPosition.position, 1f); // 1秒かけて移動
        }
    }
}
```

---

- **DOTween**: スムーズなアニメーション移動を実現。