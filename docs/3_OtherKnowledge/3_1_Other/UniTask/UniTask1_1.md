**UniTask**

# UniTaskを使用してみる(キャンセル処理なし)

## サンプル1

C#に実装されている非同期クラス「Task」を使用した例

```cs
using System;
using System.Threading.Tasks;
using UnityEngine;


//async修飾子を使用して非同期メソッドを定義します。
//awaitキーワードを使用して非同期操作を待ちます。
namespace AsyncSample
{
    public class AsyncSample1 : MonoBehaviour
    {
        private async void Start() {
            Debug.Log("処理開始①");            
            await DoSomethingAsync();// 非同期メソッドの処理を待つ
            Debug.Log("本筋処理終了④");
        }

        private async Task DoSomethingAsync() {
            Debug.Log("非同期に動かす(asynchronousの略。)②");
            await Task.Delay(1000); // 1秒待つ。1000m秒
            Debug.Log("非同期で動かす処理の終了③");
        }
    }
}
```







## サンプル2

「UniTask」を使用した例

```cs:

using UnityEngine;
using Cysharp.Threading.Tasks;


//UniTaskというライブラリをとってきて、UniTaskを使用して非同期メソッドを定義します。
//UniTask.Delayを使用して待機します。
namespace AsyncSample
{
    public class AsyncSample2 : MonoBehaviour
    {
        private async void Start() {
            Debug.Log("処理開始①");         
            await DoSomethingAsync();// 非同期メソッドを呼び出して、待つ。
            Debug.Log("本筋処理終了④");
        }

        private async UniTask DoSomethingAsync() {
            Debug.Log("非同期処理が動②");
            await UniTask.Delay(1000); // 1秒待つ
            Debug.Log("UniTask operation completed,非同期で動かした処理の終了③");
        }
    }
}
```


## サンプル3

あらゆるタスクの完了を待つ


```cs:
using UnityEngine;
using Cysharp.Threading.Tasks;

namespace AsyncSample
{
    public class UniTaskExample3 : MonoBehaviour
    {
        async void Start() {
            Debug.Log("Start①");

            // 並列で3つの非同期タスクを実行。ここでは処理終了は待たない
            var task1 = DoTaskAsync(1);
            var task2 = DoTaskAsync(2);
            var task3 = DoTaskAsync(3);
           
            await UniTask.WhenAll(task1, task2, task3);// すべてのタスクが完了するのを待つ

            Debug.Log("All tasks completed⑧");
        }

        private async UniTask DoTaskAsync(int id) {
            Debug.Log($"Start UniTask operation: {id}");
            await UniTask.Delay(id * 1000); // 時間のかかる非同期処理をシミュレート(異なる時間を待つ)
            Debug.Log($"Task {id} completed");
        }
    }
}

```



## サンプル4

返り値を受け取ることができる

```cs
using UnityEngine;
using Cysharp.Threading.Tasks;

namespace AsyncSample
{
    public class UniTaskExample4 : MonoBehaviour
    {
        async void Start() {            
            int result = await MyAsyncMethod();// 非同期メソッドを呼び出し、返り値を取得する         
            Debug.Log("Async method completed with result: " + result);// 返り値を利用して何かを行う
        }

        private async UniTask<int> MyAsyncMethod() {          
            await UniTask.Delay(1000); // 非同期処理をシミュレート          
            return 42; // 非同期メソッドが整数値を返す場合、その値を返す
        }
    }
    //このサンプルコードでは、MyAsyncMethodという非同期メソッドが整数値を返し、
    //await MyAsyncMethod()でその返り値を待ち、取得しています。
    //取得した返り値を利用して、非同期メソッドが完了した後に何らかの処理を行うことができます。

    //このように、UniTaskを使用することで非同期メソッドの返り値を扱うことができます。
    //必要に応じて非同期メソッドが返す型に合わせて、適切な型を指定してください。
}

```