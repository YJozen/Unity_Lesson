C#での関数の書き方いくつか

# 1. 通常のメソッド

Unityでは通常、メソッドは`MonoBehaviour`を継承したクラス内で定義します。

```csharp
using UnityEngine;

public class MethodExample : MonoBehaviour
{
    void Start()
    {
        int result = Add(3, 5);
        Debug.Log(result); // "8" が出力される
    }

    int Add(int a, int b) // インスタンスメソッド
    {
        return a + b;
    }
}
```

<br>

# 2. メソッドのオーバーロード

Unityでもメソッドのオーバーロードを利用できます。

```csharp
using UnityEngine;

public class OverloadExample : MonoBehaviour
{
    void Start()
    {
        Debug.Log(Add(3, 5));       // "8" が出力される
        Debug.Log(Add(3.5f, 5.5f)); // "9" が出力される
    }

    int Add(int a, int b) { return a + b; }
    float Add(float a, float b) { return a + b; }
}
```

<br>

# 3. デフォルト引数

Unityでもメソッドにデフォルト引数を指定することができます。

```csharp
using UnityEngine;

public class DefaultArgumentExample : MonoBehaviour
{
    void Start()
    {
        Greet();          // "Hello, Guest!" が出力される
        Greet("Alice");   // "Hello, Alice!" が出力される
    }

    void Greet(string name = "Guest")
    {
        Debug.Log("Hello, " + name + "!");
    }
}
```

<br>

# 4. デリゲート（関数ポインタに相当）

Unityでデリゲートを使って、関数を動的に切り替えて呼び出すことができます。

```csharp
using UnityEngine;

public class DelegateExample : MonoBehaviour
{
    delegate int Operation(int a, int b); // デリゲート型を定義
    Operation operation;

    void Start()
    {
        operation = Add;
        Debug.Log(operation(5, 3)); // "8" が出力される

        operation = Multiply;
        Debug.Log(operation(5, 3)); // "15" が出力される
    }

    int Add(int a, int b) { return a + b; }
    int Multiply(int a, int b) { return a * b; }
}
```

<br>

# 5. ラムダ式（匿名関数）

ラムダ式を使って匿名関数を作成し、Unityでメソッド内に直接書くことができます。

```csharp
using UnityEngine;
using System;

public class LambdaExample : MonoBehaviour
{
    void Start()
    {
        Func<int, int, int> add = (a, b) => a + b;
        Debug.Log(add(3, 5)); // "8" が出力される
    }
}
```

<br>

# 6. インターフェースメソッドと抽象メソッド

C#のインターフェースと抽象メソッドを使うことで、Unityでも仮想関数のようなメソッドのオーバーライドが可能です。

```csharp
using UnityEngine;

public class InterfaceExample : MonoBehaviour
{
    void Start()
    {
        Animal animal = new Dog();
        animal.Speak(); // "Woof" が出力される
    }
}

abstract class Animal
{
    public abstract void Speak(); // 抽象メソッド
}

class Dog : Animal
{
    public override void Speak()
    {
        Debug.Log("Woof");
    }
}
```

<br>

# 7. ジェネリックメソッド

Unityでもジェネリックメソッドを使って、異なる型に対応したメソッドを定義することができます。

```csharp
using UnityEngine;

public class GenericExample : MonoBehaviour
{
    void Start()
    {
        Debug.Log(Add(3, 5));      // "8" が出力される
        Debug.Log(Add(3.5f, 5.5f));// "9" が出力される
    }

    T Add<T>(T a, T b) where T : struct //T が値型（構造体）であることを制約しています。これにより、int や float などの値型しか受け取れません
    {
        dynamic x = a, y = b; //dynamic 型は、コンパイル時に型チェックを行わず、実行時に型が決まります
        return x + y;
    }
}
```

<br>


# 8. ローカル関数

以下のコードでは、Addメソッド内にローカル関数LocalAddが定義されています。LocalAddはAddメソッド内でしか呼び出せず、処理がAddメソッドに閉じ込められています。

```csharp
using UnityEngine;

public class LocalFunctionExample : MonoBehaviour
{
    void Start()
    {
        Debug.Log(Add(3, 5)); // "8" が出力される
    }

    int Add(int a, int b)
    {
        int LocalAdd(int x, int y) // ローカル関数
        {
            return x + y;
        }
        return LocalAdd(a, b);
    }
}
```

<br>

# 9. インラインメソッドの最適化

C#には直接のインライン指定はありませんが、`MethodImplOptions.AggressiveInlining`属性を使って最適化のインライン化を促せます。
ただ、C#のインライン化はJITコンパイラ次第なので、AggressiveInliningを指定しても、インライン化されないことがあります。また、コードが複雑すぎる場合や大きすぎる場合には、逆にパフォーマンスが低下する可能性もあるため、むやみに使わず、使うならパフォーマンス検証を行いながら使う必要があります。

```csharp
using UnityEngine;
using System.Runtime.CompilerServices;

public class InlineExample : MonoBehaviour
{
    void Start()
    {
        Debug.Log(Add(3, 5)); // "8" が出力される
    }

    [MethodImpl(MethodImplOptions.AggressiveInlining)]
    int Add(int a, int b)
    {
        return a + b;
    }
}
```