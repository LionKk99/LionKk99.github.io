---
layout: post
title: "Deep Agents"
date: 2025-12-24 19:21:50 +0800
categories: ['ImgAgent', 'agent', 'Deep_Agents']
tags: ['ImgAgent', 'agent', 'Deep_Agents']
image: "/images/ImgAgent/agent/Deep_Agents/F_1.png"
math: true
toc: true
---

[Deep Agents](https://blog.langchain.com/deep-agents/)
![F_1.png]({{ "/images/ImgAgent/agent/Deep_Agents/F_1.png" | absolute_url }})
如何实现 Long-Running 长时间的运行而不崩溃?

![F.png]({{ "/images/ImgAgent/agent/Deep_Agents/F.png" | absolute_url }})
现在简单的浅层循环智能体无法进行长远的规划，难以胜任多步骤、深度思考的复杂任务。
为了打破这一现象，提出了Deep Agent，能够深入探索。它们通常能够规划更复杂的任务，并在更长的时间范围内执行这些目标。

是什么让这些智能体擅长深入研究呢？

其核心算法实际上是相同的——都是一个循环运行并调用各种工具的逻辑学习模型（LLM）。与易于构建的简单智能体相比，区别在于：
- A detailed system prompt
- Planning tool
- Sub agents
- File system ![F_1.png]({{ "/images/ImgAgent/agent/Deep_Agents/F_1.png" | absolute_url }})
1）提示工作
Deep Agents 的卓越表现离不开一个精心设计的、内容详尽的系统提示。它们包含如何使用工具的详细说明，以及在特定情况下如何行动的示例（少量提示）
2）规划工具
使用“Todo List”工具来让 Agent 自行创建和维护一个任务清单，来帮助它保持对整体目标的专注和任务的有序性
3）子Agent
用于拆分任务以及更好的上下文管理，避免主agent上下文中无用信息过多。
![F_2.png]({{ "/images/ImgAgent/agent/Deep_Agents/F_2.png" | absolute_url }})4）文件系统
Deep Agents 通常需要长时间运行，在此过程中会积累大量需要管理的上下文。
- **长期记忆**：Agent 可以将中间思考、发现和笔记记录到文件中，以便后续随时读取。这解决了 LLM 有限上下文窗口的问题。
- **共享工作区**：所有 Agent（包括主 Agent 和所有子 Agent）都可以访问这个共享空间，实现高效协作。例如，研究子 Agent 可以将发现写入报告，编码子 Agent 则可以读取该报告来指导其工作。