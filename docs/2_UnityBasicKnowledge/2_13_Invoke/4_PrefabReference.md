プレハブ（Prefab）を生成する際、生成されたオブジェクトにヒエラルキー上のオブジェクト（`HierarchyObject`）の情報をセットし、それを動的に操作できる仕組みについて  
(prefabに直接セット出来ないので、それの解決案)


PrefabObjectを生成し、HierarchyObjectの情報を取得する例

---
### `HierarchyObject.cs`  
  ```csharp
  public class HierarchyObject : MonoBehaviour
  {
      public int hp = 100;
  }
  ```
　
　<br>

### `PrefabObject.cs`

生成するプレハブに、このスクリプトをアタッチします。

このプレハブは、生成された後に`HierarchyObject`の参照をセットし、その情報を利用します。  

この時点でインスペクターにセットしようとしてもセット出来ません。


- **`SetHierarchyObject`メソッド**：  
このメソッドを使って、生成時に`HierarchyObject`の参照を外部からセットします。

- **`Update()`メソッド**：   
毎フレーム、`HierarchyObject`の`hp`をデバッグログに出力することで、プレハブとヒエラルキーオブジェクトが正しく関連付けられているか確認します。

  ```csharp
  public class PrefabObject : MonoBehaviour
  {
      [SerializeField] HierarchyObject hierarchyObject;

      void Update()
      {        
          Debug.Log(hierarchyObject.hp);
      }

      public void SetHierarchyObject(HierarchyObject hObject)
      {
          this.hierarchyObject = hObject;    
      }
  }
  ```

　<br>

---

### `InstantinatePrefab.cs`
**プレハブを定期的に生成**し、その際に生成されたプレハブに対して、ヒエラルキー上にある`HierarchyObject`の参照を設定する役割を持っています。

  1. 位置をランダムな位置にプレハブを生成。
  2. 生成されたプレハブにアタッチされている`PrefabObject`を取得し、その`SetHierarchyObject()`メソッドを使って、`hierarchyObject`の参照を渡します。
  3. 一定時間後に生成されたオブジェクトを破棄します。



```csharp
public class InstantinatePrefab : MonoBehaviour
{
    [SerializeField] GameObject prefabObject;
    [SerializeField] HierarchyObject hierarchyObject;
    float interval = 3f ;

    void Start()
    {
        //実行したいメソッド名（stringで指定します）,初回実行までの遅延時間（秒単位）,その後の繰り返し実行の間隔（秒単位）
        InvokeRepeating(nameof(GeneratePrefab), 0, interval);
    }

    void GeneratePrefab()
    {
        Vector3 generatePos = new Vector3(0f, Random.Range(-1, 1), 0f);
        GameObject gObject = Instantiate(prefabObject, generatePos, Quaternion.identity);

        // 生成と同時に必要な参照をセット
        PrefabObject pObject = gObject.GetComponent<PrefabObject>();
        if (pObject != null)
        {
            pObject.SetHierarchyObject(hierarchyObject);
        }

        Destroy(gObject, interval); // 自動で指定秒数後に削除
    }
}

```



