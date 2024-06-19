**InputSystem 2**
InteractionとProcessor
# Interactionを使用し、長押しやダブルクリックなどを実装する(ひとまずInteractionを触ってみる)

## 1.Interactionで元から用意されている挙動


+ Press     – ボタンを押した瞬間、離した瞬間、またはその両方  
+ Hold      – 一定時間以上ボタンが押し込まれたら  
+ Tap       – 素早くボタンを押して離した瞬間  
+ Slow Tap  – ゆっくりとボタンを押して離した瞬間
+ Multi Tap – 指定回数タップした瞬間



ボタンの長押しやタップ、マルチタップなどの操作入力を取得したい場合、旧Inputでは判定ロジックを自前実装したりアセットを使うなどで対応する必要がありました。

Input Systemでは、Interactionとしてこのような入力パターンを検知し、コールバックとして通知する機能を備えています。

このような「特定パターンの入力があったかどうかの判定」は、コールバック経由で入力を受け取ることにより、受け取り側はこのような処理を意識しなくてよくなります。

例えば、ボタンを押した瞬間から長押しされた瞬間に変更したい場合でも、長押しのInteraction（Hold Interaction）をActionに追加するだけでよくなります。



---
## 2. Input Systemで長押しを実現する

結論を述べると、Hold InteractionというInteractionの一種を使えば実現できます。


Hold Interactionは、一定時間以上入力があったら操作を受け付けるInteractionです。


長押しと判定された瞬間にperformedコールバックが発火されます。


対象となるActionが含まれているInput Action Assetファイルをダブルクリックで開き、対象のActionを選択（今回はLongPressというActionに設定していく）
![](images/7/7_0/unity-input-system-hold-1.png "")



ウィンドウ右のAction Properties > Interactions右の＋アイコン > Holdを選択



すると、以下のようにHold Interactionが適用された状態になります。
![](images/7/7_0/unity-input-system-hold-2.png.avif "")


+ Press Point  
入力あり判定となる閾値。この値より大きな入力値が入力されていると入力ありと判定される。  
+ Hold Time  
長押し判定されるまでの時間（秒）。この時間以上の入力があると「長押し」判定となる。


GetHoldExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチ

```cs:GetHoldExample.cs

    using UnityEngine;
    using UnityEngine.InputSystem;

    public class GetHoldExample : MonoBehaviour
    {
        // 入力を受け取る対象のAction
        [SerializeField] private InputActionReference _hold;

        private void Awake()
        {
            if (_hold == null) return;
            
            // performedコールバックのみを受け取る
            // 長押し判定になったらこのコールバックが呼ばれる
            _hold.action.performed += OnHold;
            
            // 入力を受け取るためには必ず有効化する必要がある
            _hold.action.Enable();
        }

        // 長押しされたときに呼ばれるメソッド
        private void OnHold(InputAction.CallbackContext context)
        {
            Debug.Log("長押しされた！");
        }
    }

```

インスペクターの項目に長押しActionを指定すると機能します。![](images/7/7_0/unity-input-system-hold-2_2.png "")



入力値の大きさが閾値Press Point以上の状態がHold Time秒以上続いたらperformedコールバックを実行します。



入力値の大きさは、入力型によって例えば以下のように計算されます。

・ボタン入力、1軸アナログ入力（float型）  
入力値の絶対値。

・2軸アナログ入力（Vector2型）   
入力（ベクトル）の大きさ。Vector2.magnitude。


内部的には次のような状態遷移を行うステートマシンとして管理されています。

![](images/7/7_0/unity-input-system-hold-3.png.avif "")








---
## 3.長押し中の状況把握

長押しの応用例として、長押し中にゲージを表示したい場合を考えます

下記スクリプトをHoldProgressExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりActionを設定する


ボタンを離すと進捗率は0%になり、ボタンを押し続けると進捗が上がり、長押し判定になった後はボタンを離すまで100%になります。
```cs:HoldProgressExample.cs

    using UnityEngine;
    using UnityEngine.InputSystem;

    public class HoldProgressExample : MonoBehaviour
    {
        // 入力を受け取る対象のAction
        [SerializeField] private InputActionReference _hold;

        private InputAction _holdAction;
        
        private void Awake()
        {
            if (_hold == null) return;
            _holdAction = _hold.action;      
            _holdAction.Enable();// 入力を受け取るためには必ず有効化
        }

        private void Update()
        {
            if (_holdAction == null) return;
            
            // 長押しの進捗を取得
            var progress = _holdAction.GetTimeoutCompletionPercentage();

            // 進捗をログ出力
            Debug.Log($"Progress : {progress * 100}%");
        }
    }


```






---
## 4.ゲージUIに反映する


```cs:HoldGauge.cs

    using UnityEngine;
    using UnityEngine.InputSystem;
    using UnityEngine.UI;

    internal class HoldGauge : MonoBehaviour
    {
        // 入力を受け取る対象のAction
        [SerializeField] private InputActionReference _hold;
        
        // ゲージのUI
        [SerializeField] private Image _gaugeImage;

        private InputAction _holdAction;
        
        private void Awake()
        {
            if (_hold == null) return;

            _holdAction = _hold.action;
            
            // 入力を受け取るためには必ず有効化する必要がある
            _holdAction.Enable();
        }

        private void Update()
        {
            if (_holdAction == null) return;
            
            // 長押しの進捗を取得
            var progress = _holdAction.GetTimeoutCompletionPercentage();

            // 進捗をゲージに反映
            _gaugeImage.fillAmount = progress;
        }
    }

```

上記をHoldGauge.csとしてUnityプロジェクトに保存し、ゲームオブジェクトにアタッチし、インスペクターより必要な参照を指定してください。

また、ゲージとして使用するImage側のImage TypeをFilledに設定しておく必要があります。

![](images/7/7_0/unity-input-system-hold-4.png.avif "")




ボタンを押すと徐々にゲージが増えていくことが確認できるかと思います

