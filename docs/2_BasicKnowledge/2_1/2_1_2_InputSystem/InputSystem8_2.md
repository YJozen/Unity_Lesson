**InputSystem 2**

# Input SystemのProcessorで入力値を加工する Processorを自作する

ここまで紹介したProcessorは、Input Systemパッケージ側で用意されているものですが、独自のProcessorを自作して適用することも可能です。

自作の流れは次のようになります。

自作の流れ
InputProcessor<T>継承クラスをスクリプトで定義
初期化時、InputSystemにProcessorを登録する処理を実装
Processorの処理を実装
これらの手順は、以下公式リファレンスに記載されていますが、いくつか注意すべき点があります。

参考：Processors | Input System | 1.3.0

具体例を示しながら実装方法を解説します。




![](images/1/unity-input-system-intro-v2-1-940x563.png.avif "")



