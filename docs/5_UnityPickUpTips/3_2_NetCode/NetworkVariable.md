`NetworkVariable` は `int` 以外にも使用できます。  

`Netcode for GameObjects` では、`NetworkVariable` を用いて複数のデータ型の同期が可能です。

以下は、`NetworkVariable` に対応する主なデータ型の例です。

### 対応するデータ型の例
1. **整数型**: `int`, `float`, `double`, `long`, `short`, `byte`
2. **ブール型**: `bool`
3. **文字列型**: `string`
4. **ベクトル型**: `Vector2`, `Vector3`, `Vector4`
5. **色型**: `Color`
6. **構造体**: `Quaternion`, `Ray`, など
7. **配列・リスト**: 特定のジェネリック型（例えば `NetworkList<T>`）としてリストもサポートされています。



### 使用例
いくつかの異なる `NetworkVariable` 型を定義した例を示します。

```csharp
using UnityEngine;
using Unity.Netcode;

public class NetworkVariableExample : NetworkBehaviour
{
    // さまざまな型のNetworkVariableを定義
    public NetworkVariable<int> health = new NetworkVariable<int>(100);
    public NetworkVariable<float> speed = new NetworkVariable<float>(5.0f);
    public NetworkVariable<bool> isAlive = new NetworkVariable<bool>(true);
    public NetworkVariable<Vector3> position = new NetworkVariable<Vector3>(Vector3.zero);
    public NetworkVariable<Color> playerColor = new NetworkVariable<Color>(Color.white);
    
    void Start()
    {
        // サーバー/ホストが値を更新する例
        if (IsServer)
        {
            health.Value = 90;
            speed.Value = 7.5f;
            isAlive.Value = false;
            position.Value = new Vector3(1, 1, 1);
            playerColor.Value = Color.red;
        }
    }

    void Update()
    {
        // クライアント側で値を同期しているか確認
        if (IsClient)
        {
            Debug.Log($"Health: {health.Value}, Speed: {speed.Value}, IsAlive: {isAlive.Value}");
            Debug.Log($"Position: {position.Value}, PlayerColor: {playerColor.Value}");
        }
    }
}
```



### 注意点
- `NetworkVariable` に使用するデータ型は、`INetworkSerializable` インターフェースを実装するか、`NetworkVariable` によってネイティブにサポートされている必要があります。
- 複雑なクラスやカスタム型を使う場合、独自のシリアライゼーションが必要になることがあります。その場合、`INetworkSerializable` を実装することで対応できます。



### カスタム型の例
`NetworkVariable` でカスタム構造体を同期する場合、`INetworkSerializable` を実装したカスタムデータ型を使います。

```csharp
using Unity.Netcode;
using UnityEngine;

// カスタム構造体の定義とシリアライズ
public struct PlayerStats : INetworkSerializable
{
    public int level;
    public float experience;

    public void NetworkSerialize<T>(BufferSerializer<T> serializer) where T : IReaderWriter
    {
        serializer.SerializeValue(ref level);
        serializer.SerializeValue(ref experience);
    }
}

// PlayerStatsをNetworkVariableとして定義
public class PlayerStatsExample : NetworkBehaviour
{
    public NetworkVariable<PlayerStats> playerStats = new NetworkVariable<PlayerStats>(new PlayerStats { level = 1, experience = 0.0f });

    void Start()
    {
        if (IsServer)
        {
            playerStats.Value = new PlayerStats { level = 2, experience = 150.0f };
        }
    }

    void Update()
    {
        if (IsClient)
        {
            Debug.Log($"Player Level: {playerStats.Value.level}, Experience: {playerStats.Value.experience}");
        }
    }
}
```

このように、`NetworkVariable` は標準的な型からカスタムの構造体やクラスまで幅広く対応しています。