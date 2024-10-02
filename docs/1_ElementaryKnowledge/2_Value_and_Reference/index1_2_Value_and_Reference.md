 [参照型・値型](https://drive.google.com/file/d/1vthhKTKuXWux-D-0Wus-gqjaDk-XbfrN/view?usp=drive_link)


 その他
 # Sample1-1

```cs
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Value_and_Reference1
{
    public class Sample1 : MonoBehaviour
    {
        Transform t;

        void Start() {
            t = transform;
        }
        void Update() {
            t.position += Vector3.right;
        }
    }
}
```


<br>

 # Sample1-2

 

 ```cs
 using UnityEngine;

namespace Value_and_Reference1{
    public class Sample2 : MonoBehaviour
    {
        Vector3 v;

        void Start() {
            v = transform.position;
        }
        void Update() {
            v += Vector3.right;
        }
    }
}
 ```


<br>
                                                
                                            
# Sample2

```cs
sing System;
using System.Collections.Generic;
using UnityEngine;

namespace Value_and_Reference2
{
    public class Sample2 : MonoBehaviour
    {
        void Start() {
            // 参照型の例
            List<string> list1 = new List<string> { "A", "B", "C" };
            List<string> list2 = list1;
            list2[0] = "X";
            Debug.Log($"list1 :  {list1[0]}");

            // 値型の例
            int num1 = 42;
            int num2 = num1;
            num2 = 100;
            Debug.Log($"num1 :  {num1}");


            GameObject obj1 = new GameObject("Object 1");
            GameObject obj2 = obj1;
            obj2.name = "Object 2";
            Debug.Log($"obj1.name :  {obj1.name}");





            //メソッド利用
            int val1 = 5;
            ModifyValue(val1);          
            Debug.Log("Value Type (val1): " + val1);

            int val2 = 5;
            ModifyReference(ref val2);
            Debug.Log("Reference Type (val2): " + val2);
        }


        static void ModifyValue(int value) {
            value = 10;
        }

        static void ModifyReference(ref int value) {
            value = 10;
        }
    }
}
```

<br>

# Sample3

```cs
using System;
using System.Collections.Generic;
using UnityEngine;

namespace Value_and_Reference3
{
    public class Sample3 : MonoBehaviour
    {
        [SerializeField] BoxCollider box;

        private void Start()
        {
            //Debug.Log(box);
            //box = GetComponent<BoxCollider>();
            Debug.Log(box);

            Vector3 v = new Vector3();
            v.x = 10;
            v.y = 5;

            box.size = v;
        }
    }
}
```

<br>

# Sample4-1

```cs
//********************************************************
//* 参照型 を 値渡し するパターン
//* (List<T>が参照型)
//********************************************************
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace Value_and_Reference4
{

    public class Sample4_1 : MonoBehaviour
    {

        private void Start()
        {
            Ref_with_Value();
        }

        private void Ref_with_Value()
        {
            var list = new List<int>() { 2, 5, 1, -2 }; // ①この時点で list は {2, 5, 1, -2 }
            Debug.Log($"①  {string.Join(",", list.Select(x => x.ToString()))}");



            EditListRef(list, 3);
            Debug.Log($"④  {string.Join(",", list.Select(x => x.ToString()))}");
            // ④この時点で list は {2, 5, 1, -2, 3 }
            // ※③で値渡しされた参照を書き換えても外のlistには反映されない
        }

        private void EditListRef(List<int> list, int val)
        {
            list.Add(val);
            Debug.Log($"②  {string.Join(",", list.Select(x => x.ToString()))}");
            // ②この時点で list は {2, 5, 1, -2, 3 }
            // ここのlistと外のlistはこの時点では同じヒープ上のメモリを指している



            list = list.OrderBy(x => x).ToList();
            Debug.Log($"③  {string.Join(",", list.Select(x => x.ToString()))}");
            // ③OrderByで新しい領域が確保され、そこへの参照がlistに入れられる。
            // が、listは値渡しされたものであるので、引数の渡し元へは反映されない。
            // この時点で list は {-2, 1, 2, 3, 5} でソートされてるが、
            // 値渡しされたlistの参照先は、呼び出し元のlist(参照型)には反映されない
        }

    }
}
```



<br>


# Sample4-2

```cs
//********************************************************
//* 参照型 を 参照渡し するパターン
//* (List<T>が参照型)
//********************************************************
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

namespace Value_and_Reference4
{

    public class Sample4_2 : MonoBehaviour
    {

        private void Start()
        {
            Ref_with_Value();
        }

        private void Ref_with_Value()
        {
            var list = new List<int>() { 2, 5, 1, -2 };// ①この時点で list は {2, 5, 1, -2 }
            Debug.Log($"①  {string.Join(",", list.Select(x => x.ToString()))}");

            EditListRef(ref list, 3);
            Debug.Log($"④  {string.Join(",", list.Select(x => x.ToString()))}");
            // ④この時点で list は {-2, 1, 2, 3, 5}
            // ※③で代入された参照が、外にも反映される
        }

        private void EditListRef(ref List<int> list, int val)
        {
            list.Add(val);
            Debug.Log($"②  {string.Join(",", list.Select(x => x.ToString()))}");
            // ②この時点で list は {2, 5, 1, -2, 3 }
            // ここのlistと外のlistはこの時点では同じヒープ上のメモリを指している

            list = list.OrderBy(x => x).ToList();
            Debug.Log($"③  {string.Join(",", list.Select(x => x.ToString()))}");
            // ↑ここのlistと外のlistが別のメモリを指すようになったが、
            // 　参照渡しされたlistに代入されたその参照は、外のlistにも反映される
            // ③この時点で list は {-2, 1, 2, 3, 5}
        }

    }
}
```


