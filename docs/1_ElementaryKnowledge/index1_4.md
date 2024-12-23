


<br>

<br>

# メソッドの実行順について

`Awake`よりも早くスクリプトのメソッドを呼び出す方法としては、Unityの特定の初期化処理を制御する方法があります。特に`Script Execution Order`を使用すると、スクリプトの実行順序をカスタマイズすることができます。

## Script Execution Order

Unityでは、スクリプトの実行順序を制御するために、`Edit` メニューから `Project Settings` に移動し、 `Script Execution Order` を設定することができます。ここで特定のスクリプトを他のスクリプトよりも先に実行させることができます。

## Script Execution Orderの設定方法

1. **UnityのメニューからScript Execution Orderを開く**:
   - `Edit` → `Project Settings` → `Script Execution Order` を選択します。

2. **スクリプトの追加**:
   - ウィンドウの右上にある `+` ボタンをクリックし、優先的に実行したいスクリプトを選択します。

3. **実行順序の設定**:
   - 追加したスクリプトをドラッグ＆ドロップして、他のスクリプトよりも先に実行されるように順序を調整します。
   - 例えば、特定のスクリプトを`Default Time`よりも前に実行させるように設定します。

4. **設定の保存**:
   - 設定を完了したら、ウィンドウを閉じます。設定は自動的に保存されます。

<br>

## 特定の初期化処理

さらに、特定の初期化処理をカスタマイズするために、`RuntimeInitializeOnLoadMethod`属性を使用することができます。これにより、スクリプトのメソッドを非常に早い段階で実行することができます。

## `RuntimeInitializeOnLoadMethod`の使用方法

```csharp
using UnityEngine;

public class EarlyInitializer : MonoBehaviour
{
    // ここで定義するメソッドはゲームがロードされた直後に呼び出されます
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void OnBeforeSceneLoad()
    {
        Debug.Log("This is called before any scene is loaded");
    }

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    static void OnAfterSceneLoad()
    {
        Debug.Log("This is called after the first scene is loaded");
    }
}
```

## 使用例

- **`RuntimeInitializeLoadType.BeforeSceneLoad`**: シーンがロードされる前に呼び出されます。非常に早い段階での初期化処理に使用できます。
- **`RuntimeInitializeLoadType.AfterSceneLoad`**: シーンがロードされた後に呼び出されますが、`Awake`よりも早く実行されます。

## まとめ

- **Script Execution Order**を使用すると、特定のスクリプトを他のスクリプトよりも先に実行させることができます。
- **`RuntimeInitializeOnLoadMethod`属性**を使用すると、非常に早い段階でスクリプトのメソッドを実行することができます。

これらの方法を組み合わせることで、`Awake`よりも早くスクリプトのメソッドを実行することが可能になります。


<br>

<br>

`RuntimeInitializeOnLoadMethod`属性を使う際の注意点として、以下の点に注意する必要があります。

<br>

<br>

## 注意点

1. **静的メソッドであること**:
   - `RuntimeInitializeOnLoadMethod`属性を付けるメソッドは静的メソッドである必要があります。
   ```csharp
   [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
   static void MyEarlyInitializationMethod()
   {
       // 初期化処理
   }
   ```

2. **メソッド引数の無いこと**:
   - 属性を付けるメソッドは引数を持たない必要があります。
   ```csharp
   [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
   static void Initialize()
   {
       // 初期化処理
   }
   ```

3. **実行順序の制御が難しい**:
   - 他のスクリプトやシステムと実行順序を正確に制御することは難しい場合があります。特定の順序で初期化が必要な場合は、`Script Execution Order`を併用すると良いでしょう。

4. **ロードタイプの選択**:
   - `RuntimeInitializeLoadType`にはいくつかのオプションがあり、それぞれの実行タイミングが異なります。適切なオプションを選択することが重要です。
     - `BeforeSceneLoad`: 最初のシーンがロードされる前に実行されます。
     - `AfterSceneLoad`: 最初のシーンがロードされた後、`Awake`や`Start`の前に実行されます。
     - `BeforeSplashScreen`: スプラッシュスクリーンが表示される前に実行されます。
     - `AfterAssembliesLoaded`: アセンブリがロードされた後に実行されます。

5. **エディタモードでの動作**:
   - `RuntimeInitializeOnLoadMethod`属性は、エディタモードでのプレイ開始時にも呼び出されますが、エディタモードのスクリプトリロード時には呼び出されません。エディタモードでの動作を考慮する必要がある場合は、他の方法（例えば、`InitializeOnLoadMethod`属性）を使用することも考えられます。

6. **重複実行の注意**:
   - 同じ初期化処理が複数回呼ばれることを防ぐために、フラグを使用して一度だけ初期化するようにすることが有効です。
   ```csharp
   private static bool isInitialized = false;

   [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
   static void Initialize()
   {
       if (isInitialized) return;
       isInitialized = true;
       // 初期化処理
   }
   ```

7. **パフォーマンスの考慮**:
   - ゲームの起動時に重い処理を行うと、ロード時間が長くなる可能性があります。初期化処理はできるだけ軽量にすることを心がけると良いでしょう。

これらの注意点を踏まえた上で`RuntimeInitializeOnLoadMethod`属性を使用することで、効果的かつ安全な初期化処理を行うことができます。