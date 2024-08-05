Jekyll プロジェクトの初期設定と基本的なフォルダ構成、サンプルの HTML、CSS、および YAML 設定ファイルについてまとめました。

### **1. Ruby と Bundler のインストール**

- **Ruby のインストール**:
  ```bash
  rbenv install 3.2.0
  rbenv global 3.2.0
  ```

- **Bundler のインストール**:
  ```bash
  gem install bundler
  ```

### **2. Jekyll のインストール**

- **Jekyll のインストール**:
  ```bash
  bundle init
  ```

- **Gemfile の編集**:
  `Gemfile` に以下の内容を追加します。
  ```ruby
  gem "jekyll", "~> 4.2"
  gem "webrick"
  ```

- **依存関係のインストール**:
  ```bash
  bundle install
  ```

### **3. Jekyll サイトの作成**

- **新しい Jekyll サイトの作成**:
  ```bash
  bundle exec jekyll new .
  ```

### **4. フォルダ構成**

Jekyll のプロジェクトディレクトリの基本的な構成は以下の通りです:

```
/your-jekyll-site
├── _config.yml
├── _includes
│   └── header.html
├── _layouts
│   └── default.html
├── _posts
│   └── 2024-08-05-sample-post.md
├── _site
├── assets
│   └── css
│       └── style.css
├── index.md
├── Gemfile
├── Gemfile.lock
└── README.md
```

### **5. サンプルファイル**

#### **`_config.yml`** (サイト設定)

```yaml
title: My Jekyll Site
description: A simple description of my Jekyll site.
baseurl: ""
url: "http://localhost:4000"
markdown: kramdown
theme: minima
```

#### **`index.md`** (ホームページ)

```markdown
---
layout: default
title: Home
---

# Welcome to My Jekyll Site

This is a sample homepage for your Jekyll site.
```

#### **`_layouts/default.html`** (基本レイアウト)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page.title }} | {{ site.title }}</title>
  <link rel="stylesheet" href="{{ "/assets/css/style.css" | relative_url }}">
</head>
<body>
  <header>
    <h1>{{ site.title }}</h1>
  </header>
  
  <main>
    {{ content }}
  </main>

  <footer>
    <p>&copy; {{ site.time | date: '%Y' }} {{ site.title }}</p>
  </footer>
</body>
</html>
```

#### **`_includes/header.html`** (ヘッダーのサンプル)

```html
<header>
  <h1>{{ site.title }}</h1>
</header>
```

#### **`assets/css/style.css`** (スタイルシート)

```css
body {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
}

header {
  background: #333;
  color: #fff;
  padding: 10px 0;
  text-align: center;
}

footer {
  background: #333;
  color: #fff;
  padding: 10px 0;
  text-align: center;
  position: absolute;
  bottom: 0;
  width: 100%;
}

main {
  padding: 20px;
}
```

#### **`_posts/2024-08-05-sample-post.md`** (サンプルポスト)

```markdown
---
layout: default
title: "Sample Post"
date: 2024-08-05 10:00:00 +0000
categories: jekyll update
---

# Sample Post

This is a sample post to demonstrate how Jekyll handles Markdown.
```

### **6. サイトのビルドとサーブ**

- **サイトのビルドとサーブ**:
  ```bash
  bundle exec jekyll serve --trace
  ```

- **ブラウザで確認**:
  - `http://localhost:4000` でサイトを確認します。

この手順で Jekyll の環境を設定し、基本的なサイトを構築できます。各ファイルの内容はカスタマイズできますので、必要に応じて変更してください。