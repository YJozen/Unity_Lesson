
# 2. EventHandlerを用いてイベント実行

```csharp
using System;
using UnityEngine;

public class EventExample : MonoBehaviour
{
    public event EventHandler MyEvent;

    void Start()
    {
        MyEvent += OnMyEvent;
        MyEvent?.Invoke(this, EventArgs.Empty); // イベントを発火
    }

    private void OnMyEvent(object sender, EventArgs e)
    {
        Debug.Log("Event triggered!");
    }
}
```
