---
layout: post
title: "illustrated-transformer"
date: 2025-12-22 10:00:00 +0800
categories: ['Transformer', 'illustrated-transformer']
tags: ['Transformer']
math: true
toc: true
---

[The Illustrated Transformer – Jay Alammar – Visualizing machine learning one concept at a time.](https://jalammar.github.io/illustrated-transformer/)
## A High-Level Look
在机器翻译任务中，它会输入某种语言的一个句子然后将其翻译输出为另一种语言![F1.png]({{ "/images/Transformer/illustrated-transformer/F1.png" | absolute_url }})
transformer内部是由encoding component, decoding component和connections组成![F2.png]({{ "/images/Transformer/illustrated-transformer/F2.png" | absolute_url }})
 encoding component由堆砌的encoder组成（论文中是六个），相似的decoding component也是相同数量的decoder堆砌而成
 ![F3.png]({{ "/images/Transformer/illustrated-transformer/F3.png" | absolute_url }})
 每个encoder都具有相同的结构（但它们之间不共享参数），每一个encoder具有两个sub-layers(FFNN和self-attention):
 ![F4.png]({{ "/images/Transformer/illustrated-transformer/F4.png" | absolute_url }})
 Self-attention layer可以帮助encoder在编码一个特定单词（token）的时候考虑到句中其他token
 Feed-forward neural network提供更加灵活的自由度？
 Decoder也具有这两层，但是在中间会有一个Encoder-Decoder attention layer来帮助decoder专注捕捉输入语句中相关的部分
 ![F5.png]({{ "/images/Transformer/illustrated-transformer/F5.png" | absolute_url }})
## Bringing The Tensors Into The Picture

首先我们需要对每个word/token进行embedding，编码为一个512长度的向量
 ![F6.png]({{ "/images/Transformer/illustrated-transformer/F6.png" | absolute_url }})
 编码的过程发生在encoder的最开始（底部），所有的encoder都接受一个list的vector，其中vector的长度为512，而list长度（超参数）基本上是训练数据中最长句子的token数。最下层的encoder接受的是词向量，而上层的encoder接受下层encoder的output。
 Embedding结束以后，每个flow通过encoder的两个layer。
 ![F7.png]({{ "/images/Transformer/illustrated-transformer/F7.png" | absolute_url }})
 每个位置的token在self-attention layer中是具有依赖关系的，但是在FF中没有因此可以并行计算。
## Now We’re Encoding!
![F8.png]({{ "/images/Transformer/illustrated-transformer/F8.png" | absolute_url }})
## Self-Attention at a High Level

> [!NOTE] Translate
> The animal didn't cross the street because it was too tired

对于这个我们想要进行翻译的句子，我们需要知道句中“it”指代的是谁，到底是“street”还是“animal”。我们需要让我们的算法能够学习到这样的指代关系。
当模型处理“it”这个单词的时候，self-attention会指出“it”和“animal”有关。当模型处理句中每个token的时候，self-attention会查看每个别的位置的token以寻求更好的encoding。
这与RNN中维护hidden state的想法相似，Self-attention就是 Transformer 用来将其他相关词的“理解”融入到当前正在处理的词中的一种方法。
![F9.png]({{ "/images/Transformer/illustrated-transformer/F9.png" | absolute_url }})
## Self-Attention in Detail
计算自注意力的**First step**是对每个输入向量创建三个向量（Q K V），这些向量都是通过乘以相应训练的参数矩阵得到的。新产生的 Q K V 向量的维度（64维）要比输入的词嵌入向量小（512维），这是出于多头注意力的考量
![F10.png]({{ "/images/Transformer/illustrated-transformer/F10.png" | absolute_url }})What are the “query”, “key”, and “value” vectors?
 **Second step**：计算注意力分数。例如计算“Thinking”的子注意力，需要将输入句子中的每一个词和其进行计算。其得分代表了对这个词进行编码时，应该给予输入句子其他部分多少关注度。
 注意力分数的计算方法是将该词“Thinking”的查询向量Q与其他分词的键向量V进行点乘。（the dot product of q1 and k1, the dot product of q1 and k2）
 ![F11.png]({{ "/images/Transformer/illustrated-transformer/F11.png" | absolute_url }})
 The **third and fourth steps**: 将计算好的得分除以8（Q K 向量维度64开方），这样会使得到的梯度更加稳定，然后经过一个softmax将分数归一化
 ![F12.png]({{ "/images/Transformer/illustrated-transformer/F12.png" | absolute_url }})
 The **fifth step**：将值向量V乘以相应的归一化过后的分数
 The **sixth step**：将这些加权后的值向量相加，这样就产生了self-attention layer在该位置（position 1）的输出
 ![F13.png]({{ "/images/Transformer/illustrated-transformer/F13.png" | absolute_url }})
 这样单个词向量的自注意力层计算就完成了，产生的新向量将送到FFN层进行处理。为了加快处理速度，一般是以矩阵的形式进行计算的
## Matrix Calculation of Self-Attention
 **The first step**: Calculate the Query, Key, and Value matrices. 需要先将词向量embedding打包到一个矩阵X中，然后使用矩阵乘法(WQ, WK, WV)
 ![F14.png]({{ "/images/Transformer/illustrated-transformer/F14.png" | absolute_url }})
 X中的每一行代表了一个句子中的一个单词，随后我们压缩2-6步到一个公式来计算自注意力层输出
 ![F15.png]({{ "/images/Transformer/illustrated-transformer/F15.png" | absolute_url }})
## The Beast With Many Heads
使用多头注意力（类似于CNN的多个卷积层）可以进一步改进子注意力层，并从两方面提升性能：
1）扩展了模型关注不同位置的能力，虽然一种矩阵可以捕捉到所有其他单词编码的一部分，但是在复杂的语义下可能是不足够的
2）为注意力层提供了多个”表示空间“。在论文中拥有八个注意力头（相应的八组 Q K V 矩阵），每个矩阵集合都是随机初始化的。在训练之后，每个集合都用于将输入嵌入到不同的表示子空间（类似于解题的思路不止一种，但是都会得到正确的答案，学习到不同的解题思路，了解到不同的特征是有益的）
![F16.png]({{ "/images/Transformer/illustrated-transformer/F16.png" | absolute_url }})
我们通过八组QKV矩阵进行自注意力计算后会得到八个不同的Z矩阵![F17.png]({{ "/images/Transformer/illustrated-transformer/F17.png" | absolute_url }})
我们通过将这些矩阵拼接以后再乘以一个额外的权重矩阵WO（再整合）来得到正确的形式，注意到原先的Z的维数是64，八个注意力头拼接在一起为512维，其实形状上已经符合下一层encoder的输入要求。
![F18.png]({{ "/images/Transformer/illustrated-transformer/F18.png" | absolute_url }})
最后给出一个完整过程的大图
![F19.png]({{ "/images/Transformer/illustrated-transformer/F19.png" | absolute_url }})
注意力可视化示例, it这个词对animal(其中一个head)注意力高，对tired（另一个head）注意力高
![F20.png]({{ "/images/Transformer/illustrated-transformer/F20.png" | absolute_url }})
但是如果看到每个注意力头，对于其解释会变得更加复杂
![F21.png]({{ "/images/Transformer/illustrated-transformer/F21.png" | absolute_url }})
## Representing The Order of The Sequence Using Positional Encoding
注意到现在为止，这个模型还缺少一种方法来表示输入序列中单词的顺序。为了解决这个问题，Transformer会给每个input embedding加上一个向量。这些向量遵循一个特定的模式，可以帮助模型确定每个输入的位置信息/不同词之间的距离。其直观之处在于，将这些值添加到embedding中，可以在embedding投影为 Q/K/V 向量以及进行点积注意力机制处理时，提供有意义的距离。![F22.png]({{ "/images/Transformer/illustrated-transformer/F22.png" | absolute_url }})
当嵌入向量维度为4时，真实的PE编码为
![F23.png]({{ "/images/Transformer/illustrated-transformer/F23.png" | absolute_url }})What might this pattern look like?
在下图中（Tensor2Tensor implementation of the Transformer），每一行对应一个向量的位置编码。因此，第一行是我们添加到输入序列中第一个词的嵌入向量中的向量。每一行包含 512 个值——每个值介于 1 和 -1 之间。我们用颜色编码了它们，以便于观察这种模式。
![F24.png]({{ "/images/Transformer/illustrated-transformer/F24.png" | absolute_url }})该位置编码PE的优势在于能够扩展到未见过的序列长度（例如，如果我们的训练模型被要求翻译一个比训练集中任何句子都长的句子）
![F25.png]({{ "/images/Transformer/illustrated-transformer/F25.png" | absolute_url }})
上图为Method in the paper, 其不是直接连接两个信号，而是将它们交织在一起
## The Residuals
在encoder中，每个子层（self-attention, FFN）都拥有一个残差连接，并且在后面存在一个层归一化![F26.png]({{ "/images/Transformer/illustrated-transformer/F26.png" | absolute_url }})
更详细的可视化
![F27.png]({{ "/images/Transformer/illustrated-transformer/F27.png" | absolute_url }})
在decoder中也是相似的，我们应该将Transformer看作是encoder和decoder的堆叠
![F28.png]({{ "/images/Transformer/illustrated-transformer/F28.png" | absolute_url }})
## The Decoder Side
最顶层的encoder的输出会被转换成一组注意力向量 K 和 V（理论上应该是序列长度×512的矩阵，如何转换？），每个decoder都会在其“encoder-decoder attention” layer中使用这些注意力向量，来帮助decoder关注输入序列的特定位置。
![F29.png]({{ "/images/Transformer/illustrated-transformer/F29.png" | absolute_url }})
decoder输出结果是一个自回归的过程，直到其输出一个特殊字符EOS表示输出结束。否则decoder每一步的输出都会在下一时间步被送入底层decoder作为输入，decoder会像encoder一样向上冒泡输出解码结果。与encoder输入的处理方式相同，我们也会在decoder输入中嵌入并添加位置编码，以指示每个单词的位置。
![F30.png]({{ "/images/Transformer/illustrated-transformer/F30.png" | absolute_url }})
注意，decoder中的self-attention layer只能关注到输出序列中较早的位置。这是通过在自注意力计算的 softmax 步骤之前屏蔽后续位置（将其设置为 -inf）来实现的。
The “Encoder-Decoder Attention” layer工作方式与multi-headed self-attention相似，只是其只具有Q矩阵参数，而K-V键值对矩阵则是直接从encoder中获取的。
## The Final Linear and Softmax Layer

decoder输出为一个浮点数向量，我们通过一个线性层将其转换为词表长度，随后使用softmax层来得到此表中各词的概率。选择概率最高的单元格，并将其关联的单词作为该时间步的输出。
![F31.png]({{ "/images/Transformer/illustrated-transformer/F31.png" | absolute_url }})
## Recap Of Training
使用one-hot编码表示正确答案
![F32.png]({{ "/images/Transformer/illustrated-transformer/F32.png" | absolute_url }})
使用交叉熵损失/KL散度作为损失函数进行优化
![F33.png]({{ "/images/Transformer/illustrated-transformer/F33.png" | absolute_url }})
理想的输出结果
![F34.png]({{ "/images/Transformer/illustrated-transformer/F34.png" | absolute_url }})
期望的训练结果
![F35.png]({{ "/images/Transformer/illustrated-transformer/F35.png" | absolute_url }})
除了贪婪编码，还可以采用束搜索，top-k等采样方式