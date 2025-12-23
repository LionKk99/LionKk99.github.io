---
layout: post
title: "Toolformer"
date: 2025-12-22 10:00:00 +0800
categories: ['ImgAgent', 'agent', 'Toolformer']
tags: ['ImgAgent', 'agent', 'Toolformer']
image: "/images/ImgAgent/agent/Toolformer/F1.png"
math: true
toc: true
---

![F1.png]({{ "/images/ImgAgent/agent/Toolformer/F1.png" | absolute_url }})
### Intro
LLM在算数运算、事实查找方面表现不佳，但是这恰恰是一些简单模型所擅长的。文章着眼于通过简单的API自学习外部工具来兼顾两者优势。这是通过自监督的方式去完成的，每个API只需要少数示例。
### Method

![F2.png]({{ "/images/ImgAgent/agent/Toolformer/F2.png" | absolute_url }})

文章将绝大部分的篇幅放在了数据集的构建上：

假设在位置 $x_i$ 之后考虑插入 API 调用 $c$，并观察其后 $L$ 个 Token 的序列 $x_{i+1 \cdots i+L}$。
- 原始序列的条件对数概率和（基线）:

$$\mathcal{L}_{\text{orig}} = \sum_{j=1}^{L} \log P(x_{i+j} | x_{1 \cdots i}, x_{i+1 \cdots i+j-1})$$

-  增强序列的条件对数概率和（包含 API 调用 $c$）:

$$\mathcal{L}_{c} = \sum_{j=1}^{L} \log P(x_{i+j} | x_{1 \cdots i}, c, x_{i+1 \cdots i+j-1})$$

只有当 API 调用 $c$ 带来的对数概率增益（即损失降低）超过预设阈值 $\lambda$ 时，才会被保留并添加到训练数据中：

$$
\mathcal{L}_{c} - \mathcal{L}_{\text{orig}} > \lambda
$$
![T10.png]({{ "/images/ImgAgent/agent/Toolformer/T10.png" | absolute_url }})
### EXP
![F4.png]({{ "/images/ImgAgent/agent/Toolformer/F4.png" | absolute_url }})

