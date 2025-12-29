---
layout: post
title: "The Illustrated Stable Diffusion"
date: 2025-12-25 20:55:17 +0800
categories: ['Transformer', 'The_Illustrated_Stable_Diffusion']
tags: ['Transformer']
image: "/images/Transformer/The_Illustrated_Stable_Diffusion/F.png"
math: true
toc: true
---

![F.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F.png" | absolute_url }})
[The Illustrated Stable Diffusion](https://jalammar.github.io/illustrated-stable-diffusion/)
Stable Diffusion一般存在两种用法：
1）text2img
2）img edit
### The Components of Stable Diffusion

![F_1.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_1.png" | absolute_url }})

首先，我们需要一个Text Encoder将文本信息编码成向量（实际上就是the text encoder of a CLIP），其输出的是一个向量列表，该列表中每个token被表示为高维的向量。

而图像生成是一个两阶段的过程：
#### Image information creator
图像信息生成器（**Image information creator**）完全在图像信息空间（或潜在空间）中工作，这一特性使其比以往在像素空间中工作的扩散模型速度更快？why？
从技术角度来说，该组件由一个 UNet 神经网络和一个调度算法组成。它是对信息进行逐步处理的过程，最终由下一个组件（图像解码器）生成高质量图像。
![F_2.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_2.png" | absolute_url }})其需要多步（50-100步）来生成图片的信息。
#### **Image Decoder**
其作用是将图像的潜在信息转化成最终的pixel image，只在最后运行一次
![F_3.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_3.png" | absolute_url }})
#### Conclusion

Stable Diffusion具有三个组件:

- **ClipText** for text encoding.  
    Input: text.  
    Output: 77 token embeddings vectors, each in 768 dimensions.
    
- **UNet + Scheduler** to gradually process/diffuse information in the information (latent) space.  
    Input: text embeddings and a starting multi-dimensional array (structured lists of numbers, also called a _tensor_) made up of noise.  
    Output: A processed information array
    
- **Autoencoder Decoder** that paints the final image using the processed information array.  
    Input: The processed information array (dimensions: (4,64,64))  
    Output: The resulting image (dimensions: (3, 512, 512) which are (red/green/blue, width, height))
### What is Diffusion Anyway?
扩散过程发生在粉色的“图像信息生成器”组件内部。该组件拥有代表**输入文本的词嵌入**和一个**随机的初始图像信息数组**（也称为潜在信息latents），扩散过程会生成一个信息数组，图像解码器使用该信息数组来绘制最终图像。
![F_4.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_4.png" | absolute_url }})这个过程是逐步进行的。每一步都会添加更多相关信息。为了直观地理解这个过程，我们可以检查随机潜在变量数组，并发现它最终会转化为视觉噪声。这里的视觉检查指的是将图像通过图像解码器进行解码。
![F_5.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_5.png" | absolute_url }})Diffusion的每一次过程，都不断地更新latents array，这个array里面包含的信息在每一步中会更接近**输入文本**以及**模型在训练图片中提取的视觉信息**。
![F_6.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_6.png" | absolute_url }})
我们可以看到这些latents是如何随difussion step变化的
![F_7.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_7.png" | absolute_url }})在这种情况下，步骤 2 和步骤 4 之间发生了一些特别有趣的事情，就好像轮廓从嘈杂中涌现出来一样。
### How diffusion works

利用扩散模型生成图像的核心思想在于我们拥有强大的计算机视觉模型。给定足够大的数据集，这些模型可以学习复杂的运算。

扩散模型通过将问题表述如下来处理图像生成：

1）前向加噪
![F_8.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_8.png" | absolute_url }})
我们可以以此创造大量的训练数据
![F_9.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_9.png" | absolute_url }})这个例子展示了从图像（数量 0，无噪声）到完全噪声（数量 4，完全噪声）的几个噪声量值，我们可以轻松控制向图像添加多少噪声。因此我们可以将其分散到几十个步骤中，为训练数据集中的所有图像创建几十个训练样本。
![F_10.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_10.png" | absolute_url }})
利用这个数据集，我们可以训练噪声预测器，最终得到一个优秀的噪声预测器，它在特定配置下运行时能够生成图像。
![F_11.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_11.png" | absolute_url }})该训练过程与其他ML无异。
### Painting images by removing noise
训练好的噪声预测器可以接收一幅带噪声的图像，并根据去噪步骤的大小，预测出一个噪声切片。
![F_12.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_12.png" | absolute_url }})
预测采样噪声，以便从图像中减去它，我们就能得到一幅更接近模型训练所用图像的图像（不是确切的图像本身，而是分布——像素排列的世界，其中天空通常是蓝色的，在地面之上，人有两只眼睛，猫看起来是某种样子——尖耳朵，不为所动）
![F_13.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_13.png" | absolute_url }})
如果训练数据集包含美观的图像（例如，稳定扩散模型所用的 LAION Aesthetics 数据集），那么生成的图像也往往会很美观。如果我们用 logo 图像来训练模型，最终得到的就是一个生成 logo 的模型。
![F_14.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_14.png" | absolute_url }})
需要注意的是，我们目前描述的扩散过程是在不使用任何文本数据的情况下生成图像的。因此，如果我们部署此模型，它会生成非常漂亮的图像，但我们无法控制生成的图像是金字塔、猫还是其他任何物体。
### Speed Boost: Diffusion on Compressed (Latent) Data Instead of the Pixel Image
为了加快图像生成速度，diffusion未直接在pixel images做预测，而在图像的压缩版本上进行处理，这一过程称为“Departure to Latent Space”。
这种压缩（以及后续的解压缩/绘制）是通过自编码器完成的。自编码器使用其编码器将图像压缩到潜在空间，然后仅使用解码器利用压缩后的信息重建图像。
![F_15.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_15.png" | absolute_url }})
现在，前向扩散过程是在压缩后的潜在变量上进行的。噪声切片是应用于这些潜在变量的噪声，而不是应用于像素图像的噪声。因此，噪声预测器实际上是训练来预测压缩表示（潜在空间）中的噪声。
![F_16.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_16.png" | absolute_url }})
前向过程（使用自编码器的编码器）用于生成数据，以便训练噪声预测器。训练完成后，我们可以通过运行反向过程（使用自编码器的解码器）来生成图像。、
![F_17.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_17.png" | absolute_url }})
Figure 3 of the LDM/Stable Diffusion paper:
![F_18.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_18.png" | absolute_url }})
这张图还展示了“条件”组件，在本例中指的是描述模型应该生成什么图像的文本提示。
### The Text Encoder: A Transformer Language Model
Transformer 语言模型被用作语言理解组件，它接收文本提示并生成词元嵌入。已发布的稳定扩散模型使用了 ClipText（一种基于 GPT 的模型），而论文中使用的是 BERT。
Imagen 论文表明，语言模型的选择至关重要。与更大的图像生成组件相比，使用更大的语言模型对生成图像质量的影响更大。
![F_19.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_19.png" | absolute_url }})
早期的SD模型直接使用了 OpenAI 发布的预训练 ClipText 模型。未来的模型可能会切换到新发布的、规模更大的 OpenCLIP 版本 CLIP（2022 年 11 月更新：确实如此，SD V2 使用了 OpenCLIP）。这批新模型包含参数量高达 3.54 亿的文本模型，而 ClipText 的参数量仅为 6300 万。
#### How CLIP is trained?
![F_20.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_20.png" | absolute_url }})
通过在潜在空间对齐caption和img。
![F_21.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_21.png" | absolute_url }})
### Feeding Text Information Into The Image Generation Process
为了引入text引导，我们需要在noise predictor中将text作为input
![F_22.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_22.png" | absolute_url }})
我们的数据集现在包含了编码后的文本。由于我们是在潜在空间中进行操作，因此输入图像和预测噪声都位于潜在空间中
![F_23.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_23.png" | absolute_url }})
### Layers of the Unet Noise predictor (without text)
我们首先来看一个不使用文本的扩散型 Unet。它的输入和输出如下所示：
![F_24.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_24.png" | absolute_url }})
Inside, we see that:
- Unet 由一系列层组成，这些层负责转换潜在变量数组。
- 每一层都处理前一层的输出。
- 部分输出（通过残差连接）被送入网络后续的处理层。
- 时间步被转换为时间步嵌入向量，并在各层中使用。
![F_25.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_25.png" | absolute_url }})
### Layers of the Unet Noise predictor WITH text
![F_26.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_26.png" | absolute_url }})
为了支持文本输入（technical term: text conditioning），我们需要对系统进行的主要更改是在 ResNet 块之间添加一个注意力层。
![F_27.png]({{ "/images/Transformer/The_Illustrated_Stable_Diffusion/F_27.png" | absolute_url }})
请注意，ResNet 模块并不直接处理文本。但注意力层会将这些文本表征合并到潜在变量中。然后，下一个 ResNet 模块就可以利用这些合并后的文本信息进行处理。