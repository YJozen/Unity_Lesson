`Classifier.cs` は、UnityプロジェクトでWebカメラから取得した画像データを用いて画像分類を行うためのスクリプトです。このスクリプトは、事前にトレーニングされたニューラルネットワークモデルを使用して画像を分類し、結果を返します。

ここでは、`Classifier.cs` 内で使用される各クラス、メソッド、処理の流れについて詳しく説明します。

---

# 1. `Classifier` クラスの概要

- `Classifier` クラスは、Webカメラ画像の分類を実行するためのクラスです。
- 画像分類に必要なモデルとラベルデータをロードし、入力画像に対して推論を行い、結果を返します。

<br>

# 2. メンバ変数

```csharp
public const int IMAGE_SIZE = 224;           // モデルに入力する画像のサイズ
[SerializeField] private TextAsset labels;   // ラベルデータ（分類するカテゴリの名前）
[SerializeField] private NNModel modelAsset; // 事前学習済みモデルファイル
private IWorker engine;                      // モデルを実行するためのワーカー
private string[] labelsArray;                // ラベルデータを配列として格納
```

- `IMAGE_SIZE`: モデルに入力する画像の一辺の長さ。ここでは224ピクセルです。
- `labels`: テキストファイルとしてインポートされたラベルデータ（カテゴリのリスト）です。
- `modelAsset`: 事前にトレーニングされたニューラルネットワークモデル（`.onnx`形式など）をアタッチするための変数です。
- `engine`: モデルを実行するためのワーカー (`IWorker`) インスタンス。
- `labelsArray`: `labels`の内容を配列として保持することで、インデックスに基づいて分類ラベルにアクセスできるようにしています。

<br>

<br>

# 3. `Start` メソッド

```csharp
private void Start() {
    this.labelsArray = this.labels.text.Split('\n'); // ラベルデータを行ごとに分割して配列に格納
    var model = ModelLoader.Load(this.modelAsset);   // モデルをロード
    this.engine = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, model); // ワーカーを作成
}
```

1. `labelsArray`: ラベルデータを行ごとに分割し、配列に格納します。これにより、出力インデックスから分類結果（カテゴリ名）を簡単に取得できるようになります。
2. `ModelLoader.Load(this.modelAsset)`: `modelAsset` をロードし、`Model` 型としてモデルを読み込みます。
3. `WorkerFactory.CreateWorker`: モデルの推論を実行する `IWorker` インスタンス（`engine`）を作成します。`WorkerFactory.Type.ComputePrecompiled` は、コンパイル済みの計算ユニットを利用して推論を高速化します。

### 4. `Predict` メソッド

```csharp
public IEnumerator Predict(Color32[] picture, System.Action<Dictionary<string, float>> callback) {
    using (var tensor = TransformInput(picture, IMAGE_SIZE, IMAGE_SIZE)) {
        var inputs = new Dictionary<string, Tensor> { { "data", tensor } }; // モデルに入力するデータ
        this.engine.Execute(inputs); // モデルを実行
        var output = engine.PeekOutput("output"); // 出力を取得
        var results = new Dictionary<string, float>(); // 結果格納用の辞書

        for (int i = 0; i < output.length; i++) {
            results[this.labelsArray[i]] = output[i]; // ラベルと確率を対応付け
        }
        callback(results.OrderByDescending(x => x.Value).Take(3).ToDictionary(x => x.Key, x => x.Value)); // 上位3つの結果を返す
    }
    yield return null;
}
```

1. `TransformInput(picture, IMAGE_SIZE, IMAGE_SIZE)`: `Color32[]` 形式の画像データをテンソル形式に変換してモデルに入力できるようにします。
2. `engine.Execute(inputs)`: モデルに対して入力テンソルを渡し、推論を実行します。
3. `engine.PeekOutput("output")`: 出力層のテンソルを取得します。
4. `results`: ラベルと対応する確率（分類スコア）を格納する辞書です。
5. `callback(results.OrderByDescending(x => x.Value).Take(3).ToDictionary(...))`: スコアが高い順に並べ、上位3つのラベルと確率を返します。

### 5. `TransformInput` メソッド

```csharp
private static Tensor TransformInput(Color32[] pic, int width, int height) {
    float[] floatValues = new float[width * height * 3];
    for (int i = 0; i < pic.Length; ++i) {
        var color = pic[i];
        floatValues[i * 3 + 0] = (color.r - 127) / 128f; // 正規化
        floatValues[i * 3 + 1] = (color.g - 127) / 128f; // 正規化
        floatValues[i * 3 + 2] = (color.b - 127) / 128f; // 正規化
    }
    return new Tensor(1, width, height, 3, floatValues);
}
```

1. `floatValues`: 画像データを正規化して格納するための配列です。`width * height * 3` のサイズを持ちます（3はRGBの3チャネル）。
2. `for` ループで `Color32[]` の各ピクセル値を取得し、正規化した後に `floatValues` に格納します。
   - `(color.r - 127) / 128f` のように、RGB値を正規化して -1 ～ 1 の範囲に変換します。
3. `Tensor(1, width, height, 3, floatValues)`: TensorFlowまたはONNXフォーマットのニューラルネットワークモデルが処理しやすい形式でテンソルを作成します。

---

### `Classifier.cs` の動作の流れ

1. **モデルとラベルの読み込み**: `Start` メソッドでモデルをロードし、推論を実行する `IWorker` を生成します。ラベルデータも配列として読み込みます。
  
2. **画像データの前処理**: `Predict` メソッド内で、画像データを `Color32[]` からテンソル形式に変換するために `TransformInput` を使用します。

3. **推論の実行**: `engine.Execute(inputs)` によってモデルが画像データを推論し、出力テンソルから各ラベルのスコアを取得します。

4. **分類結果の取得**: 出力テンソル内のスコアに基づき、スコアの高いラベルを3つ選び、`callback` により上位3つのラベルと確率を返します。

### まとめ

`Classifier.cs` は、Unityで画像分類を行うためにモデルをロードし、画像データをテンソルに変換して推論を行い、結果を返すクラスです。