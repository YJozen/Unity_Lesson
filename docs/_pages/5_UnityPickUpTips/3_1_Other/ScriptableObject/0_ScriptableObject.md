ScriptableObjectは、ゲームデータを簡単に管理でき、エディタ上で操作するのに非常に便利です。

## 使用するファイル

* GameData.cs（ScriptableObject）
* GameDataAsset.cs（データの作成および操作）
* GameController.cs（データの使用例）




## スクリプトの例
### GameData.cs
まず、保存するゲームデータの構造をScriptableObjectで定義します。

+ playerLevel: プレイヤーのレベル。
+ health: プレイヤーの体力。
+ inventoryItems: プレイヤーが持っているアイテムのリスト。


```cs

using UnityEngine;

[CreateAssetMenu(fileName = "GameData", menuName = "Game Data", order = 1)]
public class GameData : ScriptableObject
{
    public int playerLevel;
    public float health;
    public string[] inventoryItems;
}

```


### GameDataAsset.cs
ScriptableObjectのインスタンスを作成し、エディタ上でデータを操作するためのスクリプトを作成します。


CreateAsset: エディタメニューから新しいGameDataオブジェクトを作成できるようにします。



```cs
using UnityEditor;
using UnityEngine;

public class GameDataAsset
{
    [MenuItem("Assets/Create/Game Data")]
    public static void CreateAsset()
    {
        GameData asset = ScriptableObject.CreateInstance<GameData>();

        AssetDatabase.CreateAsset(asset, "Assets/GameData.asset");
        AssetDatabase.SaveAssets();

        EditorUtility.FocusProjectWindow();
        Selection.activeObject = asset;
    }
}


```





### GameController.cs
ゲームデータを読み込み、操作し、保存するためのクラスです。

gameData: InspectorでGameDataのインスタンスをアタッチして使用します


```cs

using UnityEngine;

public class GameController : MonoBehaviour
{
    public GameData gameData;

    private void Start()
    {
        // 現在のゲームデータを表示
        Debug.Log("Player Level: " + gameData.playerLevel);
        Debug.Log("Health: " + gameData.health);
        Debug.Log("Inventory Items: " + string.Join(", ", gameData.inventoryItems));

        // ゲームデータの変更
        gameData.playerLevel++;
        gameData.health -= 10.0f;
        Array.Resize(ref gameData.inventoryItems, gameData.inventoryItems.Length + 1);
        gameData.inventoryItems[gameData.inventoryItems.Length - 1] = "Sword";

        // 変更後のゲームデータを表示
        Debug.Log("Updated Player Level: " + gameData.playerLevel);
        Debug.Log("Updated Health: " + gameData.health);
        Debug.Log("Updated Inventory Items: " + string.Join(", ", gameData.inventoryItems));
    }
}

```