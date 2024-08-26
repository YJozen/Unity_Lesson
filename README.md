# slide


(Visual studio codeなら　Live Server　などの拡張機能入れた方がいいかも)


# サーバーをたてる
npm install -g http-server
実行後、  
http-server
のコマンドだけで建てられる

## ルート設定
http-server /Users/jozenyuto/Documents/Game/Unity/Unity_Lesson/docs 


##  単体だとmdをhtmlに変換しないので
https://chromewebstore.google.com/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk
などプラグインを利用し、パスを通して変換作業を行う


# marp


# Jekyll


開発環境整えてからやろ・・・



Ruby開発環境をフルでインストールします。

Jekyllとbundler gemsをインストールします。

gem install jekyll bundler

./myblogに新しいJkyllサイトを作ります。

jekyll new myblog

新しいディレクトリに移動します。

cd myblog

サイトを構築し、ローカルサーバ上に出現させます。

bundle exec jekyll serve