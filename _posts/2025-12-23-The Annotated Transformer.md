---
layout: post
title: "The Annotated Transformer"
date: 2025-12-23 10:00:00 +0800
categories: ['Transformer', 'The Annotated Transformer']
tags: ['Transformer', 'The Annotated Transformer']
math: true
toc: true
---

Link：[The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/#embeddings-and-softmax)
## Background

减少顺序计算的目标也是扩展神经GPU、ByteNet和ConvS2S的基础，它们都以卷积神经网络为基本构建模块，并行计算所有输入和输出位置的隐藏表示。在这些模型中，关联两个任意输入或输出位置的信号所需的运算次数会随着位置间距离的增加而增长，ConvS2S呈线性增长，By​​teNet呈对数增长。这使得学习远距离位置之间的依赖关系变得更加困难。在Transformer中，运算次数减少到恒定值，但代价是由于对注意力加权位置进行平均而降低了有效分辨率，我们通过多头注意力机制来抵消这种影响。

自注意力机制（有时也称为序列内注意力机制）是一种将单个序列的不同位置关联起来以计算序列表示的注意力机制。自注意力机制已成功应用于多种任务，包括阅读理解、抽象式文本摘要、文本蕴含以及学习与任务无关的句子表示。端到端记忆网络基于循环注意力机制而非序列对齐循环，并且已证明在简单语言问答和语言建模任务中表现良好。

Transformer 是第一个完全依靠自注意力机制来计算其输入和输出表示，而无需使用序列对齐的 RNN 或卷积的转换模型。
![F.png]({{ "/images/Transformer/The Annotated Transformer/F.png" | absolute_url }})
## Structure

我们按照自顶向下的方式来对Transformer这个结构进行刨析：
```python
def make_model(

    src_vocab, tgt_vocab, N=6, d_model=512, d_ff=2048, h=8, dropout=0.1
    
):

    c = copy.deepcopy

    attn = MultiHeadAttention(h, d_model)

    ff = PositionwiseFeedForward(d_model, d_ff, dropout)

    position = PositionalEncoding(d_model, dropout)

    model = EncoderDecoder(

        Encoder(EncoderLayer(d_model, c(attn), c(ff), dropout), N),

        Decoder(DecoderLayer(d_model, c(attn), c(attn), c(ff), dropout), N)

        nn.Sequential(Embeddings(d_model, src_vocab), c(position)),

        nn.Sequential(Embeddings(d_model, tgt_vocab), c(position)),

        Generator(d_model, tgt_vocab),

    )

    # This was important from their code.

    # Initialize parameters with Glorot / fan_avg.

    # Xavier/Glorot 均匀初始化

    for p in model.parameters():

        if p.dim() > 1: #过滤掉一维的参数（通常是偏置 bias）

            nn.init.xavier_uniform_(p)

    return model

```

模型最顶层的类名为EncoderDecoder，其函数初始化需要传入：
`def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):`
- encoder
- decoder
- src_embed (源语言嵌入)
- tgt_embed (目标语言嵌入)
- generator （将512的logit映射到vocab词表，接softmax归一化概率）
```python
class EncoderDecoder(nn.Module):

    """

    A standard Encoder-Decoder architecture. Base for this and many

    other models.

    """

  

    def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):

        super(EncoderDecoder, self).__init__()

        self.encoder = encoder

        self.decoder = decoder

        self.src_embed = src_embed

        self.tgt_embed = tgt_embed

        self.generator = generator

  

    def forward(self, src, tgt, src_mask, tgt_mask):

        "Take in and process masked src and target sequences."

        return self.decode(self.encode(src, src_mask), src_mask, tgt, tgt_mask)

  

    def encode(self, src, src_mask):

        return self.encoder(self.src_embed(src), src_mask)

  

    def decode(self, memory, src_mask, tgt, tgt_mask):

        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)
```
首先要搞清楚训练时的输入张量形状：（batch, lenth, d_model）
- batch：训练的批量大小（句子数量）
- lenth： 训练batch中的最长句子的token长度，将较短句子填充特殊字符来补齐，同时添加掩码来屏蔽这一部分的特殊字符（工程上会先将句子按照长度排序，这样训练时batch中补齐的token较少）
- d_model： 选择的词嵌入维度，一般为512

### Generator
![F 1.png]({{ "/images/Transformer/The Annotated Transformer/F 1.png" | absolute_url }})
模型最顶部的部分，也最好理解，只是一个常规的分类输出头：
```python
class Generator(nn.Module):

    def _init_(self, d_model, vocab_size):

        super(Generator, self).__init__()

        self.proj = nn.Linear(d_model, vocab_size)

    def forward(self, x):

        return log_softmax(self.proj(x), dim=-1)
```
注意下文中提及，该位置的Pre-softmax Linear Transformation是与Encoder Input Embedding和Decoder Input Embedding参数复用的。
### Embeddings and Softmax
注意到在实现时，使用了参数复用（Weight Sharing）策略，有三个地方的权重矩阵 $W$ 是完全一样的（即指向内存中的同一块地址）。
- Encoder Input Embedding：把输入的单词 ID 变成 512 维向量。    
- Decoder Input Embedding：把已经生成的单词 ID 变成 512 维向量。    
- Pre-softmax Linear Transformation：在模型最后，把 Decoder 输出的 512 维向量映射回词表大小（例如 30000 维），用来预测下一个词。
这样共享参数的设计具有语义一致性（Embedding 的作用是“单词 $\to$ 向量”，输出线性层的作用是“向量 $\to$ 单词”。这两者本质上是互逆的）、减少模型大小和正则化的作用。

需要注意在embedding的时候需要乘以$\sqrt{d_{model}}$ ，这是因为在输出层（Linear + Softmax），我们希望权重较小，以保持概率分布的平稳；而在输入端，我们由于需要增加位置编码PE，希望将Embedding适当放大，使其在与位置信息PE融合时依然占据主导地位。

假设词表大小 $V = 30000$，模型维度 $d_{model} = 512$。 我们定义一个共享权重矩阵 **$W$**，它的形状是 $(30000, 512)$。
- 在Embedding 层我们只需要查表，在对应行将向量直接取出。
- 在Pre-softmax Linear 层我们需要矩阵乘法$\text{Scores} = h \times W^T$ （输出向量 $h$ 分别与 $W$ 中的每一行（即每个单词的词向量）做点积。点积结果越大，说明 $h$ 与该单词越相似，模型预测该单词的概率就越高。）
### Positional Encoding
除了上述的token的embedding以外，由于transformer是属于token并行处理（只计算其与其他位置token的注意力分数），还需要PE来进行位置表示才能理解语序（你爱我/我爱你）
![F 4.png]({{ "/images/Transformer/The Annotated Transformer/F 4.png" | absolute_url }})
![F 2.png]({{ "/images/Transformer/The Annotated Transformer/F 2.png" | absolute_url }})
使用不同频率的sin和cos函数来做位置编码，pos是token在句中的位置，i是其维度。
所以每个维度的PE都对应了一个正弦波，波长从2π to 10000⋅2π并构成等比数列。
从图中也可以发现，列（dim）直接是交错的sin/cos，并沿着行的方向进行变化，dim小的列变化快，dim大的列变化慢。
```python
class PositionalEncoding(nn.Module):

    def __init__(self, d_model, dropout, max_len=5000):

        super(PositionalEncoding, self).__init__()

        self.dropout = nn.Dropout(p=dropout)

  

        pe = torch.zeros(max_len, d_model) # 5000*512

        position = torch.arange(0, max_len).unsqueeze(1)

        div_term = torch.exp( # 频率项 长度为 d_model/2 = 256

            torch.arange(0, d_model, 2)

        )

        pe[:, 0::2] = torch.sin(position * div_term)

        pe[:, 1::2] = torch.cos(position * div_term)

        pe = pe.unsqueeze(0)

        self.register_buffer("pe", pe)

    def forward(self, x):

        x = x + self.pe[:, :x.size(1)].requires_grad_(False)

        return self.dropout
```
给定相对offset K， PE（pos+K）可以以PE（pos）的线性表示出来。
$\sin(a+b) = \sin(a)\cos(b) + \cos(a)\sin(b)$

![F 3.png]({{ "/images/Transformer/The Annotated Transformer/F 3.png" | absolute_url }})
维度低时频率高（秒针），维度高时频率低（时针）
### Position-wise Feed-Forward Networks
![F 5.png]({{ "/images/Transformer/The Annotated Transformer/F 5.png" | absolute_url }})
简单的组成部分，编码器和解码器中的每一层都包含一个两层的FFN，模型中dmodel​=512, dff​=2048.
```python
class PositionwiseFeedForward(nn.Module):

    "FFN"

    def __int__(self, d_model, d_ff, dropout=0.1):

        super(PositionwiseFeedForward, self).__init__()

        self.w_1 = nn.Linear(d_model, d_ff)

        self.w_2 = nn.Linear(d_ff, d_model)

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):

        return self.w_2(self.dropout(self.w_1(x).relu()))
```
### Encoder and Decoder Stacks

The encoder/decoder is composed of a stack of N=6 identical layers.
所以我们需要一些辅助函数来帮助我们更加高效（优雅）的实现。
#### Clone
```python
def clones(module, N):
	"Produce N identical layers."
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])
```
#### LayerNorm
```python
class LayerNorm(nn.Module):

    "Construct a layernorm module (See citation for details)."

  

    def __init__(self, features, eps=1e-6):

        super(LayerNorm, self).__init__()

        self.a_2 = nn.Parameter(torch.ones(features))

        self.b_2 = nn.Parameter(torch.zeros(features))

        self.eps = eps

  

    def forward(self, x):

        mean = x.mean(-1, keepdim=True)

        std = x.std(-1, keepdim=True)

        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2
```
self.a_2 和 self.b_2 是模型中可训练的参数，且模型中每个 LayerNorm 实例的值不一定相同。LayerNorm 是沿着特征维度（而不是 Batch 或 Sequence 维度）进行标准化的，其是将 batch 中的每个句子中的每个 token 都视作单独的对象进行标准化。

以一个输入张量 $X$ 形状为 ({Batch}, {Length}, {Features}) = (B, L, D) 为例进行对比 （8 * 1024 * 512）。LayerNorm 的计算始终发生在单个样本token内部, 也就是会计算出 B * L 组均值和方差，而BatchNorm会计算 D 组均值和方差，所以这也是为什么 LayerNorm 不依赖batch的大小。
#### Residual Connections
```python
class SublayerConnection(nn.Module):

    """

    A residual connection followed by a layer norm.

    Note for code simplicity the norm is first as opposed to last.

    """

  

    def __init__(self, size, dropout):

        super(SublayerConnection, self).__init__()

        self.norm = LayerNorm(size)

        self.dropout = nn.Dropout(dropout)

  

    def forward(self, x, sublayer):

        "Apply residual connection to any sublayer with the same size."

        return x + self.dropout(sublayer(self.norm(x)))
```
**LayerNorm(x+Sublayer(x))**，这是原始论文中的实现（Post-LN），该code中为了实现简单使用的是前归一化（Pre-LN），这也是现在主流模型的做法（训练更加稳定）。

在 Post-LN 中，残差连接之后立即进行归一化。随着层数加深，输出层附近的梯度会变得非常不稳定。而在 Pre-LN 中，由于残差分支的存在，模型在每一层都像是在原始输入的基础上做“修正”。这种结构类似于一种更平滑的迭代优化，让优化器更容易找到最优解。

注意现在最前沿的模型（如 Llama 3），使用 **RMSNorm** 代替标准的 **LayerNorm**。计算更简单，性能几乎一样，速度更快。
- **LayerNorm**：平移缩放（减均值，除方差）。    
- **RMSNorm**：仅缩放（除以均值的平方根）。    
#### Encoder
![F 6.png]({{ "/images/Transformer/The Annotated Transformer/F 6.png" | absolute_url }})
```python
class Encoder(nn.Module):

	"Core encoder is a stack of N layers"
	 
    def _init_(self, layer, N):

        super(Encoder, self)._init_()

        self.layers = clones(layer, N)

        self.norm = LayerNorm(layer.size)

    def forward(self, x, mask):

        for layer in self.layers:

            x = layer(x, mask)

        return self.norm(x)
```

可以看到，在N层layer操作完成后再最外面还存在一个LayerNorm（符合Pre-LN 结构）
```python
class EncoderLayer(nn.Module):

    "Encoder is made up of self-attn and feed forward (defined below)"
  
    def __init__(self, size, self_attn, feed_forward, dropout):

        super(EncoderLayer, self).__init__()

        self.self_attn = self_attn

        self.feed_forward = feed_forward

        self.sublayer = clones(SublayerConnection(size, dropout), 2)

        self.size = size
  

    def forward(self, x, mask):

        "Follow Figure 1 (left) for connections."

        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))

        return self.sublayer[1](x, self.feed_forward)
```
一个单层的EncoderLayer则是包含self-attn和feed forward。由于SublayerConnection函数只接受两个参数，x和作用于x的一个函数。但是self_attn需要输入四个参数，所以需要使用`lambda x: self.self_attn(x, x, x, mask)`来将其包装成一个单独的函数。这样，一个 4 参数的函数就被“包装”成了一个 1 参数的函数。
#### Decoder
The decoder is also composed of a stack of N=6N=6 identical layers.
```python
class Decoder(nn.Module):

	"Generic N layer decoder with masking."	
	
    def __init__(self, layer, N):

        super(Decoder, self)._init_()

        self.layers = clones(layer, N)

        self.norm = LayerNorm(layer.size)

  

    def forward(self, x, memory, src_mask, tgt_mask):

        for layer in self.layers:

            x = layer(x, memory, src_mask, tgt_mask)

        return self.norm(x)
```
同样的，在最外层也有LayerNorm操作。
```python
class DecoderLayer(nn.Module):
	
	"Decoder is made of self-attn, src-attn, and feed forward"
		
    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):

        super(DecoderLayer, self).__init__()

        self.size = size

        self.self_attn = self_attn

        self.scr_attn = src_attn

        self.feed_forward = feed_forward

        self.sublayer = clones(SublayerConnetion(size, dropout), 3)

  

    def forward(self, x, memory, src_mask, tgt_mask):

        m = memory

        x = self.sublayer[0](x, lambda x:self.self_attn(x, x, x, tgt_mask))

        x = self.sublayer[1](x, lambda x:self.src_attn(x, m, m, src_mask))

        return self.sublayr[2](x, self.feed_forward)
```
这里面的参数memory是指encoder层的输出，注意在实际训练/推理的时候memory只需要计算一次，然后每次decoder自回归的时候传入就可以。
#### Mask
```python
def subsequent_mask(size):

    "Mask out subsequent positions."

    attn_shape = (1, size, size)

    subsequent_mask = torch.triu(torch.ones(attn_shape), diagonal=1).type(

        torch.uint8

    )

    return subsequent_mask == 0
```
上述代码其实相当于一个下三角矩阵(包含主对角线), 这是因为在上实现中第一个token是特殊的开始符号SOS
![F 7.png]({{ "/images/Transformer/The Annotated Transformer/F 7.png" | absolute_url }})
#### Attention
![F 9.png]({{ "/images/Transformer/The Annotated Transformer/F 9.png" | absolute_url }})
![F 8.png]({{ "/images/Transformer/The Annotated Transformer/F 8.png" | absolute_url }})
```python
def attention(query, key, value, mask = None, dropout=None):

    d_k = query.size(-1)

    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
	#在decoder部分为了防止泄露会使掩码，在矩阵计算（高效）完以后用-Inf来代替
    if mask is not None: 

        scores = scores.masked_fill(mask == 0, -1e9)

    p_attn = scores.softmasx(dim=-1)

    if dropout is not None: #正则化，防止过于依赖某些词

        p_attn = dropout(p_attn) #dropout会有补偿，保证概率和为1

    return torch.matmul(p_attn, value), p_attn
```
![F 10.png]({{ "/images/Transformer/The Annotated Transformer/F 10.png" | absolute_url }})![F 11.png]({{ "/images/Transformer/The Annotated Transformer/F 11.png" | absolute_url }})
```python
class MultiHeadAttention(nn.Module):

    def __init__(self, h, d_model, dropout=0.1):

        super(MultiHeadAttention, self).__init__()

        assert d_model % h ==0

        # We assume d_v always equals d_k

        self.d_k = d_model // h

        self.h = h
        
		#四个512到512的全连接层
        self.linears = clones(nn.Linear(d_model, d_model), 4) 
        
        self.attn = None

        self.dropout = nn.Dropout(p=dropout)

  

    def forward(self, query, key, value, mask=None):

        if mask is not None:

            mask = mask.unsequeeze(1)

        nbatches = query.size(0) # 获得batch大小

  

        # 1) Do all the linear projections in batch from d_model => h x d_k

        query, key, value = [

            lin(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2)

            for lin, x in zip(self.linears, (query, key, value))

        ]

        # 2) Apply attention on all the projected vectors in batch.

        x, self.attn = attention(

            query, key, value, mask=mask, dropout=self.dropout

        )

  

        # 3) "Concat" using a view and apply a final linear.

        x = (

            x.transpose(1, 2) # (batch, head, lenth, dim) -> (batch, lenth, head, dim)

            .contiguous()

            .view(nbatches, -1, self.h * self.d_k)

        ) 

        del query

        del key

        del value

        return self.linears[-1](x)
```
- transpose(1, 2)：逻辑上把多头的信息拉回到正确的“词”位置上。
- .contiguous()：物理上把数据在内存里重新排整齐。 
- .view(...)：把排整齐的 8 个头正式“缝合”成一个大向量。  

你可以把 transpose 看作是“调整座次表”，而 .contiguous() 则是“让大家按照新座次表真正地起身换座位”。只有换完座，才能进行下一步的整体合影（view）。

实现中lenth经常是用-1参数自动计算，因为每个batch中的lenth不一定相同。
![F 12.png]({{ "/images/Transformer/The Annotated Transformer/F 12.png" | absolute_url }})
## Training
```python
class Batch:

    """Object for holding a batch of data with mask during training."""
  
    def __init__(self, src, tgt=None, pad=2):  # 2 = <blank>

        self.src = src

        self.src_mask = (src != pad).unsqueeze(-2)

        if tgt is not None:

            self.tgt = tgt[:, :-1]

            self.tgt_y = tgt[:, 1:]

            self.tgt_mask = self.make_std_mask(self.tgt, pad)

            self.ntokens = (self.tgt_y != pad).data.sum()
  
    @staticmethod

    def make_std_mask(tgt, pad):

        "Create a mask to hide padding and future words."

        tgt_mask = (tgt != pad).unsqueeze(-2)

        tgt_mask = tgt_mask & subsequent_mask(tgt.size(-1)).type_as(

            tgt_mask.data

        )

        return tgt_mask
```
src_mask：屏蔽源句中的 `<pad>`，(batch, 1, src_len)
tgt_mask：屏蔽padding填充（2 = `<pad>`）和future未来的词，(batch, tgt_len, tgt_len)
