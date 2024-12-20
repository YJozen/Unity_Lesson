ビットマップデータとは、画像を構成する画素（ピクセル）を一つ一つデジタルなデータとして記録したものです。  
各画素の色や明るさの情報を格子状に配置されたピクセル単位で保存し、画像全体を構成します。

具体的には、以下のような特徴を持っています：

1. **ピクセル単位の情報**：
   - ビットマップデータは画像を小さなピクセルの集まりとして表現します。各ピクセルはそれぞれに色（RGB値など）や透明度（アルファ値）を持ちます。

2. **解像度依存**：
   - ビットマップは解像度に依存しているため、元のサイズよりも拡大するとピクセルが目立ち、ぼやけた印象になります。このため、ビットマップ画像は高解像度であるほど、拡大時に鮮明さを維持しやすくなりますが、ファイルサイズも大きくなります。

3. **ファイル形式**：
   - ビットマップ画像の形式には、JPEG、PNG、BMP、GIFなどが含まれます。フォーマットごとに、色数、圧縮方法、透明度の対応状況などが異なります。

4. **用途**：
   - 写真やスクリーンショット、細かなディテールを含む画像など、複雑な色合いを表現するのに適しています。TextMesh Proで使われるフォントのグリフ画像も、ビットマップデータとして格納され、テキストの見た目を視覚的に再現します。

ビットマップの反対に、**ベクターデータ**は数式で形を記録するため、拡大縮小しても劣化しません。