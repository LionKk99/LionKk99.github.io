---
layout: post
title: "Chain-of-Thought"
date: 2025-12-22 10:00:00 +0800
categories: ['ImgAgent', 'reasoning', 'Chain-of-Thought']
tags: ['ImgAgent', 'reasoning']
math: true
toc: true
---

![F1.png]({{ "/images/ImgAgent/reasoning/Chain-of-Thought/F1.png" | absolute_url }})
### Intro
LLM推理能力不足，现有的解决方法：
- 推理数据微调（数据消耗/算力消耗大）
- Few-shot prompt（推理表现不佳/推理能力不随LLM能力提升）
&nbsp;
**Solution：**
Given a prompt that consists of triples: 〈input, *chain of thought*, output〉.
A *“chain of thought”* is a series of intermediate natural language reasoning steps that lead to the final output, and we refer to this approach as chain-of-thought prompting.

We will show that sufficiently large language models can generate chains of thought if demonstrations of chain-of-thought reasoning are provided in the exemplars for few-shot prompting.
### Method
![F3.png]({{ "/images/ImgAgent/reasoning/Chain-of-Thought/F3.png" | absolute_url }})
&nbsp;
### Result
![F4.png]({{ "/images/ImgAgent/reasoning/Chain-of-Thought/F4.png" | absolute_url }})
### Ablation Study
![F5.png]({{ "/images/ImgAgent/reasoning/Chain-of-Thought/F5.png" | absolute_url }})
#### 仅方程 (Equation Only)

- **⚡️ 区别：** **移除了中间的自然语言推理步骤。** 模型被要求直接输出**数学方程**，然后是答案。
    
    - **标准 CoT 示例：** “小明买了 5 个苹果，每个 2 元。他还买了 3 个梨，每个 3 元。总共花了多少钱？”
        
        - **CoT：** 苹果花了 $5 \times 2 = 10$ 元。梨花了 $3 \times 3 = 9$ 元。总共 $10 + 9 = 19$ 元。
            
        - **答案：** 19
            
    - **仅方程示例：**
        
        - **方程：** $5 \times 2 + 3 \times 3$
            
        - **答案：** 19
            
- **💡 实验发现：** 在像 **GSM8K** 这样复杂的应用题数据集上，**效果提升不大**。
    
- **📚 结论：** 这表明对于复杂的应用题，**直接将问题语义转换为方程是困难的**，自然语言的推理步骤（如“苹果花了...”“梨花了...”）在理解和规划方程方面是**不可或缺**的。
    

#### 2. 仅可变计算 (Variable Compute Only)

- **⚡️ 区别：** **移除了所有的推理内容**（无论是自然语言还是方程），仅保留了**计算量（即中间输出的标记数）**。模型被要求输出与解题所需方程字符数等量的**点（...）**序列，然后是答案。
    
    - **标准 CoT 示例：** (同上，包含推理步骤)
        
    - **仅可变计算示例：**
        
        - **中间输出：** `................` (点的数量大致等于 $5 \times 2 + 3 \times 3$ 的字符数)
            
        - **答案：** 19
            
- **💡 实验发现：** 性能**与基线（没有 CoT）差不多**。
    
- **📚 结论：** 这证明了 CoT 的成功**并非仅仅是因为增加了计算量或输出的标记数**；真正重要的是**将中间步骤表达为自然语言的语义内容**。
    

#### 3. 答案后的思维链 (Chain of Thought After Answer)

- **⚡️ 区别：** **改变了推理步骤的顺序。** 模型被要求先给出**最终答案**，然后才输出**思维链（推理步骤）**。
    
    - **标准 CoT 示例：** **推理** $\to$ **答案**
        
    - **答案后的 CoT 示例：**
        
        - **答案：** 19
            
        - **CoT：** 苹果花了 $5 \times 2 = 10$ 元。梨花了 $3 \times 3 = 9$ 元。总共 $10 + 9 = 19$ 元。
            
- **💡 实验发现：** 性能也**与基线（没有 CoT）差不多**。
    
- **📚 结论：** 这表明 CoT 的价值在于它提供了一个**顺序的推理过程**，模型需要**依赖这个过程**来得出正确的最终答案。如果先给出答案再补充推理，那么这个推理过程就**无法影响**答案的生成，说明 CoT 的成功不仅仅是“激活”了预训练知识，而是在于其**顺序的、指导性的推理作用**。

### Conclusions
We find that chain-of-thought reasoning is an ***emergent property*** of model scale that allows sufficiently large language models to perform reasoning tasks that otherwise have flat scaling curves.