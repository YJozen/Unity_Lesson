## C#のコード例

```csharp
using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hello, World!");
    }
}
```



<script>
document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelectorAll('pre code').forEach((block) => {
    var button = document.createElement('button');
    button.innerText = 'コピー';
    button.addEventListener('click', function() {
      navigator.clipboard.writeText(block.innerText).then(function() {
        button.innerText = 'コピーしました！';
        setTimeout(function() {
          button.innerText = 'コピー';
        }, 2000);
      });
    });
    block.parentNode.insertBefore(button, block);
  });
});
</script>


<style>
pre {
  position: relative;
}
pre button {
  position: absolute;
  top: 0;
  right: 0;
  padding: 5px 10px;
  background-color: #f7f7f7;
  border: none;
  border-radius: 0 0 0 5px;
  cursor: pointer;
}
</style>



<script src="https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/2.0.8/clipboard.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', (event) => {
  new ClipboardJS('.copy-button');
});
</script>


<button class="copy-button" data-clipboard-target="#code-block-id">
  コピー
</button>
<pre><code id="code-block-id">
// ここにコードを記述
</code></pre>


