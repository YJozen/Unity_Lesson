
# 1. **Animationの基本的な使い方**

Unityでのアニメーションは、`Animator`コンポーネントを使って制御されます。  
通常、次のような手順で設定します。

## ステップ：
1. **Animatorコンポーネントの追加**  
   キャラクターやオブジェクトに`Animator`コンポーネントを追加。
   
2. **AnimationClipの作成**  
   事前に作成したAnimationClip（歩く、走る、ジャンプするなど）を使って、キャラクターに動きを設定。

3. **AnimatorControllerの作成**  
   AnimationClipを管理するための`AnimatorController`を作成し、各アニメーションを遷移させるためのブレンドや条件を設定。

## サンプルプログラム：
```csharp
using UnityEngine;

public class CharacterAnimation : MonoBehaviour
{
    private Animator animator;

    void Start()
    {
        // Animatorコンポーネントを取得
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        // Wキーで走るアニメーションを再生
        if (Input.GetKey(KeyCode.W))
        {
            animator.SetBool("isRunning", true);
        }
        else
        {
            animator.SetBool("isRunning", false);
        }
    }
}
```

このスクリプトでは、`W`キーを押すと「走る」アニメーションが再生され、離すと停止します。

<br>

---

<br>

# 2. **StateMachine（デザインパターン）としての使い方**

`Animator`は、状態遷移（StateMachine）を管理するための機能としても利用できます。StateMachineは、オブジェクトやキャラクターの状態を管理し、その状態に応じて異なるアニメーションを再生します。

## ステップ：
1. **AnimatorControllerを作成し、ステートを設定**
   各ステートにはアニメーションを割り当て、ステート間の遷移を条件に基づいて制御。
   
2. **遷移条件の設定**
   パラメータ（例えば`isRunning`や`isJumping`）を使って、アニメーションの切り替えを行います。

## サンプルプログラム：
```csharp
using UnityEngine;

public class StateMachineExample : MonoBehaviour
{
    private Animator animator;

    void Start()
    {
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        // 各入力に応じてステートを切り替え
        if (Input.GetKey(KeyCode.W))
        {
            animator.SetTrigger("Walk");
        }
        else if (Input.GetKey(KeyCode.Space))
        {
            animator.SetTrigger("Jump");
        }
    }
}
```

ここでは、`W`キーで「歩き」ステートに遷移し、`Space`キーで「ジャンプ」ステートに遷移する例です。`AnimatorController`上でこれらのトリガーに対応する遷移を設定します。

<br>

---

<br>

# 3. **Avatar Maskの使い方**

`Avatar Mask`は、特定のボーンや体の部分にのみアニメーションを適用するために使われます。例えば、下半身は歩きのアニメーションを再生しつつ、上半身で射撃モーションを再生する場合に使用します。

## ステップ：
1. **Avatar Maskの作成**  
   Unityエディタで`Avatar Mask`を作成し、アニメーションを適用したいボーンを選択。
   
2. **レイヤーを分けて適用**  
   `AnimatorController`でレイヤーを作成し、マスクを適用して特定の部分にのみアニメーションを適用します。

## サンプルプログラム：
```csharp
// AnimatorControllerで設定したレイヤーごとにアニメーションを分ける例
```

<br>

---

<br>

# 4. **Ragdollの設定やプログラムから有効にする方法**

`Ragdoll`は、物理的にキャラクターが倒れたり、衝突した際に自然な動きをシミュレートするための物理設定です。Unityでは、`Ragdoll Wizard`を使って簡単に設定できます。

## ステップ：
1. **Ragdoll Wizardを使って設定**  
   キャラクターに対して、必要なボーンやコライダーを設定します。

2. **Ragdollの有効化**  
   スクリプトで物理アニメーションを切り替える際には、アニメーションを無効にしてRigidbodyの物理挙動を有効にします。

## サンプルプログラム：
```csharp
using UnityEngine;

public class RagdollController : MonoBehaviour
{
    private Animator animator;
    private Rigidbody[] rigidbodies;

    void Start()
    {
        animator = GetComponent<Animator>();
        rigidbodies = GetComponentsInChildren<Rigidbody>();

        // Ragdollを無効にする
        SetRagdollActive(false);
    }

    // Ragdollの有効化/無効化
    public void SetRagdollActive(bool active)
    {
        foreach (var rb in rigidbodies)
        {
            rb.isKinematic = !active;
        }
        animator.enabled = !active;
    }

    void Update()
    {
        // スペースキーを押すとRagdollモードになる
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SetRagdollActive(true);
        }
    }
}
```

このスクリプトでは、スペースキーを押すとRagdollが有効になります。

<br>

---

<br>

# 5. **Animationから関数呼び出し**

アニメーションの特定のフレームで関数を呼び出したい場合、`Animation Event`を使用します。アニメーションの再生中にタイミングを合わせてスクリプト内の関数を実行できます。

## ステップ：
1. **アニメーションウィンドウでイベントを追加**  
   Unityのアニメーションウィンドウで特定のフレームにイベントを設定します。
   
2. **スクリプト内の関数を呼び出す**

## サンプルプログラム：
```csharp
using UnityEngine;

public class AnimationEventExample : MonoBehaviour
{
    // アニメーションイベントから呼び出される関数
    public void OnAttack()
    {
        Debug.Log("Attack event triggered!");
    }
}
```

このスクリプトでは、アニメーション中のイベントで`OnAttack()`という関数が呼ばれます。Unityエディタのアニメーションタイムラインで設定するだけで、指定したフレームに合わせて実行できます。

<br>

---

<br>

# 6. **その他Animationの使い方（例：攻撃時に移動を含める）**

攻撃アニメーションの間にキャラクターを移動させたり、他の処理を追加することがよくあります。これには、アニメーション中に`Root Motion`や物理演算を使った移動を組み合わせることができます。

## サンプルプログラム：
```csharp
using UnityEngine;

public class AttackAnimationController : MonoBehaviour
{
    private Animator animator;
    private CharacterController characterController;

    public float attackMoveSpeed = 2.0f;

    void Start()
    {
        animator = GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();
    }

    void Update()
    {
        // 攻撃中に前進する
        if (animator.GetCurrentAnimatorStateInfo(0).IsName("Attack"))
        {
            characterController.Move(transform.forward * attackMoveSpeed * Time.deltaTime);
        }
    }
}
```

このスクリプトは、攻撃アニメーション中にキャラクターが前進する動きを追加します。`CharacterController`を使用して、アニメーションの進行とともに物理的な移動を実行しています。

<br>

---

<br>

