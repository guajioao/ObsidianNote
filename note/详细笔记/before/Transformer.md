发表于：NIPS2017
论文名：Attention Is All You Need
## 摘要：
* 主流的序列转换模型是基于复杂的循环神经网络或卷积神经网络，包括一个编码器和解码器。
	* 性能最好的模型还通过注意力机制将编码器和解码器连接起来
* 提出一个新的简单网络架构，即**Transformer**仅仅基于注意力机制，完全取消了循环和卷积。
	* 在两个翻译任务上的实验证明，本模型质量更优、更加并行，需要的训练时间更少
	* 

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、Background]]
* [[#三、Model Architecture]]
* [[#四、Why self-attention]]
* [[#五、Training]]
* [[#六、Result]]
* [[#七、Conclusion]]

## 结构
* 结构图：
	* 图1：![[Pasted image 20231020220059.png|400]]
	* 

## 一、引言 Introduction
* 循环神经网络，特别是LSTM和门控循环神经网络，已成为序列建模和转换问题的最前沿方法，比如语言建模和机器翻译。
	* 循环模型通常沿着输入输出序列的symbol位置进行因素计算。方法天然的排除了训练的并行化，而这因为内存限制在长序列上至关重要。
	* 注意力机制对依赖关系建模，而不依靠输入或输出序列中的距离。但是这种注意力机制一般与循环神经网络一起使用
* 提出Transformer，回避了循环结构而是完全依赖于注意力机制来绘制输入与输出之间的依赖关系。
	* 允许更多的并行化

## 二、Background


## 三、Model Architecture
* 大多数好的神经序列转换模型有一个编码器-解码器的结构。
	* 编码器将输入序列的符号表示$(x_1,\cdots,x_n)$转换为连续的特征序列$z = (z_1,\cdots,z_n)$
	* 给定一组z，解码器一次产生一个输出序列$(y_1,\cdots,y_n)$中的一个元素【训练时通过maskGT可以同时训练得到多个y】
	* 每一步中该模型都是**自回归**的，在生成下一个符号时使用先前生成的符号作为输入【即自己作为自己的输入】
* Transformer也大体上使用这样的结构，使用堆叠的自注意力和point-wise全连接层组成编码器和解码器。编码器和解码器的结构图1左和右。

### 3.1 编码器和解码器堆叠Stacks
* **编码器**：由$N = 6$个独立的层堆叠组成，每一层有两个子层。
	* 第一个子层为多头自注意力**MHSA**机制，第二层为一个简单的，position-wise的全连接前馈网络
	* 每个子层之间由残差结构连接，并跟着一个层归一化。即，每个子层的输出都是$LayerNorm(x+SubLayer(x))$。
* **编码器**：也由$N = 6$个独立的层堆叠组成，但每一层有三个子层。
	* 在第一个和第二个子层之间插入了第三个子层，连接Encoder的输出与Decoder【Cross Attention】
	* 每个子层之间也由残差结构连接，并跟着一个层归一化。
	* 第一个子层修改为Masked MHSA，防止当前位置后面的序列出现在输入中
	* 这样的mask再加上一个操作：输出的embeddings会后移一位，确保了对位置i的预测只能依赖于小于i的位置的已知输出

### 3.2 注意力Attention
一个注意力函数可以被形容为：将一个query和一组key-value对映射为一个输出，其中query,keys,values和输出都是向量。output输出是通过values的加权求和计算得到的，分配给每个value的权重是通过一个**compatibility function**在query和相关的key上计算得到的。【compatibility function即用q和k计算权值的函数】

### 3.2.1 Scaled Dot-Product Attention
作者将他们特别设计的attention称为"Scaled 点积注意力"，如图2所示。输入由$d_k$的queries和keys、与$d_v$维的values组成。用Q和所有Keys相乘，再除以$\sqrt{d_k}$，并用一个softmax函数来获得values的权重。【特点是用$\sqrt{d_k}$来缩放点乘结果，防止梯度过大】
![[Pasted image 20231105162138.png#Fig2|inL|244]]实际上会同时计算一组queries的attention并打包为一个matrix Q，所有keys和values也会被一起打包为K和V。通过下列公式计算输出矩阵：
$$Attention(Q,K,V) = softmax(\frac{QK^T}{\sqrt{d_k}})V$$
	* 两个使用最广的注意力函数是加法注意力和点积(乘法)注意力。该算法与点积注意力一致，除了增加了一个$\frac{1}{\sqrt{d_k}}$的scaling factor。加法注意力用包含一个隐层的前馈网络来计算compatibility function。这两者在理论复杂性上是相似的，但点积复杂度实际上更快也更有效率，因为它可以使用高度优化的矩阵乘法来实现。
在$d_k$比较小的时候二者是相似的，但加法注意力因为不需要对$d_k$个大量数值进行缩放，比乘法注意力表现更好。我们怀疑当$d_k$很大时，点积的增长幅度也很大，这会将softmax函数推到梯度很小的区域。为了减轻这样的影响，我们使用了$\frac{1}{\sqrt{d_k}}$来缩放点积。
### 3.2.2 Multi-Head Attention
不使用与模型维度$d_{model}$相同的kays,values和queries，作者发现对qkv使用h次不同的线性投影，分别学到$d_k$,$d_k$,$d_v$维，这样是更好的操作。对每一个投影后的qkv平行的应用注意力函数，产生$d_v$维度的输出值。这些输出会被Concat起来，并再次投影，获得最终的输出。
![[Pasted image 20231106103144.png|274]]
多头注意力可以关注来自不同位置的不同表征子空间。
$$MultiHead(Q,K,V) = Concat(head_1,\cdots,head_h)W^O$$
where $head_i = Attention(QW^Q_i,KW^K_i,VW^V_i)$
其中投影的参数矩阵$W^Q_i \in R^{d_{model}\times d_k},W^K_i \in R^{d_{model}\times d_k},W^V_i \in R^{d_{model}\times d_v},W^O \in R^{d_k\times d_{model}}$。在本工作中使用$h=8$个平行注意力层或头，每一层使用$d_k=d_v=d_{model}/h=64$。由于每一个头的维度减小了，总计算量与单头全维度的注意力是相似的。

### 3.2.3 Application of Attention in our Model
Transformer通过三种方式使用多头注意力：
* "编码器-解码器注意力"层


## 四、Why self-attention


## 五、Training


## 六、Result


## 七、Conclusion
提出了Transforemr，第一个**完全基于注意力**的序列转换模型，用**多头自注意力**代替了在编码器-解码器架构中常用的循环层。
对于翻译任务，Transformer比与循环或卷积层的架构的**训练快**非常多。在两个数据集上都取得了最新的sota成绩。在WMT 2014 English-to-German翻译任务中Transformer最好的模型甚至超过了之前所有的集成模型。
对于基于注意力的模型的未来非常excited，并计划将它们用于其他任务中。计划将Transformer拓展到文本以外的，输入-输出模式的问题，并研究局部受限的注意力机制，来更有效的处理大规模输入和输出，例如图像、音频和视频。产生更少的序列也是我们的研究目标之一。
