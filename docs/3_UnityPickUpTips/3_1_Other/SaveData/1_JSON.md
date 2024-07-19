# JSON保存例

### ゲームデータのクラスを定義する

```cs

[System.Serializable]
public class GameData
{
    public int playerLevel;
    public float health;
    public List<string> inventoryItems;

    public GameData()
    {
        playerLevel = 1;
        health = 100.0f;
        inventoryItems = new List<string>();
    }
}

```

<br>

### JSONでデータを保存するクラスを作成する

```cs
using UnityEngine;
using System.IO;

public static class SaveLoadManager
{
    private static string saveFilePath = Path.Combine(Application.persistentDataPath, "gamedata.json");

    // ゲームデータを保存する
    public static void SaveGame(GameData data)
    {
        string json = JsonUtility.ToJson(data, true);
        File.WriteAllText(saveFilePath, json);
        Debug.Log("Game data saved to " + saveFilePath);
    }

    // ゲームデータを読み込む
    public static GameData LoadGame()
    {
        if (File.Exists(saveFilePath))
        {
            string json = File.ReadAllText(saveFilePath);
            GameData data = JsonUtility.FromJson<GameData>(json);
            Debug.Log("Game data loaded from " + saveFilePath);
            return data;
        }
        else
        {
            Debug.LogWarning("Save file not found in " + saveFilePath);
            return new GameData(); // デフォルトのゲームデータを返す
        }
    }
}


```
<br>

### ゲームデータを保存および読み込み

```cs

using UnityEngine;

public class GameController : MonoBehaviour
{
    private GameData currentGameData;

    private void Start()
    {
        // ゲームデータの読み込み
        currentGameData = SaveLoadManager.LoadGame();

        // 現在のゲームデータを表示
        Debug.Log("Player Level: " + currentGameData.playerLevel);
        Debug.Log("Health: " + currentGameData.health);
        Debug.Log("Inventory Items: " + string.Join(", ", currentGameData.inventoryItems));

        // ゲームデータの変更
        currentGameData.playerLevel++;
        currentGameData.health -= 10.0f;
        currentGameData.inventoryItems.Add("Sword");

        // ゲームデータの保存
        SaveLoadManager.SaveGame(currentGameData);
    }
}

```

<br>

<br>

# AES暗号

UnityでゲームデータをJSON形式で保存し、そのデータをAES暗号化で保護する方法

## 準備
Unityプロジェクトを作成し、以下のスクリプトをプロジェクト内に追加します。必要なスクリプトは以下の通りです：

GameData.cs
AESCrypto.cs
SaveLoadManager.cs
GameController.cs


## スクリプトの例


### ・GameData.cs
まず、保存するゲームデータの構造を定義します。このクラスはシリアライズ可能である必要があります。

playerLevel: プレイヤーのレベル。
health: プレイヤーの体力。
inventoryItems: プレイヤーが持っているアイテムのリスト

```cs
[System.Serializable]
public class GameData
{
    public int playerLevel;
    public float health;
    public List<string> inventoryItems;

    public GameData()
    {
        playerLevel = 1;
        health = 100.0f;
        inventoryItems = new List<string>();
    }
}

```

<br>

### ・AESCrypto.cs 
AESCrypto クラスは、文字列データをAES暗号化および復号するための静的メソッドを作成

Encrypt: 平文のテキストを暗号化します。
Decrypt: 暗号化されたテキストを復号します。

```cs
using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

public static class AESCrypto
{
    private static readonly string encryptionKey = "your-encryption-key-here"; // 必ず16, 24, 32文字にする

    public static string Encrypt(string plainText)
    {
        byte[] keyBytes = Encoding.UTF8.GetBytes(encryptionKey);
        using (Aes aes = Aes.Create())
        {
            aes.Key = keyBytes;
            aes.GenerateIV();
            byte[] iv = aes.IV;

            using (var encryptor = aes.CreateEncryptor(aes.Key, iv))
            using (var ms = new MemoryStream())
            {
                ms.Write(iv, 0, iv.Length);
                using (var cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write))
                using (var sw = new StreamWriter(cs))
                {
                    sw.Write(plainText);
                }
                return Convert.ToBase64String(ms.ToArray());
            }
        }
    }

    public static string Decrypt(string cipherText)
    {
        byte[] cipherBytes = Convert.FromBase64String(cipherText);
        byte[] keyBytes = Encoding.UTF8.GetBytes(encryptionKey);

        using (Aes aes = Aes.Create())
        {
            aes.Key = keyBytes;
            using (var ms = new MemoryStream(cipherBytes))
            {
                byte[] iv = new byte[16];
                ms.Read(iv, 0, iv.Length);
                aes.IV = iv;

                using (var decryptor = aes.CreateDecryptor(aes.Key, aes.IV))
                using (var cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Read))
                using (var sr = new StreamReader(cs))
                {
                    return sr.ReadToEnd();
                }
            }
        }
    }
}

```

<br>

## ・SaveLoadManager.cs
ゲームデータを保存および読み込むためのクラスです。
データはJSON形式で保存され、保存時にAESで暗号化されます
読み込み時に復号されます。

SaveGame: GameDataオブジェクトをJSON形式で保存し、AESで暗号化します。
LoadGame: 暗号化されたJSONデータを読み込み、AESで復号してGameDataオブジェクトに変換します。


```cs
using UnityEngine;
using System.IO;

public static class SaveLoadManager
{
    private static string saveFilePath = Path.Combine(Application.persistentDataPath, "gamedata.json");

    // ゲームデータを保存する
    public static void SaveGame(GameData data)
    {
        string json = JsonUtility.ToJson(data, true);
        string encryptedJson = AESCrypto.Encrypt(json);
        File.WriteAllText(saveFilePath, encryptedJson);
        Debug.Log("Game data saved to " + saveFilePath);
    }

    // ゲームデータを読み込む
    public static GameData LoadGame()
    {
        if (File.Exists(saveFilePath))
        {
            string encryptedJson = File.ReadAllText(saveFilePath);
            string json = AESCrypto.Decrypt(encryptedJson);
            GameData data = JsonUtility.FromJson<GameData>(json);
            Debug.Log("Game data loaded from " + saveFilePath);
            return data;
        }
        else
        {
            Debug.LogWarning("Save file not found in " + saveFilePath);
            return new GameData(); // デフォルトのゲームデータを返す
        }
    }
}

```

<br>

## ・GameController

 クラスは、ゲームの開始時にデータを読み込み、データを変更し、変更後のデータを保存する例です。
```cs 
using UnityEngine;

public class GameController : MonoBehaviour
{
    private GameData currentGameData;

    private void Start()
    {
        // ゲームデータの読み込み
        currentGameData = SaveLoadManager.LoadGame();

        // 現在のゲームデータを表示
        Debug.Log("Player Level: " + currentGameData.playerLevel);
        Debug.Log("Health: " + currentGameData.health);
        Debug.Log("Inventory Items: " + string.Join(", ", currentGameData.inventoryItems));

        // ゲームデータの変更
        currentGameData.playerLevel++;
        currentGameData.health -= 10.0f;
        currentGameData.inventoryItems.Add("Sword");

        // ゲームデータの保存
        SaveLoadManager.SaveGame(currentGameData);
    }
}


```