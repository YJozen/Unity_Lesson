# Unityにおける回転処理に関する解説資料

## 回転のさせ方
Unityでは、以下のようにさまざまな回転方法があります。具体的に以下のプログラムを用いて説明します。

### 1. `transform.localEulerAngles` で回転
```csharp
//①
transform.localEulerAngles += new Vector3(0, inputX, 0) * yRotSpeed * Time.deltaTime;
```

#### 解説
- `localEulerAngles`はローカル座標系での回転角度を表す`Vector3`です。この方法は単純で直感的ですが、**オイラー角**を使っているため、**ギンバルロック**（特定の角度で回転軸が失われる問題）に注意が必要です。
- ギンバルロックは、オブジェクトが特定の角度に達すると正しく回転しなくなる問題で、複雑な回転処理には向いていません。

#### 改善点
ギンバルロックを避けたい場合は、`Quaternion`を使って回転を処理する方法が一般的です。

---

### 2. `Quaternion` を使用した回転
```csharp
//②
yRot += new Vector3(0, inputX * yRotSpeed * Time.deltaTime, 0);
transform.rotation = Quaternion.Euler(yRot); // ワールド座標での回転
```

#### 解説
- `Quaternion.Euler`を使って、**オイラー角**（`Vector3`で指定された角度）を**クォータニオン**に変換し、回転を制御しています。
- `Quaternion`はギンバルロックの問題を回避するため、**3次元回転の計算**には適しています。
- `transform.rotation`はワールド座標系で回転を設定するため、オブジェクトが**ワールド空間**での回転を維持します。

#### 改善点
回転の処理において、`Time.deltaTime`をかけて時間によるフレーム間の変動を考慮することが重要です。

---

### 3. Time.deltaTimeを直接使用してしまうケース
```csharp
//③
yRot += new Vector3(0, inputX, 0);
transform.rotation = Quaternion.Euler(yRot * Time.deltaTime * yRotSpeed); 
```

#### 解説
- `Time.deltaTime`を回転角度に直接乗算する方法は、**バグを引き起こす原因**となります。例えば、フレームレートが不安定な環境では、計算結果がばらつくため、意図しない角度の変動が発生します。
- このコードでは、`Time.deltaTime`が異なる値になるたびに回転速度が不安定になるため、オブジェクトが**不規則な速度**で回転してしまいます。

#### 修正案
`Time.deltaTime`は角度変化の速度に適用するだけで、直接回転の変化量にかけるべきではありません。正しくは以下のようにすべきです。

```csharp
yRot += new Vector3(0, inputX * yRotSpeed * Time.deltaTime, 0);
transform.rotation = Quaternion.Euler(yRot);
```

---

### 4. `transform.Rotate` メソッドを使った回転
```csharp
//④
transform.Rotate(new Vector3(0, inputX, 0) * yRotSpeed * Time.deltaTime);
```

#### 解説
- `transform.Rotate`は、回転を**ローカル座標系**または**ワールド座標系**で直接操作できるメソッドです。
- デフォルトではローカル座標系での回転を行い、`Space.World`を指定すればワールド座標で回転ができます。内部的に`Quaternion`を扱っているため、**ギンバルロック**の問題も回避できます。

#### 使用のポイント
- 簡潔に回転を表現でき、複雑な回転の計算をしなくても済むため、初心者にもわかりやすく実用的です。

---

### 5. `FixedUpdate`での回転
```csharp
//FixedUpdateでの回転処理
yRot += new Vector3(0, inputX, 0);
transform.rotation = Quaternion.Euler(yRot * yRotSpeed * Time.fixedDeltaTime);
```

#### 解説
- `FixedUpdate`は、物理演算や一定の時間間隔で行う処理に向いています。特に、**物理演算が関連するオブジェクトの回転**では、`FixedUpdate`を使用するのが適切です。
- しかし、`FixedUpdate`での回転処理でも、`Time.fixedDeltaTime`を使って**物理時間の変動**に対応することが重要です。

#### 使用例
例えば、**Rigidbodyを持つオブジェクトの回転**など、物理エンジンと連携する必要がある場合には`FixedUpdate`内で回転を処理します。

---

## まとめ：回転処理のポイント

1. **ギンバルロックを避ける**ために、`Quaternion`を使うことが推奨されます。特に、複雑な回転や連続的な回転を行う場合、`Quaternion`はより適切な回転方法です。
   
2. **`Time.deltaTime`を適切に使用**し、フレームごとの回転速度を制御する。`Time.deltaTime`を角度の変化量に直接適用すると、予測不能な動作が発生するので注意しましょう。

3. **`transform.Rotate`**は、ローカル座標系とワールド座標系のどちらでも回転を簡単に制御できる便利なメソッドです。単純な回転処理には非常に使いやすく、ギンバルロックを避けることができるため、基本的な回転処理には最適です。

4. **`FixedUpdate`での回転**は、物理演算を伴う場合に使用し、フレームレートに依存せず安定した回転を保証します。