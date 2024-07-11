# コマンドパターン

## 定義
操作（コマンド）をオブジェクトとしてカプセル化し、操作の実行と操作の内容を分離することを目的としています。  
これにより、操作の履歴を保持したり、操作を取り消したり、再実行したりすることが容易になります。

<br>

## コマンドパターンの構成要素
+ <b>コマンドインターフェース（ICommand）</b>:   
コマンドオブジェクトが実装すべきインターフェースを定義します。一般的には、Executeメソッドを持ちます。  

+ <b>具体的なコマンドクラス（ConcreteCommand）</b>:   
コマンドインターフェースを実装し、特定のアクションを実行します。

+ <b>レシーバー（Receiver）</b>:   
  コマンドが実行される対象オブジェクトです。

+ <b>インボーカー（Invoker）</b>:   
コマンドを呼び出す役割を持ちます。コマンドオブジェクトを保持し、適切なタイミングでExecuteメソッドを呼び出します。

+ <b>クライアント（Client）</b>:  
 コマンド、レシーバー、インボーカーを構成して操作を実行するクラスです。

<br>


## 使用例
+ プレイヤーアクション: プレイヤーの操作をコマンドとしてカプセル化し、操作履歴の管理や操作の取り消しを可能にする。
+ メニューシステム: メニュー項目の選択やアクションをコマンドとしてカプセル化し、メニューの動的な変更を容易にする。
+ AI行動: AIの行動をコマンドとしてカプセル化し、行動の切り替えやシーケンスを管理する。

<br>

## 利点
+ 拡張性: 新しいコマンドを追加する際に、既存のコードを変更する必要がない。
+ 取り消し/やり直し: コマンドの履歴を保持することで、取り消しややり直しが可能。
+ 柔軟性: 同じインターフェースを持つ異なるコマンドを簡単に切り替えることができる。

<br>

## 欠点
+ 複雑性の増加: コマンドクラスやインボーカークラスの数が増えるため、設計が複雑になる場合がある。
+ リソース消費: コマンドの履歴を保持するため、メモリを多く消費する可能性がある。




## コマンドパターンの実装例

コマンドインターフェース

```cs
public interface ICommand {
    void Execute();
    void Undo();
}
```


具体的なコマンドクラス

```cs
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

```


コマンドの使用例
```cs
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

```






<br>

<br>



<br>

<br>

## ちょっとだけ変えたプログラム1


<br>

<br>

<br>

MoveUpCommand と　MoveDownCommand　の内容が重複してるので１つにまとめてみた

<br>

```cs
public interface ICommand {
    void Execute();
    void Undo();
}
```
```cs
using UnityEngine;

public class MoveCommand : ICommand {
    private Transform player;
    private Vector3 direction;
    private Vector3 previousPosition;

    public MoveCommand(Transform player, Vector3 direction) {
        this.player = player;
        this.direction = direction;
    }

    public void Execute() {
        previousPosition = player.position;
        player.position += direction;
    }

    public void Undo() {
        player.position = previousPosition;
    }
}
```

```cs
using UnityEngine;
using System.Collections.Generic;

public class GameManager : MonoBehaviour {
    private Stack<ICommand> commandHistory = new Stack<ICommand>();

    public Transform player;

    void Update() {
        if (Input.GetKeyDown(KeyCode.W)) {
            ExecuteCommand(new MoveCommand(player, Vector3.up));
        }

        if (Input.GetKeyDown(KeyCode.S)) {
            ExecuteCommand(new MoveCommand(player, Vector3.down));
        }

        if (Input.GetKeyDown(KeyCode.A)) {
            ExecuteCommand(new MoveCommand(player, Vector3.left));
        }

        if (Input.GetKeyDown(KeyCode.D)) {
            ExecuteCommand(new MoveCommand(player, Vector3.right));
        }

        if (Input.GetKeyDown(KeyCode.Z) && commandHistory.Count > 0) {
            UndoLastCommand();
        }
    }

    void ExecuteCommand(ICommand command) {
        command.Execute();
        commandHistory.Push(command);
    }

    void UndoLastCommand() {
        ICommand lastCommand = commandHistory.Pop();
        lastCommand.Undo();
    }
}
```


<br>

<br>



<br>

<br>

## ちょっとだけ変えたプログラム2

<br>

<br>

コマンドの管理を分離してみた

<br>
<br>

<br>
コマンドインターフェース

```cs
public interface ICommand {
    void Execute();
    void Undo();
}
```
<br>
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
<br>
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

<br>
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
