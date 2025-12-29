---
layout: post
title: "SELF-CONSISTENCY"
date: 2025-12-02 20:26:26 +0800
categories: ['ImgAgent', 'reasoning', 'SELF-CONSISTENCY']
tags: ['ImgAgent', 'reasoning']
image: "/images/ImgAgent/reasoning/SELF-CONSISTENCY/F1.png"
math: true
toc: true
---

![F1.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/F1.png" | absolute_url }})
### Related Work

- [[Chain-of-Thought]]
### Intro
本文提出 ***self-consistency*** 这一新的解码策略，其核心为利用“multiple different ways of thinking leading to its unique correct answer.”

### Exp
![T1.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/T1.png" | absolute_url }})
对比实验指明，直接采用多数投票法效果最佳，采用正则化序列概率（即消除序列长度对概率的影响）后sum的效果也很接近。
实验时对不同模型设置了不同温度T和截断token（Top-K）。
&nbsp;
![F2.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/F2.png" | absolute_url }})
采样路径数量对正确率的影响在10次时为拐点。
![T4.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/T4.png" | absolute_url }})
sample示例如上图所示
![T6.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/T6.png" | absolute_url }})
文章还对比了束搜索、自洽解码以及使用束搜索的自洽解码。结果显示使用束搜索的自洽解码由于多样性降低不如自洽解码。
![T7.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/T7.png" | absolute_url }})
文章还对比了少样本提示和自洽解码的效果。
![F4.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/F4.png" | absolute_url }})
文章指明该策略对于不同温度、Top-k参数具有鲁棒性，且该方法对不同规模的模型均有提升。![T8F5.png]({{ "/images/ImgAgent/reasoning/SELF-CONSISTENCY/T8F5.png" | absolute_url }})
不完美的提示词会使CoT的准确率下降，但是在不完美的提示词下的Self-consistency仍有效。且文章指出，LLM的自洽性（即输出结果的一致性）同其准确性ACC成正相关，即越准确的模型结果的一致性越高。
### CONCLUSION AND DISCUSSION
局限性：引入额外成本
未来：利用自洽性生成更好的监督数据用于微调模型
