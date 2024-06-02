**sample0**


![Unity Logo](images/U_Logo_MadeWith_RichBlack_RGB.png "Unityのロゴ")

`style.css`
~~~css:./hoge/style.css
body {
  color: #abc;
}
~~~

`style.css`
```cs
    [SereializeField]HierarchyObject hierarchyObject;//インスペクターではセットできない
    public void SetHierarchyObject(HierarchyObject hObject){
    　this.hierarchyObject = hObject;
    }
```