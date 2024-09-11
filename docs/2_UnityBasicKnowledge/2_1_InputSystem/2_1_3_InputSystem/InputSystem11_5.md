# Input Systemでキーコンフィグを実装する③

## Composite Bindingに対してリバインドする
WASDキーや十字キー移動などで使われるComposite Bindingに対してもリバインドできます。

Composite Bindingでは複数のBindingを合成した一つのBindingのように振る舞いますが、Bindingとしては次のようにComposite Bindingおよびその内包されるBindingが一緒に配置されています。


<img src="images/11/11_2/unity-input-system-rebinding-6.png.avif" width="90%" alt="" title="">

<br>

リバインドするときはComposite Bindingそのものではなく、内包されるBindingに対して行う必要があります。

例えば、移動操作の4方向を順番にリバインドしたい場合、前述のインタラクティブなリバインドを順に繰り返すといった方法で実現できます。

Composite Bindingが内包する数の分だけ繰り返せばよいことになります。

<br>

## サンプルスクリプト
以下、Composite Bindingに対応するようにスクリプトを改良した例です。

RebindUI.cs
```cs
using TMPro;
using UnityEngine;
using UnityEngine.InputSystem;

public class RebindUI : MonoBehaviour
{
    // リバインド対象のAction
    [SerializeField] private InputActionReference _actionRef;

    // リバインド対象のScheme
    [SerializeField] private string _scheme = "Keyboard";

    // 現在のBindingのパスを表示するテキスト
    [SerializeField] private TMP_Text _pathText;

    // リバインド中のマスク用オブジェクト
    [SerializeField] private GameObject _mask;

    private InputAction _action;
    private InputActionRebindingExtensions.RebindingOperation _rebindOperation;

    // 初期化
    private void Awake()
    {
        if (_actionRef == null) return;

        // InputActionインスタンスを保持しておく
        _action = _actionRef.action;

        // キーバインドの表示を反映する
        RefreshDisplay();
    }

    // 後処理
    private void OnDestroy()
    {
        // オペレーションは必ず破棄する必要がある
        CleanUpOperation();
    }

    // リバインドを開始する
    public void StartRebinding()
    {
        // もしActionが設定されていなければ、何もしない
        if (_action == null) return;

        // リバインド対象のBindingIndexを取得
        var bindingIndex = _action.GetBindingIndex(
            InputBinding.MaskByGroup(_scheme)
        );

        // リバインドを開始する
        OnStartRebinding(bindingIndex);
    }

    // 上書きされた情報をリセットする
    public void ResetOverrides()
    {
        // Bindingの上書きを全て解除する
        _action?.RemoveAllBindingOverrides();
        RefreshDisplay();
    }

    // 現在のキーバインド表示を更新
    public void RefreshDisplay()
    {
        if (_action == null || _pathText == null) return;

        _pathText.text = _action.GetBindingDisplayString();
    }

    // 指定されたインデックスのBindingのリバインドを開始する
    private void OnStartRebinding(int bindingIndex)
    {
        // もしリバインド中なら、強制的にキャンセル
        // Cancelメソッドを実行すると、OnCancelイベントが発火する
        _rebindOperation?.Cancel();

        // リバインド前にActionを無効化する必要がある
        _action.Disable();

        // ブロッキング用マスクを表示
        if (_mask != null)
            _mask.SetActive(true);

        // リバインドが終了した時の処理を行うローカル関数
        void OnFinished(bool hideMask = true)
        {
            // オペレーションの後処理
            CleanUpOperation();

            // 一時的に無効化したActionを有効化する
            _action.Enable();

            // ブロッキング用マスクを非表示
            if (_mask != null && hideMask)
                _mask.SetActive(false);
        }

        // リバインドのオペレーションを作成し、
        // 各種コールバックの設定を実施し、
        // 開始する
        _rebindOperation = _action
            .PerformInteractiveRebinding(bindingIndex)
            .OnComplete(_ =>
            {
                // リバインドが完了した時の処理
                RefreshDisplay();

                var bindings = _action.bindings;
                var nextBindingIndex = bindingIndex + 1;

                if (nextBindingIndex <= bindings.Count - 1 && bindings[nextBindingIndex].isPartOfComposite)
                {
                    // Composite Bindingの一部なら、次のBindingのリバインドを開始する
                    OnFinished(false);
                    OnStartRebinding(nextBindingIndex);
                }
                else
                {
                    OnFinished();
                }
            })
            .OnCancel(_ =>
            {
                // リバインドがキャンセルされた時の処理
                OnFinished();
            })
            .OnMatchWaitForAnother(0.2f) // 次のリバインドまでの待機時間を設ける
            .Start(); // ここでリバインドを開始する
    }

    // リバインドオペレーションを破棄する
    private void CleanUpOperation()
    {
        // オペレーションを作成したら、Disposeしないとメモリリークする
        _rebindOperation?.Dispose();
        _rebindOperation = null;
    }
}
```

使用方法はこれまでの例と変わりありません。

例では、次のように移動操作のMove Actionに対して適用するものとします。

<img src="images/11/11_2/unity-input-system-rebinding-m7.mp4.gif" width="90%" alt="" title="">

<br>

## 実行結果
次のように順番に入力受け付けされるようになりました。

<img src="images/11/11_2/unity-input-system-rebinding-m8.mp4.gif" width="90%" alt="" title="">

<br>

## スクリプトの説明
インタラクティブなリバインドが開始されたらBindingのインデックスを取得するところまでは一緒です。

```cs
// リバインド対象のBindingIndexを取得
var bindingIndex = _action.GetBindingIndex(
    InputBinding.MaskByGroup(_scheme)
);

// リバインドを開始する
OnStartRebinding(bindingIndex);
```

<br>

Composite Bindingはスキームに含まれないため、上記のコードで内包されるBindingの開始インデックスを取得できます。

リバインドの設定やコールバック処理は以下のように変更しています。

```cs
// リバインドのオペレーションを作成し、
// 各種コールバックの設定を実施し、
// 開始する
_rebindOperation = _action
    .PerformInteractiveRebinding(bindingIndex)
    .OnComplete(_ =>
    {
        // リバインドが完了した時の処理
        RefreshDisplay();

        var bindings = _action.bindings;
        var nextBindingIndex = bindingIndex + 1;

        if (
            nextBindingIndex <= bindings.Count - 1 &&
            bindings[nextBindingIndex].isPartOfComposite)
        {
            // Composite Bindingの一部なら、次のBindingのリバインドを開始する
            OnFinished(false);
            OnStartRebinding(nextBindingIndex);
        }
        else
        {
            OnFinished();
        }
    })
    .OnCancel(_ =>
    {
        // リバインドがキャンセルされた時の処理
        OnFinished();
    })
    .OnMatchWaitForAnother(0.2f) // 次のリバインドまでの待機時間を設ける
    .Start(); // ここでリバインドを開始する

```

次のインデックスのBindingを調べ、それがComposite Bindingに内包されるBindingであれば、次のBindingを開始しています。

ただし、続けてインタラクティブなリバインドを行う場合、前入力が悪さして誤入力されることがあるため、次のコードで0.2秒ほど待機時間を挟んでいます。

```cs
.OnMatchWaitForAnother(0.2f) // 次のリバインドまでの待機時間を設ける
```
OnMatchWaitForAnotherメソッドは、リバインドが成功してから次のリバインドを開始するまでの待機時間を設定するメソッドです。

待機時間は状況に合わせて調整してください。

[参考：Class InputActionRebindingExtensions.RebindingOperation| Input System](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.5/api/UnityEngine.InputSystem.InputActionRebindingExtensions.RebindingOperation.html#UnityEngine_InputSystem_InputActionRebindingExtensions_RebindingOperation_OnMatchWaitForAnother_System_Single_)

<br>
