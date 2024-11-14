# 1. **Material Preset と TMP の関係**

**Material Preset** は、TextMeshPro (TMP) におけるテキスト描画の **スタイル設定** を管理しますが、**TextMeshPro自身の設定**といった役割も持っています。具体的に言うと、**Material Preset** では、テキストの外観（色、アウトライン、グラデーション、影など）を定義するために使用されますが、**TMPの他の要素（例えば、フォントサイズや行間など）は、`TextMeshPro` コンポーネント内で設定**されます。

- **色の管理**、**フォントの設定**（フォントアセット、グリフなど）、**文字の大きさの管理** は、主に **TMPコンポーネント** や **FontAsset** によって行われます。
- **Material Preset** は、そのテキストの「見た目」に関わる部分（例えば、文字のエフェクトやシェーダーによる処理、アウトライン、グラデーションなど）を定義するものです。

したがって、Material Presetは「見た目」のスタイルに特化した設定であり、**フォントサイズや行間などのテキスト内容の設定**は **TMPコンポーネント内** で行うものです。


<br>

# 2. **Material Preset と MeshRenderer に同じ Material が設定されている理由**

TextMeshProの動作において、**`Material Preset`** も **`MeshRenderer`** も **同じマテリアル** を設定しているのは、**一貫したテキストの描画設定**を提供するためです。

具体的な流れは以下のようになります：

- **Material Preset** は、**テキストの見た目を定義する設定**（色、エフェクト、グラデーションなど）を持っており、これをベースに **`Material`** を生成します。
- この生成された **`Material`** を、**`MeshRenderer`** のマテリアルとしてセットすることで、実際に描画時にそのスタイルが反映される仕組みです。

したがって、**Material Preset はスタイルのテンプレートとして機能し、それに基づいて生成された Material が最終的に描画に使用される** という流れになります。

<br>

### 3. **Material Preset は MeshRenderer 原則同じ Material に設定**



- **`Material Preset`** は、**TMPのスタイルを定義するためのテンプレート**であり、ここで定義された設定を基に **実際の `Material`** が作成されます。
- この生成された **`Material`** を **`MeshRenderer`** に設定して、最終的に描画が行われます。

**Material Preset** と **MeshRenderer の `Material`** は **同じマテリアル** を参照しているだけであり、重複するものではありません。`Material Preset` によって定義されたスタイルが、`MeshRenderer` に渡される `Material` に反映されるだけなので、この流れに問題はありません。

