<style type="text/css">
hr{
	max-width: 300px;
    border: 1px solid #808080;
}
</style> 


**InputSystem 2**
# Input SystemのAxis／Vector系Compositeのモードによる挙動の違い

Input Systemでは、矢印キー・WASDキー・十字キーなどの複数ボタンを一つのスティック入力のように合成して扱えるものが、「Composite Binding」になります 


#### 複数ボタンを合成するComposite Bindingの種類  
+ 1Daxis – 正負の2ボタンを1軸の入力に合成する
+ 2D vector – 4方向ボタンを2軸のベクトル入力に合成する
+ 3D vector – 6方向ボタンを3軸のベクトル入力に合成する


Composite Bindingの合成元となるBindingは、必ずデジタル入力(WASDキー・十字キーなど)とは限らず、連続的に変化するアナログ入力である可能性もあります。  
このような入力値をどのように計算して処理するかの設定が可能です。

#### 設定による挙動
+ 元のBindingの入力値をそのまま加工せずに加減算して使用
+ 閾値を元に0または1のように2値化してから使用
+ 2値化する際、斜め移動は長さ1になるように正規化

<br>

「Composite Bindingの種類」と「設定による挙動」について見ていきます

---
## 1.  1D axis
正と負の2つのボタンから1軸の入力に合成するComposite Binding

<img src="images/9/9_2/unity-input-system-axis-vector-composite-2.png.avif" width="50%" alt="" title="">

<br>

次のBindingを内包します。

+ Negative – 負方向の入力
+ Positive – 正方向の入力

  - プロパティとして以下パラメータがあります。   
     * Min Value   
     – 出力値の最小値。Negativeの入力値が最大になった時にこの値になる。
     * Max Value   
     – 出力値の最大値。Positiveの入力値が最大になった時にこの値になる。
     * Which Side Wins  
      – NegativeとPositive両方の入力があった時の挙動設定。


###  プロパティ　Which Side Winsの設定について
####  ①Which Side Wins = Negativeのとき  
PositiveとNegative両方の入力があったとき、Negative側の入力が優先されます。  
この時、Positiveの入力値は0とみなされます。

```
ニュートラル値 = (MaxValue + MinValue) / 2
出力値 = ニュートラル値 – (ニュートラル値 – MinValue）* Negativeの入力値
```
この計算式によって、ニュートラル値（中間値）からMinValueまでの間で変化する値が得られます。  

例えば、  
Negativeが0の時、出力値はニュートラル値、  
Negativeが1の時、出力値はMinValue  
になります。

Negativeの入力値を横軸、出力値を縦軸に取ると次のようなグラフになります。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-3.png.avif" width="50%" alt="" title="">

<br>

実際の入力と出力結果

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m1.mp4.gif" width="50%" alt="" title="">

<br>

####  ②Which Side Wins = Positiveのとき
PositiveとNegative両方の入力があったとき、Positiveの入力側が優先されます。  
この時、Negativeの入力値は0とみなされます。

出力値の計算式は次の通りです。
```
ニュートラル値 = (MaxValue + MinValue) / 2
出力値 = ニュートラル値 + (MaxValue – ニュートラル値）* Positiveの入力値
```
Positiveの入力値を横軸、出力値を縦軸に取ると次のようなグラフになります。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-4.png.avif" width="50%" alt="" title="">

<br>

実際の入力と出力結果

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m2.mp4.gif" width="50%" alt="" title="">

<br>

#### ③Which Side Wins = Neitherのとき

打ち消しあってニュートラル値が出力されます。

例えば、  
Max Valueが1、Min Valueが-1の時、出力値（ニュートラル値）は
(1–1)/2=0となります。

両方の入力がある間はニュートラル値になっていることが確認できます。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m3.mp4.gif" width="50%" alt="" title="">

<br>

<hr > 

## 2.   2D vector
4つの入力を2軸入力値に合成するComposite Bindingです。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-5.png.avif" width="50%" alt="" title="">

<br>

次の上下左右4方向のボタンのBindingを持ちます。

+ up – 上方向ボタン（y軸正方向）
+ down – 下方向ボタン（y軸負方向）
+ left – 左方向ボタン（x軸負方向）
+ right – 右方向ボタン（x軸正方向）

プロパティはmode1つのみで、上記4方向から2軸値（Vector2）に変換する際の計算方法を設定します。

### ・mode = Analogのとき
x軸およびy軸方向の正負方向の入力値をそのまま加減算するモードです。

次の計算式になります。
```
出力値 = (x, y) = (right – left, up – down)
```
値をそのまま加減算するため、ボタンの入力値が0〜1の範囲とすると次の領域となります。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-6.png.avif" width="50%" alt="" title="">

<br>

出力値が連続的に変化します。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m4.mp4.gif" width="50%" alt="" title="">

<br>

### ・mode = Digitalのとき
4方向の入力をボタン入力値（bool値）に変換してから加減算するモードです。

ボタン入力値が閾値Press Point以上なら1（true）、そうでなければ0（false）という2値化した値です。

斜め方向の補正は行わないため、領域はmodeがAnalogの時と一緒です。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-6.png.avif" width="50%" alt="" title="">

<br>

Analogの時とは異なり、出力値が離散的になっています。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m5.mp4.gif" width="50%" alt="" title="">

<br>

### ・mode = DigitalNormalizedのとき
Digitalと同様に4方向入力をボタン入力値に変換して加減算しますが、斜め方向が長さ1に補正（正規化）されます。

xy軸どちらも0の場合は(0, 0)を出力します。

出力値はダイヤモンド形の範囲になります。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-7.png.avif" width="50%" alt="" title="">

<br>

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m6.mp4.gif" width="50%" alt="" title="">

<br>

<hr > 

## 3.  3D vector
6入力から3軸入力値に合成して出力するComposite Bindingです。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-8.png.avif" width="50%" alt="" title="">

<br>

次のような上下左右前後方向のBindingを持ちます。

+ up – 上方向ボタン（y軸正方向）
+ down – 下方向ボタン（y軸負方向）
+ left – 左方向ボタン（x軸負方向）
+ right – 右方向ボタン（x軸正方向）
+ forward – 前方向ボタン（z軸正方向）
+ back – 後ろ方向ボタン（z軸負方向）

プロパティは2D vector同様「mode」のみです。  
「mode」による挙動は次のようになります。

### ①　mode = Analogのとき
3軸方向それぞれで入力値をそのまま加減算するモード。  
```
出力値 = (x, y, z) = (right – left , up – down , forward – back)
```
各軸方向の入力値をそのまま加減算するため、得られる出力値の範囲が立方体の領域になります。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-9.png.avif" width="50%" alt="" title="">

<br>

2D vectorのmodeがAnalogの時と同様、連続的に値が変化します。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m7.mp4.gif" width="50%" alt="" title="">

<br>

### ②　mode = Digitalのとき
各入力値をボタン入力値に変換してから加減算するモード。

計算方法は2D vector同様、z軸成分が増えた事以外は一緒です。出力領域もAnalogと一緒です。

出力値が離散的になっています。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m8.mp4.gif" width="50%" alt="" title="">

<br>

### ③ mode = DigitalNormalizedのとき
modeがDigitalの時の計算結果に対し、出力値（Vector3）を長さ1に正規化する処理を施します。

正規化する前の結果が(0, 0, 0)の場合はそのまま(0, 0, 0)を出力します。

内部的にはVector3.normalizeプロパティの結果を返しているだけです。


出力される領域は次のような球の内側となります。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-10.png.avif" width="50%" alt="" title="">

<br>

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m9.mp4.gif" width="50%" alt="" title="">

<br>

<hr>

## 2D vectorで円形領域の出力を得たい場合  
2D vectorのAnalogモード時、2軸の連続的な値が得られますが、その領域は正方形です。

例えば、得られる値（Vector2型）の長さが1を超えないようにしたい場合は、この出力値に対して更に補正をかける必要があります。

これはStick DeadzoneというProcessorを追加すれば解決できます。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-11.png.avif" width="50%" alt="" title="">

<br>

Stick Deadzoneはデッドゾーンを設定するProcessorですが、最大値を超えないように値を丸める（Clampする）処理も行っています。

出力される領域は以下円形です。

<img src="images/9/9_2/unity-input-system-axis-vector-composite-12.png.avif" width="50%" alt="" title="">

<br>

<img src="images/9/9_2/unity-input-system-axis-vector-composite-m10.mp4.gif" width="50%" alt="" title="">

<br>


