参考 
https://github.com/coposuke/TextMeshProAnimator


# シンプルなサンプル



```cs

using UnityEngine;
using TMPro;

[ExecuteInEditMode]
[RequireComponent(typeof(TextMeshPro))]
public class TextMeshProMaxVisibleCharaController : MonoBehaviour
{
	public int maxVisibleCharacters;
	private TextMeshPro text;

	private void Update()
	{
		if (this.text == null)
			this.text = GetComponent<TextMeshPro>();

		this.text.maxVisibleCharacters = this.maxVisibleCharacters;
	}
}

```

[ExecuteInEditModeについて](ExecuteInEditModeについて.md)


1. スクリプトがアタッチされたオブジェクトの `TextMeshPro` コンポーネントに対し、エディターや実行時にリアルタイムで最大表示文字数を制御できます。
2. 例えば、`maxVisibleCharacters` を 5 に設定した場合、テキストの最初の 5 文字のみが表示され、それ以降は表示されません。


ここでは、0から手動で文字を変える必要がありますが、下記のようにすれば自動で１文字ずつ表示されます





`サンプル`

```cs

using UnityEngine;


/// <summary>
/// 文字送りアニメーション
/// </summary>
public class TextMeshProSimpleAnimator : MonoBehaviour
{
	/// <summary>アニメーション中かどうか</summary>
	public bool isAnimating { get; private set; } = false;

	/// <summary>1文字あたりの表示速度</summary>
	public float speedPerCharacter = 0.1f;
	
	/// <summary>自動再生</summary>
	[SerializeField] private bool playOnEnable = false;

	/// <summary>ループするかどうか</summary>
	public bool isLoop = false;

	/// <summary>TextMeshPro</summary>
	private TMPro.TMP_Text text = default;

	/// <summary>アニメーション時間</summary>
	private float time = 0.0f;

	private void Awake()
	{
		text = GetComponent<TMPro.TMP_Text>();
	}

	private void Start()
	{
		if (this.playOnEnable) { Play(); }
	}

	private void OnEnable()
	{
		if (this.playOnEnable) { Play(); }
	}

	private void Update()
	{
		if(this.isAnimating)
			UpdateAnimation(Time.deltaTime);
	}

	/// <summary>アニメーション再生開始</summary>
	public void Play()
	{
		if (this.isAnimating)
			return;

		this.time = 0.0f;
		this.isAnimating = true;
		this.text.ForceMeshUpdate(true);
		UpdateAnimation(0.0f);
	}

	/// <summary>アニメーション強制終了</summary>
	public void Finish()
	{
		if (!this.isAnimating)
			return;

		this.isAnimating = false;
		this.text.maxVisibleCharacters = this.text.textInfo.characterCount;
		this.time = 0.0f;
	}

	/// <summary>アニメーション更新</summary>
	private void UpdateAnimation(float deltaTime)
	{

		int maxVisibleCharacters = this.text.textInfo.characterCount;
		float maxTime = (maxVisibleCharacters + 1) * speedPerCharacter;//文字表示の最大時間　+1 は、最後の文字を表示するための余裕を持たせてます

		this.time += deltaTime;// 累計時間

        // 何文字目まで表示するか
		int visibleCharacters = Mathf.Clamp(Mathf.FloorToInt(time / speedPerCharacter), 0, maxVisibleCharacters);

        //現在の累積時間 time を、1文字あたりの表示速度 speedPerCharacter で割り算。
		//例：1文字の表示速度が 0.1秒、累積時間が 0.35秒なら、0.35 / 0.1 = 3.5 → 3.5文字目まで表示可能
        
		//文字の表示数を指示
		if (text.maxVisibleCharacters != visibleCharacters)
			text.maxVisibleCharacters = visibleCharacters;

        //時間が最大時間を超えた場合: ループするか終わらせるか
		if (this.time > maxTime)
		{
			if (this.isLoop)
			{
				time = time % maxTime;
			}
			else
			{
				Finish();
			}
		}
	}
}

```

一部のみピックアップ

### **`ForceMeshUpdate`**

#### **概要**
`ForceMeshUpdate` は、TextMeshPro がテキストのメッシュ（頂点データや文字の見た目の情報）を再生成する際に使用されます。通常、テキストの更新は必要に応じて自動的に行われますが、手動で更新を強制する場合に便利です。

```csharp
textComponent.ForceMeshUpdate(false);
```

- **引数**
  - デフォルトは `false`。`true` に設定すると、オブジェクトが非アクティブ状態でもメッシュ更新を行います。

#### **使用例**
1. テキストやスタイルが変更された後に即座に反映させたい場合：
   ```csharp
   TMP_Text textComponent = GetComponent<TMP_Text>();
   textComponent.text = "Updated Text!";
   textComponent.ForceMeshUpdate();
   ```

2. **アニメーション**や**エフェクト**を動的に適用するために、最新のメッシュデータが必要な場合：
   - ジオメトリや頂点の操作を行う前に、テキスト情報が最新であることを保証します。

---

### **`Mathf.Clamp`**

#### **概要**
`Mathf.Clamp` は、数値を指定された範囲内に収める関数です。

```csharp
Mathf.Clamp(value, min, max);
```

- **引数**
  - `value`: 制限対象の数値。
  - `min`: 範囲の最小値。
  - `max`: 範囲の最大値。

- **戻り値**
  - `value` が `min` より小さい場合 → `min` を返す。
  - `value` が `max` より大きい場合 → `max` を返す。
  - 上記以外 → `value` をそのまま返す。

#### **使用例**
1. **制御値の範囲指定**:
   ```csharp
   float speed = Mathf.Clamp(inputSpeed, 0, 100); // 0～100の範囲に制限
   ```

2. **ゲーム内のHP管理**:
   ```csharp
   int currentHP = Mathf.Clamp(newHP, 0, maxHP); // HPを0～最大値に制限
   ```

---

### **`Mathf.FloorToInt`**

`Mathf.FloorToInt` は、指定された数値を小数点以下で切り捨て（floor）し、**整数型に変換**します。

```csharp
Mathf.FloorToInt(value);
```
- **引数**
  - `value`: 対象となる浮動小数点数値。

- **戻り値**
  - `value` の小数点以下を切り捨てた整数値。

#### **使用例**
1. **ゲーム内タイマーの表示**:
   ```csharp
   float elapsedTime = 12.9f;
   int displayedTime = Mathf.FloorToInt(elapsedTime); // 表示は12
   ```

2. **インデックスの計算**:
   ```csharp
   float position = 2.7f;
   int arrayIndex = Mathf.FloorToInt(position); // インデックスは2
   ```

---

### **コードの具体例解説**
```csharp
int visibleCharacters = Mathf.Clamp(Mathf.FloorToInt(time / speedPerCharacter), 0, maxVisibleCharacters);
```



2. **`Mathf.FloorToInt(time / speedPerCharacter)`**:
   - 現在のアニメーション時間 `time` を、文字1つあたりのアニメーション時間 `speedPerCharacter` で割ります。
   - 小数点以下を切り捨てた結果を整数に変換します。これは、「現在表示する文字数」を計算

3. **`Mathf.Clamp`**:
   - 表示する文字数を、0～最大文字数 (`maxVisibleCharacters`) に制限します。
   - 過剰に多い場合は `maxVisibleCharacters` に、少なすぎる場合は 0 に固定します。

---

### **この処理の目的**
- `visibleCharacters` に、表示可能な文字数を計算して設定します。
- アニメーションや動的な文字列表示のコントロールに利用されます。