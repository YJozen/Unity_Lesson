Debug.Log以外にもあるので紹介

##  Debug.Log / Debug.LogWarning / Debug.LogError

- **目的**:  
コンソールにメッセージを出力して、プログラムの状態やエラーを確認します。

- **使い方**:
  - `Debug.Log`で通常の情報
  - `Debug.LogWarning`で警告
  - `Debug.LogError`でエラー
  
  を出力します。

```csharp
Debug.Log("This is an info message.");
Debug.LogWarning("This is a warning message.");
Debug.LogError("This is an error message.");
```

<br>

##  Debug.DrawLine

- **目的**:  
2つの点を結ぶ線を描画します。

- **使い方**:
  - `Debug.DrawLine`メソッドを使用して、開始点と終了点を指定して線を描画します。

```csharp
Debug.DrawLine(startPosition, endPosition, Color.red); // 赤い線を描画
```

<br>

##  Debug.Break

- **目的**:  
 デバッグ実行中に一時停止します。

- **使い方**:
  - `Debug.Break()`を使用すると、ゲームが一時停止し、Unityエディタでデバッグ情報を確認できます。

```csharp
if (someCondition) {
    Debug.Break(); // 条件が満たされたら一時停止
}
```

##  Debug.DrawRay / Debug.DrawLine

- **目的**:  
レイを描画するためのメソッド。

- **使い方**:
  - `Debug.DrawRay`は始点から方向と長さを指定し、線を描画します。
  - `Debug.DrawLine`は2つの点を結ぶ線を描画します。

<br>

## 使い分け方

1. **視覚化したい対象**:
   - シーンビューにオブジェクトの情報を視覚化したい場合は、`OnDrawGizmos`や`OnDrawGizmosSelected`を使用。
   - 特定のレイや線を視覚化したい場合は、`Debug.DrawRay`や`Debug.DrawLine`を使用。

2. **情報の出力**:
   - 状態やエラーを確認するためには、`Debug.Log`、`Debug.LogWarning`、`Debug.LogError`を使います。

3. **一時停止したい場合**:
   - プログラムの実行を一時停止して、デバッグ情報を確認したい場合は`Debug.Break`を使用します。

