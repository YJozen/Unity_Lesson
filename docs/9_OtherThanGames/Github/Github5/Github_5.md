# 無視リスト

作業ディレクトリに設置したいけど、Gitでは管理したくないファイルというものがあります。

たとえば、Unityプロジェクトを編集していると、いつのまにか知らないフォルダーが生成されています。

<img src="images/1.png" width="50%" alt="" title="">

<br>

しかし、これらはツールが自動生成したファイルを保管しているフォルダーであり、Gitで管理する必要がありません。

こういった、Gitで無視したいファイル・フォルダーを登録するのが、無視リストです。

# 無視するファイルを作成

作業ディレクトリに temp.txt というファイルを設置します。

Unstaged に temp.txt が表示されますが、これをコミットしたくないという状況です。

<img src="images/2.png" width="50%" alt="" title="">

<br>

# 無視リストを作成する
temp.txt を右クリックして、 Ignore > Ignore ‘temp.txt’ をクリックします。

<img src="images/3.png" width="50%" alt="" title="">

<br>

すると、 .gitignore（ギットイグノア） というファイルが生成されます。

<img src="images/4.png" width="50%" alt="" title="">

<br>

この .gitignore が、無視リストの設定ファイルです。  
中身を見ると、temp.txtが登録されていることがわかります。

<img src="images/5.png" width="50%" alt="" title="">

<br>

この .gitignore をコミットしてください。  
temp.txt が Unstaged から消えたはずです。

temp.txt を .gitignore よりも先にコミットしないように注意してください。  
.gitignore より先にコミットしたファイルは、無視リストの対象外になります。

# フォルダー毎に無視リストを作る
フォルダーによって無視したいファイルが違うことがあります。
そんなときは、 .gitignore をフォルダー毎に作りましょう！

# 例：example.txt を２つのフォルダーに設置する
FolderA と FolderB を作成し、その中にそれぞれ example.txt を設置してください。  

FolderA/example.txt は無視したくないけど、  
 FolderB/example.txt は無視したいという状況だとします。

<img src="images/6.png" width="50%" alt="" title="">

<br>



## トップ階層の .gitignore に example.txt を追加すると、全部無視される
.gitignore をテキストエディターで開き、 example.txt という行を追加して保存してみてください。

<img src="images/7.png" width="50%" alt="" title="">

<br>

そうすると、 FolderA と FolderB の両方の example.txt が無視されます！

<img src="images/8.png" width="50%" alt="" title="">

<br>

これだと困るので、 example.txt の行はやっぱり削除してください。

## トップ階層の .gitignoreに FolderB/example.txt を追加すると、 FolderB だけ無視される
今度は、 .gitignore に FolderB/example.txt という行を追加してみてください。

<img src="images/9.png" width="50%" alt="" title="">

<br>

すると、 FolderB だけ無視されました！

<img src="images/10.png" width="50%" alt="" title="">

<br>

ただしこれだと、将来 FolderB の名前が変わったときに、 .gitignore を編集する必要があります

また、 FolderB/example.txt の行を削除してください。

## FolderB の直下に .gitignore を設置する
FolderB の中に .gitignore というファイルを作りましょう
example.txt という行を書いて保存してください。

<img src="images/11.png" width="50%" alt="" title="">

<br>

これでも、 FolderB だけ無視されます

<img src="images/12.png" width="50%" alt="" title="">

<br>

これなら、 FolderB の名前が将来変わっても、 .gitignore を編集する必要はありません。

これは、 gitignore が下のフォルダーにしか影響を及ぼせない性質があるからです。

この性質を活用すると、無視リストの管理がしやすくなるので、覚えておきましょう。










