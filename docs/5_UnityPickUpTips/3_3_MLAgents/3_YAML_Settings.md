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



