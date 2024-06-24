**InputSystem 2**

# Input Systemでキーコンフィグを実装する
1.


https://nekojara.city/unity-input-system-rebinding




キーコンフィグの実装の流れは次のようになります。

実装の流れ
設定用のUIの配置
リバインドを実施するスクリプトの実装
UIにスクリプトを適用




スクリプトで実装するリバインド（Interactive Rebinding）の処理の流れは次のようになります。

スクリプト実装の流れ
リバインド対象のActionを無効化する
どのBindingをリバインドするかを決定する
Actionに対してリバインドの動作設定を行う
リバインドを開始する
リバインドが完了または中断した時、Actionを有効化する
また、リバインドにより上書きされた設定は、ストレージなどに対してセーブ・ロードしたりできます。

本記事では、このようなキーコンフィグの実装方法について順を追って解説していきます。





例では次のようなInput Action Assetが予め作成されているものとします。




<img src="images/8/8_5/unity-input-system-custom-interaction-sprint-5.png.avif" width="50%" alt="" title="">

<br>

KeyboardとGamepadというスキームが定義され、JumpとMoveというActionの各Bindingに設定しています。

本記事で解説するキーコンフィグの実装方法は、Input Systemパッケージの公式サンプルの一つである「Rebinding UI」を参考にしています。


UIの準備
本記事では、次のようにジャンプと移動操作に対してキー割当てを変更するものとして解説を進めます。





















