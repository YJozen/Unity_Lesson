**Easing**
   Unityでは、easingを実装するために、`AnimationCurve`を使用できます。  
   以下は、オブジェクトを上に移動させるスクリプトの例です。

   ```csharp
   using UnityEngine;

   public class EasingExample : MonoBehaviour
   {
       public AnimationCurve easingCurve; // インスペクターで設定できるイージングカーブ
       public float duration = 2.0f; // アニメーションの全体時間

       private float elapsedTime = 0.0f;//経過時間

       void Update()
       {
           if (elapsedTime < duration)
           {
               elapsedTime += Time.deltaTime;
               float t = elapsedTime / duration; // 0から1の範囲に正規化
               
               float easedValue = easingCurve.Evaluate(t); // イージングカーブに基づいて値を取得
               transform.position = new Vector3(0, easedValue, 0); // Y軸の位置を更新
           }
           else
           {
                // 経過時間がdurationを超えたら、リセットして再スタート
                elapsedTime = 0.0f;
           }
       }
   }
   ```



<br>

---

<br>
