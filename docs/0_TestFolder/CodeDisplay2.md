<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css">
<script src="//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>

<style>
    .highlighted {
        color: red; /* テキストの色を赤にする */
        font-weight: bold; /* 太字にする */
    }
</style>

## コードの例1



<pre><code class="language-csharp">
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Car : MonoBehaviour {
    public List<AxleInfo> axleInfos;
    <span class="highlighted">
    public float maxMotorTorque;       // 最大駆動力
    public float maxSteeringAngle; 
    </span>
}
</code></pre>




## コードの例2

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
