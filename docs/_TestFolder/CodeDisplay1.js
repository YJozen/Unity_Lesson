function copyCode() {
    var code = document.getElementById("code-block").innerText.trim();
    navigator.clipboard.writeText(code).then(function() {
      var button = document.querySelector(".copy-button");
      button.innerText = "Copied!";
      setTimeout(function() {
        button.innerText = "Copy";
      }, 2000);
    }).catch(function(err) {
      console.error('Failed to copy: ', err);
    });
  }