C++の関数の書き方いくつか

# 1. 通常の関数

基本的な関数の定義方法です。(関数宣言と定義を別々に書くことも可能。）

```cpp
#include <iostream>

int add(int a, int b); // 宣言（プロトタイプ）

int main() {
    std::cout << add(3, 5) << std::endl;
    return 0;
}

int add(int a, int b) { // 定義
    return a + b;
}
```

<br>

# 2. 関数のオーバーロード

同じ関数名で異なる引数の型や数を持つ関数を定義できます。これを「関数のオーバーロード」といいます。

```cpp
#include <iostream>

int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }

int main() {
    std::cout << add(3, 5) << std::endl;       // int版が呼び出される
    std::cout << add(3.5, 5.5) << std::endl;   // double版が呼び出される
    return 0;
}
```

<br>

# 3. デフォルト引数

関数の引数にデフォルト値を指定することで、引数が省略された場合にその値が使われます。

```cpp
#include <iostream>

void greet(const std::string& name = "Guest") {
    std::cout << "Hello, " << name << "!" << std::endl;
}

int main() {
    greet();               // "Hello, Guest!" が出力される
    greet("Alice");        // "Hello, Alice!" が出力される
    return 0;
}
```

<br>

# 4. 関数ポインタ

関数のアドレスを保持し、動的に関数を呼び出すことができます。

```cpp
#include <iostream>

int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }

int main() {
    int (*operation)(int, int); // 関数ポインタの宣言
    operation = &add;           // add関数を指す
    std::cout << operation(5, 3) << std::endl; // "8" が出力される

    operation = &multiply;      // multiply関数を指す
    std::cout << operation(5, 3) << std::endl; // "15" が出力される
    return 0;
}
```

<br>

# 5. ラムダ式（匿名関数）

C++11以降ではラムダ式を使って無名関数（匿名関数）を作成できます。特に、短い関数をその場で定義したい場合や関数オブジェクトのように使いたいときに便利です。

```cpp
#include <iostream>

int main() {
    auto add = [](int a, int b) { return a + b; }; // ラムダ式で関数を定義
    std::cout << add(3, 5) << std::endl;           // "8" が出力される
    return 0;
}
```

<br>

# 6. メンバー関数（クラス内関数）

クラスや構造体内で定義される関数で、クラス内のデータにアクセスするために使用されます。

```cpp
#include <iostream>

class Calculator {
public:
    int add(int a, int b) { return a + b; }       // メンバー関数
};

int main() {
    Calculator calc;
    std::cout << calc.add(3, 5) << std::endl;     // "8" が出力される
    return 0;
}
```

<br>

# 7. 仮想関数（Virtual関数）

仮想関数は、派生クラスでオーバーライド可能な関数で、主にポリモーフィズム（多態性）を実現するために使われます。

```cpp
#include <iostream>

class Animal {
public:
    virtual void speak() { std::cout << "Some sound" << std::endl; }
};

class Dog : public Animal {
public:
    void speak() override { std::cout << "Woof" << std::endl; }
};

int main() {
    Animal* animal = new Dog();
    animal->speak(); // Dogのspeak()が呼び出され "Woof" が出力される
    delete animal;
    return 0;
}
```

<br>

# 8. テンプレート関数

テンプレート関数は、データ型を指定せずに関数を定義し、任意の型で呼び出せるようにするための仕組みです。C++でのジェネリックプログラミングに使われます。

```cpp
#include <iostream>

template <typename T>
T add(T a, T b) {
    return a + b;
}

int main() {
    std::cout << add(3, 5) << std::endl;       // int型の add
    std::cout << add(3.5, 5.5) << std::endl;   // double型の add
    return 0;
}
```

<br>

# 9. constexpr関数（定数式関数）

`constexpr`関数はコンパイル時に計算されることを保証する関数です。コンパイル時に決まる定数として評価されるため、パフォーマンスが向上します。

```cpp
#include <iostream>

constexpr int square(int x) {
    return x * x;
}

int main() {
    constexpr int result = square(5); // コンパイル時に計算される
    std::cout << result << std::endl; // "25" が出力される
    return 0;
}
```

<br>

# 10. インライン関数

```cpp
inline int add(int a, int b) {
    return a + b;
}

int result = add(3, 5); 
```

### 1. 通常の関数

通常の関数を呼び出すと、プログラムは**関数のアドレス**を参照し、そこで実行するように動きます。この動きには以下の手順が含まれます：

1. **関数呼び出し**: 呼び出し元である関数から、呼び出したい関数の場所（メモリ上のアドレス）に移動します。
2. **スタックの操作**: 関数の引数や戻り先の情報をスタック（メモリの一時保管場所）に保存します。
3. **処理の実行**: 関数の処理を実行し、戻り値を返します。
4. **元の場所に戻る**: スタックを片付け、元の関数に戻って処理を続行します。

この手順には**関数の呼び出しごとにオーバーヘッド**（処理の遅延）が発生しますが、同じ関数を複数回呼び出しても、関数本体のコードは1か所に置かれるため、**メモリ効率が良い**です。

### 2. インライン関数

インライン関数は、関数を呼び出す際に**関数の内容を呼び出し元に直接埋め込む**ことで、通常の関数と異なる方法で処理します：

1. **展開**: コンパイラは関数呼び出し時にインライン関数のコードをそのまま呼び出し元に展開します。実際に関数が呼び出されるのではなく、あたかもコードがその場に直接書かれたような形になります。
   
   - 例えば、`inline int add(int a, int b) { return a + b; }` を `add(3, 5)` と呼び出すと、コンパイラはそれを `3 + 5` として直接埋め込みます。

2. **呼び出しオーバーヘッドなし**: 通常の関数のようなアドレス参照やスタック操作が不要です。そのため、呼び出しオーバーヘッドがなくなり、**実行速度が向上**します。

3. **コードサイズ増加の可能性**: インライン展開は、関数呼び出しのたびに関数コードを挿入するため、同じ関数が多く呼ばれる場合、**コードサイズが大きくなる**可能性があります。

### 比較まとめ

| 特徴                  | 通常の関数                                 | インライン関数                                           |
|-----------------------|------------------------------------------|---------------------------------------------------------|
| 呼び出しオーバーヘッド     | あり                                      | なし                                                    |
| コードのメモリ効率         | メモリ効率が良い                            | 頻繁に使われるとコードが大きくなる可能性がある               |
| 実行速度               | 比較的遅い                                  | 呼び出しオーバーヘッドがなく高速                           |
| 使用目的               | 大きくて複雑な関数や頻繁に呼び出されない関数 | 小さな関数や頻繁に呼び出される関数に適している              |

インライン関数は、短く頻繁に呼ばれる関数のパフォーマンスを向上させるための工夫ですが、大きすぎる関数や複雑な処理には向いていません。