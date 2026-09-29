# 王阳明行动陪伴智能体

## 项目简介
智能体应当：
多帮助用户澄清，少替用户判断；
将认识转化成行动；
根据行动结果复盘；
尊重外部事实；
不把能力、疾病或环境问题简单说成“私欲”；
不让用户越来越依赖智能体。

用户描述“想得多、做得少”的困境
→ 智能体帮助澄清真实目标
→ 必要时检索王阳明原典
→ 生成24小时内可执行的小行动
→ 保存行动
→ 用户反馈完成情况
→ 智能体根据事实帮助复盘
→ 一周后生成知行差距报告


## 环境要求
- Python 3.11
- Anaconda / Miniconda 环境配置
- github账号
- pytorch环境配置
- git使用与配置

## 安装
1. 创建环境：conda create -n wangyangming python=3.11
2. 激活：conda activate wangyangming
3. 装依赖：pip install -r requirements.txt

## 配置
复制 .env.example 为 .env，填入 DEEPSEEK_API_KEY。

## 运行
streamlit run app.py
