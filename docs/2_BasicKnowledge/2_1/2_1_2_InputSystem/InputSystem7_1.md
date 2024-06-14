**InputSystem 2**
InteractionとProcessor
# Interactionを使用し、ダブルクリックなどを実装する


https://nekojara.city/unity-input-system-interaction

---
## Interaction


ボタンが押された
入力値が変化した
長押しされた
ダブルタップされた
その他、独自に定義した入力パターン
基本的な入力パターンは幾つかプリセットとして用意されていますが、これらで物足りない場合は自作することも可能です。

InteractionはInput Action内で使用され、Actionまたはその中のBindingに対して1つまたは複数指定することが可能です。

Interactionとは

特定の入力パターンを表現するものです。例えば、HoldというInteractionは「一定時間ボタンが押され続けた」という入力パターンを表します。

![](images/7/7_1//unity-input-system-interaction-1.png.avif "")

## Interactionの基本的な仕組み

![](images/7/7_1//unity-input-system-interaction-2.png.avif "")

各フェーズ遷移時に発生するイベント


## Interactionの適用

![](images/7/7_1//unity-input-system-interaction-3.png.avif "")




![](images/7/7_1//unity-input-system-interaction-4.png.avif "")



# 入力の受取りテスト


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




















