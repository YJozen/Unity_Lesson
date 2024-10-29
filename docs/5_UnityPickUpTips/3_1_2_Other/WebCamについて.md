`WebCam.cs` は、UnityでWebカメラを利用してリアルタイムで画像を取得し、その画像をAIモデルに入力して画像分類を行うスクリプトです。このスクリプトの役割や、各メソッドや処理の流れについて詳しく解説します。

### スクリプト概要
- `WebCam` クラスは、接続されたWebカメラから画像を取得し、AIモデル（`Classifier` クラス）を用いて画像をリアルタイムで分類します。
- 結果は`UI`のテキストエリアに出力され、Webカメラ画像が常に表示されます。

### コード解説

#### メンバ変数
```csharp
RawImage rawImage;           // Webカメラ画像を表示するためのUI要素
WebCamTexture webCamTexture; // Webカメラの映像をテクスチャとして格納
[SerializeField]int CameraNumber = 2; // 使用するWebカメラの番号（PCによって異なる）

public Classifier classifier;   // 画像分類を行う`Classifier`クラスの参照
public TextMeshProUGUI uiText;  // 結果を表示するテキストUI要素
private bool isWorking = false; // 推論処理中かどうかのフラグ
WebCamDevice[] devices;         // PCに接続されているWebカメラのリスト
private string webCamName;      // 選択されたWebカメラの名前
```

- `RawImage`: Webカメラの画像をUIに表示するために使用されます。
- `WebCamTexture`: Webカメラの映像をリアルタイムに取得するクラスです。
- `classifier`: `Classifier` クラスのインスタンスで、画像の分類を行います。
- `uiText`: 結果を画面に表示するためのUIです。
- `isWorking`: `true`の時は推論中で、次の推論を待機します。

#### `Start` メソッド
```csharp
void Start() {
    devices = WebCamTexture.devices; // 接続されている全Webカメラを取得
    webCamName = devices[CameraNumber].name; // 使用するカメラの名前を指定

    // Webカメラの開始
    this.rawImage = GetComponent<RawImage>();
    this.webCamTexture = new WebCamTexture(
        webCamName,
        Classifier.IMAGE_SIZE, Classifier.IMAGE_SIZE, 30);
    this.rawImage.texture = this.webCamTexture;
    this.webCamTexture.Play();
}
```
1. `devices = WebCamTexture.devices`: PCに接続されているWebカメラデバイスを取得し、`devices`配列に格納します。
2. `webCamName = devices[CameraNumber].name`: `CameraNumber` に指定した番号のカメラを選び、その名前を取得します。
3. `WebCamTexture` インスタンスを作成し、カメラ映像を`rawImage.texture`に設定して、`Play()`メソッドで映像を再生します。

#### `Update` メソッド
```csharp
private void Update() {
    TFClassify(); // 画像分類を実行
}
```
- 毎フレーム `TFClassify()` メソッドを呼び出して画像分類を行います。

#### `TFClassify` メソッド
```csharp
private void TFClassify() {
    if (this.isWorking) { return; }
    this.isWorking = true;

    StartCoroutine(ProcessImage(result => {
        StartCoroutine(this.classifier.Predict(result, probabilities => {
            this.uiText.text = "";
            for (int i = 0; i < 2; i++) {
                this.uiText.text += probabilities[i].Key + ": " + string.Format("{0:0.000}%", probabilities[i].Value) + "\n";
            }
            Resources.UnloadUnusedAssets(); // メモリを開放
            this.isWorking = false;
        }));
    }));
}
```
1. `isWorking`が`true`なら処理をスキップし、`false`の場合は推論処理を開始し、`isWorking`を`true`に設定。
2. `StartCoroutine(ProcessImage(...))`: `ProcessImage()`を呼び出し、Webカメラの画像を前処理して分類用のデータ形式に変換します。
3. `StartCoroutine(this.classifier.Predict(...))`: `Classifier` クラスの `Predict` メソッドを呼び出して画像分類を行い、結果を`uiText`に表示。
4. 推論が完了したら `Resources.UnloadUnusedAssets()` でメモリを解放し、`isWorking`を`false`に戻します。

#### `ProcessImage` メソッド
```csharp
private IEnumerator ProcessImage(System.Action<Color32[]> callback) {
    yield return StartCoroutine(CropSquare(webCamTexture, texture => {
        var scaled = Scaled(texture, Classifier.IMAGE_SIZE, Classifier.IMAGE_SIZE);                                 
        callback(scaled.GetPixels32());
    }));
}
```
1. `CropSquare`: Webカメラの画像を正方形にクロップし、Texture2Dに変換。
2. `Scaled`: `Classifier.IMAGE_SIZE` のサイズにスケールダウンし、結果をカラー値配列`Color32[]`にして`callback`として返します。

#### `CropSquare` メソッド
```csharp
public static IEnumerator CropSquare(WebCamTexture texture, System.Action<Texture2D> callback) {
    var smallest = texture.width < texture.height ? texture.width : texture.height;
    var rect = new Rect(0, 0, smallest, smallest);
    Texture2D result = new Texture2D((int)rect.width, (int)rect.height);

    if (rect.width != 0 && rect.height != 0) {
        result.SetPixels(
            texture.GetPixels(
                Mathf.FloorToInt((texture.width - rect.width) / 2),
                Mathf.FloorToInt((texture.height - rect.height) / 2),
                Mathf.FloorToInt(rect.width),
                Mathf.FloorToInt(rect.height)
            )
        );
        yield return null;
        result.Apply();
    }

    yield return null;
    callback(result);
}
```
1. `smallest`にWebカメラ映像の幅・高さの小さい方の長さを代入し、`rect`で正方形の範囲を定義。
2. `result.SetPixels(...)` で、正方形の範囲を取得し、`Texture2D`に保存。
3. `result.Apply()`で処理を適用し、`callback`で結果を返します。

#### `Scaled` メソッド
```csharp
public static Texture2D Scaled(Texture2D texture, int width, int height) {       
    var rt = RenderTexture.GetTemporary(width, height); // リサイズ後のRenderTextureの生成
    Graphics.Blit(texture, rt);

    var preRT = RenderTexture.active;
    RenderTexture.active = rt;
    var ret = new Texture2D(width, height);
    ret.ReadPixels(new Rect(0, 0, width, height), 0, 0);
    ret.Apply();
    RenderTexture.active = preRT;
    RenderTexture.ReleaseTemporary(rt);
    return ret;
}
```
1. `RenderTexture` でリサイズ処理を行い、テクスチャを指定されたサイズに変換します。
2. `ret.ReadPixels` でリサイズ済みのピクセルデータを取得し、`Texture2D`として返します。

### まとめ
- `WebCam`クラスはWebカメラの画像を取得して、指定されたモデルで分類を行い、結果をリアルタイムで画面に表示します。
- `TFClassify` や`ProcessImage`で画像を処理し、`Classifier`で分類を行い、テキストで結果を表示する流れが構築されています。