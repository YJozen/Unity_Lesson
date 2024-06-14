**InputSystem 2**
InteractionとProcessor
# Interactionを使用し、長押しやダブルクリックなどを実装する


【Unity】Input Systemでボタンの押した瞬間／離した瞬間を判定する

https://nekojara.city/unity-input-system-get-down-up

Press Interactionで判定する
Press Interactionの適用
Player Inputの準備
タイミングを検知するスクリプトの実装
コールバックの登録
実行結果
Updateイベントでチェックする
Input Action経由で判定する
サンプルスクリプト
実行結果
スクリプトの説明
低レベルAPIから参照する
サンプルスクリプト
スクリプトの説明
使用上の注意点


https://nekojara.city/unity-input-system-action-callback










Interactionが設定されているときの挙動
InteractionsがPressの場合
InteractionsがHoldの場合
InteractionsがTapの場合
InteractionsがSlow Tapの場合
InteractionsがMulti Tapの場合
複数のInteractions指定された場合
呼び元のInteractionの判別



# ひとまずInteractionを触ってみる

## 1.Interaction  


+ Press     – ボタンの押した瞬間、離した瞬間、またはその両方を通知する  
+ Hold      – 一定時間以上ボタンが押し込まれたら通知する  
+ Tap       – 素早くボタンを押して離した瞬間に通知する  
+ Slow Tap  – ゆっくりとボタンを押して離した瞬間に通知する  
+ Multi Tap – 指定回数タップした瞬間に通知する  



ボタンの長押しやタップ、マルチタップなどの操作入力を取得したい場合、旧Inputでは判定ロジックを自前実装したりアセットを使うなどで対応する必要がありました。

Input Systemでは、Interactionとしてこのような入力パターンを検知し、コールバックとして通知する機能を備えています。

このような「特定パターンの入力があったかどうかの判定」は、コールバック経由で入力を受け取ることにより、受け取り側はこのような処理を意識しなくてよくなります。

例えば、ボタンを押した瞬間から長押しされた瞬間に変更したい場合でも、長押しのInteraction（Hold Interaction）をActionに追加するだけでよくなります。



---
## 2. Input Systemで長押しを実現する

結論を述べると、Hold InteractionというInteractionの一種を使えば実現できます。


Hold Interactionは、一定時間以上入力があったら操作を受け付けるInteractionです。


長押しと判定された瞬間にperformedコールバックが発火されます。


対象となるActionが含まれているInput Action Assetファイル（拡張子が.inputactionsのファイル）をダブルクリックで開き、対象のActionを選択
![](images/7/7_0/unity-input-system-hold-1.png.avif "")



ウィンドウ右のAction Properties > Interaction右の＋アイコン > Holdを選択



すると、以下のようにHold Interactionが適用された状態になります。
![](images/7/7_0/unity-input-system-hold-2.png.avif "")


Press Point  
入力あり判定となる閾値。この値より大きな入力値が入力されていると入力ありと判定される。デフォルトではInput Systemパッケージの設定内容が反映される。  
Hold Time  
長押し判定されるまでの時間（秒）。この時間以上の入力があると「長押し」判定となる。デフォルトではInput Systemパッケージの設定内容が反映される。


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


GetHoldExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターの項目に長押しActionを指定すると機能します。



入力値の大きさが閾値Press Point以上の状態がHold Time秒以上続いたらperformedコールバックを実行します。



入力値の大きさは、入力型によって例えば以下のように計算されます。

ボタン入力、1軸アナログ入力（float型） – 入力値の絶対値。
2軸アナログ入力（Vector2型） – 入力（ベクトル）の大きさ。Vector2.magnitudeとなる。
内部的には次のような状態遷移を行うステートマシンとして管理されています。

![](images/7/7_0/unity-input-system-hold-3.png.avif "")








---
## 3.

長押しの応用例として、次のように長押し中にゲージを表示したい場合を考えます


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


上記をHoldProgressExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりActionを設定する



ボタンを離すと進捗率は0%になり、ボタンを押し続けると進捗が上がり、長押し判定になった後はボタンを離すまで100%になります。



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

