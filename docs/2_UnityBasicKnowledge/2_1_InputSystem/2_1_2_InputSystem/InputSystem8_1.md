# Input SystemのProcessorで入力値を加工する

## Processorの使用方法
+ 値を反転する
+ 値に対してスケールを掛ける（感度を調整する）
+ デッドゾーンを設ける
+ 自作の加工処理を施す

## Processorの種類一覧
入力値を加工するための機能Processorには、予め次のような種類が用意されています。(これらのProcessorでは物足りない場合、Processorを自作することも可能です。)

+ Clamp
+ Invert
+ Normalize
+ Normalize Vector 2
+ Normalize Vector 3
+ Scale
+ Scale Vector 2
+ Scale Vector 3
+ Axis Deadzone
+ Stick Deadzone


例えば、ScaleというProcessorは、入力値に係数を掛ける加工を行います。

<img src="images/8/8_1/unity-input-system-processor-1.png.avif" width="80%" alt="" title="">


Processorが受け取れる入力値の型は決まっています。  
入力値に対して適用するProcessorは、入力値の型（Control Type）とProcessorが要求する型（Operand Type）が一致している必要があります。

例えば、２軸入力を処理するProcessorであるScale Vector 2は、Operand TypeがVector2型であるため、ボタンのような１軸入力（Control Typeがfloat）を処理することが出来ません。


<img src="images/8/8_1/unity-input-system-processor-2.png.avif" width="80%" alt="" title="">



また、Processorは一つのActionまたはBindingに対して複数適用することが可能です。  
複数適用した場合、Processorの登録順に処理が実行され、バケツリレー方式で順番に値が渡されていきます。

<img src="images/8/8_1/unity-input-system-processor-3.png.avif" width="80%" alt="" title="">


## Processorの設定手順
予め作成したInput Actionアセットファイルをダブルクリックし、ウィンドウを開きます。そして、Processorを適用したいActionまたはBindingをクリックで選択しておきます。

すると、右側に表示されるAction Properties下にProcessorsの設定項目が表示されます。

<img src="images/8/8_1/unity-input-system-processor-4.png.avif" width="80%" alt="" title="">


Processorの追加は、Processors右の＋アイコンから行います。一覧には、Control Typeに適合したProcessorのみが表示されます。

<img src="images/8/8_1/unity-input-system-processor-5.png.avif" width="80%" alt="" title="">



例では、スティック入力を反転するためのInvert Vector 2のProcessorを追加しています。

<img src="images/8/8_1/unity-input-system-processor-6.png.avif" width="80%" alt="" title="">



Save Assetボタンをクリックすると、Input Actionアセット内に設定内容が保存されます。
<img src="images/8/8_1/unity-input-system-processor-7.png.avif" width="80%" alt="" title="">



## Processorの一覧
Input Systemには値を反転させたり、スケールを掛けたりといったProcessorが予め用意されています。

### Clamp
値を指定された範囲に丸めるProcessorの一種です。  
値を下限（Min）から上限（Max）の間に丸めます。

<img src="images/8/8_1/unity-input-system-processor-8.png.avif" width="80%" alt="" title="">


### Invert
入力値の符号を反転するProcessorです。float型のほか、Vector2、Vector3に対応したものも存在します。  

float版には設定項目がなく、Processorを追加するだけで反転処理が適用されます。

<img src="images/8/8_1/unity-input-system-processor-9.png.avif" width="80%" alt="" title="">

Vector2とVector3については、ベクトルの各要素に対して反転の有無を指定できます。

<img src="images/8/8_1/unity-input-system-processor-10.png.avif" width="80%" alt="" title="">
<img src="images/8/8_1/unity-input-system-processor-11.png.avif" width="80%" alt="" title="">


### Normalize
入力値を指定された範囲に正規化するProcessorです。

入力値がfloat、Vector2、Vector3の三種類のバリエーションが存在します

#### ・ floatの場合

<img src="images/8/8_1/unity-input-system-processor-12.png.avif" width="80%" alt="" title="">

下限（Min）を0、上限（Max）を1として、その間で値を正規化します。

Zeroはニュートラルの値を示すもので、ZeroがMin以下の場合は0～1の範囲で正規化、ZeroがMinより大きい場合は-1～1の範囲で正規化されます。

例えば、  
Minが0、Maxが5、Zeroが0、入力値が1の場合、出力値は0.2になります。  
Minが-10、Maxが10、Zeroが0、入力値が-5の場合、出力値は-0.5となります。



#### ・ Vector2、Vector3の場合
float版とは違い、入力値のベクトルを長さ１に正規化する処理を行います。内部的には、Vector2.normalized、Vector3.normalizedの値をリターンしているだけです。

設定するパラメータは特にありません。

<img src="images/8/8_1/unity-input-system-processor-13.png.avif" width="80%" alt="" title="">

<img src="images/8/8_1/unity-input-system-processor-14.png.avif" width="80%" alt="" title="">



### Scale
入力値に対して係数を掛けるProcessorです。  
float、Vector2、Vector3型に対応したものが存在します。  
Vector2、Vector3型に関しては、それぞれの要素毎に個別の係数を指定できます。  
Scale系のProcessorは、一部のデバイスの入力感度を個別に変えたい場合などに重宝します。

<img src="images/8/8_1/unity-input-system-processor-15.png.avif" width="80%" alt="" title="">
<img src="images/8/8_1/unity-input-system-processor-16.png.avif" width="80%" alt="" title="">
<img src="images/8/8_1/unity-input-system-processor-17.png.avif" width="80%" alt="" title="">



### Axis deadzone、Stick deadzone
ゲームパッドのジョイスティックの中には、ニュートラル位置にあるにもかかわらず0以外の入力が得られてしまう（ドリフトが発生する）ことがあります。

この問題は、センサの取り得る値の範囲を決めて、ソフトウェア的に遊びを設けることで解消できます。

1軸入力版のAxis deadzone、  
2軸入力版のStick deadzoneがあります。  
(Operand TypeはAxis deadzoneがfloat、  
Stick deadzoneがVector2です。)

<img src="images/8/8_1/unity-input-system-processor-18.png.avif" width="80%" alt="" title="">
<img src="images/8/8_1/unity-input-system-processor-19.png.avif" width="80%" alt="" title="">

