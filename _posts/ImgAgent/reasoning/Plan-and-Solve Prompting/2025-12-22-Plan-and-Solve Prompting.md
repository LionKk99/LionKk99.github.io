---
layout: post
title: "Plan-and-Solve Prompting"
date: 2025-12-22 10:00:00 +0800
categories: ['ImgAgent', 'reasoning', 'Plan-and-Solve Prompting']
tags: ['ImgAgent', 'reasoning']
math: true
toc: true
---

### Related Work
- [[Chain-of-Thought]]
### Intro

- Chain of Thought （CoT）的继承
- 在 Zero-shot-CoT 场景下，采用 ”Let’s first understand the problem and devise a plan to solve the problem. Then, let’s carry out the plan and solve the problem step by step“ 替换 ”Let's think step by step“. (PS prompting)
- Add more detailed instructions to PS prompting. Extend it with “extract relevant variables and their corresponding numerals” and “calculate intermediate results (pay attention to calculation and commonsense)” instructions. (PS+ prompting strategy)
![F2.png]({{ "/images/ImgAgent/reasoning/Plan-and-Solve Prompting/F2.png" | absolute_url }})

### Method
#### Step 1: Prompting for Reasoning Generation
- The templates should elicit LLMs to deter mine subtasks and accomplish the subtasks.
- The templates should guide LLMs to pay more attention to calculations and intermediate results and to ensure that they are correctly performed as much as possible.
```
Q: \<question\>. 
A: Let’s first understand the problem and devise a plan to solve the problem. Then, let’s carry out the plan and solve the problem step by step. 
```
自己提出进行复杂推理的三个问题：
- Calculation errors -> “pay attention to calculation”
- Missing Step errors -> “extract relevant variables and their corresponding numerals”
- Semantic misunderstanding -> “calculate intermediate results”
#### Step 2: Prompting for Answer Extraction
```
“Q: Grace weighs 125 pounds · · · Variables: Grace: 125 pounds · · · Answer: Combined weight of Grace and Alex = 125 + 498 = 623 pounds. Therefore, the answer (arabic numerals) is”
```
For this example, the final answer returned by LLM is “623”.
![F3.png]({{ "/images/ImgAgent/reasoning/Plan-and-Solve Prompting/F3.png" | absolute_url }})
### Experimental Results
![T2.png]({{ "/images/ImgAgent/reasoning/Plan-and-Solve Prompting/T2.png" | absolute_url }})
&nbsp;
![T5.png]({{ "/images/ImgAgent/reasoning/Plan-and-Solve Prompting/T5.png" | absolute_url }})