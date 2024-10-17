# 5. シングルトンから実行

<br>

<br>

```csharp
using UnityEngine;

public class SingletonExample : MonoBehaviour
{
    public static SingletonExample Instance { get; private set; }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
        }
        else
        {
            Instance = this;
        }
    }

    public void MySingletonMethod()
    {
        Debug.Log("Singleton method called!");
    }
}
```


```csharp
using UnityEngine;

public class Caller : MonoBehaviour
{
    void Start()
    {
        SingletonExample.Instance.MySingletonMethod(); // シングルトンメソッドを呼び出し
    }
}
```