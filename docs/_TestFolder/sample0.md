## コードの例

以下のボタンをクリックすると、コードをコピーできます。


<div class="code-container">
  <button class="copy-button" onclick="copyCode(this)">コピー</button>
  <pre><code class="language-csharp">
using System;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }
}
  </code></pre>
</div>



<style>
.code-container {
  position: relative;
  background-color: #f4f4f4;
  border-radius: 4px;
  padding: 1em;
}

.copy-button {
  position: absolute;
  top: 5px;
  right: 5px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

code {
  font-family: 'Courier New', Courier, monospace;
}

/* C# syntax highlighting */
.token.keyword { color: #0000ff; }
.token.string { color: #a31515; }
.token.comment { color: #008000; }
.token.class-name { color: #2b91af; }
</style>

<script>
function copyCode(button) {
  var codeBlock = button.nextElementSibling.querySelector('code');
  var code = codeBlock.innerText.trim();

  navigator.clipboard.writeText(code).then(function() {
    button.innerText = "コピーしました";
    setTimeout(function() {
      button.innerText = "コピー";
    }, 2000);
  }).catch(function(err) {
    console.error('コピーに失敗しました: ', err);
  });
}
</script>
