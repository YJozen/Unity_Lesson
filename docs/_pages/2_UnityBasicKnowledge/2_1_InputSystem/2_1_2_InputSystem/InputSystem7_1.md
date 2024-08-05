# Interactionを使用し、少し複雑な入力を実装する

---
## 1.Interaction概要

InteractionはInput Action内で使用され、Actionまたはその中のBindingに対して1つまたは複数指定することが可能です。　  
基本的な入力パターンは幾つかプリセットとして用意されていますが、これらで物足りない場合は自作することも可能です。

## 2.Interactionとは

特定の入力パターンを表現するものです。  
例えば、HoldというInteractionは「一定時間ボタンが押され続けた」という入力パターンを表します。

<img src="images/7/7_1//unity-input-system-interaction-1.png.avif" width="80%" alt="" title="">




## 3.Interactionの基本的な仕組み

内部的には、次のステートマシンとして管理されます。


<img src="images/7/7_1//unity-input-system-interaction-2.png.avif" width="80%" alt="" title="">

Interactionでは、この状態はフェーズと呼ばれています。次の5つのフェーズがあります。

+ Waiting – 入力待ち状態
+ Started – Interactionが開始された状態
+ Performed – Interactionが期待する入力を満たした状態
+ Canceled – Interactionがキャンセルされた状態
+ Disabled – Actionが無効な状態  

このうち、Interactionが直接扱うのはDisabled以外の4フェーズです。
また、Performedフェーズに限り、同じPerformedフェーズに遷移することも出来ます。


## 4.各フェーズ遷移時に発生するイベント
Interaction内でステートマシンとして管理される各フェーズ間で遷移する時、次のイベントが発生します。

+ started – 入力され始めた時などに呼ばれる
+ performed – 特定の入力があった時などに呼ばれる
+ canceled – 入力が中断された時などに呼ばれる  

基本的に、Started、Performed、Canceledフェーズに遷移する時に上記イベントがコールバックとして通知されます。  
PerformedフェーズからPerformedフェーズへの遷移でもperformedコールバックは通知されます。  
また、Waiting、Disabledフェーズへの遷移ではイベントは発火しません。



## 5.Interactionの適用
Interactionは、各BindingまたはAction単位で1つ以上指定できます。

<img src="images/7/7_1//unity-input-system-interaction-3.png.avif" width="80%" alt="" title="">



<img src="images/7/7_1//unity-input-system-interaction-4.png.avif" width="80%" alt="" title="">


Actionに直接Interactionを指定した場合は、その下のBindingすべてにInteractionが指定されたのと同じことになります。

Interactionが未指定の場合は、Default Interactionが暗黙的に指定されます。

# 6.入力の受取りテスト

指定したActionのコールバックをログ出力する例になります

InteractionExample.cs
```cs

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
            _actionRef.action.started   += OnAction;
            _actionRef.action.performed += OnAction;
            _actionRef.action.canceled  += OnAction;
        }

        private void OnDestroy()
        {
            // 登録したイベントハンドラを解除する
            _actionRef.action.started 　-= OnAction;
            _actionRef.action.performed -= OnAction;
            _actionRef.action.canceled  -= OnAction;
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
上記をInteractionExample.csという名前でUnityプロジェクトに保存し、適当なゲームオブジェクトにアタッチし、インスペクターよりInteractionが適用されたActionを指定してください。

<img src="images/7/7_1//unity-input-system-interaction-8.png.avif" width="80%" alt="" title="">



Hold Interactionが指定された場合、対象ボタンを一定時間押し込むとPerformedフェーズに遷移してログ出力されます。

一定時間に満たないうちにボタンを離すと、Performedフェーズに遷移しません。


## 7.ReadValueで入力値を取得する場合

```cs

InputAction action;// 独自のInteractionが設定されたAction

・・・（中略）・・・

private void Update()
{
    // フェーズがWaitingのままだと常に0を返す
    var value = action.ReadValue<float>();
}

```

Updateイベント等でReadValueメソッドを通じて入力値を取得する場合、Waitingフェーズでは入力値が常に0。

プリセットとして提供されているInteractionは、いずれも入力があった時にStartedフェーズに遷移するため、ReadValueメソッドから入力値を取得できます。  
ただし、自作のInteractionを用いる場合、入力があってもStartedフェーズに遷移しない実装になっているとReadValueが返す値はいつまでも0のままなので注意


## 8.Default Interactionの挙動

Interactionが指定されていないBindingには、暗黙的にDefault Interactionが指定されます。

Default Interactionの挙動は、Action PropertiesのAction項目から設定

基本的な挙動はAction Typeの設定によって決まります。

<img src="images/7/7_1/unity-input-system-interaction-9.png.avif" width="80%" alt="" title="">

+ Value  
入力値が変化したときにフェーズ遷移。  
0から0以外に変化したときはStarted → Performedの順に遷移。   
0以外から別の0以外の値に変化したときはPerformedからPerformedに遷移。  
0以外から0に変化したときはCanceledに遷移。  

+ Button  
入力値が0から0以外に変化したときにはStartedに遷移。  
Press Point以上に変化したときにPerformedに遷移。  
PerformedフェーズでRelease Point未満に値が変化するとCanceledに遷移。

+ Pass Through  
デバイスからの入力がある度に常にPerformedに遷移。

## 9.Interactionのプリセット一覧

### Press
ボタンの押した瞬間、離した瞬間、またはその両方を検知（performedコールバックを通知）するInteraction


<img src="images/7/7_1/unity-input-system-interaction-10.png.avif" width="70%" alt="" title="">


どの瞬間を検知するかは、Trigger Behaviour項目から設定できます。設定内容は次の通りです。

+ Press Only – 押した瞬間  
+ Release Only – 離した瞬間  
+ Press And Release – 押した瞬間と離した瞬間両方

<br>
<br>

### Hold

一定時間ボタンが押されたことを検知するInteractionです。

<img src="images/7/7_1/unity-input-system-interaction-11.png.avif" width="70%" alt="" title="">



Hold Timeに指定された時間（秒）以上押され続けたらPerformedフェーズに遷移し、performedコールバックが通知される。

ボタンを押してからHold Time秒経過する前にボタンを離すと、Performedフェーズに遷移せずにCanceledフェーズに遷移。  
Hold Time秒経過すると、その瞬間にPerformedフェーズに遷移。

<br>
<br>

### Tap

一定時間以内にボタンを押して離したことを検知するInteraction。

<img src="images/7/7_1/unity-input-system-interaction-12.png.avif" width="70%" alt="" title="">



Max Tap Durationに指定した時間（秒）以内にボタンを押して離すと、離した瞬間にPerformedフェーズに遷移してperformedコールバックが通知される。

逆に、ボタンを押してからMax Tap Duration秒以上押され続けたらCanceledフェーズに遷移してcanceledコールバックが通知される。


<br>
<br>

### SlowTap

ボタンが押されてから一定時間以上経過して離されたことを検知するInteractionです。ゆっくりとタップされたかどうかを判定するのに使います。


<img src="images/7/7_1/unity-input-system-interaction-13.png.avif" width="70%" alt="" title="">



Min Tap Duration秒以上ボタンが押され続けるとPerformedフェーズに遷移。

その前にボタンが離されるとCanceledフェーズに遷移。

<br>
<br>

### MultiTap

ある時間内に指定回数タップされたことを検知するInteraction。  
ダブルクリックやダブルタップなどを判定する場合に使います。


<img src="images/7/7_1/unity-input-system-interaction-14.png.avif" width="70%" alt="" title="">



Tap Countには、必要なタップ回数を指定。ダブルタップなら2、トリプルタップなら3という値を指定。
  
Max Tap Spacingには、ボタンが離されてから次のボタンが押されるまでの最大許容時間（秒）を指定。この時間を超えてボタンが離されたままだとキャンセル扱いになる。
  
Max Tap Durationには、ボタンが押されてから離されるまでの最大許容時間（秒）を指定。ボタンが押されてからこの時間を超えるとキャンセル扱いになります。

