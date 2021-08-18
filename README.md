# 韭菜日记之韭菜机器人

基于《韭菜日记》系列，实现币圈量化交易的韭菜机器人，体验万恶资本家的快感。

微信公众号：NextB

二维码：

![qrcode](./qrcode.jpeg)

## 项目目录结构

```
.
├── README.md
├── nextb
│   ├── __init__.py
│   ├── libs
│   │   ├── db: 交易数据存储模块
│   │   ├── platform: 交易所操作模块
│   │   ├── robot: 韭菜机器人模块
│   │   └── utils: 其他通用组件模块
│   └── main.py: 工具入口
├── requirements.txt
├── supervisor_config: supervisor配置文件
└── setup.py
```

## 交易平台

|交易平台名称|是否支持|备注|
|----|----|----|
|币安|✔||
|火币|✖||
|Okex|✖||