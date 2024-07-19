## 1.Input Systemを使用し、「Action」に登録した入力を検知する

キャラクターの『移動』や『ジャンプ』などといった操作を「Action」として扱います
 
<img src="images/3/unity-input-system-intro-v2-1.png.avif" width="70%" alt="" title="">

<br>  
<br>     
例えば、PCであればスペースキー、GamePadであればButton South(XBoxコントローラーならAボタン)を押せば、『ジャンプ』という「Action」を行うことができます

<img src="images/3/unity-input-system-intro-v2-2.png.avif" width="70%" alt="" title="">

<br>  
<br>    
＊　これから色々とややこしく感じるかもしれませんが、   
「InputActionというクラスを作成し、入力やActionの設定をインスタンス化し、入力情報を操る」という考え方は変わりません。  
先の文章の意味も今は理解不能でも少しずつ慣れていきましょう。

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

+ `Disable()`メソッド  
    入力アクションを一時的に無効化しますが、再度有効化(Enable())することが可能です。例えば、ゲームの一時停止やメニューの表示時に一時的に入力を無効化したい場合に使用します。  

+ `Dispose()`メソッド  
    入力アクションを完全に破棄し、リソースを解放します。これを呼び出すと、再度有効化することはできません。アプリケーションの終了時や、もうその入力アクションを一切使用しないことが確定している場合に使用します。

<br>

例として、スペースキーをBindingとして追加してみましょう。  
<br>
<br>


インスペクタからActionを編集していきます。

<img src="images/3/unity-input-system-intro-v2-3.png.avif" width="70%" alt="" title="">

Action右の「＋」アイコンをクリックし、Add Bindingを選択

<img src="images/3/unity-input-system-intro-v2-4.png.avif" width="70%" alt="" title="">

Path右のドロップダウンをクリック

<img src="images/3/unity-input-system-intro-v2-5.png.avif" width="70%" alt="" title="">


Listenボタンから実際に入力されたキーで割り当てることができます。    
もしくは、その下の一覧から手動で選択することもできます。    
スペースキーを割り当ててみて下さい

<img src="images/3/unity-input-system-intro-v2-6.png.avif" width="70%" alt="" title="">

<br>

以下のように設定できたら実行確認してください

<img src="images/3/unity-input-system-intro-v2-m2.mp4.gif" width="70%" alt="" title="">

float型（1軸）の入力値として受け取っているため、0か1の値が出力されると思います。

ゲームパッドのトリガーボタンやスティックなどアナログ入力を割り当てた場合は0～1の間の値が出力されます。



## スクリプトについて

```cs
// Actionをインスペクターから編集できるようにする
[SerializeField] private InputAction _action;
```
インスペクターからActionを編集できるようにフィールドを定義しています。  
その後、インスペクターからActionを設定すると、実行時にInputActionインスタンスが生成されます。

ただし、このままでは入力値を受け取れず、以下処理でオブジェクトが有効化されたタイミングなどでInputAction自身を有効化する必要があります。

```cs
// 有効化
private void OnEnable()
{
    // InputActionを有効化
    // これをしないと入力を受け取れないことに注意
    _action?.Enable();
}
```
これにより、次のコードでActionから入力値を受け取れるようになります。

```cs
// Actionの入力値を読み込む
var value = _action.ReadValue<float>();
```

InputAction.ReadValue<T>メソッドによって入力値を受け取れますが、テンプレート引数はActionで指定した型と一致する必要があります。(https://docs.unity3d.com/Packages/com.unity.inputsystem@1.5/api/UnityEngine.InputSystem.InputAction.html#UnityEngine_InputSystem_InputAction_ReadValue__1)

例ではスペースキー（1軸入力）なので、float型としています。

