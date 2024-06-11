[Sample0_Test](Sample0_TestFolder/sample0.md)

# Unity Documentation

## **目次**

1. Unity前提知識. 
   [参照型・値型](#sample12_1)
    - [参照型・値型_Sample1](#sample12_1_1)
    - [参照型・値型_Sample2](#sample12_1_2)
    - [参照型・値型_Sample3](#sample12_1_3)

2. Unity基本. 
    1. [Sample1-入力](#sample1-入力)   
        + [InputManager](#sample1_1) 
        + [InputSystem](#sample1_2)
    2. [Sample2-移動](#sample2-移動)  
        + [Move_Transform](#sample2_1) 
        + [Move_Rigidbody](#sample2_2)
        + [Move_CharacterController](#sample2_3)
        + [Move_Sample](#sample2_4)
        - [TPS](#sample2_4_1)
        - [Warp](#sample2_4_2)
    3. [Sample3-回転](#sample3-回転)
        + [Transform](#sample3_1) 
        + [Rigidbody](#sample3_2)
    4. [Sample4-UI](#sample4-ui)
        + [UI_Basic](#sample4_1)
           - [UI_Basic_Sample1](#sample4_1_1)
           - [UI_Basic_RectTransform](#sample4_1_2)
           - [UI_Basic_Pop](#sample4_1_2)
           - [UI_Basic_CountDown](#sample4_1_2)
           - [UI_Basic_LookAt_HPBar](#sample4_1_2)
           - [Minimap]
        + [UI_MVP](#sample4_2)
           - [MVP_Basic](#sample4_2_1)
           - [MVP_DependencyInjection](#sample4_2_2)
        + [TextMeshPro](#sample4_3)
    5. [Sample5-サウンド](#sample5-サウンド)
       + [AudioSource](#sample5_1)
       + [AudioMixer](#sample5_2)
       + [CRI_Ware](#sample5_3)
    6. [Sample6-アニメーション](#sample6-アニメーション)
        + [AnimationControllerの利用](#sample6_1) 
        - [Animation_Basic](#sample6_1_1)
        - [Animation_StateMachine](#sample6_1_2)
        - [Animation_AvaterMask](#sample6_1_3)   
        - [Animation_Ragdoll](#sample6_1_4)  
        + [DOTween](#sample6_2)
    7. [Sample7-シーン](#sample7-シーン)
    8. [Sample8-エフェクト](#sample8-エフェクト)  
        + [ParticleSystem](#sample8_1)
        + [VFX](#sample8_2)
    9. [Sample9-メソッド実行](#sample9-メソッド実行)
        + [メソッド実行_Basic](#sample9_1)
        + [メソッド実行_Event](#sample9_2)
        + [メソッド実行_UnityEvent](#sample9_2_1)
        + [メソッド実行_PrefabReference](#sample9_3)
        + [メソッド実行_Singleton](#sample9_4)


3. Unity機能_その他. [Sample-いろいろ](#sample-いろいろ) 
  + [Cinemachine](#sample_cinemachine)
  + [ScriptableObject](#sample_scriptableobject)    
  + [Timeline](#sample_timeline)
  + [NavMesh](#sample_navmesh)
  + [Ray](#sample_ray)
     - [Jump](#sample_jump)
        * [Ray_Basic](#sample_ray_basic)
        * [Ray_3Combo](#sample_ray_3combo)
     - [Mouse](#sample_mouse)
        * [Mouse_Ray](#sample_mouse_ray)
        * [Mouse_TargetLock](#sample_mouse_targetlock)
        * [Mouse_Effect](#sample_mouse_effect)
  + [Shader_Basic](#sample_shader_basic)
     - [Shader1-CS](#sample_shader1)
     - [Shader2-HLSL_CG](#sample_shader2)
     - [Shader3-ShaderGraph](#sample_shader3)  
  + [Shader_Advanced](#sample_shader_advanced)
     - [Shader1-Tessellation](#sample_shader1)
     - [Shader2-Geometry](#sample_shader2)
     - [Shader3-Liquid](#sample_shader3) 
     - [Shader4-Ink](#sample_shader4)
     - [Shader5-DynamicMesh](#sample_shader5)
  + [データ保存](#sample_データ保存)
      - [データ保存_PlayerPrefs](#sample_データ保存_PlayerPrefs)
      - [データ保存_Json](#sample_データ保存_Json)
      - [データ保存_Playfab](#sample_データ保存_Playfab)
      - [データ保存_QuickSaveAssets](#sample_データ保存_QuickSaveAssets)
      - [データ保存_AssetBundle](#sample_データ保存_AssetBundle)
      - [データ保存_Addressable](#sample_データ保存_Addressable)
  + [Coroutine](#sample_coroutine)
  + [UniTask](#sample_unitask)
      - [UniTask_Async](#sample_unitask_async)
         * [UniTask_Sample1](#sample_unitask_sample1)
         * [UniTask_Sample2](#sample_unitask_sample2)
         * [UniTask_Sample3](#sample_unitask_sample3)
      - [UniTask_Cancel](#sample_unitask_cancel)
         * [UniTask_CancelSample1](#sample_unitask_cancelsample1)
         * [UniTask_CancelSample2](#sample_unitask_cancelsample2)
         * [UniTask_CancelSample3](#sample_unitask_cancelsample3)
(#sample_unitask_statemachine_advanced)
  + [NetCode_for_GameObjects](#sample_netcode_for_gameobjects)
  + [ML-Agents](#sample_ml-agents)




4. 小ネタ. [Sample9-小ネタ](Sample9/sample9.md)
  + [シャッフル](#sample_シャッフル)  
  + [LineDraw](#sample_linedraw)
  + [MoveFloor](#sample_movefloor)
  + [Reflection](#sample_reflection)
  + [A*](#sample_a*)




5. ミニゲーム. [Sample10-ミニゲーム](Sample10/sample10.md)
  + [ブロック崩し](#sample10_1)
  + [オセロ](#sample10_2)
  + [ステルスゲーム](#sample10_3)

6. Unity雑学. [Sample11-Unity雑学](Sample11/sample11.md)
  + [シリアライズ](#sample11_1)
  + [GUID](#sample11_2)
  + [Rigidbody](#sample11_3)


7. プログラム基本. [Sample13-プログラム基本](Sample13/sample13.md)
  + [C#基本](#sample13_1)
  + [インターフース](#sample13_2)
  + [デリゲート](#sample13_3)
  + [イベント](#sample13_4)
  + [デリゲートとイベント](#sample13_5)
  + [SOLID](#sample13_6)
  + [Generics](#sample13_7)
  + [デザインパターン](#sample13_8)
  　　 - [デザインパターン_State](#sample13_8_1)
       * [デザインパターン_State_NonGeneric](#sample13_8_1_2)
       * [デザインパターン_State_Generic](#sample13_8_1_1)  　　  
  　　 - [デザインパターン_Command](#sample13_8_2)


8. UnrealEngine


9. ゲーム以外
  + [GitHub](#sample_github)
  + [Gas](#sample_gas)
  + [Python](#sample_python)
  + [Docker](#sample_docker)



***
# sample1-入力

[Sample1へ移動](Sample1/sample1.md)  


***
# Sample2-移動
[Sample2へ移動](Sample2/sample2.md)



***
# Sample3-回転
[Sample3へ移動](Sample3/sample3.md)
### sample3_1

### sample3_2





***
# Sample4-UI
[Sample4へ移動](Sample4/sample4.md)




***
# Sample5-サウンド
[Sample5へ移動](Sample5/sample5.md)


***
# Sample6-アニメーション
[Sample6へ移動](Sample6/sample6.md)
### sample6_1

### sample6_2



***
# Sample-いろいろ
[Sampleへ移動](Sample/sample.md)
### sample_ScriptableObject

### sample_シャッフル

### sample_Timeline

### sample_Shader
- ##### sample_Shader1
- ##### sample_Shader2
- ##### sample_Shader3

