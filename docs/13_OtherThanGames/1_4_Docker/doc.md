Flaskをバックエンド（API）として、Flutterをフロントエンドとして連携させるアプリケーションをDockerを使って構築する手順を、以下のように詳しく解説します。このチュートリアルを一度実行すれば、FlaskとFlutterのアプリケーションを簡単に構築、デプロイできるようになります。

### **構成図**
- **Flask**: APIサーバー
- **Flutter**: フロントエンド（Web）
- **Docker**: 開発環境のコンテナ化

---

### **前提条件**
以下のツールがインストールされていることを前提とします。
- **Docker**: [公式サイトからインストール](https://www.docker.com/get-started)
- **Flutter**: [公式サイトからインストール](https://flutter.dev/docs/get-started/install)

---

### **ステップ1: Flask APIの作成**

#### 1. Flaskプロジェクトのセットアップ
まず、Flaskアプリケーションを作成します。

1. プロジェクトフォルダを作成します。
   ```bash
   mkdir flask_flutter_app
   cd flask_flutter_app
   ```

2. Flaskの必要なパッケージをインストールします。`requirements.txt`というファイルを作成し、以下の内容を記述します。
   ```text
   Flask==2.3.3
   Flask-Cors==3.1.1
   ```

3. Flask API用のPythonコード（`app.py`）を作成します。
   ```python
   from flask import Flask, jsonify
   from flask_cors import CORS

   app = Flask(__name__)
   CORS(app)  # Cross-Origin Resource Sharingを有効にする

   @app.route('/api', methods=['GET'])
   def get_data():
       return jsonify({"message": "Hello from Flask API"})

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

4. 次に、**`Dockerfile`** を作成します。これにより、Flaskアプリケーションをコンテナとして実行できるようにします。
   ```Dockerfile
   # Pythonの公式イメージを使用
   FROM python:3.10-slim

   # 作業ディレクトリの作成
   WORKDIR /app

   # requirements.txtをコピー
   COPY requirements.txt /app/

   # 必要なPythonライブラリをインストール
   RUN pip install --no-cache-dir -r requirements.txt

   # アプリケーションコードをコピー
   COPY . /app/

   # Flaskアプリケーションを起動
   CMD ["python", "app.py"]
   ```

5. **`docker-compose.yml`** ファイルを作成して、Flaskアプリを管理します。
   ```yaml
   version: '3'

   services:
     flask-api:
       build: .
       ports:
         - "5000:5000"
       environment:
         - FLASK_ENV=development
       volumes:
         - .:/app
       networks:
         - flask-network

   networks:
     flask-network:
       driver: bridge
   ```

6. コンテナをビルドして起動します。
   ```bash
   docker-compose up --build
   ```

これでFlaskのAPIが`http://localhost:5000/api`で利用可能になります。

---

### **ステップ2: Flutterフロントエンドの作成**

次に、Flutterを使ってフロントエンドを作成します。

1. Flutterプロジェクトを作成します。
   ```bash
   flutter create flutter_frontend
   cd flutter_frontend
   ```

2. Flutterの`http`パッケージを使ってFlask APIと通信します。`pubspec.yaml`の依存関係に`http`を追加します。
   ```yaml
   dependencies:
     flutter:
       sdk: flutter
     http: ^0.14.0
   ```

3. Flutterの`lib/main.dart`ファイルを以下のように編集して、Flask APIからデータを取得する処理を追加します。
   ```dart
   import 'package:flutter/material.dart';
   import 'package:http/http.dart' as http;
   import 'dart:convert';

   void main() {
     runApp(MyApp());
   }

   class MyApp extends StatelessWidget {
     @override
     Widget build(BuildContext context) {
       return MaterialApp(
         title: 'Flutter & Flask',
         theme: ThemeData(
           primarySwatch: Colors.blue,
         ),
         home: MyHomePage(),
       );
     }
   }

   class MyHomePage extends StatefulWidget {
     @override
     _MyHomePageState createState() => _MyHomePageState();
   }

   class _MyHomePageState extends State<MyHomePage> {
     String message = 'Loading...';

     @override
     void initState() {
       super.initState();
       fetchMessage();
     }

     Future<void> fetchMessage() async {
       final response = await http.get(Uri.parse('http://localhost:5000/api'));
       if (response.statusCode == 200) {
         setState(() {
           message = json.decode(response.body)['message'];
         });
       } else {
         setState(() {
           message = 'Failed to load data';
         });
       }
     }

     @override
     Widget build(BuildContext context) {
       return Scaffold(
         appBar: AppBar(
           title: Text('Flutter & Flask'),
         ),
         body: Center(
           child: Text(message),
         ),
       );
     }
   }
   ```

4. Flutterアプリをビルドして実行します。
   ```bash
   flutter run -d chrome
   ```

これで、ブラウザでFlutterアプリが起動し、Flask APIからメッセージが表示されることを確認できます。

---

### **ステップ3: FlutterとFlaskをDockerで統合**

#### 1. **FlutterのDocker化**

FlutterのWebアプリもDockerで実行するためには、Flutterのビルドを行い、Webサーバーを使って公開する必要があります。

1. Flutter Web用にビルドします。
   ```bash
   flutter build web
   ```

2. `Dockerfile`を作成して、FlutterのWebアプリを公開します。
   ```Dockerfile
   # ベースイメージとしてnginxを使用
   FROM nginx:alpine

   # Flutterのビルド成果物をnginxの公開ディレクトリにコピー
   COPY build/web /usr/share/nginx/html

   # nginxを起動
   CMD ["nginx", "-g", "daemon off;"]
   ```

3. `docker-compose.yml`を編集して、FlutterのWebアプリとFlask APIを同時に起動するようにします。
   ```yaml
   version: '3'

   services:
     flask-api:
       build: ./flask
       ports:
         - "5000:5000"
       environment:
         - FLASK_ENV=development
       volumes:
         - ./flask:/app
       networks:
         - flask-network

     flutter-web:
       build: ./flutter_frontend
       ports:
         - "80:80"
       networks:
         - flask-network

   networks:
     flask-network:
       driver: bridge
   ```

4. 最後に、`docker-compose`を使って両方のサービスを起動します。
   ```bash
   docker-compose up --build
   ```

これで、`http://localhost`でFlutterアプリが表示され、`http://localhost:5000/api`からFlask APIを利用できるようになります。

---

### **まとめ**

1. **Flask**: APIを提供するバックエンド。
2. **Flutter**: フロントエンドWebアプリケーション。
3. **Docker**: アプリケーションをコンテナ化して簡単に開発、デプロイ。

上記の手順に従えば、FlaskとFlutterを使ったアプリケーションの開発環境をDockerで構築できます。すべての依存関係はDockerコンテナ内で管理されるため、仮想環境や手動でのライブラリインストールは不要です。