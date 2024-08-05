# 画面を分割し、ローカルマルチを実装

Player Input Managerでは、プレイヤー毎のカメラ分割機能もサポートしています。

カメラ分割を有効にするには、Split-Screen > Enable Split-Screen項目にチェックを入れます。  
すると、詳細設定項目が出現します。

<img src="images/12/12_1/unity-input-system-local-multiplayer-12.png.avif" width="60%" alt="" title="">

<br>

## カメラの配置
Player Input Managerの画面分割機能を有効化すると、各プレイヤー毎の視点のカメラで画面分割することができます。

まず、プレイヤーを写すカメラオブジェクトを配置します。

プレイヤーをPrefabとしている場合、Prefabの子オブジェクトとして配置すれば良いでしょう。

<img src="images/12/12_1/unity-input-system-local-multiplayer-m8.mp4.gif" width="90%" alt="" title="">

<br>

この場合、例えばルートのプレイヤーオブジェクト直下にカメラオブジェクトとCharacter Controllerオブジェクトが存在する形になります。

<img src="images/12/12_1/unity-input-system-local-multiplayer-13.png.avif" width="60%" alt="" title="">

<br>

### Player Input側の設定
Player InputコンポーネントのCamera項目に、前述のプレイヤー用カメラを指定します。

<img src="images/12/12_1/unity-input-system-local-multiplayer-14.png.avif" width="60%" alt="" title="">

<br>

### 画面分割方法の設定
画面分割の仕方は、Player Input ManagerコンポーネントのSplie-Screen以下の項目から設定します。

<img src="images/12/12_1/unity-input-system-local-multiplayer-12.png.avif" width="60%" alt="" title="">

<br>

Maintain Aspect Ratio項目は、画面分割する際にカメラのアスペクト比を維持する設定です。

Set Fixed Number項目は、分割表示する画面数を固定化する設定です。チェックを入れると、その下に出現するNumber of Screens項目から画面数を指定できます。

<img src="images/12/12_1/unity-input-system-local-multiplayer-15.png.avif" width="60%" alt="" title="">

<br>

例えば4を指定すると、最初から画面を4分割する前提でカメラ画面の表示領域が計算されます。

Screen Rectangle項目には、画面全体の表示領域をビューポート座標として指定します。

<img src="images/12/12_1/unity-input-system-local-multiplayer-16.png.avif" width="70%" alt="" title="">

<br>

初期値は画面全体を表す(0, 0) 〜 (1, 1)です。

+ ビューポート座標  
左下を(0, 0)、右上を(1, 1)とした座標系。  
画面サイズを１（単位）とするため、解像度に依存しない。
+ スクリーン座標  
左下を(0, 0)、右上を(画面の幅, 画面の高さ)とした座標系。   
１ピクセルを１（単位）とするため、解像度に依存する。


実行すると、プレイヤー入室時、数に応じて適切に画面分割されているのを確認できます。








