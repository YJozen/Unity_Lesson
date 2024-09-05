using UnityEngine;

public class MoveObjectWithMouse : MonoBehaviour
{
    private Camera _camera;
    private float _initialDistance;

    void Start()
    {
        _camera = Camera.main;
        // カメラとオブジェクトの初期距離を計算
        _initialDistance = Vector3.Distance(transform.position, _camera.transform.position);
    }

    void Update()
    {
        MoveObjectToMousePosition();
    }

    void MoveObjectToMousePosition()
    {
        // マウスのスクリーン座標を取得
        Vector3 mousePosition = Input.mousePosition;
        // 初期距離を使って、スクリーン座標をワールド座標に変換
        mousePosition.z = _initialDistance;  // Zに距離をセット

        Vector3 worldPosition = _camera.ScreenToWorldPoint(mousePosition);

        // オブジェクトの位置を更新
        transform.position = worldPosition;
    }
}
