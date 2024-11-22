


# **1. MousePainter.cs**
- **役割**:
  - ユーザーのマウス操作をキャッチし、ペイントの指示を`PaintManager.cs`にお願いするクラス。
  - レイキャストを使って3D空間でのペイント位置を検出。

- **主な機能**:
  - マウスのクリック/ドラッグでペイント操作をトリガー。
  - マウス位置からペイント対象 (`Paintable`がついているObject) を特定し、`PaintManager` にペイント指示を送る。

- **依存関係**:
  - `PaintManager.cs` と連携してペイント処理を適用。
  - `Paintable.cs` を使用してペイント対象を判定。

<br>

<br>


# サンプルコード1


```cs
using UnityEngine;

//マウスで色づけるためのクラス
public class MousePainter : MonoBehaviour
{
    public Camera cam;
    
    [Space]
    
    public bool mouseSingleClick;
    
    [Space]

    // - ペイントの設定:
    public Color paintColor;    //ペイントの色。
    public float radius   = 1;  //ペイントの半径（影響範囲）。
    public float strength = 1;  //ペイントの強さ（濃さ）。
    public float hardness = 1;  //ペイントの境界の硬さ（ぼかしの具合）。

    maxRaycastDistance　= 100f;

    void Update(){

        bool click;

        click = mouseSingleClick ? Input.GetMouseButtonDown(0) : Input.GetMouseButton(0);//マウスクリックを連続的に取得するか単発で取得するかどうか
        // - `true`: シングルクリックでのみペイント。
        // - `false`: クリックし続けている間ペイント。

        if (click){
            // - マウスのスクリーン座標（2D座標）を取得
            //   カメラからその位置に向けてレイを生成します。
            Vector3 position = Input.mousePosition;  //画面上のマウスの位置取得
            Ray ray = cam.ScreenPointToRay(position);//カメラからレイを飛ばす

            RaycastHit hit;

            if (Physics.Raycast(ray, out hit, maxRaycastDistance)){
                Debug.DrawRay(ray.origin, hit.point - ray.origin, Color.red);
                transform.position = hit.point;//`MousePainter.cs` をアタッチした GameObjectが、マウスの当たった位置に移動します。
                Paintable paintableObject = hit.collider.GetComponent<Paintable>(); //Paintableコンポーネントをつけてるかどうか判断
                if (paintableObject  != null) {
                    PaintManager.instance.paint(paintableObject , hit.point, radius, hardness, strength, paintColor);
                    //Paintableがついてたら
                    //例が当たった場所に　 
                    //Paintableクラスのアドレス情報(paintableObject)・hit.point当たった場所情報・半径・hardness・strength・paintColor情報
                    //などを渡してペイント操作を実行
                }
            }
        }

    }

}

```



---


