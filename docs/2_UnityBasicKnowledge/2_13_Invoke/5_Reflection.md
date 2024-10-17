

### 6. リフレクションを用いてメソッドを実行

```csharp
using System;
using System.Reflection;
using UnityEngine;

public class ReflectionExample : MonoBehaviour
{
    void Start()
    {
        Type type = typeof(MyComponent);
        MyComponent instance = (MyComponent)Activator.CreateInstance(type);
        MethodInfo method = type.GetMethod("MyMethod");

        if (method != null)
        {
            method.Invoke(instance, null); // リフレクションでメソッドを呼び出し
        }
    }
}

public class MyComponent
{
    public void MyMethod()
    {
        Debug.Log("Reflection method called!");
    }
}
```


