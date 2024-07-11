コマンドパターン







## 定義:
 コマンドパターンは、要求をオブジェクトとしてカプセル化し、リクエストのパラメータ化、キューイング、ログ記録、および操作の取り消しを可能にするデザインパターンです。


定義
コマンドパターンは、要求をオブジェクトとしてカプセル化し、異なる要求、キューイング、ログ、および取り消し可能な操作をサポートするデザインパターンです。このパターンにより、要求をパラメータ化し、クライアントとレシーバーを分離できます。






## 目的:
 操作をオブジェクトとして扱い、操作を遅延実行したり、キューに入れたり、取り消したりできるようにする。


目的
要求をカプセル化: 操作をオブジェクトとしてカプセル化し、要求をパラメータ化する。
クライアントとレシーバーの分離: 要求の送信者（クライアント）とその要求の処理者（レシーバー）を分離する。
柔軟な操作管理: コマンドのキューイング、ログ、および取り消し可能な操作をサポートする。








使用例
GUIボタン: ユーザーがクリックしたときに実行されるアクションをカプセル化。
ゲーム開発: キャラクターの動きやアクションの履歴を記録し、取り消しややり直しを実現。
キューイングシステム: 処理をキューに入れ、順番に実行するシステム。

Unityでの実際の使用例
プレイヤーアクション: プレイヤーの操作をコマンドとしてカプセル化し、操作履歴の管理や操作の取り消しを可能にする。
メニューシステム: メニュー項目の選択やアクションをコマンドとしてカプセル化し、メニューの動的な変更を容易にする。
AI行動: AIの行動をコマンドとしてカプセル化し、行動の切り替えやシーケンスを管理する。





4. コマンドパターンの利点と欠点
利点
拡張性: 新しいコマンドを追加する際に、既存のコードを変更する必要がない。
取り消し/やり直し: コマンドの履歴を保持することで、取り消しややり直しが可能。
柔軟性: 同じインターフェースを持つ異なるコマンドを簡単に切り替えることができる。
欠点
複雑性の増加: コマンドクラスやインボーカークラスの数が増えるため、設計が複雑になる場合がある。
リソース消費: コマンドの履歴を保持するため、メモリを多く消費する可能性がある。






利点
柔軟性: 要求をオブジェクトとして扱うことで、柔軟な操作管理が可能になる。
拡張性: 新しいコマンドを追加する際に既存のコードを変更せずに拡張できる。
取り消し可能: 操作をオブジェクトとして保存することで、操作の取り消しや再実行が容易になる。
注意点
複雑性の増加: コマンドオブジェクトの導入により、システム全体の複雑性が増加する可能性がある。
メモリのオーバーヘッド: コマンドオブジェクトの生成と管理により、メモリのオーバーヘッドが増える可能性がある。
コマンドパターンの実装例
以下に、Unityでコマンドパターンを使用してプレイヤーアクションを管理する例を示します。












## コマンドパターンの実装
C#でのコマンドパターン実装
コマンドのインターフェース:

```cs
public interface ICommand {
    void Execute();
    void Undo();
}
```
具体的なコマンドクラス:

```cs
using UnityEngine;

public class MoveCommand : ICommand {
    private Transform _transform;
    private Vector3 _position;
    private Vector3 _previousPosition;

    public MoveCommand(Transform transform, Vector3 position) {
        _transform = transform;
        _position = position;
    }

    public void Execute() {
        _previousPosition = _transform.position;
        _transform.position = _position;
    }

    public void Undo() {
        _transform.position = _previousPosition;
    }
}
```
インボーカークラス:

```cs
using System.Collections.Generic;

public class CommandInvoker {
    private Stack<ICommand> _commandHistory = new Stack<ICommand>();

    public void ExecuteCommand(ICommand command) {
        command.Execute();
        _commandHistory.Push(command);
    }

    public void Undo() {
        if (_commandHistory.Count > 0) {
            var command = _commandHistory.Pop();
            command.Undo();
        }
    }
}
```
使用例:


```cs
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Transform player;
    private CommandInvoker _invoker;

    void Start() {
        _invoker = new CommandInvoker();
    }

    void Update() {
        if (Input.GetKeyDown(KeyCode.W)) {
            MovePlayer(new Vector3(0, 0, 1));
        } else if (Input.GetKeyDown(KeyCode.S)) {
            MovePlayer(new Vector3(0, 0, -1));
        } else if (Input.GetKeyDown(KeyCode.Z)) {
            _invoker.Undo();
        }
    }

    void MovePlayer(Vector3 direction) {
        var moveCommand = new MoveCommand(player, player.position + direction);
        _invoker.ExecuteCommand(moveCommand);
    }
}
```



5. 実際のコマンドパターンの使用例
Unityでのコマンドパターンの使用例
具体的なジャンプコマンドクラス:

```cs
using UnityEngine;

public class JumpCommand : ICommand {
    private Transform _transform;
    private float _jumpHeight;
    private Vector3 _previousPosition;

    public JumpCommand(Transform transform, float jumpHeight) {
        _transform = transform;
        _jumpHeight = jumpHeight;
    }

    public void Execute() {
        _previousPosition = _transform.position;
        _transform.position += Vector3.up * _jumpHeight;
    }

    public void Undo() {
        _transform.position = _previousPosition;
    }
}
```
ジャンプコマンドの使用例:

```cs
public class GameManager : MonoBehaviour {
    public Transform player;
    private CommandInvoker _invoker;

    void Start() {
        _invoker = new CommandInvoker();
    }

    void Update() {
        if (Input.GetKeyDown(KeyCode.W)) {
            MovePlayer(new Vector3(0, 0, 1));
        } else if (Input.GetKeyDown(KeyCode.S)) {
            MovePlayer(new Vector3(0, 0, -1));
        } else if (Input.GetKeyDown(KeyCode.Space)) {
            JumpPlayer(2.0f);
        } else if (Input.GetKeyDown(KeyCode.Z)) {
            _invoker.Undo();
        }
    }

    void MovePlayer(Vector3 direction) {
        var moveCommand = new MoveCommand(player, player.position + direction);
        _invoker.ExecuteCommand(moveCommand);
    }

    void JumpPlayer(float height) {
        var jumpCommand = new JumpCommand(player, height);
        _invoker.ExecuteCommand(jumpCommand);
    }
}
```

コマンドパターンは、操作をオブジェクトとして扱い、柔軟で再利用可能なコードを実現するためのデザインパターンです。このパターンを使用することで、操作の遅延実行や取り消し、キューイングなどを容易に実現できます。この授業を通じて、コマンドパターンの正しい使い方とその限界を理解し、適切な場面で効果的に活用できるようになります。











```cs
public interface ICommand
{
    void Execute();
}
```
```cs
public class MoveCommand : ICommand
{
    private Transform player;
    private Vector3 direction;

    public MoveCommand(Transform player, Vector3 direction)
    {
        this.player = player;
        this.direction = direction;
    }

    public void Execute()
    {
        player.Translate(direction);
    }
}
```
```cs
public class InputHandler : MonoBehaviour
{
    public Transform player;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.W))
        {
            ICommand moveUp = new MoveCommand(player, Vector3.up);
            moveUp.Execute();
        }
        // 他の入力処理...
    }
}
```
コマンドパターンを使用して、プレイヤーの入力を管理











コマンドインターフェース
csharp
Copy code
public interface ICommand {
    void Execute();
    void Undo();
}
具体的なコマンドクラス
csharp
Copy code
using UnityEngine;

public class MoveUpCommand : ICommand {
    private Transform player;
    private Vector3 previousPosition;

    public MoveUpCommand(Transform player) {
        this.player = player;
    }

    public void Execute() {
        previousPosition = player.position;
        player.position += Vector3.up;
    }

    public void Undo() {
        player.position = previousPosition;
    }
}

public class MoveDownCommand : ICommand {
    private Transform player;
    private Vector3 previousPosition;

    public MoveDownCommand(Transform player) {
        this.player = player;
    }

    public void Execute() {
        previousPosition = player.position;
        player.position += Vector3.down;
    }

    public void Undo() {
        player.position = previousPosition;
    }
}
コマンドの使用例
csharp
Copy code
using UnityEngine;
using System.Collections.Generic;

public class GameManager : MonoBehaviour {
    private Stack<ICommand> commandHistory = new Stack<ICommand>();

    public Transform player;

    void Update() {
        if (Input.GetKeyDown(KeyCode.W)) {
            ICommand moveUp = new MoveUpCommand(player);
            moveUp.Execute();
            commandHistory.Push(moveUp);
        }

        if (Input.GetKeyDown(KeyCode.S)) {
            ICommand moveDown = new MoveDownCommand(player);
            moveDown.Execute();
            commandHistory.Push(moveDown);
        }

        if (Input.GetKeyDown(KeyCode.Z) && commandHistory.Count > 0) {
            ICommand lastCommand = commandHistory.Pop();
            lastCommand.Undo();
        }
    }
}