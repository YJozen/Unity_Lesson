



UnityのAddressable Assets System（アドレッサブル）は、アセットを動的にロード・管理できる仕組みです。  
特に、複数のプラットフォームやサイズの大きなゲームでのメモリ管理とロード時間の改善に役立ちます。  
ここでは、基本的な使い方、実践例、メリット、注意点について解説します。

<br>

# Addressableの使い方の基本

1. **Addressableのインストール**
   - Unityの「Package Manager」から「Addressables」パッケージをインストールします。

2. **アセットの設定**
   - アセットをAddressable化するには、インスペクターで「Addressable」のチェックをオンにし、アセットに一意の名前（Address）を付けます。このAddressを使って後でアクセスできます。

3. **Addressable Groupsの作成**
   - 「Window > Asset Management > Addressables > Groups」から「Addressables Groups」ウィンドウを開きます。ここで、アセットをグループごとに整理します。
   - グループごとにビルド設定（メモリ内に保持するか、圧縮するか、外部に保持するかなど）を細かく設定できます。

4. **アセットのロードとアンロード**
   - `Addressables.LoadAssetAsync<T>("Address")` を使ってアセットを非同期でロードします。
   - ロードしたアセットを使い終わったら `Addressables.Release(asset)` でメモリから解放します。

<br>

# Addressableの実践例

## シンプルなアセットの読み込み例

```csharp
using UnityEngine;
using UnityEngine.AddressableAssets;

public class AddressableExample : MonoBehaviour
{
    public string assetAddress; // インスペクターで設定できるアセットのアドレス

    private GameObject loadedObject;

    public void LoadAsset()
    {
        Addressables.LoadAssetAsync<GameObject>(assetAddress).Completed += handle =>
        {
            if (handle.Status == UnityEngine.ResourceManagement.AsyncOperations.AsyncOperationStatus.Succeeded)
            {
                loadedObject = handle.Result;
                Instantiate(loadedObject);
            }
            else
            {
                Debug.LogError("アセットのロードに失敗しました");
            }
        };
    }

    public void UnloadAsset()
    {
        if (loadedObject != null)
        {
            Addressables.Release(loadedObject);
            loadedObject = null;
        }
    }
}
```

<br>

## アセットバンドルを使ったレベルの動的読み込み例

ゲームのレベル（シーン）ごとにアセットをアドレッサブルで管理すると、メモリ使用量を最適化できます。

```csharp
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.SceneManagement;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AddressableSceneLoader : MonoBehaviour
{
    public string sceneAddress; // 読み込みたいシーンのアドレス

    public void LoadScene()
    {
        Addressables.LoadSceneAsync(sceneAddress, LoadSceneMode.Additive).Completed += OnSceneLoaded;
    }

    private void OnSceneLoaded(AsyncOperationHandle<SceneInstance> handle)
    {
        if (handle.Status == AsyncOperationStatus.Succeeded)
        {
            Debug.Log("シーンの読み込み成功");
        }
        else
        {
            Debug.LogError("シーンの読み込みに失敗しました");
        }
    }

    public void UnloadScene()
    {
        Addressables.UnloadSceneAsync(sceneAddress);
    }
}
```

<br>

# Addressableのメリット

1. **メモリ管理とロード時間の最適化**
   - 必要なアセットのみをオンデマンドでロードでき、使用しないアセットを解放できるため、メモリ使用量を効率的に抑えることが可能です。

2. **マルチプラットフォーム対応**
   - プラットフォームごとに異なるアセット設定が可能で、デバイスのスペックに合わせた管理がしやすくなります。

3. **柔軟なアセット更新**
   - サーバーにアップロードしたアセットを随時更新することが可能で、ゲームのアップデートを効果的に行えます。

4. **スケーラビリティの向上**
   - ゲームの規模が拡大しても、ロードとメモリ管理の調整により、ゲーム全体の最適化がしやすくなります。

### Addressableを使う上での注意点

1. **アセットのビルド管理**
   - ビルド後のアセットのパスや依存関係が増えるため、複数のAddressable Groupsを設定する際は、メモリ負荷が高くならないようグループを慎重に構成しましょう。

2. **ロード時間**
   - 非同期ロードとはいえ、アセットのサイズが大きいとロード時間が増えます。ゲームプレイに影響を与えないよう、事前にバックグラウンドでロードするなど工夫が必要です。

3. **デバッグ**
   - Addressableは動的に管理されるため、エラーやロード失敗時に問題の特定が難しい場合があります。ログ出力やエラーハンドリングを適切に行うことで、デバッグをしやすくしておきましょう。

4. **アドレスの一意性**
   - 同じAddress名を異なるアセットに設定するとロードが混乱するため、ユニークな名前を付けることが必須です。プロジェクト内でのネーミングルールを決めておくと良いです。

5. **デプロイメント時の構成**
   - Addressableに含めるアセットのサイズや数が大きすぎると、ダウンロード量やメモリ負荷が増加し、パフォーマンスに影響する可能性があります。