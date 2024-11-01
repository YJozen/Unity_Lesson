# Input Systemでキーコンフィグを実装する②

## 設定をリセットする
リバインドによって上書きされたキー割当ては、リセットして無かったことにすることも可能です。

上書き情報はActionのBinding情報とは別で管理されているため、内部的には上書き情報を削除するだけで済みます。


<img src="images/11/11_2/unity-input-system-rebinding-4.png.avif" width="90%" alt="" title="">

<br>

リセットには、RemoveBindingOverride拡張メソッドまたはRemoveAllBindingOverrides拡張メソッドを使います。

```cs
InputAction action;

・・・（中略）・・・

// Bindingの上書きを全て解除する
action.RemoveAllBindingOverrides();
```

[参考：Class InputActionRebindingExtensions| Input System | 1.5.1]()

## ・サンプルスクリプト
前述のスクリプトにリセットメソッドを追加した例です。

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

        // もしリバインド中なら、強制的にキャンセル
        // Cancelメソッドを実行すると、OnCancelイベントが発火する
        _rebindOperation?.Cancel();

        // リバインド前にActionを無効化する必要がある
        _action.Disable();

        // リバインド対象のBindingIndexを取得
        var bindingIndex = _action.GetBindingIndex(
            InputBinding.MaskByGroup(_scheme)
        );

        // ブロッキング用マスクを表示
        if (_mask != null)
            _mask.SetActive(true);

        // リバインドが終了した時の処理を行うローカル関数
        void OnFinished()
        {
            // オペレーションの後処理
            CleanUpOperation();

            // 一時的に無効化したActionを有効化する
            _action.Enable();

            // ブロッキング用マスクを非表示
            if (_mask != null)
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
                OnFinished();
            })
            .OnCancel(_ =>
            {
                // リバインドがキャンセルされた時の処理
                OnFinished();
            })
            .Start(); // ここでリバインドを開始する
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

    // リバインドオペレーションを破棄する
    private void CleanUpOperation()
    {
        // オペレーションを作成したら、Disposeしないとメモリリークする
        _rebindOperation?.Dispose();
        _rebindOperation = null;
    }
}
```
RebindUI.csを上記の内容に置き換えれば機能します。インスペクターからの設定方法は変わりありません。

リセットボタンなどが押された際にResetOverridesメソッドを呼び出すと上書き情報がすべて削除されてリセットされます。

<br>

<img src="images/11/11_2/unity-input-system-rebinding-m5.mp4.gif" width="90%" alt="" title="">

<br>

# 実行結果
リセットボタンを押すと、キー割り当てが初期設定（Space）に戻っていることが確認できました。

<img src="images/11/11_2/unity-input-system-rebinding-m6.mp4.gif" width="90%" alt="" title="">

<br>

## スクリプトの説明
リセットする処理は以下部分です。
```cs
// 上書きされた情報をリセットする
public void ResetOverrides()
{
    // Bindingの上書きを全て解除する
    _action?.RemoveAllBindingOverrides();
    RefreshDisplay();
}
```
リセットした後は、画面を更新するようにしています。
