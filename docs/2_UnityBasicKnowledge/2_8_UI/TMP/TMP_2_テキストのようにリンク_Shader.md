https://github.com/coposuke/TextMeshProAnimator



# TextMwshをクリックしたら反応するようにする





Link機能の実装



Link




カメラの取得


```cs

using UnityEngine;
using UnityEngine.Events;
using TMPro;

/// <summary>
/// Linkタグで囲まれたテキストのクリックを検知するコンポ―ネント
/// </summary>
[RequireComponent(typeof(TMP_Text))]
public class TextClick : MonoBehaviour
{
	/// <summary>クリック時のイベントハンドラー</summary>
	[SerializeField] private UnityEvent<string, string, int, int> onClickLink;

	/// <summary>TextMeshProのテキストコンポーネント</summary>
	private TMP_Text textComponent;
	/// <summary>TextMeshProのテキストを描画しているカメラ</summary>
	private Camera targetCamera;


	/// <summary>
	/// Unity Event Awake
	/// </summary>
	private void Awake()
	{
		this.textComponent = GetComponent<TMP_Text>();

		// ①カメラを取得する
		var rootCanvas = this.GetComponentInParent<Canvas>();
		if (rootCanvas != null)
		{
			switch (rootCanvas.renderMode)
			{
				case RenderMode.ScreenSpaceOverlay: this.targetCamera = null; break;
				case RenderMode.ScreenSpaceCamera:  this.targetCamera = rootCanvas.worldCamera; break;
				case RenderMode.WorldSpace:         this.targetCamera = rootCanvas.worldCamera; break;
			}
		}
		else
		{
			this.targetCamera = Camera.main;
		}

	}

	/// <summary>
	/// Unity Event Update
	/// </summary>
	private void Update()
	{
		// ②クリック（タップ）座標を取得する
		Vector3 touchPosition = Input.mousePosition;
		bool touchDown = Input.GetMouseButtonDown(0);

		if (0 < Input.touchCount)
		{
			Touch touchInfo = Input.GetTouch(0);
			touchPosition = touchInfo.position;
			touchDown = touchInfo.phase == TouchPhase.Began;
		}

		// ③クリック判定を行う
		if (touchDown)
		{
			int linkIndex = TMP_TextUtilities.FindIntersectingLink(this.textComponent, touchPosition, this.targetCamera);

			if (0 <= linkIndex)
			{
				int charIndex = TMP_TextUtilities.FindIntersectingCharacter(this.textComponent, touchPosition, this.targetCamera, true);

				if (0 <= charIndex)
				{
					TMP_LinkInfo linkInfo = textComponent.textInfo.linkInfo[linkIndex];

					Debug.Log($"linkInfo.GetLinkID() :  {linkInfo.GetLinkID()} ,\n" +
							  $"linkInfo.GetLinkText() :  {linkInfo.GetLinkText()} ,\n" +	
							  $"linkInfo.linkTextfirstCharacterIndex :  {linkInfo.linkTextfirstCharacterIndex},\n"+
							  $"linkIndex :  {linkIndex}");		


					// ④アニメーションを再生する
					// this.onClickLink.Invoke(linkInfo.GetLinkID(),
					// 				 		linkInfo.GetLinkText(),
					// 						linkInfo.linkTextfirstCharacterIndex,
					// 						linkIndex);
				}
			}
		}
	}
}

```
