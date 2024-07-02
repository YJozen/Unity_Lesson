# C#機能 Task

ここからが本題。　　

async/awaitにキャンセル処理をつける場合はどうしたらいいのか?   

async/awaitの「キャンセル方法」を、C#の機能である「Task」を使って見ていく。

<br>

### async/awaitに「キャンセル処理」をつける場合はどうすればいいのか?

結論からいうと、async/awaitにおけるキャンセル処理では、次の一連の流れをすべて実装する必要があります。

```
① CancellationTokenを適切なタイミングで生成し、キャンセルしたいタイミングでキャンセル状態にする  
 
② asyncメソッドを定義するときはCancellationTokenを引数にとる  

③ awaitするときは、await対象にCancellationTokenが渡せるなら渡す  

④ await対象にCancellationTokenが渡せないのであれば、CancellationToken.ThrowIfCancellationRequested()を適宜呼び出す  

⑤　async/awaitとtry-catchを併用する場合はOperationCancelledExceptionの扱いを考える
```

<br>

# ①CancellationTokenを適切なタイミングで生成し、キャンセルしたいタイミングでキャンセル状態にする 

`CancellationToken`とは、async/awaitにおいて「処理のキャンセルを伝えるためのオブジェクト」 

このCancellationTokenを適切なタイミングで生成し、
処理を中止したいタイミングで「キャンセル状態」に変更することでasync/awaitをキャンセルさせることができます


具体的には、CancellationTokenSourceを使ってCancellationTokenを生成します。  
この親クラス`CancellationTokenSource`のCancel()を呼び出すことで、
ここから発行されたCancellationTokenがキャンセル状態になります。


```cs
using System;
using System.Threading;
using UnityEngine;

namespace CancelSamples
{
    /// <summary> たとえば、このクラスのインスタンスの寿命に紐づけたCancellationTokenが欲しい場合 </summary>
    public class AsyncProcessSample1 : MonoBehaviour
    {
        [SerializeField] KeyCode _destroyObjectKey = KeyCode.D;       
        private readonly CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();// CancellationTokenSourceを用意

        // CancellationToken(キャンセル状態を把握できるクラス)  を CancellationTokenSourceから生成。getできるように
        //public CancellationToken Token => _cancellationTokenSource.Token;

        private void Update() {
            if (Input.GetKeyDown(_destroyObjectKey)) {
                Destroy(this.gameObject);
                Debug.Log("Destroy GameObject");
            }
        }

        void OnDestroy() {
            _cancellationTokenSource.Cancel();// クラスを破棄するタイミング・処理をキャンセルしたいタイミングでキャンセル実行            
            _cancellationTokenSource.Dispose();// 破棄
            Debug.Log("キャンセル処理");
        }
    }
}

```


---

## ②asyncメソッドを定義するときはCancellationTokenを引数にとる   

CancellationTokenが用意できているなら、これをasyncメソッドに渡す必要があります。
そのためにもasyncメソッドはCancellationTokenを引数にとるようにしましょう。

```cs
using System;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;


namespace CancelSamples
{
    public class AsyncProcessSample2 : MonoBehaviour
    {
        [SerializeField] KeyCode _destroyObjectKey = KeyCode.D;       
        private readonly CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();// CancellationTokenSourceを用意

        // CancellationToken(キャンセル状態を把握できるクラス) を CancellationTokenSourceから生成。getできるように
        //public CancellationToken Token => _cancellationTokenSource.Token;

        private void Update() {
            if (Input.GetKeyDown(_destroyObjectKey)) {
                Destroy(this.gameObject);
                Debug.Log("Destroy GameObject");
            }
        }

        void OnDestroy() {
            _cancellationTokenSource.Cancel();// クラスを破棄するタイミング・処理をキャンセルしたいタイミングでキャンセル実行            
            _cancellationTokenSource.Dispose();// トークンソースを破棄
            Debug.Log("キャンセル処理");
        }

        /// <summary>
        /// asyncメソッドを定義した場合は「CancellationToken」を引数に取る
        /// 作法としては引数の一番最後をCancellationTokenにすることがほとんど
        /// あとメソッド名も ~Async にしておく
        /// </summary>
        //public async ValueTask DelayRunAsync(Action action, CancellationToken token) {
        //    // これから何か処理をする
        //    //await 時間のかかる処理・待つ処理;
        //}
    }
}


```

---

## ③awaitするときは、await対象にCancellationTokenが渡せるなら渡す 


```cs

using System;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

namespace CancelSamples
{
    public class AsyncProcessSample3 : MonoBehaviour
    {
        [SerializeField] KeyCode _destroyObjectKey = KeyCode.D;       
        private readonly CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();// CancellationTokenSourceを用意        
        public CancellationToken Token => _cancellationTokenSource.Token;  // CancellationToken(キャンセル状態を把握できるクラス)  を CancellationTokenSourceから生成。getできるように

        private void Start()
        {
            //処理の起点　処理を実行
            _ = PrintMessagesAsync(Token);//変数が実際には使用されていないことを明示的に示しただけ
        }

        private void Update() {
            if (Input.GetKeyDown(_destroyObjectKey)) {
                Destroy(this.gameObject);
                Debug.Log("Destroy GameObject");
            }
        }

        /// <summary>
        /// asyncメソッドを定義した場合はCancellationTokenを引数に取る
        /// 作法としては引数の一番最後をCancellationTokenにすることがほとんど
        /// あとメソッド名も ~Async にしておく
        /// </summary>
        public async ValueTask PrintMessagesAsync(CancellationToken token) {
            // これから何か処理をする　　// 受け取ったTokenはすべて下流にも渡す
            await DelayRunAsync(() => Debug.Log("Hello!"), token);//処理を待って、CancellationTokenSource.Token(キャンセル状態を把握できるクラス)を次々に渡していく
            await DelayRunAsync(() => Debug.Log("World!"), token);
            await DelayRunAsync(() => Debug.Log("Bye!")  , token);
        }

        /// <summary> 1秒後にActionを実行する </summary>
        private async ValueTask DelayRunAsync(Action action, CancellationToken token) {            
            await Task.Delay(TimeSpan.FromSeconds(1), token);// 1秒待つ、キャンセル処理を仕込む
            action();
        }

        void OnDestroy() {
            _cancellationTokenSource.Cancel();// クラスを破棄するタイミング・処理をキャンセルしたいタイミングでキャンセル実行            
            _cancellationTokenSource.Dispose();// 破棄
            Debug.Log("キャンセル処理");
        }
    }
}

```

---

## ④await対象に`CancellationToken`が渡せないのであれば、`CancellationToken.ThrowIfCancellationRequested()`を適宜呼び出す
`CancellationToken.ThrowIfCancellationRequested()`メソッドは、
「`CancellationToken`がキャンセル状態になっていたときに、`OperationCanceledException`を発行する」 というメソッドです。

あとで後述しますが、async/awaitでは（正確にいうとTaskたちは）
`OperationCanceledException`を特殊な例外として扱っています。

もしawait実行時に`CancellationToken`が相手に渡せない場合は、キャンセル時にこの`OperationCanceledException`を発行してあげる必要があります。  
これらを自動でやってくれるのが`CancellationToken.ThrowIfCancellationRequested()`です。


```cs

using System;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

namespace CancelSamples
{
    public class AsyncProcessSample4 : MonoBehaviour
    {
        [SerializeField] KeyCode _destroyObjectKey = KeyCode.D;       
        private readonly CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();// CancellationTokenSourceを用意        
        public CancellationToken Token => _cancellationTokenSource.Token;//キャンセル状態を把握

        private void Start()
        {
            _ = PrintMessagesAsync(Token);//変数が実際には使用されていないことを明示的に示しただけ
        }

        private void Update() {
            if (Input.GetKeyDown(_destroyObjectKey)) {
                Destroy(this.gameObject);
                Debug.Log("Destroy GameObject");
            }
        }

        public async ValueTask PrintMessagesAsync(CancellationToken token) {
            // これから何か処理をする　　// 受け取ったTokenはすべて下流にも渡す
            await DelayRunAsync(() => Debug.Log("Hello!"), token);//処理を待って、CancellationTokenSource.Token(キャンセル状態を把握できるクラス)を次々に渡していく
            await DelayRunAsync(() => Debug.Log("World!"), token);
            await DelayRunAsync(() => Debug.Log("Bye!")  , token);
        }

        /// <summary> 1秒後にActionを実行する </summary>
        private async ValueTask DelayRunAsync(Action action, CancellationToken token) {            
            await Task.Delay(TimeSpan.FromSeconds(1), token);// 1秒待つ、キャンセル処理を仕込む
            action();
        }

        void OnDestroy() {
            _cancellationTokenSource.Cancel();// クラスを破棄するタイミング・処理をキャンセルしたいタイミングでキャンセル実行            
            _cancellationTokenSource.Dispose();// 破棄
            Debug.Log("キャンセル処理");
        }

        // 何か別のライブラリの非同期メソッドを実行したいが、そのライブラリのお行儀が悪く
        // CancellationTokenを渡すことができない場合など
        //private async ValueTask UseOtherFrameworkAsync(CancellationToken token) {

            // NankanoAsync()自体は走り出したらキャンセルできないので諦めるとして、
            //await なんかのライブラリ.NankanoAsync();

            // キャンセル状態になっていたらこの時点で処理を止める
            // （例外が発行されてここで中断される）
            //token.ThrowIfCancellationRequested();

            // SugoiAsync()も走り出したら後から止めることはできない（諦める）
            //await なんかのライブラリ.SugoiAsync();
        //}
    }
}


```

---

## ⑤async/awaitとtry-catchを併用する場合はOperationCancelledExceptionの扱いを考える

`OperationCancelledException`はC#において特殊な例外として設定されています。
この例外は「asyncメソッド内から外に向かって発行された場合、そのメソッドに紐づいたTask（ValueTask/UniTask）はキャンセル扱いになる」という性質があります。

```cs

using System;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;



namespace CancelSamples
{
    public class AsyncProcessSample5 : MonoBehaviour
    {
        [SerializeField] KeyCode _destroyObjectKey = KeyCode.D;
        [SerializeField] KeyCode _confirmKey       = KeyCode.C;
        private readonly CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();    
        public CancellationToken Token => _cancellationTokenSource.Token; 

        private void Start()
        {
            _ = PrintMessagesAsync(Token);//変数が実際には使用されていないことを明示的に示しただけ
        }

        private void Update() {
            if (Input.GetKeyDown(_destroyObjectKey)) {
                Destroy(this.gameObject);
                Debug.Log("Destroy GameObject");
            }
            if (Input.GetKeyDown(_confirmKey)) {
                Debug.Log("Destroy GameObject");
            }

        }

        public async ValueTask PrintMessagesAsync(CancellationToken token) {
            // これから何か処理をする　　// 受け取ったTokenはすべて下流にも渡す
            await DelayRunAsync(() => Debug.Log("Hello!"), token);//処理を待って、CancellationTokenSource.Token(キャンセル状態を把握できるクラス)を次々に渡していく
            await DelayRunAsync(() => Debug.Log("World!"), token);
            await DelayRunAsync(() => Debug.Log("Bye!")  , token);
        }

        /// <summary> 1秒後にActionを実行する </summary>
        private async ValueTask DelayRunAsync(Action action, CancellationToken token) {            
            await Task.Delay(TimeSpan.FromSeconds(1), token);// 1秒待つ、キャンセル処理を仕込む
            action();
        }

        void OnDestroy() {
            _cancellationTokenSource.Cancel();// クラスを破棄するタイミング・処理をキャンセルしたいタイミングでキャンセル実行            
            _cancellationTokenSource.Dispose();// 破棄
            Debug.Log("キャンセル処理");
        }

        //private static async ValueTask TestAsync(CancellationToken token) {
        //    try {
        //        await HogeAsync(token);
        //    }
        //    // 例外のうち OperationCanceledException は「キャッチしない」
        //    catch (Exception ex) when (!(ex is OperationCanceledException)) {
        //        Console.WriteLine(ex);
        //    }
        //}


        //// 何か別のライブラリの非同期メソッドを実行したいが、そのライブラリのお行儀が悪く
        //// CancellationTokenを渡すことができない場合など
        //private async ValueTask UseOtherFrameworkAsync(CancellationToken token) {
        //    // NankanoAsync()自体は走り出したらキャンセルできないので諦めるとして、
        //    await なんかのライブラリ.NankanoAsync();

        //    // キャンセル状態になっていたらこの時点で処理を止める
        //    // （例外が発行されてここで中断される）
        //    token.ThrowIfCancellationRequested();

        //    // SugoiAsync()も走り出したら後から止めることはできない（諦める）
        //    await なんかのライブラリ.SugoiAsync();
        //}
    }
}

```
