**sample0**


![Unity Logo](images/U_Logo_MadeWith_RichBlack_RGB.png "Unityのロゴ")

```cs:PrefabObject.cs

[SereializeField]HierarchyObject hierarchyObject;//インスペクターではセットできない

public void SetHierarchyObject(HierarchyObject hObject){
　this.hierarchyObject = hObject;
}
```