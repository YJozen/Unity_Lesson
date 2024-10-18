# 3. UnityEventを用いてイベント実行

```csharp
using UnityEngine;
using UnityEngine.Events;

public class UnityEventExample : MonoBehaviour
{
    public UnityEvent myUnityEvent;

    void Start()
    {
        myUnityEvent.Invoke(); // UnityEventを発火
    }

    private void OnEnable()
    {
        myUnityEvent.AddListener(OnMyUnityEvent);
    }

    private void OnMyUnityEvent()
    {
        Debug.Log("UnityEvent triggered!");
    }
}
```
