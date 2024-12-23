# Time.deltaTimeについて

<br>

## `transform.Translate`

- **`transform`**: これは、スクリプトがアタッチされているGameObjectのTransformコンポーネントを指します。Transformコンポーネントは、オブジェクトの位置、回転、スケールを管理するためのもので、3D空間でのオブジェクトの状態を制御します。

- **`Translate`**: これは、Transformコンポーネントのメソッドで、指定された方向にオブジェクトを移動させます。このメソッドは、オブジェクトの現在の位置を基準にして、移動させたい方向と距離を指定します。

### 引数の説明

#### `moveDirection * speed * Time.deltaTime`

1. **`moveDirection`**: 
   - これは、プレイヤーの移動方向を示すベクトルです。具体的には、`transform.forward` に基づいて計算されたもので、プレイヤーが向いている方向です。
   - このベクトルの大きさ（長さ）は、プレイヤーがどれだけの速度で進むかに影響します。

2. **`speed`**: 
   - プレイヤーの移動速度を示す浮動小数点数です。この値により、移動の速さが調整されます。
   - 例えば、`speed` が 5 の場合、プレイヤーは 1秒間に5ユニットの距離を移動します。

3. **`Time.deltaTime`**: 
   - フレームごとの経過時間を表す値です。これにより、異なるフレームレートでも移動速度が一定になります。
   - `Time.deltaTime` を掛けることで、移動がフレームレートに依存しないようにします。これにより、スムーズな動きが実現されます。

#### 例

- 例えば、`moveDirection` が (0, 0, 1) で、`speed` が 5 の場合、`moveDirection * speed` は (0, 0, 5) になります。
- これに `Time.deltaTime` を掛けることで、例えば1フレームの時間が0.016秒（約60FPSの場合）なら、最終的に (0, 0, 0.08) というベクトルが得られます。この値が`Translate`メソッドに渡され、プレイヤーはフレーム毎に約0.08ユニット前方に移動します。


# **課題**：

```
    Time.deltaTimeは、Update()とUpdate()の間の時間になります。  
    マイフレーム、値が異なります。  
    話は変わって問題です。
    「１秒で10m進みたいなら、Δt秒で何m進めばいいでしょうか？」
```
