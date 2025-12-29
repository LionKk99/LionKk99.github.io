---
layout: post
title: "A Comprehensive Survey of Self-Evolving AI Agents"
date: 2025-12-05 17:11:57 +0800
categories: ['ImgAgent', 'agent', 'A_Comprehensive_Survey_of_Self-Evolving_AI_Agents']
tags: ['ImgAgent', 'agent', 'A_Comprehensive_Survey_of_Self-Evolving_AI_Agents']
image: "/images/ImgAgent/agent/A_Comprehensive_Survey_of_Self-Evolving_AI_Agents/F1.png"
math: true
toc: true
---

![F1.png]({{ "/images/ImgAgent/agent/A_Comprehensive_Survey_of_Self-Evolving_AI_Agents/F1.png" | absolute_url }})
### Intro 
Limitation: LLM remain static after deployment.
Solution: Self-evolving AI agent (interaction data and environmental feedback), bridge the static capabilities of foundation models with the continuous adaptability.

The framework highlights four key components: 
- System inputs
- Agent System
- Environment
- Optimisers

Self-evolving techniques that target different components of the agent: 
- System foundation models
- Agent prompts
- memory
- tools
- workflows 
- communication mechanisms across agents

Specific evolution strategies developed for specialised fields:
- biomedicine
- programming
- finance

Effectiveness and Reliability:
- evaluation
- safety
- ethical considerations

**Definition:**
```
Self-evolving AI agents are autonomous systems that continuously and systematically optimise their internal components through interaction with environments, with the goal of adapting to changing tasks, contexts and resources while preserving safety and enhancing performance.
```

**Three Laws of Self-Evolving AI Agents:** 
- **I. Endure (Safety Adaptation) :** Self-evolving AI agents must maintain safety and stability during any modification;  
- **II. Excel (Performance Preservation) :** Subject to the First law, self-evolving AI agents must preserve or enhance existing task performance;  
- **III. Evolve (Autonomous Evolution) :** Subject to the First and Second law, self-evolving AI agents must be able to autonomously optimise their internal components in response to changing tasks, environments, or resources.

- MOP (Model Offline Pretraining): 离线语料训练，冻结参数
- MOA (Model Online Adaptation): 部署后通过SFT、lore和RLHF进行微调。
- MAO (Multi-Agent Orchestration): 多个LLM通过消息交换和辩论进行通信协作
- MASE (Multi-Agent Self-Evolving): 根据环境反馈和元奖励不断改进其提示、记忆、工具的策略，达到终身自演化循环

![T1.png]({{ "/images/ImgAgent/agent/A_Comprehensive_Survey_of_Self-Evolving_AI_Agents/T1.png" | absolute_url }})
人工智能代理演化和优化技术的三大方向：单代理优化、多代理优化和领域特定优化
![F2.png]({{ "/images/ImgAgent/agent/A_Comprehensive_Survey_of_Self-Evolving_AI_Agents/F2.png" | absolute_url }})
### Foundation of AI Agent Systems
