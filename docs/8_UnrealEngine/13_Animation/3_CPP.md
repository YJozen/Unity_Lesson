# C++でのネイティブアニメーション設定

## 1. 基本用語と概念の詳細説明
- **ボーン（Bone）**:   
3Dモデルの内部構造を形成する基礎要素。ボーンは階層構造を持ち、親子関係で繋がっています。各ボーンは位置、回転、スケールの変換を持ち、これによりメッシュを動かします。

- **スキンメッシュ（Skinned Mesh）**:   
ボーンに付随する3Dモデル。ボーンの動きに応じてメッシュが変形します。キャラクターの外見を構成するメッシュ部分です。

- **リギング（Rigging）**:   
モデルにボーンを配置し、ボーンとメッシュを連動させるプロセス。キャラクターのアニメーションの基本骨格を作成します。

- **ウェイトペインティング（Weight Painting）**:   
各頂点がどのボーンにどれだけ影響されるかを指定する作業。これにより、ボーンの動きに対するメッシュの変形がスムーズになります。

- **キーフレームアニメーション（Keyframe Animation）**:   
重要な位置（キーフレーム）におけるモデルの状態を設定し、それらの間を補間してアニメーションを生成する方法。
- **スケルトンアニメーション（Skeletal Animation）**: ボーンの変換を時間に沿って変化させるアニメーション手法。キャラクターアニメーションに広く使用されます。

<br>

## 2. C++での具体的な手順

### モデルのインポートと初期設定
1. **3Dモデルの準備**: 3Dモデリングソフト（Blender、Mayaなど）でボーンとスキンメッシュを設定したモデルを作成し、FBXやOBJ形式でエクスポートします。
2. **C++プロジェクトのセットアップ**: 開発環境（Visual Studioなど）で新しいC++プロジェクトを作成し、必要なライブラリ（AssimpやOpenGLなど）をインクルードします。

### リギングの設定

1. **ボーン構造の定義**:
   - ボーンの階層構造をプログラムで定義し、各ボーンの親子関係を設定します。

```cpp
struct Bone
{
    std::string name;
    glm::mat4 offsetMatrix; // ボーンの初期オフセット行列
    glm::mat4 finalTransformation; // 最終的な変換行列
    Bone* parent;
    std::vector<Bone*> children;
};
```

<br>

2. **スキンメッシュの設定**:
   - スキンメッシュをボーンに関連付け、各頂点のウェイトを設定します。

```cpp
struct Vertex
{
    glm::vec3 position;
    glm::vec3 normal;
    glm::vec2 texCoords;
    std::vector<int> boneIDs;
    std::vector<float> weights;
};
```

### アニメーションの作成
1. **キーフレームの定義**:
   - 各ボーンの変換行列（位置、回転、スケール）を時間に沿って変化させるためのキーフレームを定義します。

```cpp
struct Keyframe
{
    float time;
    glm::vec3 position;
    glm::quat rotation;
    glm::vec3 scale;
};
```

<br>

2. **アニメーションの補間**:
   - キーフレーム間の補間を行い、ボーンの変換を計算します。

```cpp
glm::mat4 Interpolate(float currentTime, const std::vector<Keyframe>& keyframes)
{
    // キーフレーム間の補間を実装
    // 例: 線形補間
}
```
<br>

### アニメーションの制御
1. **ステートマシンの実装**:
   - アニメーションの遷移ロジックをプログラムで実装します。

```cpp
enum class AnimationState
{
    Idle,
    Walking,
    Running,
    Jumping
};

AnimationState currentState = AnimationState::Idle;

void UpdateAnimation(float deltaTime)
{
    switch (currentState)
    {
        case AnimationState::Idle:
            // Idleアニメーションの処理
            break;
        case AnimationState::Walking:
            // Walkingアニメーションの処理
            break;
        case AnimationState::Running:
            // Runningアニメーションの処理
            break;
        case AnimationState::Jumping:
            // Jumpingアニメーションの処理
            break;
    }
}
```

<br>

## 3. C++での実践例

以下に、C++でキャラクターアニメーションを設定するための基本的な手順とサンプルコードを示します。

### ボーンとスキンメッシュの設定例
1. **ボーンの定義とスキンメッシュの設定**:

```cpp
class Model
{
public:
    std::vector<Bone> bones;
    std::vector<Vertex> vertices;

    void LoadModel(const std::string& path)
    {
        // Assimpを使用してモデルをロード
        // ボーンとスキンメッシュの情報を抽出
    }

    void UpdateAnimation(float deltaTime)
    {
        // アニメーションを更新
        for (Bone& bone : bones)
        {
            bone.finalTransformation = CalculateBoneTransform(bone, deltaTime);
        }
    }

private:
    glm::mat4 CalculateBoneTransform(const Bone& bone, float deltaTime)
    {
        // ボーンの変換を計算
        glm::mat4 transform;
        // キーフレーム補間のロジックを実装
        return transform;
    }
};
```

## 4. トラブルシューティング

- **モデルが正しく動かない**: 
  - ボーンの階層構造やウェイトペインティングが正しく設定されているか確認します。  
  特に、ボーンの初期オフセット行列が正しいかをチェックします。
- **アニメーションが滑らかでない**:   
  - キーフレーム間の補間ロジックが適切であるか確認します。  
  補間の方法（線形補間、スプライン補間など）を適切に選択することが重要です。

