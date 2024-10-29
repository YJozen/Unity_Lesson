## モデルの準備について

(TeachableMachineなどでモデル生成)

https://teachablemachine.withgoogle.com/


参考サイト

https://qiita.com/s_yosh1d/items/0ac1e5c941ecda52b131

<br>


<br>



Webカメラ映像から画像をキャプチャし、機械学習モデル（Barracudaを使用）で分類を行うシステムです。


+ WebCam.csファイルでWebカメラ映像を取得  
+ Classifier.csで機械学習モデルを用いた画像分類

を行います。

<br>

<br>


# WebCam.cs スクリプトについて

[WebCam.cs スクリプトについての詳細](WebCamについて.md)

Webカメラの映像をキャプチャし、Barracudaモデルで画像分類するクラスです。

1. **フィールド宣言**
   - `rawImage`: Webカメラの映像を表示するための `RawImage` コンポーネント。
   - `webCamTexture`: Webカメラの映像テクスチャ。
   - `CameraNumber`: 使用するカメラのインデックス（`WebCamTexture.devices` 配列から選択）。
   - `classifier`: 分類用クラスの参照。
   - `uiText`: 分類結果を表示するテキストフィールド。
   - `isWorking`: 処理中フラグ。
   - `devices`: 接続されているカメラデバイスのリスト。
   - `webCamName`: 選択したカメラの名前。

2. **Startメソッド**
   - 使用するWebカメラデバイスを選択し、`webCamTexture` を作成します。解像度は `Classifier.IMAGE_SIZE` に基づきます。
   - Webカメラをスタートし、`rawImage` にカメラ映像を表示します。

3. **Updateメソッド**
   - `TFClassify()` を毎フレーム実行し、カメラ映像をもとに分類処理を行います。

4. **TFClassifyメソッド**
   - 処理中でない場合に `ProcessImage` コルーチンを開始し、分類結果を表示します。

5. **ProcessImageメソッド**
   - `CropSquare` コルーチンを呼び出してカメラ画像を正方形に切り出し、スケーリングして、Barracudaモデルで扱える `Color32[]` フォーマットに変換します。

6. **CropSquareメソッド**
   - 入力画像を中心から正方形にトリミングするコルーチンです。 `Texture2D` に変換後、画像データをコールバックに返します。

7. **Scaledメソッド**
   - 渡された `Texture2D` 画像を指定された解像度にリサイズします。

<br>



<br>

# Classifier.cs スクリプトの詳細解説

[Classifierスクリプトについての詳細](Classifierについて.md)



`Classifier` クラスは、Barracudaフレームワークを用いてWebカメラ映像の分類を行うためのクラスです。

1. **フィールド宣言**
   - `modelFile`: 推論に使用するニューラルネットワークモデルファイル。
   - `labelsFile`: 各クラス（分類ラベル）の名前が記載されたテキストファイル。
   - `IMAGE_SIZE`, `IMAGE_MEAN`, `IMAGE_STD`: 画像サイズと正規化のための定数。
   - `INPUT_NAME`, `OUTPUT_NAME`: モデルファイルの入力と出力の名前。
   - `worker`: Barracudaのモデルを実行するためのエンジン。
   - `labels`: ラベルデータの配列。

2. **Startメソッド**
   - `labelsFile` からラベルを読み込み、Barracudaモデルの初期化を行います。

3. **Predictメソッド**
   - `Color32[]` 配列の画像データをBarracudaモデルに入力して推論を行うメソッドです。
   - 入力画像をテンソル化し、モデルに渡して予測を実行します。
   - 推論結果は確率の降順にソートされて `callback` 関数で返されます。

4. **TransformInputメソッド**
   - `Color32` 配列の画像データを `Tensor` に変換し、Barracudaモデルが扱える形式にします。

5. **OnDestroyメソッド**
   - ワーカー（Barracudaエンジン）を解放してリソースをクリーンアップします。


<br>

<br>

# labels.txt ファイル

このファイルには各クラスのラベルが記述されており、Barracudaモデルが分類結果として返すラベルのリストです。例えば、`Unity-Chan` と `Jozen` の2つのクラスが含まれています。

<br>

<br>

# 実行フロー
1. WebCam.csでWebカメラ映像を取得し、一定間隔で画像を切り出して分類処理へ送信。
2. Classifier.csで機械学習モデルが推論を実行し、分類結果を表示。
