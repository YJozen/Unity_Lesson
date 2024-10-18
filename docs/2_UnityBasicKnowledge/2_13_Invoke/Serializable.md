Unityにおいて、クラスに属性を付けることは、特定の用途でクラスの挙動やインスペクターでの表示を制御するために使われます。  
これにより、Unityエディター上での動作をカスタマイズしたり、クラスのインスペクターでの表示方法を制御することができます。  
いくつかの代表的なクラスに対する属性とその用途を紹介します。

<br>

# 1. **[System.Serializable]**
`[System.Serializable]`属性は、クラスをインスペクターで表示するために使用されます。この属性を付けることで、そのクラスがUnityのシリアル化システムに対応し、インスペクターで表示・編集できるようになります。

#### 使用例：

```csharp
[System.Serializable]
public class CustomData
{
    public string message;
    public int value;
}

public class SerializableExample : MonoBehaviour
{
    public CustomData data;
}
```

- `CustomData`クラスに`[System.Serializable]`を付けることで、`SerializableExample`クラスの`data`フィールドがインスペクターで表示されるようになります。

<br>

# 2. **[RequireComponent]**
`[RequireComponent]`属性は、指定したコンポーネントが**必須**であることを示します。この属性をクラスに付けると、スクリプトがアタッチされたときに、指定したコンポーネントも自動的にアタッチされます。

#### 使用例：

```csharp
[RequireComponent(typeof(Rigidbody))]
public class RequireComponentExample : MonoBehaviour
{
    void Start()
    {
        Rigidbody rb = GetComponent<Rigidbody>();
        if (rb != null)
        {
            Debug.Log("Rigidbody is attached");
        }
    }
}
```

- `RequireComponent`属性を使うと、このスクリプトをオブジェクトにアタッチするときに、自動的に`Rigidbody`コンポーネントが追加されます。

<br>

# 3. **[AddComponentMenu]**
`[AddComponentMenu]`属性を使うと、スクリプトを**コンポーネントメニューに登録**し、メニュー内で簡単に見つけられるようにできます。カスタムクラスを特定の場所に配置するのに便利です。

#### 使用例：

```csharp
[AddComponentMenu("Custom/CustomComponent")]
public class CustomComponent : MonoBehaviour
{
    void Start()
    {
        Debug.Log("Custom Component Added");
    }
}
```

- `AddComponentMenu`属性を付けることで、Unityエディターの「Add Component」メニューに`Custom/CustomComponent`という項目が追加され、そこから直接アタッチできるようになります。

<br>

# 4. **[ExecuteInEditMode]**
`[ExecuteInEditMode]`属性を付けることで、クラスのメソッドが**エディター上で実行中でも動作**するようになります。通常はプレイモードでしか実行されない処理を、エディターでオブジェクトを編集している際にも実行できます。

#### 使用例：

```csharp
[ExecuteInEditMode]
public class EditModeExample : MonoBehaviour
{
    void Update()
    {
        Debug.Log("Running in Edit Mode");
    }
}
```

- `ExecuteInEditMode`を付けることで、このクラスはプレイモード外でも`Update`メソッドが呼び出されるようになります。

<br>

# 5. **[DisallowMultipleComponent]**
`[DisallowMultipleComponent]`属性を付けると、**同じコンポーネントを複数追加することを防ぐ**ことができます。この属性は、特定のコンポーネントが1つしか存在しないようにしたい場合に使用します。

#### 使用例：

```csharp
[DisallowMultipleComponent]
public class SingleComponentExample : MonoBehaviour
{
    void Start()
    {
        Debug.Log("This component can't be added more than once");
    }
}
```

- `DisallowMultipleComponent`を付けると、このスクリプトをオブジェクトに2つ以上追加することができなくなります。



<br>


<br>

<br>


---


---

<br>

<br>

<br>


`System.Serializable`を使って、カスタムクラスや構造体を作成し、それを`UnityEvent`の引数として利用することは可能です。さらに、これによりインスペクターでカスタムクラスのフィールドを設定できるようになります。

ただし、`UnityEvent`自体に直接`System.Serializable`を適用するわけではなく、**カスタムクラス**や**データ構造**を`System.Serializable`にして、それを`UnityEvent`の引数として扱う形になります。

以下に、`System.Serializable`なカスタムクラスを作成し、それを`UnityEvent`に渡してインスペクターから引数を設定する例を示します。

<br>

---

<br>

# 1. **SerializableなクラスをUnityEventに渡す例**

## ステップ 1: カスタムクラスを作成し、Serializableにする

```csharp
using System;
using UnityEngine;

// このクラスをインスペクターでシリアライズ可能にする
[System.Serializable]
public class CustomData
{
    public string message;
    public int value;
}
```

- `CustomData`クラスは、`System.Serializable`属性を使用してインスペクターで編集できるようにしています。
- このクラスには、`string`型の`message`と、`int`型の`value`というフィールドを持っています。

## ステップ 2: UnityEventでカスタムクラスを使用する

```csharp
using UnityEngine;
using UnityEngine.Events;

public class UnityEventWithCustomData : MonoBehaviour
{
    // CustomDataを引数に取るUnityEvent
    [System.Serializable]
    public class CustomDataEvent : UnityEvent<CustomData> { }

    // インスペクターで設定できるUnityEvent
    public CustomDataEvent onCustomDataEvent;

    public CustomData data;

    void Start()
    {
        // イベントを発火し、CustomDataを渡す
        onCustomDataEvent?.Invoke(data);
    }
}
```

- `UnityEvent<CustomData>`を定義して、インスペクターから`CustomData`を渡せるようにしています。
- `onCustomDataEvent`は`CustomDataEvent`型で、`CustomData`を引数として受け取ります。

## ステップ 3: インスペクターで設定

1. Unityエディター上で、このスクリプトをGameObjectにアタッチします。
2. スクリプトをアタッチしたGameObjectのインスペクターに、`onCustomDataEvent`が表示されます。
3. さらに`CustomData`クラスのフィールド（`message`と`value`）もインスペクターに表示されます。
4. イベントリスナーを設定し、実行時に指定した引数が渡されるようにします。

<br>

---

---

<br>

# 2. **カスタムクラスを使ってイベントを処理する例**

```csharp
using UnityEngine;

public class CustomDataReceiver : MonoBehaviour
{
    // イベントが発生したときに呼び出されるメソッド
    public void OnCustomDataReceived(CustomData data)
    {
        Debug.Log($"Received message: {data.message}, Value: {data.value}");
    }
}
```

- こちらは、`UnityEvent`で渡された`CustomData`を受け取るクラスです。
- `OnCustomDataReceived`メソッドをインスペクターでイベントリスナーに登録し、イベントが発生したときにこのメソッドが実行されます。

<br>

---

<br>

# 3. **インスペクターでの設定方法**

1. `UnityEventWithCustomData`スクリプトを持つGameObjectを選択すると、インスペクターに`onCustomDataEvent`の設定フィールドが表示されます。
2. **「+」ボタン**を押してリスナーを追加します。
3. リスナーに`CustomDataReceiver`を持つGameObjectを割り当て、その中の`OnCustomDataReceived`メソッドを選択します。
4. これで、`Start`メソッドで`onCustomDataEvent.Invoke(data)`が実行されると、`CustomDataReceiver`の`OnCustomDataReceived`メソッドが呼び出され、`CustomData`が渡されます。

<br>

<br>

<br>

---
---

<br>
<br>
<br>


# System.Serializableの別の使い方

`[System.Serializable]`は**JSONシリアライズ**の際にも役立ちます。   UnityでデータをJSON形式に変換する場合、クラスやデータ構造が**シリアライズ可能**である必要があり、`[System.Serializable]`を使うことでそれが実現できます。

`[System.Serializable]`の主な使いどころは、**Unityのシリアライズシステム**や**データの永続化**に関わる部分です。JSONシリアライズ以外にも、いくつかの使い所がありますので、それぞれについて詳しく説明します。

<br>

---
---

<br>

# 1. **JSONシリアライズ**
`[System.Serializable]`は、Unityの**`JsonUtility`**を使ってデータをJSONに変換するために必要です。`JsonUtility`は、クラスや構造体をJSON形式に変換したり、逆にJSONからオブジェクトに変換したりできますが、その際にシリアライズ可能であることが前提です。

#### 使用例：
```csharp
using UnityEngine;

[System.Serializable]
public class PlayerData
{
    public string playerName;
    public int level;
    public float health;
}

public class JsonExample : MonoBehaviour
{
    void Start()
    {
        PlayerData player = new PlayerData { playerName = "John", level = 10, health = 99.5f };
        
        // オブジェクトをJSONに変換
        string json = JsonUtility.ToJson(player);
        Debug.Log("Serialized JSON: " + json);
        
        // JSONをオブジェクトに変換
        PlayerData deserializedPlayer = JsonUtility.FromJson<PlayerData>(json);
        Debug.Log("Deserialized Player Name: " + deserializedPlayer.playerName);
    }
}
```

- `PlayerData`クラスは`[System.Serializable]`を付けているので、`JsonUtility`でJSON形式に変換できます。

<br>

---
---

<br>

# 2. **インスペクターでカスタムクラスを表示**
`[System.Serializable]`は、**Unityのインスペクター**にカスタムクラスや構造体を表示させるためにも使用されます。通常、Unityのインスペクターではプリミティブ型（int、float、stringなど）やUnityの組み込み型（Vector3、Quaternionなど）のみが表示されますが、`[System.Serializable]`を付けることで、独自に定義したクラスもインスペクターに表示できるようになります。

#### 使用例：
```csharp
[System.Serializable]
public class Weapon
{
    public string name;
    public int damage;
}

public class Inventory : MonoBehaviour
{
    public Weapon sword;
}
```

- この例では、`Weapon`クラスに`[System.Serializable]`を付けているため、`Inventory`スクリプトをアタッチしたGameObjectのインスペクターに`Weapon`クラスのフィールドが表示されます。

<br>

---
---

<br>

# 3. **スクリプタブル・オブジェクトでのデータ保存**
`[System.Serializable]`は、**スクリプタブル・オブジェクト**と組み合わせて使用され、ゲームデータや設定を保存するために利用されます。スクリプタブル・オブジェクトは、データをオブジェクトとして扱うための仕組みであり、Unityエディター上でデータを作成・保存・編集できるようにします。シリアライズ可能にすることで、カスタムデータを保存可能にします。

#### 使用例：
```csharp
[System.Serializable]
public class EnemyStats
{
    public int health;
    public int attack;
    public float speed;
}

[CreateAssetMenu(fileName = "NewEnemy", menuName = "Enemy Stats")]
public class EnemyData : ScriptableObject
{
    public EnemyStats stats;
}
```

- `EnemyStats`をシリアライズすることで、`ScriptableObject`のインスペクターで敵のステータスを設定・保存できるようになります。

<br>

---
---

<br>

# 4. **セーブデータの永続化**
`[System.Serializable]`は、データを**ファイルに保存**する場合にも利用されます。例えば、バイナリ形式やJSON形式でセーブデータを保存する場合、シリアライズ可能なオブジェクトとして扱われ、ゲームの状態を保存・読み込む際に使われます。

#### 使用例：
```csharp
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
using UnityEngine;

[System.Serializable]
public class GameData
{
    public int score;
    public int level;
}

public class SaveLoadExample : MonoBehaviour
{
    public GameData data;

    public void SaveGame()
    {
        BinaryFormatter formatter = new BinaryFormatter();
        using (FileStream file = File.Create(Application.persistentDataPath + "/savefile.dat"))
        {
            formatter.Serialize(file, data);
        }
    }

    public void LoadGame()
    {
        if (File.Exists(Application.persistentDataPath + "/savefile.dat"))
        {
            BinaryFormatter formatter = new BinaryFormatter();
            using (FileStream file = File.Open(Application.persistentDataPath + "/savefile.dat", FileMode.Open))
            {
                data = (GameData)formatter.Deserialize(file);
            }
        }
    }
}
```

- この例では、`GameData`クラスがシリアライズされ、バイナリ形式でセーブファイルに保存されています。

<br>

---
---

<br>

# 5. **カスタムエディターの作成**
`[System.Serializable]`は、**カスタムエディター**を作成するときにも役立ちます。インスペクターの見た目をカスタマイズしたり、特定のクラスやデータ構造を扱いやすくするために利用されます。

例えば、カスタムクラスをシリアライズして、そのデータをカスタムエディター上で扱うことで、より直感的なUIを作成できます。

シリアライズするデータクラスを作成

```cs
using UnityEngine;

[System.Serializable]
public class Weapon
{
    public string weaponName;
    public int damage;
    public float range;
}

public class WeaponHolder : MonoBehaviour
{
    public Weapon[] weapons;
}

```

<br>

このデータクラスを表示するカスタムエディターを作成

```cs
using UnityEngine;
using UnityEditor;

[CustomEditor(typeof(WeaponHolder))]
public class WeaponHolderEditor : Editor
{
    public override void OnInspectorGUI()
    {
        // デフォルトのインスペクターレイアウトを描画
        DrawDefaultInspector();

        // ターゲットのWeaponHolderオブジェクトを取得
        WeaponHolder weaponHolder = (WeaponHolder)target;

        // カスタムフィールドの表示
        if (GUILayout.Button("Print Weapon Names"))
        {
            foreach (Weapon weapon in weaponHolder.weapons)
            {
                Debug.Log(weapon.weaponName);
            }
        }
    }
}

```

ボタンを押すと、インスペクターに表示された武器リストの名前がログに出力されます。


[シリアライズ](シリアライズ.md)







