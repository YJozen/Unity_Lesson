**InputSystem 2**

# Composite Bindingの1D Axisや2D Vector



![](images/1/unity-input-system-intro-v2-1-940x563.png.avif "")

---
2.
Packages: ～ボタンをクリックし、Unity Registryを選択

![](images/1/unity-input-system-intro-v2-2.png.avif "")

---
3.


---
4.



ActionまたはBindingにInteractionが設定されている場合、Interaction側の設定が優先されます。

Hold
MultiTap
Press
SlowTap
Tap



 Press

Press Only	押した瞬間のみperformedが呼ばれる
Release Only	離された瞬間のみperformedが呼ばれる
Press And Release	押した瞬間と離された瞬間両方でperformedが呼ばれる



InteractionsがHoldの場合
一定時間ボタンを押した判定になった時にperformedが呼ばれます。



InteractionsがHoldの場合
一定時間ボタンを押した判定になった時にperformedが呼ばれます。







InteractionsがSlow Tapの場合
ゆっくりとタップした時にperformedコールバックが走るInteractionです。

タップ判定の最大許容時間は、Max Tap Duration項目で設定
タップの最小時間はMin Tap Duration項目から設定できます。






InteractionsがMulti Tapの場合
マルチタップされたときにperformedコールバックが呼ばれるInteractionです。

必要なタップ回数をTap Countに、マルチタップ判定とする最大許容時間をMax Tap Spacingに、タップの最大許容時間をMax Tap Durationに設定






複数のInteractions指定された場合
各々のInteractionのコールバックが同時に実行されるようになります。

以下はHoldとMulti Tapを同時に指定した例です。

どのInteractionからコールバックが呼ばれたかは、以下のようにInputAction.CallbackContext引数のinteractionフィールドから判別できます。

// 攻撃
public void OnFire(InputAction.CallbackContext context)
{
    // performedコールバックだけ受け取る
    if (!context.performed) return;

    if (context.interaction is HoldInteraction)
    {
        Debug.Log("長押しされたよ！");
    }
    else if (context.interaction is MultiTapInteraction)
    {
        Debug.Log("マルチタップされたよ！");
    }
}


ボタン入力として扱う場合はperformedコールバックを扱うのが安全です。startedコールバックは閾値Press Pointに関係なく入力があった時に呼ばれることがあるため注意が必要です。






自作


Input Systemでカスタムインタラクションを作成する際の使用用途として、特定の入力条件や複雑な入力シーケンスを処理する場合が挙げられます。以下に具体的な例を示します。

1. 複雑な入力パターンの検出
標準のインタラクションでは対応しきれない、複雑な入力パターンを検出したい場合にカスタムインタラクションを使用します。

例:
連続クリック: 1秒以内に3回クリックする。
コマンド入力: 特定の順序でボタンを押す（例: 格闘ゲームの必殺技コマンド）。
2. 特定の時間条件を満たす入力の検出
長押しや特定の時間内に入力が行われたかどうかを判断する場合。

例:
チャージ攻撃: ボタンを2秒以上押してから放す。
ダブルタップ: 素早く2回タップする。
3. 組み合わせ入力の検出
複数の入力を同時に行った場合の検出。

例:
コンボ操作: 特定の順序で複数のキーやボタンを押す。
モディファイアキー: シフトキーを押しながら特定のキーを押す（例: シフト + C でコピー）。
4. ジェスチャーの検出
タッチデバイスやVRコントローラーでのジェスチャー検出。

例:
スワイプジェスチャー: 画面上で特定の方向にスワイプする。
ピンチジェスチャー: 画面をピンチインまたはピンチアウトする。
5. カスタムロジックによる入力検出
特定のゲームロジックやアプリケーションロジックに基づいた入力検出。

例:
特定の条件下でのみ有効な入力: ゲーム内の特定の状態やシーンでのみ有効な入力。
コンテキスト依存の入力: ゲーム内の異なるコンテキストに応じて異なる動作をする入力。














カスタムインタラクションの作成方法
カスタムインタラクションを作成するためには、IInputInteractionインターフェースを実装します。以下は、簡単なカスタムインタラクションの例です。

csharp
Copy code
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.Interactions;

public class TripleClickInteraction : IInputInteraction
{
    private float lastClickTime;
    private int clickCount;

    public void Process(ref InputInteractionContext context)
    {
        if (context.control is ButtonControl button && button.wasPressedThisFrame)
        {
            float currentTime = Time.time;

            if (currentTime - lastClickTime < 0.5f)
            {
                clickCount++;
            }
            else
            {
                clickCount = 1;
            }

            lastClickTime = currentTime;

            if (clickCount == 3)
            {
                context.Performed();
                clickCount = 0;
            }
        }
    }

    public void Reset()
    {
        clickCount = 0;
        lastClickTime = 0;
    }
}

#if UNITY_EDITOR
[UnityEditor.InitializeOnLoad]
#endif
public static class TripleClickInteractionEditorRegistration
{
    static TripleClickInteractionEditorRegistration()
    {
        InputSystem.RegisterInteraction<TripleClickInteraction>("TripleClick");
    }
}
カスタムインタラクションの使用方法
作成したカスタムインタラクションを使用するには、インタラクション名を指定して入力アクションに追加します。

csharp
Copy code
var action = new InputAction(binding: "<Mouse>/leftButton", interactions: "TripleClick");
action.performed += ctx => Debug.Log("Triple click detected!");
action.Enable();
まとめ
カスタムインタラクションは、ゲームやアプリケーションの特定のニーズに合わせた入力パターンの検出を実現するための強力なツールです。標準のインタラクションでは対応しきれない複雑な入力条件やシーケンスを扱う場合に非常に有用です。






using UnityEngine.InputSystem;

public class MyButtonInteraction : IInputInteraction
{
#if UNITY_EDITOR
    [UnityEditor.InitializeOnLoadMethod]
#else
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
#endif
    public static void Initialize()
    {
        // 初回にInteractionを登録する必要がある
        InputSystem.RegisterInteraction<MyButtonInteraction>();
    }

    public void Process(ref InputInteractionContext context)
    {
        switch (context.phase)
        {
            case InputActionPhase.Waiting:
                // ボタンが押されたらStarted→Performedフェーズの順に遷移
                if (context.ControlIsActuated(InputSystem.settings.defaultButtonPressPoint))
                {
                    // ボタンが押された時の処理
                    context.Started();
                    context.PerformedAndStayPerformed();
                }

                break;

            case InputActionPhase.Performed:
                // ボタンが離されたらCanceledフェーズに遷移
                if (!context.ControlIsActuated(InputSystem.settings.buttonReleaseThreshold))
                {
                    // ボタンが押された時の処理
                    context.Canceled();
                }

                break;
        }
    }

    public void Reset()
    {
    }
}