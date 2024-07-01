**UniTask**

# キャンセル
C#におけるasync/awaitを使う上で、絶対に意識しないといけないものは「キャンセル処理」です。  
正しく処理をキャンセルしないとメモリリークを起こしたり、デッドロックやデータ不整合を引き起こす可能性があります。

## キャンセル1

```cs
using UnityEngine;
using Cysharp.Threading.Tasks;
using System;
using System.Threading;
using UnityEngine.SceneManagement;
using Unity.VisualScripting.Antlr3.Runtime;

//CancellationTokenを使用して非同期タスクを監視し、必要な場合にキャンセルします。
//OnDestroyメソッド内でキャンセルを行い、メモリリークを防ぎます。
namespace AsyncSample
{
    public class CancelExample1 : MonoBehaviour
    {
        [SerializeField] KeyCode _destroyObjectKey = KeyCode.D;
        private CancellationTokenSource cancellationTokenSource;

        private async void Start() {
            Debug.Log("開始");
            cancellationTokenSource = new CancellationTokenSource();//キャンセルしたことを把握するための変数
            try {
                //非同期処理を実行してみる
                await DoSomethingCancelableAsync(cancellationTokenSource.Token);
                Debug.Log("本筋処理終了");
            }

            catch (OperationCanceledException ex) when (ex.CancellationToken == cancellationTokenSource.Token) {

                Debug.Log(ex);
                Debug.Log("Operation canceled");

            }
            //catch (OperationCanceledException) {
            //    Debug.Log("Operation canceled");
            //}
        }

        private void Update()
        {        
            if (Input.GetKeyDown(_destroyObjectKey)) {
                Destroy(this.gameObject);//キャンセル処理したらどうなるか確認用
                Debug.Log("Destroy GameObject");
            }   
        }

        private async UniTask DoSomethingCancelableAsync(CancellationToken cancellationToken) {
            Debug.Log("非同期メソッド開始");
            await UniTask.Delay(5000); // 5秒待つ (この時間に処理を止めてみる。オブジェクトを削除してみてください）
                                       // キャンセルトークンを監視し続けて、タスクをキャンセルしてみる
            cancellationToken.ThrowIfCancellationRequested();// タスク内部でキャンセル状態を確認
            Debug.Log("UniTask operation completed");
        }

        private void OnDestroy() {
            // シーン遷移などでGameObjectが破棄される際にキャンセル処理を行う。
            cancellationTokenSource?.Cancel();
            Debug.Log("UniTask operation の　キャンセル処理");
        }
    }
}


```


## キャンセル2

```cs
using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityEngine;

//MoveAsync()(目標地点までの移動)をタイムアウトさせてみます。
namespace Timeouts
{
    public class CancelExample2_TimeOut1 : MonoBehaviour
    {
        private void Start()
        {
            _ = MoveStart();
            Debug.Log("先に実行される");
        }

        private async UniTaskVoid MoveStart() {
            transform.position = Vector3.zero;
            //UniTaskはシーンの切り替えや、オブジェクトの破棄では止まらない
            //コルーチンは、StartCoroutineしたGameObjectに紐づくんですが、
            //UniTaskはそういった紐づけはありません。
            //UniTaskの関数を呼ぶ時に引数でthis.GetCancellationTokenOnDestroy()を渡して止める必要がある
            var token = this.GetCancellationTokenOnDestroy();//トークン

            Debug.Log("移動開始！");
            await MoveAsync(new Vector3(8, 0, 0), token);//対象座標まで移動させるメソッド
            Debug.Log("移動終了！");
        }

        /// <summary>オブジェクトが対象座標に到着するまで移動させる</summary>
        private async UniTask MoveAsync(Vector3 targetPosition, CancellationToken cancellationToken) {
            while (true) {               
                var deltaPosition = (targetPosition - transform.position);// 目的の座標　と　自分の座標との差分                
                if (deltaPosition.magnitude < 0.1f) return;               // 0.1m以内に近づいていたら終了
               
                var moveSpeed = 1.0f;                    // 移動速度                
                var direction = deltaPosition.normalized;// 移動方向                
                transform.position += direction * moveSpeed * Time.deltaTime;// 移動させる                
                await UniTask.Yield(cancellationToken);// UniTask.Yieldで1F待つ
            }
        }
    }
}


```

## キャンセル3

```cs
using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityEngine;

namespace Timeouts
{
    public class CancelExample2_TimeOut2 : MonoBehaviour
    {
        private void Start() {
            _ = MoveStart();
            Debug.Log("先に実行される");
        }

        private async UniTaskVoid MoveStart() {
            transform.position = Vector3.zero;
            var timeoutController = new TimeoutController();// TimeoutControllerを生成
            Debug.Log("移動開始！");

            try {
                // TimeoutControllerから指定時間後にキャンセルされるCancellationTokenを生成
                var timeoutToken = timeoutController.Timeout(TimeSpan.FromSeconds(1));//タイムアウト設定

                // このGameObjectが破棄されたらキャンセルされるCancellationTokenを生成
                var destroyToken = this.GetCancellationTokenOnDestroy();

                // タイムアウトとDestroyのどちらもでキャンセルするようにTokenを生成
                var linkedToken = CancellationTokenSource.CreateLinkedTokenSource(timeoutToken, destroyToken).Token;

                // 1秒でタイムアウトさせてみる
                await MoveAsync(new Vector3(8, 0, 0), linkedToken);

                // 使い終わったらReset()してあげる必要あり
                timeoutController.Reset();

                Debug.Log("移動終了");
            }
            catch (Exception ex) {
                Debug.LogException(ex);//警告にする必要はない
                if (timeoutController.IsTimeout()) {
                    Debug.LogError("Timeoutによるキャンセルです");
                }
            }
        }

        /// <summary>オブジェクトが対象座標に到着するまで移動させる</summary>
        private async UniTask MoveAsync(Vector3 targetPosition, CancellationToken ct) {
            while (true) {                
                var deltaPosition = (targetPosition - transform.position);// 目的座標までの差分        
                if (deltaPosition.magnitude < 0.1f) return;// 0.1m以内に近づいていたら終了               
                var moveSpeed = 1.0f;                      // 移動速度              
                var direction = deltaPosition.normalized;  // 移動方向              
                transform.position += direction * moveSpeed * Time.deltaTime;// 移動させる              
                await UniTask.Yield(ct);// 1F待つ
            }
        }
    }
}


```




## キャンセル4

簡単なボタンUIを用意

<img src="images/2_4.png" width="50%" alt="" title="">
<br>



```cs
using UnityEngine;
using Cysharp.Threading.Tasks;
using UnityEngine.UI;
using System.Threading;
using System;

public class CancelExample3_UIButton : MonoBehaviour
{
    private CancellationTokenSource cancellationTokenSource;
    private bool isTaskRunning;

    [SerializeField] private Button startButton;
    [SerializeField] private Button cancelButton;

    private void Start() {
        Debug.Log("Startメソッド開始");

        cancellationTokenSource = new CancellationTokenSource();
        isTaskRunning = false;//初期設定

        startButton.onClick.AddListener(StartAsyncOperation);  // 開始ボタンにメソッドを設定        
        cancelButton.onClick.AddListener(CancelAsyncOperation);// キャンセルボタンにメソッドを設定
    }

    //スタートボタンを押した時
    private async void StartAsyncOperation() {
        if (isTaskRunning) {//bool値でタスクが走っているかどうかを見る
            Debug.Log("Task is already running.");
            return;
        }

        Debug.Log("Starting async operation");

        try {
            isTaskRunning = true; //           
            await DoSomethingCancelableAsync(cancellationTokenSource.Token);// キャンセル可能な非同期メソッドを呼び出す
            Debug.Log("Async method completed");//非同期メソッドの処理終了
        }
        catch (OperationCanceledException) {//トークンのキャンセルで呼び出される
            Debug.Log("Operation canceled");
        }
        finally {
            isTaskRunning = false;//最終的にはfalseに戻しとく
        }
    }

    private async UniTask DoSomethingCancelableAsync(CancellationToken cancellationToken) {
        Debug.Log("Doing something asynchronously");

        try {
            // キャンセルトークンを監視してタスクをキャンセル可能にする
            await UniTask.Delay(5000); // 5秒待つ

            // タスク内部でキャンセル状態を確認
            //ここまでに実行された関数はキャンセルできないが、
            //ここまでにキャンセルが呼ばれたかどうかの確認ができる。
            //ここより下に書くと確認ができないので、エラーが出そうなメソッドなどあるなら何回か書く必要がある
            cancellationToken.ThrowIfCancellationRequested();

            Debug.Log("Async operation completed");
        }
        catch (OperationCanceledException) {//タスクのキャンセルが確認できたら、ここが実行される
            Debug.Log("Async operation canceled");
            throw;
            // OperationCanceledExceptionを再スローしてキャッチできるようにする
            //throwすることで元のキャンセル例外が保持されます。
            //これにより、キャンセルが発生した元のコンテキストやスタックトレースが維持され、
            //デバッグやログのトラッキングが容易になります。
            //簡単に言えば、throw; ステートメントは、キャンセルが要求された場合に、
            //その要求を正しく処理し、例外がキャッチされたことを示すために使用されます。
        }
    }

    //キャンセルボタンを押した時
    private void CancelAsyncOperation() {
        if (isTaskRunning) {
            // タスクが実行中であればキャンセルを実行
            cancellationTokenSource.Cancel();
        }
    }
}


```



### 「結論」
asyncメソッドはCancellationTokenを引数に取るべき
await対象が引数にCancellationTokenを要求する場合は省略せずに渡すべき
OperationCanceledExceptionの取り扱いを意識するべき


### 「解説」
「async / awaitにおけるキャンセル」とは2つの意味があります。
・awaitをキャンセルする
・await対象の実行中の処理をキャンセルする
「キャンセル処理」といえばこの2つをまとめて指すことが多いのですが、文脈によっては片方しか意味していないこともあります。

①「awaitをキャンセルする」
awaitをキャンセルするとは、「今裏で実行している処理そのものは止めず、待つのをやめる」という意味です。
「処理が終わるのを待つのを諦める」に近いです。
たとえば「レストランで注文して料理を作ってもらっているが、時間がかかりすぎているので諦めて店員に何も伝えずに店を出てきた（待つのを止めた）」みたいな。

②「await対象の実行中の処理をキャンセルする」
こちらは「裏で走っている処理を止める」という、おそらく「キャンセル処理」という名称からイメージする内容だと思います。
先程のレストランの例でいうと、「レストランで注文して料理を作ってもらっているが、気が変わったので店員に伝えて作るのを止めてもらった」みたいな。

                                                                                                                                                                                                          
### クイズ

async / awaitのキャンセル処理では、このどちらを意識すればいいのか
→答:両方意識してください。  
「awaitはキャンセルしたが、処理自体はスレッドプールで走ったままだった」みたいな事故はよく起きます。（とくにTask.Runを使っているとき）  
そのため「このキャンセル処理は何を止めればいいのか」をちゃんと把握した上でキャンセルを実装する必要があります。  
ひとまず、これから紹介する内容を守れば「awaitのキャンセル」「await対象の実行処理のキャンセル」の2つは実現できます。

<br>