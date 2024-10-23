color
width &height
child
alignment
padding margin


```dart
 final con = Container(
    color: Colors.deepOrange,
    width: 100,
    height: 100,
  );

  final row = Row(
    mainAxisAlignment: MainAxisAlignment.center,
    crossAxisAlignment: CrossAxisAlignment.center,
    children: [col , con ,img  ]
  );

  final a = MaterialApp(
    home: Scaffold(
        body:  Center(
            child: row,
        ),
    ),
  );
  runApp(a);
```