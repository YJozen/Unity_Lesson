
### 外部サイト

<a href="https://zenn.dev/meson/articles/make-dll-for-unity" target="_blank">・C++ライブラリ（DLL）をUnity（C#）向けに作成して利用するシンプルな方法</a>


<a href="https://dokuro.moe/unity-how-to-make-dll-from-c-charp-scripts/" target="_blank">・【Unity】C#スクリプトをDLL化する手順</a>

<a href="https://qiita.com/r-ngtm/items/50afdb29c671001bb290" target="_blank">・C#スクリプトをDLL化してUnityで使う</a>

<br>

<br>


# DLLを用意する

C++の関数を外部ライブラリとしてDLL（動的リンクライブラリ）ファイルにコンパイルする方法を解説します。  
以下は、Windows環境でVisual Studioを使用する方法を説明しますが、他のコンパイラやIDEを使用する場合でも概念は同じです。

### 手順

#### 1. DLLプロジェクトの作成
Visual Studioを使用してC++ DLLを作成するためには、まずDLLプロジェクトを作成します。

1. **Visual Studioを開く**  
   Visual Studioを開き、「新しいプロジェクト」を作成します。

2. **プロジェクトタイプの選択**  
   「C++」を選択し、「DLL」を選択します。「空のプロジェクト」や「動的ライブラリ」を選択しても構いません。

3. **プロジェクト名と保存先を設定**  
   プロジェクトに名前を付け、保存場所を決めて「作成」ボタンをクリックします。

#### 2. DLLとしてエクスポートする関数の定義

C++でDLLを作成する際、関数をエクスポートするには`__declspec(dllexport)`を使います。DLLからインポートする際には`__declspec(dllimport)`を使います。

以下のようにコードを記述します：

```cpp
// example.h

#ifdef EXAMPLE_EXPORTS  // EXAMPLE_EXPORTSが定義されていれば、dllのエクスポートを有効にする
#define EXAMPLE_API __declspec(dllexport)
#else
#define EXAMPLE_API __declspec(dllimport)
#endif

extern "C" {  // C++の名前修飾を避けるためにextern "C"を使用
    EXAMPLE_API void helloWorld();
}
```

```cpp
// example.cpp

#include "example.h"
#include <iostream>

void helloWorld() {
    std::cout << "Hello, World!" << std::endl;
}
```

- `__declspec(dllexport)`は関数がDLLからエクスポートされることを示します。
- `__declspec(dllimport)`は関数がDLLからインポートされることを示します。
- `extern "C"`は、C++の名前修飾（mangling）を防ぎ、Cスタイルの名前で関数をエクスポートするために使用します。

#### 3. プロジェクトのビルド設定

1. **プロジェクトのプロパティ設定**  
   プロジェクトを右クリックし、「プロパティ」を選択します。

2. **C/C++ の設定**  
   「C/C++」 > 「コード生成」 > 「ランタイムライブラリ」で「マルチスレッド DLL」を選択します。

3. **出力設定**  
   「構成プロパティ」 > 「リンカー」 > 「出力ファイル」でDLLの出力先を設定します。例: `$(OutDir)example.dll`

#### 4. DLLのビルド

1. ビルドの準備が整ったら、「ビルド」 > 「ソリューションのビルド」をクリックしてDLLをコンパイルします。
2. 成功すると、`example.dll`というファイルが出力フォルダに作成されます。

#### 5. DLLのインポートと使用

DLLを使用するプロジェクトで、`example.h`をインクルードし、エクスポートされた関数を呼び出せるようにします。

```cpp
// main.cpp
#include <iostream>
#include "example.h"

int main() {
    helloWorld();  // DLL内の関数を呼び出す
    return 0;
}
```

このコードをビルドするには、先程作成したDLLが必要です。リンクする際にDLLのインポートライブラリ（`example.lib`）も必要になる場合があります。

#### 6. DLLの実行

1. 実行時に、作成したDLL（`example.dll`）を実行可能ファイルと同じディレクトリに置いてください。
2. 実行すると、DLL内の`helloWorld`関数が呼ばれ、「Hello, World!」がコンソールに出力されます。




<br>

# DLLをUnityで使用する


C++で作成したDLLをUnityで使用するには、UnityからそのDLLを呼び出せるように設定する必要があります。  
以下は、UnityでC++ DLLを使用する方法を説明します。

### 手順

#### 1. UnityプロジェクトにDLLを追加

まず、作成したC++ DLL（例：`example.dll`）をUnityプロジェクトに追加します。

1. **Unityプロジェクトを開く**  
   Unityエディタで、使用するプロジェクトを開きます。

2. **DLLをPluginsフォルダに追加**  
   プロジェクト内に`Plugins`というフォルダを作成し、その中にC++で作成したDLLファイル（例：`example.dll`）を追加します。  
   フォルダ構造の例：
   ```
   Assets/
      Plugins/
         example.dll
   ```

#### 2. C#コードからDLL関数を呼び出す

次に、UnityのC#コードからC++ DLLを呼び出せるようにします。これには、`[DllImport]`属性を使用します。

以下は、C#からC++ DLLの関数を呼び出す例です：

```csharp
using System;
using System.Runtime.InteropServices;
using UnityEngine;

public class DLLExample : MonoBehaviour
{
    // C++の関数をインポート
    [DllImport("example.dll", CallingConvention = CallingConvention.Cdecl)]
    private static extern void helloWorld();

    void Start()
    {
        // DLL内の関数を呼び出す
        helloWorld();
    }
}
```

#### 3. 解説

- `DllImport`属性は、C++ DLL内の関数をC#から呼び出すために使います。`example.dll`は、Unityが実行時に探すDLLの名前です。`example.dll`が`Plugins`フォルダにあるため、UnityはそのDLLを自動的に探します。
- `CallingConvention.Cdecl`は、C++のデフォルトの呼び出し規約です。もしC++の関数で異なる呼び出し規約（例えば`stdcall`）を使っている場合は、`CallingConvention.StdCall`に変更する必要があります。
- `extern "C"`はC++の名前修飾を防ぎ、Cスタイルでエクスポートされる関数を呼び出すために使用しています。

#### 4. DLLを正しく読み込むための注意点

- **ビルド設定**  
   `example.dll`を正しくインポートするためには、UnityがDLLを正しく読み込むことができるビルド設定を行う必要があります。例えば、`example.dll`が64bitのアーキテクチャ用である場合、Unityのプロジェクト設定も64bitのターゲットに設定しておく必要があります。
  
- **DLLの依存関係**  
   C++で作成したDLLが他のライブラリに依存している場合、そのライブラリもUnityプロジェクトの`Plugins`フォルダに配置する必要があります。

- **プラットフォームに合わせたDLLの配置**  
   Unityはプラットフォームごとに異なるビルド設定を使用します。例えば、Windowsの64bit用にコンパイルしたDLLをUnityに組み込む場合、Unityのビルドターゲットも64bitに設定する必要があります。

   DLLのプラットフォーム設定は、Unityのインスペクターで以下のように設定できます：
   1. `Assets`フォルダ内で`example.dll`を選択します。
   2. インスペクターの「Platform Settings」セクションで、ターゲットプラットフォーム（例えば、`x86_64`や`x86`）を選択し、適切に設定します。

#### 5. 実行

C#コードが正常に記述され、DLLが正しく設定されていれば、Unityを実行した際に、`helloWorld`関数が呼び出され、C++で定義された動作（例：コンソールへの出力など）が実行されます。


<br>


<br>

1. **C++で作成したDLLをUnityの`Plugins`フォルダに追加**  
2. **C#コードで`[DllImport]`属性を使用してC++ DLL内の関数を呼び出す**  
3. **ビルドターゲットやプラットフォームに応じたDLL設定を行う**

これで、UnityでC++ DLLを呼び出して、関数を実行できるようになります。


<br>


<br>