---
layout: post
title: "Tree of Thoughts"
date: 2025-12-22 10:00:00 +0800
categories: ['ImgAgent', 'reasoning', 'Tree_of_Thoughts']
tags: ['ImgAgent', 'reasoning', 'Tree_of_Thoughts']
image: "/images/ImgAgent/reasoning/Tree_of_Thoughts/F1.png"
math: true
toc: true
---

![F1.png]({{ "/images/ImgAgent/reasoning/Tree_of_Thoughts/F1.png" | absolute_url }})
### Related Work
- [[Chain-of-Thought]]
- [[SELF-CONSISTENCY]]
- [[SELF-REFINE]]
### Intro
- ToT支持对问题解决中间步骤进行探索
- 引入“双过程”决策理论，(Ⅰ) A fast, automatic, unconscious mode （Ⅱ）A slow, deliberate, conscious mode。并提出LLM的token-level choices是接近于“System 1”，所以想尝试ToT所代表的更深思熟虑的规划过程来增强推理。
- 规划过程具有两个特性：(Ⅰ）可以维护并探索多种方案，而不是单独的一种（Ⅱ）具有评估状态的能力（通过对未来的预测），采取积极的回溯来做出更优的全局决策
### Tree of Thoughts: Deliberate Problem Solving with LM
```
A genuine problem-solving process involves the repeated use of available information to initiate exploration, which discloses, in turn, more information until a way to attain the solution is finally discovered.
																—— Newell et al.
```
现有的LLM推理存在两个问题：
- 没有探索思维过程中不同（树结构的）分支的延续（一条路走到底）
- 没有采取规划、前瞻或回溯来评估这些不同的选项（分支），但这种启发式引导的搜索是人类问题解决的特征

ToT引入四个问题：
- 如何分解出中间过程?
Solution: 对于不同的问题采用不同方法。如24点，保留一行equation表示当前产生的数字。足够小（保证未来发展的的多样性），足够大（足以进行状态评估）。
- 如何在每个状态（state）生成潜在想法?
Solution: 存在两种
（a）独立同分布 (i.i.d.) 采样
$k$ 个候选思考 $z^{(j)}$ 是独立地从模型中采样出来的。这样思考空间 “丰富”（rich），即下一步的思考有很多可能性，且彼此之间差异较大。（创意写作）
![F4.png]({{ "/images/ImgAgent/reasoning/Tree_of_Thoughts/F4.png" | absolute_url }})
（b)  顺序提议 (Sequential Proposing)
模型被提示一次性输出一个包含 $k$ 个候选思考的列表或序列 $[\mathbf{z}^{(1)}, \cdots, \mathbf{z}^{(k)}]$。思考空间 “受限”（constrained），即下一步的思考选项较少、较具体，这样有助于避免重复。（24点）
![F2.png]({{ "/images/ImgAgent/reasoning/Tree_of_Thoughts/F2.png" | absolute_url }})
- 如何启发式评估状态?
Solution: 使用LM来主动推理状态，两种方式:
（a）Value
根据状态 s 生成标量值 v（例如 1-10）或分类（例如确定/可能/不可能），无需完美，只要有帮助就行。
（b）Vote
问题难以评估时，直接投票（类似于self-consist），选得票多的。
- 使用什么搜索算法?
（a）BFS 
维护每一步中最有希望的b个状态
（b）DFS
首先探索最有希望的状态，直到达到最终输出

```
Conceptually, ToT has several benefits as a method for general problem-solving with LMs: 
(1) Generality. IO, CoT, CoT-SC, and self-refinement can be seen as special cases of ToT (i.e. trees of limited depth and breadth; Figure 1). 
(2) Modularity. The base LM, as well as the thought decomposition, generation, evaluation, and search procedures can all be varied independently.
(3) Adaptability. Different problem properties, LM capabilities, and resource constraints can be accommodated. 
(4) Convenience. No extra training is needed, just a pre-trained LM is sufficient.
```

