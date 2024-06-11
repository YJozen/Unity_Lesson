# Unity Documentation

## **目次**

1. Unity前提知識
   - [参照型・値型](#参照型・値型)
     - [参照型・値型_Sample1](#参照型・値型_sample1)
     - [参照型・値型_Sample2](#参照型・値型_sample2)
     - [参照型・値型_Sample3](#参照型・値型_sample3)

2. Unity基本
   1. [Sample1-入力](#sample1-入力)
       + [InputManager](#inputmanager)
       + [InputSystem](#inputsystem)
   2. [Sample2-移動](#sample2-移動)
       + [Move_Transform](#move_transform)
       + [Move_Rigidbody](#move_rigidbody)
       + [Move_CharacterController](#move_charactercontroller)
       + [Move_Sample](#move_sample)
         - [TPS](#tps)
         - [Warp](#warp)
   3. [Sample3-回転](#sample3-回転)
       + [Transform](#transform)
       + [Rigidbody](#rigidbody)
   4. [Sample4-UI](#sample4-ui)
       + [UI_Basic](#ui_basic)
         - [UI_Basic_Sample1](#ui_basic_sample1)
         - [UI_Basic_RectTransform](#ui_basic_recttransform)
         - [UI_Basic_Pop](#ui_basic_pop)
         - [UI_Basic_CountDown](#ui_basic_countdown)
         - [UI_Basic_LookAt_HPBar](#ui_basic_lookat_hpbar)
       + [Minimap](#minimap)
       + [UI_MVP](#ui_mvp)
         - [MVP_Basic](#mvp_basic)
         - [MVP_DependencyInjection](#mvp_dependencyinjection)
       + [TextMeshPro](#textmeshpro)
   5. [Sample5-サウンド](#sample5-サウンド)
       + [AudioSource](#audiosource)
       + [AudioMixer](#audiomixer)
       + [CRI_Ware](#cri_ware)
   6. [Sample6-アニメーション](#sample6-アニメーション)
       + [AnimationControllerの利用](#animationcontrollerの利用)
         - [Animation_Basic](#animation_basic)
         - [Animation_StateMachine](#animation_statemachine)
         - [Animation_AvaterMask](#animation_avatermask)
         - [Animation_Ragdoll](#animation_ragdoll)
       + [DOTween](#dotween)
   7. [Sample7-シーン](#sample7-シーン)
   8. [Sample8-エフェクト](#sample8-エフェクト)
       + [ParticleSystem](#particlesystem)
       + [VFX](#vfx)
   9. [Sample9-メソッド実行](#sample9-メソッド実行)
       + [メソッド実行_Basic](#メソッド実行_basic)
       + [メソッド実行_Event](#メソッド実行_event)
       + [メソッド実行_UnityEvent](#メソッド実行_unityevent)
       + [メソッド実行_PrefabReference](#メソッド実行_prefabreference)
       + [メソッド実行_Singleton](#メソッド実行_singleton)

3. Unity機能_その他
   - [Sample-いろいろ](#sample-いろいろ)
     + [Cinemachine](#cinemachine)
     + [ScriptableObject](#scriptableobject)
     + [Timeline](#timeline)
     + [NavMesh](#navmesh)
     + [Ray](#ray)
       - [Jump](#jump)
         * [Ray_Basic](#ray_basic)
         * [Ray_3Combo](#ray_3combo)
       - [Mouse](#mouse)
         * [Mouse_Ray](#mouse_ray)
         * [Mouse_TargetLock](#mouse_targetlock)
         * [Mouse_Effect](#mouse_effect)
     + [Shader_Basic](#shader_basic)
       - [Shader1-CS](#shader1-cs)
       - [Shader2-HLSL_CG](#shader2-hlsl_cg)
       - [Shader3-ShaderGraph](#shader3-shadergraph)
     + [Shader_Advanced](#shader_advanced)
       - [Shader1-Tessellation](#shader1-tessellation)
       - [Shader2-Geometry](#shader2-geometry)
       - [Shader3-Liquid](#shader3-liquid)
       - [Shader4-Ink](#shader4-ink)
       - [Shader5-DynamicMesh](#shader5-dynamicmesh)
     + [データ保存](#データ保存)
       - [データ保存_PlayerPrefs](#データ保存_playerprefs)
       - [データ保存_Json](#データ保存_json)
       - [データ保存_Playfab](#データ保存_playfab)
       - [データ保存_QuickSaveAssets](#データ保存_quicksaveassets)
       - [データ保存_AssetBundle](#データ保存_assetbundle)
       - [データ保存_Addressable](#データ保存_addressable)
     + [Coroutine](#coroutine)
     + [UniTask](#unitask)
       - [UniTask_Async](#unitask_async)
         * [UniTask_Sample1](#unitask_sample1)
         * [UniTask_Sample2](#unitask_sample2)
         * [UniTask_Sample3](#unitask_sample3)
       - [UniTask_Cancel](#unitask_cancel)
         * [UniTask_CancelSample1](#unitask_cancelsample1)
         * [UniTask_CancelSample2](#unitask_cancelsample2)
         * [UniTask_CancelSample3](#unitask_cancelsample3)
       - [UniTask_StateMachine_Advanced](#unitask_statemachine_advanced)
     + [NetCode for GameObjects](#netcode_for_gameobjects)
     + [ML-Agents](#ml-agents)

4. 小ネタ
   - [Sample9-小ネタ](Sample9/sample9.md)
     + [シャッフル](#シャッフル)
     + [LineDraw](#linedraw)
     + [MoveFloor](#movefloor)
     + [Reflection](#reflection)
     + [A*](#a*)

5. ミニゲーム
   - [Sample10-ミニゲーム](Sample10/sample10.md)
     + [ブロック崩し](#ブロック崩し)
     + [オセロ](#オセロ)
     + [ステルスゲーム](#ステルスゲーム)

6. Unity雑学
   - [Sample11-Unity雑学](Sample11/sample11.md)
     + [シリアライズ](#シリアライズ)
     + [GUID](#guid)
     + [Rigidbody](#rigidbody)

7. プログラム基本
   - [Sample13-プログラム基本](Sample13/sample13.md)
     + [C#基本](#c基本)
     + [インターフース](#インターフース)
     + [デリゲート](#デリゲート)
     + [イベント](#イベント)
     + [デリゲートとイベント](#デリゲートとイベント)
     + [SOLID](#solid)
     + [Generics](#generics)
     + [デザインパターン](#デザインパターン)
       - [デザインパターン_State](#デザインパターン_state)
         * [デザインパターン_State_NonGeneric](#デザインパターン_state_nongeneric)
         * [デザインパターン_State_Generic](#デザインパターン_state_generic)
       - [デザインパターン_Command](#デザインパターン_command)

8. UnrealEngine

9. ゲーム以外
   + [GitHub](#github)
   + [Gas](#gas)
   + [Python](#python)
   + [Docker](#docker)


***

# Sample1-入力
[Sample1へ移動](Sample1/sample1.md)

### InputManager

### InputSystem

***

# Sample2-移動
[Sample2へ移動](Sample2/sample2.md)

### Move_Transform

### Move_Rigidbody

### Move_CharacterController

### Move_Sample
#### TPS
#### Warp

***

# Sample3-回転
[Sample3へ移動](Sample3/sample3.md)

### Transform

### Rigidbody

***

# Sample4-UI
[Sample4へ移動](Sample4/sample4.md)

### UI_Basic
#### UI_Basic_Sample1
#### UI_Basic_RectTransform
#### UI_Basic_Pop
#### UI_Basic_CountDown
#### UI_Basic_LookAt_HPBar

### Minimap

### UI_MVP
#### MVP_Basic
#### MVP_DependencyInjection

### TextMeshPro

***

# Sample5-サウンド
[Sample5へ移動](Sample5/sample5.md)

### AudioSource

### AudioMixer

### CRI_Ware

***

# Sample6-アニメーション
[Sample6へ移動](Sample6/sample6.md)

### AnimationControllerの利用
#### Animation_Basic
#### Animation_StateMachine
#### Animation_AvaterMask
#### Animation_Ragdoll

### DOTween

***

# Sample-いろいろ
[Sampleへ移動](Sample/sample.md)

### Cinemachine

### ScriptableObject

### Timeline

### NavMesh

### Ray
#### Jump
##### Ray_Basic
##### Ray_3Combo
#### Mouse
##### Mouse_Ray
##### Mouse_TargetLock
##### Mouse_Effect

### Shader_Basic
#### Shader1-CS
#### Shader2-HLSL_CG
#### Shader3-ShaderGraph

### Shader_Advanced
#### Shader1-Tessellation
#### Shader2-Geometry
#### Shader3-Liquid
#### Shader4-Ink
#### Shader5-DynamicMesh

### データ保存
#### データ保存_PlayerPrefs
#### データ保存_Json
#### データ保存_Playfab
#### データ保存_QuickSaveAssets
#### データ保存_AssetBundle
#### データ保存_Addressable

### Coroutine

### UniTask
#### UniTask_Async
##### UniTask_Sample1
##### UniTask_Sample2
##### UniTask_Sample3
#### UniTask_Cancel
##### UniTask_CancelSample1
##### UniTask_CancelSample2
##### UniTask_CancelSample3
#### UniTask_StateMachine_Advanced

### NetCode for GameObjects

### ML-Agents

***

# Sample9-小ネタ
[Sample9へ移動](Sample9/sample9.md)

### シャッフル

### LineDraw

### MoveFloor

### Reflection

### A*

***

# Sample10-ミニゲーム
[Sample10へ移動](Sample10/sample10.md)

### ブロック崩し

### オセロ

### ステルスゲーム

***

# Sample11-Unity雑学
[Sample11へ移動](Sample11/sample11.md)

### シリアライズ

### GUID

### Rigidbody

***

# Sample13-プログラム基本
[Sample13へ移動](Sample13/sample13.md)

### C#基本

### インターフース

### デリゲート

### イベント

### デリゲートとイベント

### SOLID

### Generics

### デザインパターン
#### デザインパターン_State
##### デザインパターン_State_NonGeneric
##### デザインパターン_State_Generic
#### デザインパターン_Command

***

# ゲーム以外

### GitHub

### Gas

### Python

### Docker
