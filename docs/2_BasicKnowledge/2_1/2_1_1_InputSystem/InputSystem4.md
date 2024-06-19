**InputSystem 1**

## 1.ボタンが「押された瞬間」「押され続けた時」などの入力を、コールバックを利用し受け取る

適当なゲームオブジェクトにアタッチ

```cs:ActionCallback.cs
using UnityEngine;
using UnityEngine.InputSystem;

public class ActionCallbackExample : MonoBehaviour
{
    [SerializeField] private InputAction _action;

    private void OnEnable()
    {
        // Actionのコールバックを登録
        _action.performed += OnPerformed;
        _action?.Enable();
    }

    private void OnDisable()
    {
        // Actionのコールバックを解除
        _action.performed -= OnPerformed;

        // 自身が無効化されるタイミングなどでActionを無効化
        _action?.Disable();
    }

    //破壊された時など
    private void OnDestroy()
    {
        _action?.Dispose();// 破壊された時などに、Actionを無効化
    }

    // コールバックを受け取ったときの処理
    private void OnPerformed(InputAction.CallbackContext context)
    {    
        var value = context.ReadValue<float>();// Actionの入力値を読み込む       
        Debug.Log($"Actionの入力値 : {value}"); // 入力値をログ出力
    }
}

```

Actionをインスペクターから設定した後、Action右の歯車アイコンをクリック

<img src="images/4/unity-input-system-intro-v2-1.png.avif" width="50%" alt="" title="">


Action TypeをValueに設定

<img src="images/4/unity-input-system-intro-v2-2.png.avif" width="50%" alt="" title="">


---
## 2.呼び出されるタイミング３種(started・performed・canceled)

+ Value – スティックなど値が入力されたときにコールバックを受け取る設定
    - started – 入力が0から0以外に変化したとき
    - performed – 入力が0以外に変化したとき
    - canceled – 入力が0以外から0に変化したとき


<img src="images/4/unity-input-system-action-callback-1.png.avif" width="50%" alt="" title="">

<br>
<br>

+ Button – ボタンが押された瞬間にコールバックを受け取る設定
    - started – 入力が0から0以外に変化したとき
    - performed – 入力の大きさが閾値Press以上に変化したとき
    - canceled – 入力が0以外から0に変化したとき、またはperformedが呼ばれた後に入力の大きさが閾値Release以下に変化したとき

        *閾値の設定は、トップメニューのEdit > Project Settings > Input System Packageの以下項目から変更できます
        
        <img src="images/4/unity-input-system-action-callback.png.avif" width="50%" alt="" title="">

        閾値Pressの値はDefault Press Button Point、
        閾値Releaseの値は「Press × Button Release Threshold」となり、Pressと掛け算した値

<img src="images/4/unity-input-system-action-callback-2.png.avif" width="50%" alt="" title="">

<br>
<br>

+ Pass Through - デバイス入力がある間にperformedが呼ばれ続けます
    - performed - 入力があったとき
    - canceled - 例えば、デバイスが切り替わった場合、切り替わり前のデバイスが無効（Disabled）となり、canceledコールバックが呼び出されます。

<img src="images/4/unity-input-system-action-callback-3.png.avif" width="50%" alt="" title="">

<br>
<br>

