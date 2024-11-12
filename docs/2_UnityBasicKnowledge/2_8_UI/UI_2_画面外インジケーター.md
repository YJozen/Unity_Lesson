#  画面外インジケーター

ターゲット（たとえばキャラクターやオブジェクト）の位置をスクリーン上でUI（インジケーター）として表示するためのものです。

例えば画面内に配置してあるOjectを

<img src="images/画面内.png" width="90%" alt="" title="">

例えば画面外に配置して場所を表示するなど

<img src="images/画面外.png" width="90%" alt="" title="">

このスクリプトは、ターゲットがカメラの前にあるか後ろにあるか、または画面外に出ているかを判断し、その位置に合わせてインジケーター（UI）が適切に表示されるようにします。
特に、ターゲットがカメラの後ろにある場合、インジケーターを反転させて表示し、画面外に出ないようにスケーリングして調整する処理を組み込んでいます。


<br>

# 例１　文字の表示など（回転なし）

## 1. 変数と初期化

```csharp
[SerializeField] private Transform target = default;
[SerializeField] private RectTransform textObj = default;

private Camera mainCamera;
private RectTransform rectTransform;
```

- `target`：  
インジケーターが追いかける対象（ターゲット）を設定します。  
このターゲットの位置を使ってインジケーターの位置を決定します。

- `textObj`：  
UIのインジケーター（テキストや画像など）の`RectTransform`。  
ターゲットの位置に応じてこのUIの位置が動きます。

- `mainCamera`：  
カメラを参照するための変数です。ターゲットのワールド座標をスクリーン座標に変換する際に必要です。

- `rectTransform`：  
`TargetIndicator`がアタッチされている`RectTransform`を取得します。UIの位置を制御するために使います。

`Start`メソッドで`mainCamera`をメインカメラに設定し、`rectTransform`を自分の`RectTransform`に設定しています。

<br>

## 2. `LateUpdate` メソッド

`LateUpdate`内でUIの位置を毎フレーム更新しています。このメソッドが選ばれている理由は、`LateUpdate`は`Update`が終了した後に呼ばれるため、他のオブジェクトが動いてからインジケーターを更新することができるからです。

### 2.1 キャンバススケールの取得とスクリーン座標の計算

```csharp
float canvasScale = transform.root.localScale.z;
var center = 0.5f * new Vector3(Screen.width, Screen.height);

var pos = mainCamera.WorldToScreenPoint(target.position) - center;
```

- `canvasScale`：キャンバスのスケールを取得します。`transform.root.localScale.z`により親オブジェクトのスケールを取得し、スケーリングを適用します。
- `center`：画面の中心座標です。`Screen.width`と`Screen.height`を使用してスクリーンの幅と高さを取得し、それらを半分にして中央の位置を計算します。
- `pos`：ターゲットのワールド座標をスクリーン座標に変換し、画面の中心からの相対位置に変更します。これで、ターゲットの位置が画面中央を基準に調整されます。

<br>

### 2.2 ターゲットがカメラの後ろにある場合

```csharp
if (pos.z < 0f) {
    pos.x = -pos.x;
    pos.y = -pos.y;

    if (Mathf.Approximately(pos.y, 0f)) {
        pos.y = -center.y;
    }
}
```

- `pos.z < 0f`：ターゲットがカメラの後ろにある場合、`pos.z`は負の値になります。この場合、ターゲットの位置を反転させる処理が行われます。
- `pos.x`と`pos.y`を反転させることで、ターゲットがカメラの後ろにいる場合にインジケーターが画面の反対側に表示されます。
- `Mathf.Approximately(pos.y, 0f)`：ターゲットのy座標が0に非常に近い場合（画面中央）に、`pos.y`を強制的に反転して中央に配置します。

<br>

### 2.3 ターゲットが画面外にある場合のスケーリング

```csharp
var halfSize = 0.5f * canvasScale * rectTransform.sizeDelta;
float d = Mathf.Max(
    Mathf.Abs(pos.x / (center.x - halfSize.x)),
    Mathf.Abs(pos.y / (center.y - halfSize.y))
);
```

- `halfSize`：  
インジケーターのサイズを取得し、その半分の大きさを計算します。このサイズを使って、インジケーターが画面外に出ないように調整します。
- `d`：ターゲットのスクリーン位置（`pos`）が画面の中心からどれくらい離れているかを計算します。これによって、ターゲットが画面外にある場合に、インジケーターの位置が端に寄るようにスケールされます。

<br>

### 2.4 画面外に出る場合の処理

```csharp
bool isOffscreen = (pos.z < 0f || d > 1f);
if (isOffscreen) {
    pos.x /= d;
    pos.y /= d;
}
```

- `isOffscreen`：ターゲットがカメラの後ろにあるか、スクリーン外に出ているかを判定します。
- 画面外に出ている場合、`pos.x`と`pos.y`を`d`で割ることで、インジケーターが画面端にぴったりくるように調整します。

<br>

### 2.5 UIの位置設定と表示

```csharp
rectTransform.anchoredPosition = pos / canvasScale;
textObj.gameObject.SetActive(true);
```

- `rectTransform.anchoredPosition`：インジケーターの位置を最終的に設定します。`pos / canvasScale`で、インジケーターの位置をキャンバスのスケールに合わせて調整します。
- `textObj.gameObject.SetActive(true)`：ターゲットが表示されている限り、インジケーターを表示するようにします。



<br>

---


<br>

---

<br>

# プログラム全体

<br>

---

<br>

```cs
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(RectTransform))]
public class TargetIndicator : MonoBehaviour
{
    [SerializeField] private Transform target = default;
    [SerializeField] private RectTransform textObj = default;

    private Camera mainCamera;
    private RectTransform rectTransform;

    private void Start() {
        mainCamera    = Camera.main;
        rectTransform = GetComponent<RectTransform>();
    }

    private void LateUpdate() {
        float canvasScale = transform.root.localScale.z;
        var center = 0.5f * new Vector3(Screen.width, Screen.height);

        var pos = mainCamera.WorldToScreenPoint(target.position) - center;
        if (pos.z < 0f) {
            pos.x = -pos.x;
            pos.y = -pos.y;


            if (Mathf.Approximately(pos.y, 0f)) {
                pos.y = -center.y;
            }
        }

        var halfSize = 0.5f * canvasScale * rectTransform.sizeDelta;
        float d = Mathf.Max(
            Mathf.Abs(pos.x / (center.x - halfSize.x)),
            Mathf.Abs(pos.y / (center.y - halfSize.y))
        );

        bool isOffscreen = (pos.z < 0f || d > 1f);
        if (isOffscreen) {
            pos.x /= d;
            pos.y /= d;
        }
        rectTransform.anchoredPosition = pos / canvasScale;
        textObj.gameObject.SetActive(true);
    }
}
```



<br>

---

<br>

#例２ 　矢印の表示など（回転あり）


<br>

---

<br>

```cs
using UnityEngine;
using UnityEngine.UI;

[RequireComponent(typeof(RectTransform))]
public class TargetIndicator : MonoBehaviour
{
    [SerializeField] private Transform target = default;
    [SerializeField] private Image arrow = default;

    private Camera mainCamera;
    private RectTransform rectTransform;

    private void Start() {
        mainCamera = Camera.main;
        rectTransform = GetComponent<RectTransform>();
    }

    private void LateUpdate() {
        float canvasScale = transform.root.localScale.z;
        var center = 0.5f * new Vector3(Screen.width, Screen.height);

        var pos = mainCamera.WorldToScreenPoint(target.position) - center;
        if (pos.z < 0f) {
            pos.x = -pos.x;
            pos.y = -pos.y;


            if (Mathf.Approximately(pos.y, 0f)) {
                pos.y = -center.y;
            }
        }

        var halfSize = 0.5f * canvasScale * rectTransform.sizeDelta;
        float d = Mathf.Max(
            Mathf.Abs(pos.x / (center.x - halfSize.x)),
            Mathf.Abs(pos.y / (center.y - halfSize.y))
        );

        bool isOffscreen = (pos.z < 0f || d > 1f);
        if (isOffscreen) {
            pos.x /= d;
            pos.y /= d;
        }
        rectTransform.anchoredPosition = pos / canvasScale;

        arrow.enabled = isOffscreen;
        if (isOffscreen) {
             arrow.rectTransform.eulerAngles = new Vector3(
                 0f, 0f,
                 Mathf.Atan2(pos.y, pos.x) * Mathf.Rad2Deg
             );
         }
    }
}
```