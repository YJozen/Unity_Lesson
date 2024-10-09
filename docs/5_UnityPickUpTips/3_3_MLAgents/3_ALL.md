
# 全体のまとめ

UnityのML-Agents（Machine Learning Agents）は、ゲームやシミュレーション環境でAIエージェントをトレーニングするためのツールです。このツールは、強化学習（Reinforcement Learning, RL）とニューラルネットワーク（Neural Networks, NN）を組み合わせてエージェントの行動を学習させます。

### 1. 強化学習の基本概念
強化学習は、エージェントが環境との相互作用を通じて報酬を最大化する行動を学ぶための機械学習の一分野です。主な要素は以下の通りです：

- **エージェント（Agent）**: 学習する主体。環境内で行動し、報酬を受け取ります。
- **環境（Environment）**: エージェントが操作する外部システム。エージェントの行動に応じて状態が変化し、報酬を返します。
- **状態（State）**: 環境の現在の状況を表します。エージェントはこの状態を基に行動を決定します。
- **行動（Action）**: エージェントが環境に対して取る行動です。行動は離散的な場合もあれば、連続的な場合もあります。
- **報酬（Reward）**: エージェントが特定の行動を取った結果として得られる数値。エージェントはこの報酬を最大化するように学習します。
- **方策（Policy）**: 状態に基づいて次に取るべき行動を決定する戦略です。強化学習の目的は、最適な方策を学習することです。

### 2. ニューラルネットワークと方策学習
強化学習における方策は、ニューラルネットワークによってモデル化されることが多いです。ニューラルネットワークは、状態を入力として受け取り、行動を出力として返す関数として機能します。このネットワークは、トレーニングを通じて最適な方策を学習します。

- **入力層**: エージェントの観測（状態）を受け取ります。例えば、視覚情報やセンサー情報が含まれます。
- **隠れ層**: 入力された情報を処理します。複数の隠れ層を通じて、複雑な非線形関数を学習できます。
- **出力層**: 行動を予測します。出力は、離散的な行動（例えば、前進、後退、回転など）や連続的な行動（例えば、速度や角度の調整など）に対応します。

### 3. Unity ML-Agentsにおける強化学習の流れ
UnityのML-Agentsでは、強化学習のプロセスは以下のように進行します：

1. **環境の初期化**:
   - エージェントの初期位置や環境の設定が行われます（`OnEpisodeBegin()`メソッドなど）。
   
2. **観測の収集**:
   - エージェントが現在の状態（環境の観測）を収集します（`CollectObservations()`メソッド）。これには位置、速度、センサー情報などが含まれます。
   
3. **行動の選択**:
   - エージェントはニューラルネットワークを使用して、収集した観測に基づいて行動を選択します（`OnActionReceived()`メソッド）。
   
4. **行動の実行**:
   - エージェントは選択した行動を実行し、環境に影響を与えます。
   
5. **報酬の受け取り**:
   - 環境はエージェントの行動に基づいて報酬を与えます。この報酬は、エージェントが目標に近づいたか、障害物に衝突したかなどに基づいて決定されます。
   
6. **方策の更新**:
   - エージェントは受け取った報酬に基づいて、ニューラルネットワークの重みを更新します。これにより、将来の行動が改善されます。
   
7. **エピソードの終了**:
   - ある条件（例えば、目標地点に到達、制限時間切れ、落下など）でエピソードが終了し、次のエピソードが開始されます。

### 4. 学習プロセスと報酬信号
エージェントの学習は報酬信号を基に進行します。報酬が大きくなる行動を繰り返し、逆に報酬が少ない行動を避けるようにニューラルネットワークが調整されます。学習の過程でエージェントは、環境の状態をより良く観察し、効率的な行動を選択する能力を向上させます。

### 5. ML-Agentsにおける強化学習アルゴリズム
Unity ML-Agentsでは、一般的な強化学習アルゴリズムがサポートされています。最も一般的なのは、以下のアルゴリズムです：

- **PPO（Proximal Policy Optimization）**: 方策勾配法の一種で、安定した学習を実現します。ML-Agentsのデフォルトのアルゴリズムとしてよく使用されます。
- **SAC（Soft Actor-Critic）**: より柔軟でスムーズな方策更新を行うためのアルゴリズムです。

### まとめ
Unity ML-Agentsは、強化学習とニューラルネットワークを組み合わせることで、エージェントが複雑な環境での行動を学習することを可能にします。エージェントは、観測された状態を基に行動を選択し、環境から得られる報酬を最大化するように学習します。これにより、ゲームやシミュレーション環境でのAI開発が大幅に効率化されます。


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


