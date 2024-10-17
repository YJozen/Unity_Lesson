
### 4. Prefabを生成してからPrefabにあるコンポーネントにあるメソッドを実行

```csharp
using UnityEngine;

public class PrefabMethodCaller : MonoBehaviour
{
    public GameObject prefab;

    void Start()
    {
        GameObject instance = Instantiate(prefab);
        MyComponent myComponent = instance.GetComponent<MyComponent>();
        if (myComponent != null)
        {
            myComponent.MyMethod(); // メソッドを呼び出し
        }
    }
}
```
