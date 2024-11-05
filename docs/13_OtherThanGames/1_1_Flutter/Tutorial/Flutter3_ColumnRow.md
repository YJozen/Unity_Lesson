cd xxx
flutter run --device-id chrome 

# Column

```dart
void main() {
  final col = Column(children:[

    Text("レモン"),
    Text("林檎"),
    Text("ぶどう")
  ]);

  const a = MaterialApp(
    home:Scaffold(
        body:  Center(
            child:col,
        ),
    ),
  );
  runApp(a);
}
```

<br>



```dart
void main() {
  final col = Column(
    mainAxisAlignment: MainAxisAlignment.center,
    crossAxisAlignment: CrossAxisAlignment.center,
    children:[
      Text("レモン"),
      Text("林檎"),
      Text("ぶどう")
    ]
  );

  final a = MaterialApp(
    home:Scaffold(
        body:  Center(
            child: col,
        ),
    ),
  );

  runApp(a);
}
```

# Row


```dart
void main() {
  final col = Row(
    mainAxisAlignment: MainAxisAlignment.center,
    crossAxisAlignment: CrossAxisAlignment.center,
    children:[
      Text("レモン"),
      Text("林檎"),
      Text("ぶどう")
    ]
  );

  final a = MaterialApp(
    home:Scaffold(
        body:  Center(
            child: col,
        ),
    ),
  );

  runApp(a);
}
```