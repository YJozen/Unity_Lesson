**InputSystem 2**


Input SystemのAxis／Vector系Compositeのモードによる挙動の違い

1D axis – 正負の2ボタンを1軸の入力に合成する
2D vector – 4方向ボタンを2軸のベクトル入力に合成する
3D vector – 6方向ボタンを3軸のベクトル入力に合成する


Input Systemでは、矢印キーやWASDキー、十字キーなどの複数ボタンを一つのスティック入力のように合成して扱うようにする手段をComposite Bindingとして提供しています


また、Composite Bindingの合成元となるBindingは、必ずデジタル入力とは限らず、連続的に変化するアナログ入力である可能性があります。

このような入力値をどのように計算して処理するかの設定が可能です。

設定による挙動
元のBindingの入力値をそのまま加工せずに加減算して使用する
閾値を元に0または1に2値化してから使用する
2値化する際、斜め移動は長さ1になるように正規化する
本記事では、これら3種類のComposite Bindingの使い方および設定による挙動の違いについて解説していきます。



1D axis
正と負の2つのボタンから1軸の入力に合成するComposite Bindingです。




次のBindingを内包します。

Negative – 負方向の入力
Positive – 正方向の入力
また、プロパティでは以下パラメータがあります。

Min Value – 出力値の最小値。Negativeの入力値が最大になった時にこの値になる。
Max Value – 出力値の最大値。Positiveの入力値が最大になった時にこの値になる。
Which Side Wins – NegativeとPositive両方の入力があった時の挙動設定。
Which Side Winsは設定によって次のような挙動になります。




Which Side Wins = Negativeのとき
PositiveとNegative両方の入力があったとき、Negative側の入力が優先されます。この時、Positiveの入力値は0とみなされます。

参考：Enum AxisComposite.WhichSideWins| Input System | 1.5.1

この時、出力値は次のように計算されます。

出力値 = ニュートラル値 – (ニュートラル値 – MinValue）* Negativeの入力値

ニュートラル値 = (MaxValue + MinValue) / 2

この計算式によって、ニュートラル値（中間値）からMinValueまでの間で変化する値が得られます。例えば、Negativeが0の時は出力値がニュートラル値、Negativeが1の時は出力値がMinValueになります。

Negativeの入力値を横軸、出力値を縦軸に取ると次のようなグラフになります。


https://nekojara.city/unity-input-system-axis-vector-composite









