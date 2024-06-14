**InputSystem 2**

https://nekojara.city/unity-input-system-interaction

# Interactionを自作する

プリセットでは物足りない場合、Interactionを自作することも可能です。

---
## 1


ボタンが押された
入力値が変化した
長押しされた
ダブルタップされた
その他、独自に定義した入力パターン
基本的な入力パターンは幾つかプリセットとして用意されていますが、これらで物足りない場合は自作することも可能です。

InteractionはInput Action内で使用され、Actionまたはその中のBindingに対して1つまたは複数指定することが可能です。




```cs:MyButtonInteraction.cs
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

```

上記をMyButtonInteraction.csという名前でUnityプロジェクトに保存すると、Input System側にInteractionとして登録され、使用できるようになります。


```cs:InteractionExample.cs

using UnityEngine;
using UnityEngine.InputSystem;

public class InteractionExample : MonoBehaviour
{
    // 入力を受け取る対象のAction
    [SerializeField] private InputActionReference _actionRef;

    private void Awake()
    {
        // InputActionReferenceのActionに対して、
        // 3つのイベントハンドラを登録する
        _actionRef.action.started += OnAction;
        _actionRef.action.performed += OnAction;
        _actionRef.action.canceled += OnAction;
    }

    private void OnDestroy()
    {
        // 登録したイベントハンドラを解除する
        _actionRef.action.started -= OnAction;
        _actionRef.action.performed -= OnAction;
        _actionRef.action.canceled -= OnAction;
    }

    private void OnEnable()
    {
        _actionRef.action.Enable();
    }

    private void OnDisable()
    {
        _actionRef.action.Disable();
    }

    private void OnAction(InputAction.CallbackContext context)
    {
        // Interactionのフェーズをログに出力する
        print($"OnAction: {context.phase}");
    }
}

```