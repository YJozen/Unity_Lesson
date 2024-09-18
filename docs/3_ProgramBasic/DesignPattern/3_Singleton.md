<head>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>


# シングルトンパターン

## 定義 

シングルトンパターンは、特定のクラスのインスタンスが一つしか存在しないことを保証するデザインパターンです。  
このインスタンスにはグローバルなアクセスポイントが提供され、必要に応じてこのインスタンスを共有します。

<br>

## 目的
グローバルなアクセス点を提供し、インスタンスの数を制限する。

特定のクラスのインスタンスがプログラム全体で唯一であり、その唯一性を保証することで、リソース消費を最適化し、一貫性を保つ。

<br>

## Unityでの実際の使用例
+ GameManager    : ゲームの進行管理や設定の取得などゲーム全体で共通のゲームマネージャーを管理
+ SoundManager   : ゲーム内の音声管理。
+ ResourceManager: リソースの読み込みや解放管理。
など

<br>

## 利点
+ 一貫性: 一つのインスタンスのみが存在するため、一貫した状態を維持できます。
+ グローバルアクセス: グローバルなアクセス点を提供するため、複数のコンポーネントが同じインスタンスにアクセスできます。どこからでもアクセス可能。
+ リソース効率: 不要なインスタンスの生成を防ぎ、メモリや処理リソースを節約。

<br>

# 注意点
+ スレッドセーフ: 複数のスレッドからアクセスする場合、適切な同期が必要。  
+ 密結合: グローバルな状態を持つため、システム全体が密結合になるリスクがあります。
+ テストの難しさ: グローバルな状態を持つため、テストが難しくなる場合があります。
+ 柔軟性の欠如: インスタンスの数を制限するため、柔軟性が低下する可能性があります。

<br>

## シングルトンパターンの実装例

下記２つのスクリプトのうち、GameManager.csを適当なGameObjectにアタッチして再生

<br>
SettingsManager.cs

```cs
using UnityEngine;

public class SettingsManager {
    // シングルトンインスタンス
    private static SettingsManager instance;

    // 設定データ
    private int soundVolume = 50;
    private bool isFullScreen = true;

    // コンストラクターをprivateにすることで外部からのインスタンス化を防止する
    private SettingsManager() { }

    // インスタンスの取得メソッド
    public static SettingsManager Instance {
        get {
            if (instance == null) {
                instance = new SettingsManager();
                //DontDestroyOnLoad(gameObject);
            }else{
                return instance;
            }
            
        }
    }

    // 設定の取得と設定
    public int SoundVolume {
        get { return soundVolume; }
        set { soundVolume = Mathf.Clamp(value, 0, 100); }
    }

    public bool IsFullScreen {
        get { return isFullScreen; }
        set { isFullScreen = value; }
    }

    // その他の設定管理メソッド
    public void SaveSettings() {
        // 設定の永続化など
        Debug.Log("Settings saved.");
    }

    public void LoadSettings() {
        // 設定の読み込みなど
        Debug.Log("Settings loaded.");
    }
}

```

<br>
GameManager.cs

```cs
using UnityEngine;

public class GameManager : MonoBehaviour {
    void Start() {
        // 設定マネージャーのインスタンスを取得
        SettingsManager settingsManager = SettingsManager.Instance;

        // 設定の利用
        Debug.Log("Current Sound Volume: " + settingsManager.SoundVolume);
        settingsManager.SoundVolume = 80;
        Debug.Log("New Sound Volume: " + settingsManager.SoundVolume);

        Debug.Log("Is FullScreen? " + settingsManager.IsFullScreen);
        settingsManager.IsFullScreen = false;
        Debug.Log("Set FullScreen to: " + settingsManager.IsFullScreen);

        // 保存と読み込み
        settingsManager.SaveSettings();
        settingsManager.LoadSettings();
    }
}

```

<br>


<div class="mermaid">


classDiagram
    class SettingsManager {
        -static instance : SettingsManager
        -soundVolume : int
        -isFullScreen : bool
        +Instance : SettingsManager
        +SoundVolume : int
        +IsFullScreen : bool
        +SaveSettings() : void
        +LoadSettings() : void
    }

    class GameManager {
        +Start() : void
    }

    GameManager --> SettingsManager : "Uses Singleton Instance"
    SettingsManager <-- SettingsManager : "Singleton Instance"

</div>

### 説明
+ SettingsManager クラスは Singleton パターンで実装されており、クラス内で一つのインスタンス (instance) しか存在しません。
+ GameManager は SettingsManager.Instance を介して、音量やフルスクリーン状態などの設定を管理・操作しています。
+ 図の中で、SettingsManager クラスはインスタンスの管理、設定の保存・読み込みの機能を持っています。また、GameManager はゲーム内でその設定を利用しています。

このように、SettingsManager クラスはゲーム全体で一度しか作成されないインスタンスを管理し、それを他のクラス（この場合は GameManager）が利用する仕組みになっています。



