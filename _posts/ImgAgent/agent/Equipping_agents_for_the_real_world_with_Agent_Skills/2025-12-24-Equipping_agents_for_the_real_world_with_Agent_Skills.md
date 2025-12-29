---
layout: post
title: "Equipping agents for the real world with Agent Skills"
date: 2025-12-24 19:18:58 +0800
categories: ['ImgAgent', 'agent', 'Equipping_agents_for_the_real_world_with_Agent_Skills']
tags: ['ImgAgent', 'agent', 'Equipping_agents_for_the_real_world_with_Agent_Skills']
image: "/images/ImgAgent/agent/Equipping_agents_for_the_real_world_with_Agent_Skills/F.png"
math: true
toc: true
---


[Equipping agents for the real world with Agent Skills \ Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
将专业知识融入Agent
- Prompt: 试图把业务逻辑“翻译”成模型能懂的口吻。这种方式往往僵化且死板，难以灵活应对复杂场景。
- RAG: 虽然能解决知识体量问题。但需要定义 Index、处理向量化、精心切分文档……整个过程笨重。

 Anthropic 在 2025 年 10 月提出了 **Agent Skills**，本质上是一个多层级的文件系统。将领域知识通过更加结构化的文件封装，使Agent可以动态的发现和组合加载这些内容，从而将通用代理转化为专业代理。
  ![F.png]({{ "/images/ImgAgent/agent/Equipping_agents_for_the_real_world_with_Agent_Skills/F.png" | absolute_url }})
 具体而言，skill就是一个包含一个SKILL.md文件的路径，该md包含了许多指令和脚本。
 以PDF的功能为例，一份SKILL.md文件必须以YAML格式开始，包含元数据name和description。启动时，agent会将这些skill的元数据都加载到其上下文中。
 
 这些元数据（第一层）提供了足够的信息，让Agent知道何时应该使用哪些skill而无需将全部skill的详细信息（第二层）加载。
 ![F_1.png]({{ "/images/ImgAgent/agent/Equipping_agents_for_the_real_world_with_Agent_Skills/F_1.png" | absolute_url }})

倘若这个skill过于复杂，可以添加额外的md文件到与Skill.md同级的目录下，并将其用处放在skill的详细信息（第二层）中，这样可以保证Agent只在需要使用到额外的md文件时进行调用。
![F_2.png]({{ "/images/ImgAgent/agent/Equipping_agents_for_the_real_world_with_Agent_Skills/F_2.png" | absolute_url }})在所示的 PDF 技能示例中，SKILL.md 引用了两个额外的文件（reference.md 和 forms.md），技能作者选择将它们与核心 SKILL.md 文件一起捆绑在一起。通过将表单填写说明移至单独的文件（forms.md），技能作者可以保持技能核心内容的简洁，并相信 Claude 只会在填写表单时才会阅读 forms.md 文件。
![F_3.png]({{ "/images/ImgAgent/agent/Equipping_agents_for_the_real_world_with_Agent_Skills/F_3.png" | absolute_url }})
渐进式披露是使代理技能灵活且可扩展的核心设计原则。就像一本组织良好的手册，从目录开始，然后是具体章节，最后是详细的附录一样，技能允许 Claude 仅在需要时加载信息。
![F_4.png]({{ "/images/ImgAgent/agent/Equipping_agents_for_the_real_world_with_Agent_Skills/F_4.png" | absolute_url }})该图展示了当用户消息触发技能时，上下文窗口如何变化。
The sequence of operations shown:
1. To start, the context window has the core system prompt and the metadata for each of the installed skills, along with the user’s initial message;
2. Claude triggers the PDF skill by invoking a Bash tool to read the contents of `pdf/SKILL.md`;
3. Claude chooses to read the `forms.md` file bundled with the skill;
4. Finally, Claude proceeds with the user’s task now that it has loaded relevant instructions from the PDF skill.
![F_5.png]({{ "/images/ImgAgent/agent/Equipping_agents_for_the_real_world_with_Agent_Skills/F_5.png" | absolute_url }})
由于code的确定性和复用性高，我们可以直接将准备好的脚本最为skill提供给Agent。

技能编写和测试的实用指南：

1）首先进行评估：通过在典型任务上运行智能体，观察它们在哪些方面遇到困难或需要更多上下文信息，从而找出智能体能力的具体不足之处。然后逐步构建技能以弥补这些缺陷。

2）可扩展的结构：当 SKILL.md 文件变得难以管理时，将其内容拆分为单独的文件并进行引用。如果某些上下文信息互斥或很少同时使用，则保持路径分离可以减少token的使用。最后，代码既可以作为可执行工具，也可以作为文档。应该明确 Claude 是应该直接运行脚本，还是应该将其作为参考信息读取到上下文中。

3）从 Claude 的角度思考：监控 Claude 在实际场景中如何使用您的技能，并根据观察结果进行迭代：注意是否存在意外的运行轨迹或对某些上下文信息的过度依赖。特别注意技能的名称和描述。Claude 会根据这些信息来决定是否触发技能以响应其当前任务。

4）与 Claude 迭代：在与 Claude 一起完成任务时，请 Claude 将成功的方法和常见错误记录下来，并将其转化为可复用的技能代码和上下文。如果它在使用技能完成任务时偏离了方向，请它进行自我反思，找出问题所在。这个过程将帮助你发现 Claude 实际需要的上下文，而不是试图预先预测它需要什么。