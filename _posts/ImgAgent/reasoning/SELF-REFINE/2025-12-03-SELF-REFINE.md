---
layout: post
title: "SELF-REFINE"
date: 2025-12-03 13:20:27 +0800
categories: ['ImgAgent', 'reasoning', 'SELF-REFINE']
tags: ['ImgAgent', 'reasoning', 'SELF-REFINE']
image: "/images/ImgAgent/reasoning/SELF-REFINE/F1.png"
math: true
toc: true
---

![F1.png]({{ "/images/ImgAgent/reasoning/SELF-REFINE/F1.png" | absolute_url }})
### Relative work
- [[Chain-of-Thought]]
### Intro
The main idea is to generate an initial output using an LLM; then, the same LLM provides feedback for its output and uses it to refine itself, iteratively.
![F2.png]({{ "/images/ImgAgent/reasoning/SELF-REFINE/F2.png" | absolute_url }})
### Algorithm 
需要构建三个prompts（生成、反馈、改进）
![F3.png]({{ "/images/ImgAgent/reasoning/SELF-REFINE/F3.png" | absolute_url }})
### Result
![T1.png]({{ "/images/ImgAgent/reasoning/SELF-REFINE/T1.png" | absolute_url }})
