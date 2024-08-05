# MLAgents
- [はじめに(神戸電子_宮本先生による導入動画)](https://drive.google.com/file/d/1YiVMleM__0kqXRKBs5UO9bq2N7a0mhYO/view?usp=drive_link)

- 授業スライドや資料  
  -  <a href="https://drive.google.com/drive/folders/1Qxd4PeikBb7pztRt8RDlirOxi1tCofYk" target="_blank">MLAgentsをとりあえず動かしてみよう</a>

- ニューラルネットワークについて触れるならこっちから、触れてみてもいいかも  
  - [Python機械学習](https://drive.google.com/drive/folders/1Pwr0G_I46uJpsPWQFGAk6pymbJDx_hR_)
 
- [ニューラルネットワークと強化学習](3_7_NN_RL.md)

<br>

<br>


<br>

<br>

# エージェントスクリプトについて  
**エージェントスクリプト**は、ML-Agentsの中心的なコンポーネントであり、このスクリプトで、エージェントが観測、行動、報酬を受け取り、どのように環境と相互作用するかを定義します。  
Agentクラスを継承させたスクリプトを作成します。  

<br>

<br>

<br>

<br>

# エージェントスクリプトの例  
以下は、簡単なエージェントスクリプトの例です。  
このスクリプトでは、エージェントが特定の目標に到達したときに報酬を与える例です。

```cs
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;

public class MyAgent : Agent
{
    public Transform targetTransform;
    public float moveSpeed = 1f;

    // エピソードの開始時に呼び出されます
    public override void OnEpisodeBegin()
    {
        // エージェントとターゲットの位置をリセット
        transform.localPosition = new Vector3(Random.Range(-4f, 4f), 0, Random.Range(-4f, 4f));
        targetTransform.localPosition = new Vector3(Random.Range(-4f, 4f), 0, Random.Range(-4f, 4f));
    }

    // 観測を収集するために呼び出されます
    public override void CollectObservations(VectorSensor sensor)
    {
        // エージェントとターゲットの相対位置を観測
        sensor.AddObservation(targetTransform.localPosition - transform.localPosition);
    }

    // 行動を実行するために呼び出されます
    public override void OnActionReceived(ActionBuffers actions)
    {
        // 行動を取得
        float moveX = actions.ContinuousActions[0];
        float moveZ = actions.ContinuousActions[1];

        // エージェントを移動
        transform.localPosition += new Vector3(moveX, 0, moveZ) * moveSpeed * Time.deltaTime;

        // ターゲットに到達したら報酬を与える
        float distanceToTarget = Vector3.Distance(transform.localPosition, targetTransform.localPosition);
        if (distanceToTarget < 1.5f)
        {
            SetReward(1.0f);
            EndEpisode();
        }

        // 毎ステップ小さな負の報酬を与えることで、迅速な行動を促す
        AddReward(-0.001f);
    }

    // ヒューマンデバッグ用のヒント
    public override void Heuristic(in ActionBuffers actionsOut)
    {
        var continuousActions = actionsOut.ContinuousActions;
        continuousActions[0] = Input.GetAxis("Horizontal");
        continuousActions[1] = Input.GetAxis("Vertical");
    }
}

```

<br>

<br>

<br>

<br>

# 実際の処理の流れ

1. **ゲーム開始、ついでにエピソード開始**
   - ゲームが開始されると、Unityシーンがロードされ、AwakeやStartなどが実行されたのち、エージェントとターゲットの初期位置が設定されます。ここでエージェントの初期状態が決まります。(`OnEpisodeBegin`)(ちなみにStartの方が先に呼ばれる)

2. **ステップ開始**
   - ML-Agents環境が次のステップに進む準備をします。具体的には、次のフレームの処理を行う準備が整います。このタイミングで物理エンジンの更新や、シーンの状態の変化が行われることがあります。

3. **CollectObservations呼び出し（観測収集）**
   - エージェントが環境の状態を観測するために、`CollectObservations` メソッドが呼び出されます。ここで収集される観測データは、エージェントの次の行動決定に使われます。

4. **OnActionReceived呼び出し（行動決定）**
   - `OnActionReceived` メソッドが呼び出され、エージェントが決定した行動が環境に適用されます。この段階で、エージェントの行動によって環境が変化し、エージェントの位置や状態が更新されます。

5. **エピソード終了**
   - エピソードが終了する条件が満たされると、`EndEpisode` メソッドが呼び出されます。この時点で、エピソードの成績や報酬が計算され、エージェントと環境の状態がリセットされます。

6. **次のエピソード開始**
   - 新しいエピソードが開始されると、再び `OnEpisodeBegin` が呼び出され、エージェントとターゲットの位置がリセットされ、新しいエピソードの準備が整います。これにより、環境が初期状態に戻り、新しい学習サイクルが始まります。

<br>

<br>

**環境の更新がされるタイミング**:
- **ステップ開始**: 環境の物理エンジンやシーンの状態が更新されます。
- **OnActionReceived呼び出し（行動決定）**: エージェントの行動が適用され、環境が変化します。
- **エピソード終了**: エピソード終了時にエージェントと環境の状態がリセットされます。

環境の更新はエージェントの行動が適用される際や、エピソードが終了する際に行われます。

[AIにおける「環境」とは](3_1_AI_Enviroment.md)

<br>

<br>

<br>

<br>


# エージェントスクリプトの詳細

**エージェントスクリプト**は、ML-Agentsの中心的なコンポーネントであり、このスクリプトで、エージェントが観測、行動、報酬を受け取り、どのように環境と相互作用するかを定義します。  
Agentクラスを継承するスクリプトを作成します。  

### エージェントスクリプトの構成要素

1. **`OnEpisodeBegin` メソッド**:
   - **目的**: エピソードの開始時にエージェントの状態をリセットします。これにより、各エピソードが一貫して同じ条件から開始されます。
   - **使い方**: 通常、エージェントやターゲットの位置をリセットしたり、エピソードに関する初期設定を行います。
   - **コード例**:
     ```csharp
     public override void OnEpisodeBegin()
     {
         transform.localPosition = new Vector3(Random.Range(-4f, 4f), 0, Random.Range(-4f, 4f));
         targetTransform.localPosition = new Vector3(Random.Range(-4f, 4f), 0, Random.Range(-4f, 4f));
     }
     ```

2. **`CollectObservations` メソッド**:
   - **目的**: 環境の状態をエージェントに提供するために、観測データを収集します。これにより、エージェントは現在の状況を理解し、適切な行動を選択できます。
   - **使い方**: 環境からの状態や特徴をセンサーを使って収集し、`VectorSensor`オブジェクトに追加します。
   - **コード例**:
     ```csharp
     public override void CollectObservations(VectorSensor sensor)
     {
         sensor.AddObservation(targetTransform.localPosition - transform.localPosition);
     }
     ```
   - **説明**: ここでは、エージェントとターゲット間の距離ベクトルを観測データとして追加しています。

3. **`OnActionReceived` メソッド**:
   - **目的**: エージェントが選択したアクションを実行し、報酬を設定します。エージェントの行動が環境にどのような影響を与えたかに応じて報酬を調整します。
   - **使い方**: 行動に基づいてエージェントの位置を変更し、ターゲットへの距離を計算して報酬を設定します。
   - **コード例**:
     ```csharp
     public override void OnActionReceived(ActionBuffers actions)
     {
         float moveX = actions.ContinuousActions[0];
         float moveZ = actions.ContinuousActions[1];

         transform.localPosition += new Vector3(moveX, 0, moveZ) * moveSpeed * Time.deltaTime;

         float distanceToTarget = Vector3.Distance(transform.localPosition, targetTransform.localPosition);
         if (distanceToTarget < 1.5f)
         {
             SetReward(1.0f);
             EndEpisode();
         }

         AddReward(-0.001f);
     }
     ```
   - **説明**: `ContinuousActions`から移動方向を取得し、エージェントの位置を更新します。ターゲットに近づくと高い報酬を与え、エピソードを終了します。毎ステップで小さな負の報酬を与えます。

4. **`Heuristic` メソッド**:
   - **目的**: 人間がエージェントの操作を試すための補助機能を提供します。デバッグや手動操作の際に役立ちます。
   - **使い方**: キーボードやコントローラーの入力をエージェントのアクションとして変換します。
   - **コード例**:
     ```csharp
     public override void Heuristic(in ActionBuffers actionsOut)
     {
         var continuousActions = actionsOut.ContinuousActions;
         continuousActions[0] = Input.GetAxis("Horizontal");
         continuousActions[1] = Input.GetAxis("Vertical");
     } 
     ```

<br>

<br>

# エピソードとステップの違い

- **エピソード**:
  - **定義**: エージェントが開始から終了までの一連の行動と環境との相互作用を含む期間。
  - **例**: エージェントがゲームのレベルをクリアする、または目標に到達するまでのプロセス。

- **ステップ**:
  - **定義**: エピソード内の各サイクル。エージェントが1つのアクションを実行し、その結果に基づいて観測を行います。
  - **例**: エージェントが1フレームごとに実行するアクションと観測。

<br>

<br>

# `CollectObservations` と `OnActionReceived` の呼び出しタイミング

- **`CollectObservations`**:
  - **タイミング**: 各ステップの開始時に呼び出され、エージェントが環境の状態を観測します。
  - **例**: エージェントがターゲットの位置や周囲の環境を観測します。

- **`OnActionReceived`**:
  - **タイミング**: 各ステップの後に呼び出され、エージェントが選択した行動を実行します。
  - **例**: エージェントが移動し、報酬を受け取ります。

<br>

<br>

### ContinuousActions

- **定義**: エージェントが連続値のアクションを選択するためのスペース。例えば、移動速度や角度などを含む。
- **コード例**:
  ```csharp
  public override void OnActionReceived(ActionBuffers actions)
  {
      float moveX = actions.ContinuousActions[0];
      float moveZ = actions.ContinuousActions[1];
  }
  ```
- **説明**: `ContinuousActions`配列から移動方向を取得し、エージェントの動きを制御します。

[ContinuousActionsについて](3_2_ContinuousActions.md)

<br>

<br>

今回は使用していないが
### DiscreteActions

- **定義**: エージェントが離散的なアクションを選択するためのスペース。例えば、ジャンプ、回転、停止など、あらかじめ定義されたアクションの中から選ぶ形式。
- **コード例**:
  ```csharp
  public override void OnActionReceived(ActionBuffers actions)
  {
      int action = actions.DiscreteActions[0];
      
      switch (action)
      {
          case 0:
              // アクション0: 移動する
              MoveForward();
              break;
          case 1:
              // アクション1: ジャンプする
              Jump();
              break;
          case 2:
              // アクション2: 止まる
              Stop();
              break;
      }
  }
  ```
- **説明**: `DiscreteActions`配列から選択されたアクションのインデックスを取得し、エージェントの動作を制御します。`DiscreteActions`は離散的な値（整数）を提供し、それぞれの整数値が特定のアクションにマッピングされます。この方法で、エージェントはアクションの選択肢から1つを選び、それに応じて振る舞いを変えることができます。

### 詳細

- **使用例**:
  - **ゲーム内のキャラクター制御**: 例えば、キャラクターが「前進」、「後退」、「左旋回」、「右旋回」などのアクションを選択する場合。
  - **ロボットの操作**: ロボットが「アームを上げる」、「アームを下げる」、「物を掴む」などの具体的な操作を選択する場合。

- **メリット**: 離散的なアクションは簡単に理解でき、特定のアクションの選択肢を管理するのが容易です。適用しやすい場合も多いですが、アクションの選択肢が多すぎると、学習が複雑になることがあります。

- **設定**:
  - **`Behavior Parameters`** コンポーネントで、`Space Type`を`Discrete`に設定し、アクションの数を指定します。
  - 各アクションに対応するインデックスを定義し、`OnActionReceived`内で適切な処理を行います。

これにより、エージェントは定義されたアクションセットから選択し、環境に応じた行動を取ることができます。

[ContinuousActionsとDiscreteActionsについて](3_2_ContinuousActions.md)

<br>

<br>

<br>

<br>

### `AddReward` と `SetReward` の使い分け

- **`AddReward`**:
  - **目的**: 現在の報酬に追加の報酬を加算します。ステップごとに小さな報酬を与える場合に使用します。
  - **コード例**:
    ```csharp
    AddReward(-0.001f);
    ```

- **`SetReward`**:
  - **目的**: 報酬の値を直接設定します。エージェントが特定の目標を達成したときなどに使用します。
  - **コード例**:
    ```csharp
    SetReward(1.0f);
    ```

---


<br>

<br>

<br>

<br>

ML-Agentsでの「ステップ数」の設定は、エージェントが環境内で行動を決定するためのサイクル回数に関わります。  
具体的には、以下のような設定が関係します。

### 1. **Max Step Count (最大ステップ数)**

- **設定場所**: 学習設定ファイル（`trainer_config.yaml`）またはトレーニングのスクリプトで設定します。
- **説明**: エピソードが開始されてから終了するまでに許可される最大のステップ数を指定します。エピソード内でエージェントが何ステップまで行動できるかを制限するために使用します。
- **効果**: 最大ステップ数に達すると、そのエピソードは終了します。これにより、エージェントが学習中に無限にエピソードを続けるのを防ぎます。

### 2. **Academy Step Interval (アカデミー・ステップ間隔)**

- **設定場所**: `Academy` スクリプトで設定します。
- **説明**: 環境が更新される間隔を指定します。例えば、アカデミーが毎フレーム更新される場合や、指定されたフレーム間隔で更新される場合があります。
- **効果**: 環境の更新頻度を調整し、学習の安定性やパフォーマンスに影響を与えることがあります。



### 3. **Time Horizon (タイムホライズン)**

- **設定場所**: 学習設定ファイル（`trainer_config.yaml`）またはトレーニングのスクリプトで設定します。
- **説明**: エージェントが将来の報酬を考慮するためのステップ数です。エージェントが未来の報酬をどれだけ先のステップまで考慮するかを決定します。
- **効果**: 長いタイムホライズンを設定すると、エージェントはより長期的な報酬を重視しますが、計算量が増える可能性があります。

[Time Horizonについて](3_5_TimeHorizon.md)

### 4. **Environment Reset**

- **設定場所**: コード内の `OnEpisodeBegin` メソッドでエピソード開始時にリセットします。
- **説明**: エピソードが終了するたびに環境がリセットされるため、新しいエピソードが開始されます。
- **効果**: 各エピソードごとに環境が初期状態に戻り、エージェントが新たに学習を開始できるようになります。

### ステップ数の管理方法

- **トレーニングのスクリプト**や**設定ファイル**で適切な最大ステップ数やタイムホライズンを設定します。
- **アカデミーの更新間隔**を調整することで、エージェントの学習にかかる時間や精度に影響を与えることができます。

これらの設定を適切に調整することで、エージェントの学習プロセスを最適化し、効果的なトレーニングを実現できます。


<br>

<br>

<br>

<br>


# YAMLファイルの詳細

[一般的な話(yamlファイルについて)](3_6_YAML.md)

### YAMLファイルの目的

- **設定管理**: 環境やトレーニングの設定を管理するために使用します。これにより、トレーニングのパラメータを簡単に調整できます。

### YAMLファイルの構造

- **`behaviors` セクション**: 各エージェントの振る舞いの設定を含みます。トレーニングの種類やハイパーパラメータ、ネットワーク設定などが含まれます。
- **例**:
  ```yaml
  behaviors:
    MyAgentBehavior:
      trainer_type: ppo
      hyperparameters:
        learning_rate: 3.0e-4
        batch_size: 1024
        buffer_size: 2048
        number_of_epoch: 3
      network_settings:
        normalize: false
        hidden_units: 128
        num_layers: 2
      reward_signals:
        extrinsic:
          strength: 1.0
          gamma: 0.99
      keep_checkpoints: 5
      max_steps: 5.0e4
  ```

### 主なパラメータの説明

- **`trainer_type`**: トレーニングアルゴリズムの種類。例えば、`ppo`（Proximal Policy Optimization）や`sac`（Soft Actor-Critic）など。
- **`hyperparameters`**: 学習率やバッチサイズ、バッファサイズなどのハイパーパラメータ。
- **`network_settings`**: ニューラルネットワークの設定。隠れ層のユニット数やレイヤー数を定義します。
- **`reward_signals`**: 報酬信号の設定。報酬の強さや割引率（`gamma`）などを含みます。
- **`keep_checkpoints`**: 保存するチェックポイントの数。
- **`max_steps`**: 最大ステップ数。エピソードごとにこの数に達するまで実行します。

### YAMLファイルの使い方

1. **設定の作成**: 必要な設定をYAMLファイルに記述します。
2. **トレーニングの実行**: ML-Agentsのトレーニングコマンドを使用して、YAMLファイルを指定し、トレーニングを開始します。

   コマンド
   ```bash
   mlagents-learn config/trainer_config.yaml --run-id=MyRun
   ```

これで、ML-Agentsのエージェントスクリプト、メソッド、エピソードとステップの違い、ContinuousActions、報酬設定、YAMLファイルの詳細についての理解が深まると思います。質問があれば、さらに深掘りしてお答えします！

<br>

<br>

<br>

<br>

Unity ML-Agentsのトレーニングを実行する際に使用するコマンドについて、以下に詳細を説明します。再実行時やトレーニングの設定変更後にどう対応するかも含めて解説します。

### 基本的なトレーニングコマンド

#### 1. トレーニングの実行

トレーニングを開始する基本的なコマンドは以下のようになります:

```bash
mlagents-learn <config_file> --run-id=<run_id>
```

- `<config_file>`: トレーニング設定が記述されたYAMLファイルへのパス。
- `<run_id>`: トレーニングセッションを識別するための一意のID。新しいトレーニングセッションごとに異なるIDを指定することが推奨されます。

#### 2. サンプルコマンド

```bash
mlagents-learn config/trainer_config.yaml --run-id=my_first_run
```

このコマンドは、`config/trainer_config.yaml`に基づいてトレーニングを開始し、セッションIDとして`my_first_run`を使用します。

### 再実行時の注意点

#### 1. 既存のトレーニングを再実行する

- **新しいセッションとして再実行**: トレーニングの設定を変更した場合や、別の実験を行いたい場合は、新しい`run-id`を指定して再実行します。これにより、前回のトレーニング結果に影響を与えずに新しいトレーニングが開始されます。

  ```bash
  mlagents-learn config/trainer_config.yaml --run-id=my_second_run
  ```

- **既存のセッションを再開**: 既存のセッションを再開したい場合は、以前に使用した`run-id`を指定します。ただし、ML-Agentsでは通常、新しいトレーニングを開始するために新しい`run-id`を使用することが推奨されます。

#### 2. 中断したトレーニングの再開

トレーニングが中断された場合は、以下の手順で再開できます。

- **チェックポイントの確認**: トレーニングのチェックポイントが保存されていることを確認します。これにより、トレーニングの途中から再開できます。

- **再開コマンド**: `--resume`フラグを使用して、既存のセッションを再開します。

  ```bash
  mlagents-learn config/trainer_config.yaml --run-id=my_first_run --resume
  ```

  ただし、`--resume`フラグは通常、前回のトレーニングで中断があった場合に使用されます。デフォルトでは、トレーニングは最初から開始されます。

### その他のオプション

- **`--train`**: トレーニングモードで実行することを指定します（デフォルトではトレーニングモードが使用されます）。

- **`--inference`**: モデルの推論を行うために使用します。このオプションは、トレーニングとは異なり、エージェントの行動をテストするのに適しています。

  ```bash
  mlagents-learn config/trainer_config.yaml --run-id=my_inference_run --inference
  ```

- **`--base-port`**: ポート番号のベースを指定するオプションです。複数のエージェントを使用する場合や、複数のトレーニングセッションを同時に実行する場合に役立ちます。

  ```bash
  mlagents-learn config/trainer_config.yaml --run-id=my_run --base-port=5005
  ```

これで、Unity ML-Agentsのトレーニングの実行や再実行についての基本的な`bash`コマンドとその使い方が理解できると思います。



