# MLAgents
- はじめに
  - [はじめに(神戸電子_宮本先生による導入動画)](https://drive.google.com/file/d/1YiVMleM__0kqXRKBs5UO9bq2N7a0mhYO/view?usp=drive_link)

- 概要
  - [Python機械学習(教師ありデータを中心に)](https://drive.google.com/drive/folders/1Pwr0G_I46uJpsPWQFGAk6pymbJDx_hR_)
  - [ニューラルネットワークと強化学習(概要)](3_7_NN_RL.md)

- 授業スライドや資料  
  -  <a href="https://drive.google.com/drive/folders/1Qxd4PeikBb7pztRt8RDlirOxi1tCofYk" target="_blank">環境設定等(MLAgentsをとりあえず動かしてみよう(スライド))</a>

  - [ML-Agents 詳細解説(サンプル付き)](Textbook/0.md)

  - [全体のまとめ(必須項目のみ)](3_ALL.md)
     + [YAML_Settings](3_YAML_Settings.md)




<br>

<br>

## よく使うコマンド

```
conda info -e

activate mlagents110

cd C:\ML_Agents_Lesson\ml-agents

mlagents-learn .\config\ppo\Crawler.yaml --run-id=crawler-test --force

mlagents-learn .\config\ppo\Crawler.yaml --run-id=crawler-test --resume


tensorboard --logdir=./results
```



<br>

<br>


## おまけ

<a href="https://netron.app/" target="_blank">onnxファイルの中身を確認できるサイト</a>

<a href="https://developer.mamezou-tech.com/blogs/2023/02/06/ml-model-visualizer-netron/" target="_blank">紹介サイト</a>


TeachableMachine

MNIST

サンプルプロジェクト参照

2_Other > 20_Onnx_MachineLearning
(2025年度版)

