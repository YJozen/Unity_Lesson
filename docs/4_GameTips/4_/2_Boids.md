ボイドアルゴリズムの基本
Unityプロジェクトの設定
ボイド（Boid）の作成
ボイドの行動ルールの実装
シーンでのテストと調整





# 1.ボイドアルゴリズムの基本
ボイドアルゴリズムは3つの基本ルールに基づいています：

分離（Separation）: 他のボイドから一定の距離を保つ。
整列（Alignment）: 近くのボイドの平均方向に向かって進む。
結合（Cohesion）: 近くのボイドの中心に向かって移動する。


# 2. Unityプロジェクトの設定
1.新しいプロジェクトの作成:
Unity Hubを開き、新しい3Dプロジェクトを作成します。

2.基本的なシーンの設定:
新しいシーンを作成し、「Main Camera」と「Directional Light」を適切に配置します。  
「Main Camera」を選択し、位置を(0, 10, -10)、回転を(45, 0, 0)に設定します。  

# 3. ボイド（Boid）の作成
1.ボイドのプレハブを作成:

Hierarchyで右クリックし、「Create Empty」を選択して空のゲームオブジェクトを作成し、「Boid」と名前を付けます。
「Boid」オブジェクトに「Sphere」を子オブジェクトとして追加し、適当なスケールに設定します（例：(0.5, 0.5, 0.5)）。
「Boid」オブジェクトに「Boid.cs」スクリプトを追加します。
「Boid」オブジェクトをプロジェクトビューの「Prefabs」フォルダにドラッグ＆ドロップしてプレハブを作成します。


2.




分離（Separation）

```compute
    for (uint blockIndex = 0; blockIndex < (uint) _MaxBoidNum; blockIndex += SIMULATION_BLOCK_SIZE)
    {

      ・・・略・・・

            // 分離: 近づきすぎたら離れる
            if (distance <= _SeparationDistance)
            {
                separationPositionSum += diffPosition;
                separationCount++;
            }

            ・・・略・・・

    }

    ・・・略・・・

    if (separationCount > 0)
    {
        const float3 separationPosition = separationPositionSum / (float) separationCount;
        force += separationPosition * _SeparationCoefficient;
    }
```







整列（Alignment）



```compute

    for (uint blockIndex = 0; blockIndex < (uint) _MaxBoidNum; blockIndex += SIMULATION_BLOCK_SIZE)
    {

      ・・・略・・・

            // 整列: 近くの向きに合わせる
            if (distance <= _AlignmentDistance)
            {
                alignmentVelocitySum += targetVelocity;
                alignmentCount++;
            }

            ・・・略・・・

    }

    ・・・略・・・

    if (alignmentCount > 0)
    {
        const float3 alignmentVelocity = alignmentVelocitySum / (float) alignmentCount;
        force += alignmentVelocity * _AlignmentCoefficient;
    }


```






結合（Cohesion）


```
    for (uint blockIndex = 0; blockIndex < (uint) _MaxBoidNum; blockIndex += SIMULATION_BLOCK_SIZE)
    {

      ・・・略・・・

            // 結合: 近くのboidsの重心に近づく
            if (distance <= _CohesionDistance)
            {
                cohesionPositionSum += targetPosition;
                cohesionCount++;
            }

    }

    ・・・略・・・

    if (cohesionCount > 0)
    {
        const float3 cohesionPosition = cohesionPositionSum / (float) cohesionCount;
        force += (cohesionPosition - inPosition) * _CohesionCoefficient;
    }


```





GPUインスタンシング


GPUインスタンシングは、同じメッシュを複数回描画する際に非常に効率的な手法です。これにより、CPUからGPUへのドローコールを減らし、パフォーマンスを向上させることができます。以下に、UnityでGPUインスタンシングを使用する方法について説明します。

基本的なGPUインスタンシングの使用
Unityでは、マテリアルに対してインスタンシングを有効にすることで、簡単にGPUインスタンシングを利用することができます。

GPUインスタンシングとは不要なGameObjectの生成を行うことなく、同じメッシュのコピーを一度に描画できる手法のことです。
その結果、ドローコールの数が軽減され、大量オブジェクトを高速に描画できるようになります



ステップ 1: シェーダーの準備
まず、シェーダーでGPUインスタンシングをサポートする必要があります。Unityの標準シェーダーでは、インスタンシングをサポートしていますが、カスタムシェーダーの場合、以下のように記述します。



テップ 2: マテリアルの設定
シェーダーを使用してマテリアルを作成し、インスタンシングを有効にします。




ステップ 3: インスタンスの描画
上記のスクリプトを使用してインスタンスを生成します。シーン内でこのスクリプトをアタッチしたオブジェクトを配置し、prefab にインスタンス化したいオブジェクトを設定します。instanceCount にインスタンス化する数、radius に配置する範囲を設定します。
























