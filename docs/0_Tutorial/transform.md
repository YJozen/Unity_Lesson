# transformのスクロウとを直接見ることができるか

Unityの`Transform`クラスは、C#のソースコードとして直接見ることはできません  

が、Unityのソースコードに関しては、Unityの公式のC# APIリファレンスでドキュメントが提供されています。ただし、`Transform`クラスは内部でネイティブコード（C++）によって実装されているため、その内部ロジックを直接確認することはできません。




### `Transform`クラスの概要
`Transform`クラスは、ゲームオブジェクトの位置（`position`）、回転（`rotation`）、スケール（`localScale`）を制御するために使用されます。また、親子関係の設定や、ワールド座標系とローカル座標系の変換、親子間での座標の伝播（`SetParent()`や`localPosition`など）なども管理します。




### 主なメソッド・プロパティ
- `position`: ワールド座標でのオブジェクトの位置
- `localPosition`: ローカル座標系でのオブジェクトの位置
- `rotation`: ワールド座標系でのオブジェクトの回転（クォータニオン）
- `localRotation`: ローカル座標系でのオブジェクトの回転（クォータニオン）
- `localScale`: オブジェクトのスケール（ローカル座標系に基づく）
- `forward`, `right`, `up`: オブジェクトのローカル軸をワールド座標系で取得
- `TransformDirection()`: ローカル座標系からワールド座標系への変換
- `Rotate()`: ローカル軸での回転
- `LookAt()`: 指定した位置またはオブジェクトを向く




### `Transform`のソースコードの確認方法
もしソースコードそのものにアクセスしたい場合、以下の方法を使います。

1. **Unityのソースコードにアクセスする方法**: Unityのソースコードは、Unityがオープンソースで公開しているわけではないため、`Transform`クラスの具体的な実装は見ることができません。しかし、Unityの`Transform`クラスに関するAPIや実装の詳細は、**UnityのC# APIドキュメント**に記載されています。
   - [Transform API ドキュメント](https://docs.unity3d.com/ScriptReference/Transform.html)



2. **Unityのソースコードのオープン化**: Unityの一部のソースコード（特にエディター関連）は公開されています。もし特定のコードや拡張機能に興味がある場合は、Unityの[GitHubリポジトリ](https://github.com/Unity-Technologies)や、[UnityのPackage Manager](https://docs.unity3d.com/Manual/PackageManager.html)を確認することも有益かもしれません。



3. **逆アセンブルツール**: Unityの内部コードはネイティブコードとしてコンパイルされているため、C#のコードとしては直接見ることができませんが、デバッガや逆アセンブルツール（ILSpyやdotPeekなど）を使用して、実行時に内部で呼び出されているコードを逆コンパイルすることは可能です。




直接的に`Transform`クラスの実装コードを見たい場合は、UnityのC++ネイティブコードとしての実装部分に関してはソースコードが公開されていないため、逆アセンブルなどの方法を取ることになります。







`Transform`クラスはUnityのC#スクリプトとして実装されており、Unityのランタイムで利用されるアセンブリ（DLL）として配置されています。

これらのDLLは、Unityエディタのインストールディレクトリ内にあります。

### UnityのDLL配置場所

Unityの`Transform`クラスは、Unityエディタやゲーム実行時に使用される基本的なクラスの一部です。これに関連するDLLは、主に以下の場所に配置されています。


#### 1. **Unityエディタのインストールフォルダ内**
   Unityエディタをインストールしたフォルダ内の`Editor/Data/Managed`ディレクトリに、UnityのランタイムDLLが格納されています。特に、`UnityEngine.dll`というファイルが、`Transform`クラスを含む多くのUnityの基本的な機能を提供しています。

   - **場所例 (Windows):**
     ```
     C:\Program Files\Unity\Hub\Editor\<Unityのバージョン>\Editor\Data\Managed\UnityEngine\UnityEngine.dll
     ```
   - **場所例 (Mac):**
     ```
     /Applications/Unity/Hub/Editor/<Unityのバージョン>/Unity.app/Contents/Managed/UnityEngine/UnityEngine.dll
     ```

#### 2. **プロジェクト内の`Library`フォルダ**
   Unityでプロジェクトを開いてビルドすると、`Library`フォルダ内に依存関係のDLLがコピーされます。これにより、エディタ内や実行中に必要なDLLが参照されます。

   - **プロジェクト内の場所:**
     ```
     <YourProject>/Library/ScriptAssemblies/Assembly-CSharp.dll
     ```
   ここに格納されているDLLは、あなたが作成したスクリプトや、Unityが自動的にビルドしたコードが含まれます。`UnityEngine.dll`はプロジェクトのDLLには含まれておらず、Unityのインストールディレクトリから参照されます。

#### 3. **その他の関連DLL**
   Unityでは他にも、`UnityEditor.dll`（エディタ用機能）や、`UnityEngine.CoreModule.dll`（基本的なランタイム機能）などが使われており、これらも`Transform`のようなクラスを含んでいます。

### DLLの確認方法
`Transform`クラスやその他のUnityランタイムクラスが格納されたDLLを確認するための方法として、以下の手順があります。

1. **DLLの場所を確認する**
   Unityエディタがインストールされているフォルダにアクセスし、`UnityEngine.dll`が存在するかを確認します。

2. **逆コンパイルツールを使用する**
   `UnityEngine.dll`の内部コードを確認したい場合、逆コンパイルツール（例えば**ILSpy**や**dotPeek**）を使うことができます。これらのツールでDLLを開くと、`Transform`クラスの実装を調べることができます。

   - **ILSpyを使う方法**:
     1. ILSpyをインストール。
     2. `UnityEngine.dll`をILSpyで開く。
     3. `Transform`クラスを検索して、内部コードを見ることができます。

### 注意点
- `Transform`クラスは、Unityの`UnityEngine.dll`に含まれており、ネイティブコード（C++）で実装されている部分もあります。そのため、C#側で見ることができるのは、APIのインターフェースや一部のメソッド呼び出しのみで、低レベルのネイティブ実装（C++）は見ることができません。
- Unityのソースコードはオープンではないので、完全な内部実装を見ることはできませんが、C# APIとして利用可能な部分については、逆コンパイルを利用して理解することができます。

