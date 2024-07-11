**InputSystem 2**

# Input Systemでデッドゾーンを設定する

コントローラーの製品の劣化などにより、スティックを離しているのに入力値が０とならない場合があります。（このような現象はドリフトと呼ばれます）

また、製品によっては想定より大きな入力値を返してしまうこともあり得ます。

このような問題は、特定範囲の入力値を補正するデッドゾーンを設けることで解決可能です。

デッドゾーンの補正では、ある閾値より小さい入力値は０にし、ある閾値より大きい入力値は１にするような処理を行います。

Input Systemでもこのようなデッドゾーン機能がサポートされています。

<img src="images/8/8_3/unity-input-system-deadzone-1.png.avif" width="50%" alt="" title="">


## スティックのデッドゾーンを設定する

Input Systemにおけるデッドゾーン指定は、Input ActionのProcessorより行います。



指定できるデッドゾーンには、Axis DeadzoneとStick Deadzoneの２種類が存在します。

それぞれ次のような特徴があります。

+ Axis Deadzone
  - １軸入力の大きさ（絶対値）基準でデッドゾーンを適用する
  - ２軸のスティック入力の場合は、もう一方のStick Deadzoneを推奨
+ Stick Deadzone
  - ２軸入力のベクトルの大きさ（半径）基準でデッドゾーンを適用する
  - スティック入力などに適している


なお、これらのProcessorは、Action単位、Binding単位などで指定できます。本記事では、一般的なBinding単位で指定するものとして手順を説明していきます。


## デッドゾーンのProcessorを追加する

該当するInput Actionファイルを開き、デッドゾーンを適用したいBindingを選択します。

例では、キャラクター移動操作に使う左スティックに適用するものとします。

<img src="images/8/8_3/unity-input-system-deadzone-2.jpg.avif" width="50%" alt="" title="">

<br>

※Stick Deadzoneを適用するためには、該当するBindingが属するActionのAction TypeがValue、Control TypeがVector2かStickになっている必要があります。

<img src="images/8/8_3/unity-input-system-deadzone-3.jpg.avif" width="50%" alt="" title="">

<br>

Bindingを選択した状態で右側に表示されるBinding Properties > Processors右の＋アイコンをクリックし、Stick Deadzoneを選択します。

<img src="images/8/8_3/unity-input-system-deadzone-4.jpg.avif" width="50%" alt="" title="">

<br>

すると、Processors項目にデッドゾーンが適用された状態になります。

<img src="images/8/8_3/unity-input-system-deadzone-5.jpg.avif" width="50%" alt="" title="">

<br>

この状態でSave Assetボタンをクリックすれば設定がInput Actionファイルに保存されます。

<img src="images/8/8_3/unity-input-system-deadzone-6.jpg.avif" width="50%" alt="" title="">

<br>

##  デッドゾーンの範囲を設定する  


Stick Deadzoneには、次の２つの設定パラメータがあります。

+ min
  - ２軸入力の大きさがこの値より小さい場合、零ベクトル(0, 0)を返す
+ max
  - ２軸入力の大きさがこの値より大きい場合、長さ１に正規化されたベクトルを返す

Defaultのチェックを外すことで、デフォルト設定以外の値を個別指定できます。

<img src="images/8/8_3/unity-input-system-deadzone-7.jpg.avif" width="50%" alt="" title="">

項目に0を入力すると、自動的にDefaultにチェックが入る仕様になっています。


入力値と出力値のベクトルの長さは、次のグラフのような関係になります


<img src="images/8/8_3/unity-input-system-deadzone-8.png.avif" width="50%" alt="" title="">

<br>

横軸が入力値、縦軸がデッドゾーンを適用した後の出力値です。

minからmaxまでの入力を0から1に正規化する処理を行っています。範囲外の入力値は0～1の間に丸められます。

## デフォルトの範囲を変更する
デッドゾーンのminとmaxのデフォルト設定は、以下Open Input Settingsボタンから変更できます。


<img src="images/8/8_3/unity-input-system-deadzone-9.jpg.avif" width="50%" alt="" title="">


<br>

ボタンをクリックすると、Project Settingsウィンドウが開かれます。Default Deadzone MinとDefault Deadzone Max項目でデフォルト値を変更できます。

<img src="images/8/8_3/unity-input-system-deadzone-10.jpg.avif" width="50%" alt="" title="">

<br>

上記画面はUnityエディタトップメニューのEdit > Project Settings…からProject Settingsウィンドウを開き、左側のInput System Package項目を選択することでも表示できます。他にも様々なデフォルト値を変更できます。

※デフォルト値の変更はアプリケーション全体の動作に影響を及ぼしますので、十分ご注意ください。

## １軸単位でデッドゾーンを設定する

スティック入力のような２軸入力ではなく、１軸入力に対して適用できるデッドゾーンもあります。

この場合、Axis DeadzoneをProcessorに追加します。Axis Deadzoneを追加するためには、該当するActionのControl TypeがAxisなど１軸の入力値になっている必要があります。

<img src="images/8/8_3/unity-input-system-deadzone-11.jpg.avif" width="50%" alt="" title="">

<br>

Axis Deadzoneの追加もStick Deadzoneと同様、該当すwqqるBindingを選択した状態でProcessor右の＋アイコンから追加してください。

Axis Deadzoneの入力値補正処理も、基本的にStick Deadzoneと一緒です。絶対値に対してminとmaxの間の入力値を0～1の範囲に正規化する処理を行います。

---
### 複数のProcessorが存在する場合は順番に注意

次のように複数のProcessorを追加する場合、追加する順序に注意する必要があります。


<img src="images/8/8_3/unity-input-system-deadzone-12.jpg.avif" width="50%" alt="" title="">

<br>

登録されたProcessorは上から順に実行されていきます。画像の例の場合

+ Invert Vector 2 （入力値反転）
+ Stick Deadzone（デッドゾーン適用）
+ Scale Vector 2（入力値に対して係数を掛ける）

という処理が上から順に実行されますが、例えばStick DeadzoneとScale Vector 2を逆にしてしまうと、係数倍（画像では300倍）された値に対して0～1に入力値を正規化するデッドゾーン処理を適用する挙動になってしまい、期待した結果が得られません。

デッドゾーンに限らず、Processorは上から順に実行されることを意識しておくと良いでしょう。