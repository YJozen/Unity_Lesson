# 1. インスペクターからObjectをセットし、そこからメソッド実行

```csharp
using UnityEngine;

public class InspectorMethodCaller : MonoBehaviour
{
    public MyComponent myComponent; // インスペクターで設定

    void Start()
    {
        if (myComponent != null)
        {
            myComponent.MyMethod(); // メソッドを呼び出し
        }
    }
}

public class MyComponent : MonoBehaviour
{
    public void MyMethod()
    {
        Debug.Log("MyMethod called!");
    }
}
```
