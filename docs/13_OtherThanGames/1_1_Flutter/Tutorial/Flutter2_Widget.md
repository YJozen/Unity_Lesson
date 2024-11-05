flutter create xxx
cd xxx
flutter run --device-id chrome 

lib

main.dart


```dart
import 'package:flutter/material.dart';
```


```dart
void main() {
  
}
```


```dart
void main() {
  const b = "バナナ";
  //ここから下　ウィジェット
  const t = Text(b);
  const c = Center(child:t);
  const s = Scaffold(body: c);
  const a = MaterialApp(home: s);
  runApp(a);
}
```



```dart
void main() {
  const b = "バナナ";
  const a = MaterialApp(
    home:Scaffold(
        body:  Center(
            child:Text("バナナ")
        ),
    ),
  );
  runApp(a);
}
```