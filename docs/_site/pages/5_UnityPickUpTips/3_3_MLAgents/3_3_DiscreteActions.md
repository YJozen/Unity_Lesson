`actions.ContinuousActions`と`actions.DiscreteActions`は、通常、同時には存在しません。ML-Agentsでは、エージェントは連続アクションまたは離散アクションのいずれかを選択しますが、両方を同時に使用することはできません。これらのアクションのタイプは、エージェントのポリシー設定によって決定されます。

### 設定の例

#### 連続アクションの場合

YAML設定ファイルで連続アクションを指定する例：

```yaml
behaviors:
  MyAgentBehavior:
    trainer_type: ppo
    behavior_parameters:
      vector_action_space_type: continuous
      vector_action_space_size: 3  # 連続アクションの数
```

#### 離散アクションの場合

YAML設定ファイルで離散アクションを指定する例：

```yaml
behaviors:
  MyAgentBehavior:
    trainer_type: ppo
    behavior_parameters:
      vector_action_space_type: discrete
      vector_action_space_size: 3  # 離散アクションの数
```

### C#コード内での使用

#### 連続アクションの場合

```csharp
public override void OnActionReceived(ActionBuffers actions)
{
    float moveX = actions.ContinuousActions[0];
    float moveZ = actions.ContinuousActions[1];
    float rotation = actions.ContinuousActions[2];

    Vector3 move = new Vector3(moveX, 0, moveZ) * Time.deltaTime * moveSpeed;
    transform.Translate(move, Space.World);
    transform.Rotate(new Vector3(0, rotation, 0) * Time.deltaTime * rotationSpeed);
}
```

#### 離散アクションの場合

```csharp
public override void OnActionReceived(ActionBuffers actions)
{
    int action = actions.DiscreteActions[0];

    switch (action)
    {
        case 0:
            // 動かない
            break;
        case 1:
            // 前進
            transform.Translate(Vector3.forward * Time.deltaTime * moveSpeed);
            break;
        case 2:
            // 後退
            transform.Translate(-Vector3.forward * Time.deltaTime * moveSpeed);
            break;
    }
}
```

### まとめ

エージェントは、連続アクションか離散アクションのいずれかを使用しますが、両方を同時に使用することはできません。YAML設定ファイルの`vector_action_space_type`でどちらのアクションタイプを使用するかを指定します。エージェントのポリシー設定に従って、`actions.ContinuousActions`または`actions.DiscreteActions`を使用してエージェントの行動を制御します。