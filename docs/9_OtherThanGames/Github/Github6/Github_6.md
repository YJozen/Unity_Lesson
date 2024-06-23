# LFSにファイルを登録する

100MBを超えるファイルを、サーバーへプッシュしようとするとエラーになります。  
そのエラーをでないようにする仕組みがLFSです。  
LFSは Large File System の略で、巨大ファイル用システムという意味です。

<br>

# 下準備

[Sample101MB.bin](https://drive.google.com/file/d/1rD9HGFIvNc3W-dAJaAMNHKFgAjwKDcHg/view?usp=sharing) をダウンロードしてください。  
だいたい101MBのファイルです。中身は意味のないデータが詰まっています。  

これを、作業ディレクトリに設置してください。  
コミットして、プッシュしようとすると、以下のようなエラーがでます。

<img src="images/1.png" width="50%" alt="" title="">

<br>

> remote: error: File Sample101MB.bin is 101.00 MB;
this exceeds GitHub's file size limit of 100.00 MB
remote: error: GH001: Large files detected.
You may want to try Git Large File Storage - https://git-lfs.github.com.

要約すると、以下のような感じです。

> 100MBを超えている巨大ファイルを検知しました。
LFSを利用してください。

巨大ファイルをコミットした1つ前の状態まで、 [Mixed Reset](../Github4/Github_4.md) してください。


# LFSを有効にする

Repository > Git LFS > Initialize Git LFS を実行してください。

<img src="images/2.png" width="50%" alt="" title="">

<br>

この作業はリポジトリ毎に必要となります  
(Initialize Git LFS が見つからない場合は、すでにLFSが有効になっています)

# 巨大ファイルを設置する
Sample101MB.bin を 右クリック > LFS > Track ‘Sample101MB.bin’ をクリックします。

<img src="images/3.png" width="50%" alt="" title="">

<br>

すると、 .gitattributes というファイルが生成されます。

<img src="images/4.png" width="50%" alt="" title="">

<br>

.gitattributes というのは、LFSの設定ファイルです。  
中身を見ると、 Sample101MB.bin が登録されていることがわかります。

<img src="images/5.png" width="50%" alt="" title="">

<br>

この .gitattributes のみをまずコミットしてください。  
その次に、 Sample101MB.bin をコミットしてください。

Sample101MB.bin を .gitattributes よりも先にコミットしないようにご注意ください。

Sample101MB.bin と .gitattributes を同時にコミットするのは問題ありません。

# プッシュする
再びプッシュをしてみます。  
今度は、問題なくプッシュできます！

# LFSに登録されているファイルを確認する

Forkの右上から Open in > View on GitHub で、リモートリポジトリのページを開きます。

<img src="images/6.png" width="50%" alt="" title="">

<br>

Sample101MB.bin をクリックします。  
Stored with Git LFS と表記されています。  
これは、このファイルがLFSに登録されているという証です！

<img src="images/7.png" width="50%" alt="" title="">

<br>

# LFSを利用しているリポジトリ一覧を確認する

GitHub右上から Settings をクリック。

<img src="images/8.png" width="50%" alt="" title="">

<br>

左サイドバーの Billing and plans > Plans and usage をクリック。

<img src="images/9.png" width="50%" alt="" title="">

<br>

下の方にスクロールして、 Git LFS Data > Storage をクリックします。

<img src="images/10.png" width="50%" alt="" title="">

<br>

すると、LFSを利用しているリポジトリの一覧が表示されました！  
無料プランの場合、<b>合計1GB</b>まで利用できます。

課金している場合1GB以上利用できますが、費用を抑えるためにも、巨大ファイルを大量に登録しないようにしましょう(基本大きすぎるファイルは別の方法でやりとりする方がいいかと思います。)

# LFSからファイルを削除

GitHubのコストを削減するためにも、不要なファイルは削除すべきです。 
しかし、LFSファイルの削除は、実はとても大変です。  

以下の作業が必要になります。

+ コミットの履歴を改ざんし、巨大ファイルのコミットをなかったことにする。
+ リポジトリのLFS機能を無効にする。
+ リポジトリを削除して再作成する。  

詳しい手順は[こちら](https://docs.github.com/ja/repositories/working-with-files/managing-large-files/removing-files-from-git-large-file-storage)などを参照してください。

<br>

# リポジトリを削除する
今回は、リポジトリを削除することで、LFSも削除する方法を見ていきます。  
GitHubのリポジトリのページの右上にある Settings をクリックします。

<img src="images/11.png" width="50%" alt="" title="">

<br>

一番下までスクロールし、 Danger Zone > Delete this repository をクリックします。

<img src="images/12.png" width="50%" alt="" title="">

<br>

表示にしたがって進め、リポジトリの名前をタイプして Delete this repository をクリックします。  

GitHubのパスワードの入力を求められるので、入力します。

リポジトリ一覧ページに遷移したら、削除成功です！