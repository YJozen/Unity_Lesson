<head>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>

# MVPパターンの定義
MVP (Model-View-Presenter) パターンは、ユーザーインターフェース (UI) ロジックとビジネスロジックを分離し、アプリケーションの保守性とテスト性を向上させる設計パターンです。特にUIの要素が頻繁に変化する場合に有効で、視覚部分 (View) とロジック部分 (Presenter) の結びつきを最小限にします。


<br>

<br>


# 目的
MVPパターンの目的は、以下のようにロジックを明確に分けることで、コードのテストが容易になり、UIの変更が頻繁に発生してもビジネスロジックに影響を与えないようにすることです：
1. **Model**: データやビジネスロジックを担当
2. **View**: UIの表示を担当
3. **Presenter**: ViewとModelを繋げ、UIロジックを実装

<br>

<br>

# サンプルコード

### 1. **Model.cs**
```cs
public class PlayerModel {
    public string Name { get; set; }
    public int Score { get; set; }
}
```

### 2. **View.cs**
```cs
public interface IPlayerView {
    void UpdatePlayerInfo(string playerName, int playerScore);
}

public class PlayerView : MonoBehaviour, IPlayerView {
    public Text playerNameText;
    public Text playerScoreText;

    public void UpdatePlayerInfo(string playerName, int playerScore) {
        playerNameText.text = "Player: " + playerName;
        playerScoreText.text = "Score: " + playerScore.ToString();
    }
}
```

### 3. **Presenter.cs**
```cs
public class PlayerPresenter {
    private IPlayerView view;
    private PlayerModel model;

    public PlayerPresenter(IPlayerView view, PlayerModel model) {
        this.view = view;
        this.model = model;
    }

    public void UpdateView() {
        view.UpdatePlayerInfo(model.Name, model.Score);
    }

    public void SetPlayerData(string playerName, int playerScore) {
        model.Name = playerName;
        model.Score = playerScore;
        UpdateView();
    }
}
```

### 4. **GameManager.cs**
```cs
public class GameManager : MonoBehaviour {
    private PlayerPresenter playerPresenter;

    void Start() {
        PlayerModel playerModel = new PlayerModel();
        PlayerView playerView = FindObjectOfType<PlayerView>();
        playerPresenter = new PlayerPresenter(playerView, playerModel);

        playerPresenter.SetPlayerData("John", 100);
    }
}
```


<div class="mermaid">
classDiagram
    class PlayerModel {
        - string Name
        - int Score
    }

    class IPlayerView {
        <<interface>>
        + UpdatePlayerInfo(string playerName, int playerScore)
    }

    class PlayerView {
        + Text playerNameText
        + Text playerScoreText
        + UpdatePlayerInfo(string playerName, int playerScore)
    }

    class PlayerPresenter {
        - IPlayerView view
        - PlayerModel model
        + UpdateView()
        + SetPlayerData(string playerName, int playerScore)
    }

    class GameManager {
        + PlayerPresenter playerPresenter
    }

    PlayerPresenter --> IPlayerView
    PlayerPresenter --> PlayerModel
    GameManager --> PlayerPresenter
    PlayerView --> IPlayerView
</div>

<br>

<br>

# 解説
- **Model**:   
`PlayerModel` はデータを持つクラスで、プレイヤーの名前やスコアなどのビジネスロジックを管理します。
- **View**:   
`IPlayerView` インターフェースを実装する `PlayerView` は、UI部分を担当し、プレイヤーの情報を画面に表示します。
- **Presenter**:  
 `PlayerPresenter` は、ModelとViewを結びつけ、プレイヤーの情報を更新したりUIに反映させます。
- **GameManager**:   
`PlayerPresenter` を作成し、アプリケーションの起動時にViewとModelを初期化します。

### 利点
1. **ロジックの分離**: ビジネスロジックとUIロジックが分離されているため、各コンポーネントが独立して保守できます。
2. **テスト容易性**: Viewがインターフェースに基づいているため、PresenterとModelを単体テストしやすくなります。
3. **UIの柔軟性**: UIの変更が頻繁に行われる場合も、ビジネスロジックに影響を与えずに変更可能です。

### 欠点
1. **コードの複雑化**: 小規模なアプリケーションでは、クラスの分割が複雑さを増してしまう可能性があります。
2. **パフォーマンスへの影響**: 複雑なUIや頻繁なデータ更新の場合、MVPパターンの導入によって処理が増え、パフォーマンスに影響が出ることがあります。

### 注意点
- 小規模なプロジェクトには適していない場合があります。UIとビジネスロジックの複雑さに応じて採用を検討するべきです。
- Presenterが複雑化しすぎないようにするため、必要に応じてヘルパークラスなどでロジックを分割することが推奨されます。