
#### **6. Paintable.shadergraph**
- **役割**:
  - ペイント結果を表示するためのシェーダー（Shader Graphで作成）。
  - ペイントマスク、ペイント結果、グリッターやノイズの効果を合成。

- **主な機能**:
  - 視覚的なペイントエフェクト（色、金属感、滑らかさ、エミッション）を表現。
  - 最終的な描画結果として、ゲームオブジェクトの見た目を更新。

- **依存関係**:
  - `Paintable.cs` で割り当てられた `RenderTexture` を元に描画。








# サンプルコード6



Shadergraph

<br>
<br>

インク部分

<img src="images/1_ink.png" width="90%" alt="" title="">

<br>
<br>

最終出力先

<img src="images/2_output.png" width="90%" alt="" title="">

<br>
<br>

キラキラ

<img src="images/3_glitter.png" width="90%" alt="" title="">

<br>
<br>

inkの形をglitterに

<img src="images/4_inkの形をglitterに.png" width="90%" alt="" title="">

<br>
<br>

変数

<img src="images/5_変数.png" width="90%" alt="" title="">

<br>
<br>

基本設定

<img src="images/6_基本設定.png" width="90%" alt="" title="">


<br>
<br>

Paintable_Ink_Normal

<img src="images/Paintable_Ink_Normal.png" width="90%" alt="" title="">


<br>
<br>

Paintable_Ink_BaseColor.

<img src="images/Paintable_Ink_BaseColor.png" width="90%" alt="" title="">


<br>
<br>

Paintable_Ink_Metallic

<img src="images/Paintable_Ink_Metallic.png" width="90%" alt="" title="">


<br>
<br>

Paintable_Ink_Smoothness

<img src="images/Paintable_Ink_Smoothness.png" width="90%" alt="" title="">

<br>
<br>

Paintable_Emmision_Glitter1

<img src="images/Paintable_Emmision_Glitter1.png" width="90%" alt="" title="">


<br>
<br>

Paintable_Emmision_Glitter2

<img src="images/Paintable_Emmision_Glitter2.png" width="90%" alt="" title="">