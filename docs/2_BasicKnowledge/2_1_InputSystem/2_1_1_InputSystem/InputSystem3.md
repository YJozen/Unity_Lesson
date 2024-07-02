**InputSystem 1**

## 1.Input Systemを使用し、「Action」に登録した入力を検知する

キャラクターの『移動』や『ジャンプ』などといった操作を「Action」として扱います
 
<img src="images/3/unity-input-system-intro-v2-1.png.avif" width="50%" alt="" title="">

<br>  
<br>     
例えば、PCであればスペースキー、GamePadであればButton South(XBoxコントローラーのAボタン)を押せば、『ジャンプ』という「Action」を行うことができます

<img src="images/3/unity-input-system-intro-v2-2.png.avif" width="50%" alt="" title="">

<br>  
<br>    
＊　これから色々とややこしく感じるかもしれませんが、「InputActionというクラスを生成し、入力やAction設定をインスタンス化し、入力情報を操る」ということは変わりません。少しずつ慣れていって下さい。

---
## 2.　インスペクターから入力を設定し、「Action」の入力値をログ出力してみましょう

適当なゲームオブジェクトにアタッチしてください

InputActionExample.cs
```cs

using UnityEngine;
using UnityEngine.InputSystem;

public class InputActionExample : MonoBehaviour
{
    // Actionをインスペクターから編集できるようにする
    [SerializeField] private InputAction _action;

    // 有効時、実行
    private void OnEnable()
    {
        // InputActionを有効化。 これをしないと入力を受け取れないことに注意
        _action?.Enable();
    }

    // 無効時などに実行
    private void OnDisable()
    {
        // 無効化されるタイミングなどで、Actionを無効化
        _action?.Disable();
    }

    //破壊された時など
    private void OnDestroy()
    {
        _action?.Dispose();// 破壊された時などに、Actionを無効化
    }

    private void Update()
    {
        if (_action == null) return;

        // Actionの入力値（指定した型と一致するもの）を読み込む
        var value = _action.ReadValue<float>();

        // 入力値をログ出力
        Debug.Log($"Actionの入力値 : {value}");
    }
}

```

+ Disable()メソッド  
    入力アクションを一時的に無効化しますが、再度有効化(Enable())することが可能です。例えば、ゲームの一時停止やメニューの表示時に一時的に入力を無効化したい場合に使用します。  

+ Dispose()メソッド  
    入力アクションを完全に破棄し、リソースを解放します。これを呼び出すと、再度有効化することはできません。アプリケーションの終了時や、もうその入力アクションを一切使用しないことが確定している場合に使用します。

<br>

例として、スペースキーをBindingとして追加してみましょう。  
<br>
<br>


インスペクタからActionを編集していきます。

<img src="images/3/unity-input-system-intro-v2-3.png.avif" width="50%" alt="" title="">

Action右の「＋」アイコンをクリックし、Add Bindingを選択

<img src="images/3/unity-input-system-intro-v2-4.png.avif" width="50%" alt="" title="">

Path右のドロップダウンをクリック

<img src="images/3/unity-input-system-intro-v2-5.png.avif" width="50%" alt="" title="">


Listenボタンから実際に入力されたキーで割り当てる  
もしくは、その下の一覧から手動で選択  
スペースキーを割り当てて下さい

<img src="images/3/unity-input-system-intro-v2-6.png.avif" width="50%" alt="" title="">



float型（1軸）の入力値として受け取っているため、0か1の値が出力される。

ゲームパッドのトリガーボタンやスティックなどアナログ入力を割り当てた場合は0～1の間の値が出力される。
