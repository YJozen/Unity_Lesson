# ContinuousActions

- **定義**: エージェントが連続値のアクションを選択するためのスペース。例えば、移動速度や角度などを含む。

- **コード例**:

  ```csharp
  public override void OnActionReceived(ActionBuffers actions)
  {
      // エージェントの移動方向を取得
      float moveX = actions.ContinuousActions[0];
      float moveZ = actions.ContinuousActions[1];
      
      // エージェントの回転角度を取得
      float rotation = actions.ContinuousActions[2];
      
      // 移動を適用
      Vector3 move = new Vector3(moveX, 0, moveZ) * Time.deltaTime * moveSpeed;
      transform.Translate(move, Space.World);
      
      // 回転を適用
      transform.Rotate(new Vector3(0, rotation, 0) * Time.deltaTime * rotationSpeed);
  }
  ```

- **説明**:
  - `ContinuousActions`配列から移動方向 (`moveX` と `moveZ`) を取得し、エージェントの動きを制御します。
  - `ContinuousActions`配列から回転角度 (`rotation`) を取得し、エージェントの回転を制御します。
  - 上記の例では、エージェントの移動速度 (`moveSpeed`) と回転速度 (`rotationSpeed`) を調整することで、連続値のアクションを適用しています。

### 追加の説明

- **速度の調整**:
  - エージェントの移動速度や回転速度は、学習や環境の要件に応じて調整できます。これにより、エージェントの動きが自然で効率的になります。

- **複数の連続アクション**:
  - 複数の連続アクションを組み合わせることで、エージェントに複雑な行動をさせることができます。例えば、同時にジャンプと移動を行う場合などです。

  ```csharp
  public override void OnActionReceived(ActionBuffers actions)
  {
      float moveX = actions.ContinuousActions[0];
      float moveZ = actions.ContinuousActions[1];
      float rotation = actions.ContinuousActions[2];
      float jump = actions.ContinuousActions[3];

      // 移動の適用
      Vector3 move = new Vector3(moveX, 0, moveZ) * Time.deltaTime * moveSpeed;
      transform.Translate(move, Space.World);

      // 回転の適用
      transform.Rotate(new Vector3(0, rotation, 0) * Time.deltaTime * rotationSpeed);

      // ジャンプの適用
      if (jump > 0.5f && isGrounded)
      {
          Rigidbody rb = GetComponent<Rigidbody>();
          rb.AddForce(new Vector3(0, jumpForce, 0), ForceMode.Impulse);
      }
  }
  ```

- **説明**:
  - `jump` アクションはジャンプの強さを表し、一定のしきい値 (`0.5f`) を超えた場合にジャンプを実行します。
  - `isGrounded` フラグはエージェントが地面に接触しているかを確認し、ジャンプを制限します。

このように、連続値のアクションを使ってエージェントに様々な動作をさせることができます。エージェントの学習と最適化には、これらのアクションがどのように環境と相互作用するかを理解することが重要です。

<br>

<br>

`actions.ContinuousActions[]`の配列の長さは、エージェントのポリシー設定に依存します。  
この設定は通常、UnityのML-Agentsトレーナーの設定ファイル（YAMLファイル）やエージェントのコンポーネントで指定されます。

### 設定ファイルの例

以下は、YAML設定ファイルの一部です。このファイルで連続アクションの数を指定します：

```yaml
behaviors:
  MyAgentBehavior:
    trainer_type: ppo
    hyperparameters:
      batch_size: 1024
      buffer_size: 10240
    network_settings:
      normalize: false
      hidden_units: 128
      num_layers: 2
    reward_signals:
      extrinsic:
        gamma: 0.99
        strength: 1.0
    max_steps: 500000
    time_horizon: 64
    summary_freq: 1000
    keep_checkpoints: 5
    checkpoint_interval: 50000
    threaded: true
    # Continuous action space of size 3
    behavior_parameters:
      vector_action_space_type: continuous
      vector_action_space_size: 3
```

この例では、`vector_action_space_size: 3`により、連続アクションの数が3に設定されています。

### 具体的なC#コード例

エージェントのスクリプト内で、`OnActionReceived`メソッドを使用して連続アクションを取得し、エージェントの動きを制御します：

```csharp
public override void OnActionReceived(ActionBuffers actions)
{
    // 連続アクション配列の長さを取得
    int actionSize = actions.ContinuousActions.Length;
    Debug.Log("Continuous Action Size: " + actionSize);

    // 連続アクションの値を取得
    float moveX = actions.ContinuousActions[0];
    float moveZ = actions.ContinuousActions[1];
    float rotation = actions.ContinuousActions[2];

    // 取得した値を用いてエージェントの動きを制御
    Vector3 move = new Vector3(moveX, 0, moveZ) * Time.deltaTime * moveSpeed;
    transform.Translate(move, Space.World);
    transform.Rotate(new Vector3(0, rotation, 0) * Time.deltaTime * rotationSpeed);
}
```

### まとめ

`actions.ContinuousActions[]`の配列の長さは、YAML設定ファイルやエージェントの設定に基づきます。上記の例では、連続アクションの数は3に設定されていますが、これはプロジェクトの要件に応じて変更可能です。