Unity Sentisを使ったサンプルプログラムの例をいくつか紹介します。

### **サンプル1: ONNXモデルを使った物体検出**

このサンプルでは、ONNX形式の事前学習された物体検出モデルをUnity Sentisに組み込んで、ゲーム内で物体を検出するプログラムを作成します。

#### **手順**
1. **ONNXモデルのインポート**
   - UnityプロジェクトにONNX形式の物体検出モデルをインポートします。モデルをONNX形式で取得したら、Unityエディタで`Assets`フォルダにドラッグ＆ドロップします。
2. **Sentisでモデルをロード**
   - Sentis APIを使用して、ONNXモデルをロードします。

```csharp
using UnityEngine;
using Unity.Barracuda; // Sentisを使用するための名前空間

public class ObjectDetection : MonoBehaviour
{
    public NNModel modelAsset;
    private IWorker worker;

    void Start()
    {
        // モデルをロード
        Model model = ModelLoader.Load(modelAsset);
        worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, model);
    }

    void Update()
    {
        // 画像データを入力としてモデルに渡す
        Tensor inputTensor = new Tensor(256, 256, 3); // サンプルとして256x256のRGB画像

        // 推論実行
        worker.Execute(inputTensor);
        
        // 結果の取得
        Tensor outputTensor = worker.PeekOutput();
        Debug.Log("検出された物体数: " + outputTensor.length);
    }

    void OnDestroy()
    {
        worker.Dispose();
    }
}
```

3. **物体検出結果の表示**
   - `worker.PeekOutput()`で得られる物体検出の結果（例えば、バウンディングボックスや物体の種類）を使って、ゲーム内で表示します。

### **サンプル2: 音声認識モデルを使った音声入力処理**

次に、音声認識AIモデルをUnity Sentisで使って、ユーザーの音声をゲーム内で活用するサンプルを紹介します。

#### **手順**
1. **音声認識モデルのインポート**
   - 音声認識用に事前学習されたONNX形式の音声モデルをインポートします。
2. **音声データの収集**
   - Unityの`Microphone`クラスを使用して、ユーザーの音声入力を収集します。
3. **音声認識モデルを使った推論**

```csharp
using UnityEngine;
using Unity.Barracuda; // Sentis API

public class SpeechRecognition : MonoBehaviour
{
    public NNModel modelAsset;
    private IWorker worker;
    private AudioClip recordedClip;

    void Start()
    {
        // 音声認識モデルをロード
        Model model = ModelLoader.Load(modelAsset);
        worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, model);

        // マイクから音声を取得
        recordedClip = Microphone.Start(null, true, 10, 44100); // 10秒の音声録音
    }

    void Update()
    {
        if (Microphone.IsRecording(null))
        {
            // 音声データをTensorに変換
            Tensor inputTensor = new Tensor(recordedClip.samples, 1, 1, recordedClip.samples);

            // 音声認識モデルを実行
            worker.Execute(inputTensor);
            
            // 結果を取得し、認識結果をログに出力
            Tensor outputTensor = worker.PeekOutput();
            Debug.Log("認識された音声: " + outputTensor[0]);
        }
    }

    void OnDestroy()
    {
        worker.Dispose();
    }
}
```

### **サンプル3: Sentisを使ったリアルタイムNPCの行動制御**

このサンプルでは、Sentisを使ってNPCの行動をリアルタイムでAIモデルによって制御します。NPCは周囲の状況を感知し、適切な行動を取るようになります。

#### **手順**
1. **AIモデルのロード**
   - Sentisを使って事前にトレーニングしたNPC行動モデルをロードします。
2. **NPCの行動決定**
   - 例えば、NPCが障害物に近づいたときに回避行動を取るようにします。

```csharp
using UnityEngine;
using Unity.Barracuda;

public class NPCBehavior : MonoBehaviour
{
    public NNModel modelAsset;
    private IWorker worker;

    void Start()
    {
        // AIモデルをロード
        Model model = ModelLoader.Load(modelAsset);
        worker = WorkerFactory.CreateWorker(WorkerFactory.Type.ComputePrecompiled, model);
    }

    void Update()
    {
        // NPCの状態（例えば、障害物との距離）を入力として渡す
        Tensor inputTensor = new Tensor(1, 3); // 状態をベクトルで表す（例：位置、速度、周囲の情報）

        // 推論実行
        worker.Execute(inputTensor);
        
        // 出力結果をもとにNPCの行動を決定
        Tensor outputTensor = worker.PeekOutput();
        HandleNPCBehavior(outputTensor);
    }

    void HandleNPCBehavior(Tensor output)
    {
        if (output[0] > 0.5)
        {
            // 例: 回避行動
            transform.Translate(Vector3.left);
        }
        else
        {
            // 例: 前進
            transform.Translate(Vector3.forward);
        }
    }

    void OnDestroy()
    {
        worker.Dispose();
    }
}
```

### **まとめ**
これらのサンプルプログラムは、Unity Sentisを使用してAIをゲーム内で活用する基本的な方法を示しています。これらを元に、さらに複雑なAIシステムを構築することができます。

- **物体検出**や**音声認識**、**NPCの行動制御**など、Sentisを使ってゲーム内でAIを活用する方法を学びながら、実際に手を動かして試してみてください。

Unity Sentisの詳細なドキュメントやチュートリアルについては、公式ドキュメントやフォーラムを参照することをお勧めします。