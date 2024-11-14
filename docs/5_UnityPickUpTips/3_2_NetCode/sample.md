以下に、`Netcode for GameObjects` を使用して、RPC（リモートプロシージャコール）、`NetworkVariable`、および `NetworkObject` を組み合わせたサンプルプログラムを示します。

このプログラムでは、ホストがカウントを管理し、クライアントはその値を受け取ることができます。また、クライアントがリモートプロシージャコールでカウントを増加させることも可能です。

### サンプルプログラムの概要
1. **`NetworkVariable<int> count`**：ホストによって管理され、すべてのクライアントに同期されるカウンター。
2. **`IncrementCountServerRpc()`**：クライアントがホストにリクエストして、カウントを増加させるためのRPCメソッド。
3. **`PrintCountClientRpc()`**：ホストからクライアントへカウント値を表示するためのRPCメソッド。

### スクリプトの実装例

#### CountManager.cs
このスクリプトを `NetworkObject` を持つゲームオブジェクトにアタッチします。

```csharp
using UnityEngine;
using Unity.Netcode;

public class CountManager : NetworkBehaviour
{
    // NetworkVariableでカウント変数を定義し、全クライアントと同期させる
    private NetworkVariable<int> count = new NetworkVariable<int>(0);

    void Start()
    {
        // サーバーまたはホストのみカウントを定期的に増加させる
        if (IsServer)
        {
            InvokeRepeating(nameof(IncreaseCount), 1.0f, 1.0f);
        }
    }

    void Update()
    {
        // カウントの値を画面に表示（ホストとクライアント両方）
        if (IsClient)
        {
            Debug.Log($"Count Value (Synced): {count.Value}");
        }
    }

    // サーバー側で定期的にカウントを増やす
    private void IncreaseCount()
    {
        if (IsServer)
        {
            count.Value += 1;
            PrintCountClientRpc(count.Value); // クライアントに現在のカウントを送信
        }
    }

    // クライアントから呼び出せるRPCでカウントを増やす
    [ServerRpc(RequireOwnership = false)]
    public void IncrementCountServerRpc()
    {
        if (IsServer)
        {
            count.Value += 1;
            PrintCountClientRpc(count.Value); // クライアントに最新のカウントを送信
        }
    }

    // クライアント側でカウント値を表示するためのRPC
    [ClientRpc]
    private void PrintCountClientRpc(int newCountValue)
    {
        Debug.Log($"Updated Count Value from Server: {newCountValue}");
    }
}
```

### このスクリプトの動作説明
1. **`NetworkVariable<int> count`**：
   - `count` は `NetworkVariable` として定義されており、サーバーで変更されるとすべてのクライアントと同期されます。
   - `NetworkVariable` は基本的にサーバー（またはホスト）側からのみ変更され、変更がクライアントに自動的に反映されます。

2. **`IncreaseCount()` メソッド**：
   - このメソッドはホスト/サーバー側でのみ定期的に呼ばれ、`count` の値を1ずつ増やします。
   - 増加したカウントをすべてのクライアントに通知するために `PrintCountClientRpc()` を呼び出します。

3. **`IncrementCountServerRpc()` メソッド**：
   - このメソッドは `ServerRpc` として宣言されており、クライアントからホスト/サーバーに対して呼び出されます。
   - クライアントがカウントを増加させることができるようにし、ホスト/サーバーで `count` を更新し、クライアントへ通知します。

4. **`PrintCountClientRpc()` メソッド**：
   - これは `ClientRpc` メソッドで、ホスト/サーバーがクライアントにカウントの更新を通知します。
   - `ClientRpc` メソッドを使うことで、ホスト/サーバーからすべてのクライアントに対して特定の動作を実行できます（今回はカウント値を表示するために使用）。

### 使用手順
1. `NetworkManager` をシーンに追加し、必要な設定を行います。
2. カウントを管理するための空オブジェクトを作成し、このオブジェクトに `NetworkObject` コンポーネントと `CountManager` スクリプトをアタッチします。
3. シーンを実行し、ホストとして開始します。クライアントを接続すると、カウントの同期を確認できます。
4. クライアントで任意のイベント（UIボタンなど）に `IncrementCountServerRpc` メソッドを紐づけることで、クライアントからカウントを増加させることも可能です。

このサンプルにより、`NetworkVariable` と `RPC` の使い分け、サーバーからクライアントへのデータ同期の流れが確認できます。


<br>

[NetworkVariableで使える型について](NetworkVariable.md)