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
	* 图1：![[Pasted image 20231020220059.png|450]]
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

#### 3.2.1 Scaled Dot-Product Attention
作者将他们特别设计的attention称为"Scaled 点积注意力"，如图2所示。输入由$d_k$的queries和keys、与$d_v$维的values组成。用Q和所有Keys相乘，再除以$\sqrt{d_k}$，并用一个softmax函数来获得values的权重。【特点是用$\sqrt{d_k}$来缩放点乘结果，防止梯度过大】
图2(left):![[Pasted image 20231105162138.png#Fig2|inC|244]]
实际上会同时计算一组queries的attention并打包为一个matrix Q，所有keys和values也会被一起打包为K和V。通过下列公式计算输出矩阵：
$$Attention(Q,K,V) = softmax(\frac{QK^T}{\sqrt{d_k}})V$$
	* 两个使用最广的注意力函数是加法注意力和点积(乘法)注意力。该算法与点积注意力一致，除了增加了一个$\frac{1}{\sqrt{d_k}}$的scaling factor。加法注意力用包含一个隐层的前馈网络来计算compatibility function。这两者在理论复杂性上是相似的，但点积复杂度实际上更快也更有效率，因为它可以使用高度优化的矩阵乘法来实现。
在$d_k$比较小的时候二者是相似的，但加法注意力因为不需要对$d_k$个大量数值进行缩放，比乘法注意力表现更好。我们怀疑当$d_k$很大时，点积的增长幅度也很大，这会将softmax函数推到梯度很小的区域。为了减轻这样的影响，我们使用了$\frac{1}{\sqrt{d_k}}$来缩放点积。

#### 3.2.2 Multi-Head Attention
不使用与模型维度$d_{model}$相同的kays,values和queries
* 对qkv使用h次不同的线性投影，分别学到$d_k$,$d_k$,$d_v$维
* 对每一个投影后的qkv平行的应用注意力函数，产生$d_v$维度的输出值
* Concat这些输出，并再次做投影，获得最终的输出。

图2(right)：![[Pasted image 20231106103144.png|274]]
多头注意力可以关注来自不同位置的不同表征子空间。
$$MultiHead(Q,K,V) = Concat(head_1,\cdots,head_h)W^O$$
其中 $head_i = Attention(QW^Q_i,KW^K_i,VW^V_i)$，投影的参数矩阵:$W^Q_i \in R^{d_{model}\times d_k}$,$W^K_i \in R^{d_{model}\times d_k}$,$W^V_i \in R^{d_{model}\times d_v}$,$W^O \in R^{d_k\times d_{model}}$。
在本工作中使用$h=8$个平行的注意力层或头，每一层使用$d_k=d_v=d_{model}/h=64$。由于每一个头的维度减小了，总计算量与单头全维度的注意力是相似的。

#### 3.2.3 Application of Attention in our Model
Transformer通过三种方式使用多头注意力：
* "编码器-解码器注意力"层【即解码器第二层】![[Pasted image 20231108101213.png]]
	* q来自前一个decoder层，k和v来自编码器的输出。
	* 这使得编码器的每一个position都能够关注【attend】输入序列的每一个位置【我的理解是让q能够看到所有的inputs】【与mask的作用区别】
	* 这模仿了Seq2Seq模型中经典的编码器-解码器注意力机制
* **编码器**中的自注意力层![[Pasted image 20231108101240.png]]
	* 所有的keys,values和queries都来自上一层的输出的同一个地方。
	* 当前层的每一个position可以关注到上一层的所有位置
* **解码器**中的自注意力层(Masked Multi-Head Attention)![[Pasted image 20231108101251.png]]
	* 当前层的每一个位置都可以关注到上一层所有传来的未被mask的区域
	* 需要防止信息向左流动，以保持自回归特性
	* 通过在缩放的点积注意力中mask所有不合适位置的连接来实现

### 3.3 Position-wise Feed-Forward Networks
在注意力子层之外，编码器和解码器每一层还包含一个全连接前馈网络，它分别独立的应用于每个position。
*  这里的position指什么？输入很多个单词，每个单词都是一个position 。对每一个词都用同样的一个MLP作用一次，即point-wise
* head之间分别独立？
![[Pasted image 20231108100634.png]]
* 由两个线性变换组成，中间夹一个ReLu激活$$FFN(x)=max(0,xW_1+b_1)W_2+b2$$
	* $xW_1+b_1$即第一个线性层，然后用一个ReLU的激活函数，之后在外面再套一个线性层
	* 其中线性变化虽然在不同位置是相同的，但是每一层的参数不同
* 另一种描述方法：两个大小为1的卷积
	* 输入输出维度是$d_{model}=512$，且the inner-layer的维度为$d_{ff}=2048$

### 3.4 Embeddings and Softmax
对于任何一个词，学习一个长度为$d_model$的向量来表示它
* 与其他序列转化模型一样，
	* 使用学习到的embedding将输入tokens和输出tokens转换为$d_{model}$维的向量
	* 使用寻常的线性变换和softmax函数来转换decoder的输出来预测下一个token的概率
* 在两个embedding层(Input Embedding和Output Embedding)和pre-softmax线性变换之间共享同一个权值矩阵
* 在embedding层，将这些权重乘以$\sqrt{d_{model}}$
	* 在学习embedding的时候，学到的L2 norm会是一个比较小的值，d越大，l2 norm后就越小。因此需要乘以$\sqrt{d_{model}}$，使其在与位置编码相加的时候二者的范围差不多
	* 位置编码是三角函数，值在-1到+1之间抖动

### 3.5 Positional Encoding
![[Pasted image 20231108100941.png]]

因为没有循环和卷积了，要利用序列的顺序，必须注入关于序列中tokens的相对或绝对位置的信息：
* 为此，在编码器和解码器栈底的输入embeddings中加入位置编码"Positional Encoding"
* 位置编码与embeddings一样也是$d_{model}$维的，因此可以直接相加
* 位置编码有许多选择，学习的或者固定的。
	* 在本文中使用不同频率的sine和cosine函数：
	$$PE_{(pos,2i)}= sin(pos/10000^{2i/d_{model}})$$
	$$PE_{(pos,2i+1)}= cos(pos/10000^{2i/d_{model}})$$
	* 其中pos指位置，i是维度。即，位置编码的每一个维度都对应一个正弦曲线。例如$PE(1,2)=sin(1*10000^{-2/d_{model}})$就是指位置0的第2个维度的值
	* 对于任何一个值，可以用一个长为$d_{model}$的向量表示，这个向量记录了时序信息
	* Transformer选择这个函数是因为，他们假设它使得模型能够很容易的通过相对位置学习注意力(注意力矩阵A)，因为对于固定偏移k，$PE_{pos+k}$可以用一个$PE_{pos}$的线性函数表示
		* 防止$x_1,x_2$调换位置后A不变
		* 未加入位置编码前：对于$x_t,x_s$，二者之间的注意力$A_{t,s}=q_t^Tk_s=x_t^TW_Q^TW_Kx_s$
		* 加入位置编码后：$A_{t,s}=q_t^Tk_s=(x_t+p_t)^TW_Q^TW_K(x_s+p_s)$
		* $A_{t,s}=x_t^TW_Q^TW_Kx_s+x_t^TW_Q^TW_Kp_s+p_t^TW_Q^TW_Kx_s+p_t^TW_Q^TW_Kp_s$
		$p_t=[\cdots,sin(\frac{t}{10000^{2i/d}}),cos(\frac{t}{10000^{2i/d}}),\cdots]^T \in \mathbb{R}^d$
【拓展】Transformer意图在$q_t,k_s$做内积时通过两个p来得到token间的相对位置，即：
	$p_t^Tp_s^T=\sum(\sin t\theta_i \sin s\theta_i+\cos t\theta_i \cos s\theta_i) = \sum \cos(t-s)\theta_i$
	$\theta_i = 10000^{-2n/d}$ 
	希望获得cos(t-s)这一相对位置
**但是**，在TENER文中指出，由于参数矩阵的存在，实际上相对位置由$p_t^TW_Q^TW_Kp_s$表示，而非$p_t^Tp_s^T$。如下图所示，蓝色的线是$p_t^Tp_s^T$，而下面两条是两个随机$W_S$计算得出的$p_t^TW_Q^TW_Kp_s$。可以看出实际上无法真正在计算注意力矩阵式感知到相对位置信息
![[Pasted image 20231108112654.png|475]]

* RNN跟Transformer一样都是通过MLP来做语义空间的转换。
不一样的地方是如何传递序列的信息。
	RNN通过将上一个时刻的信息输出传入下一个时刻来作为输入的一部分【先MLP获取当前时刻语义信息，再向后传递信息】
	Transformer通过一个Attention层全局的获取整个序列的信息然后再用MLP来做语义信息的转换【先获取全局信息再转换成语义信息】

## 四、Why self-attention
将自注意力的各个方面与循环层和卷积层比较。这两种层通常用于将一个任意长度的符号表示序列$(x_1,\cdots,x_n)$映射为另一个等长的序列$(z_1,\cdots,z_n)$，其中$x_i,z_i \in \mathbb{R}^d$，例如经典序列转换编码-解码器中的隐藏层。
相比之下注意力层的优势有三个（表1）：
* 每层的总计算复杂度。
* 可以并行计算
* 输入与输出序列长距离依赖关系之间的路径更短。
	* 在输入和输出序列中的任意两个位置的组合之间的路径越短，就越容易学习长期依赖关系
	* Maximum Path Length:信息从一个数据点到另一个数据点要走多远
		* Attention中：任何一个query可以跟任何一个key做运算，即最大长度也只需要一次运算
		* RNN中最前面的信息需要经过N个时刻才能传达到最后
![[Pasted image 20231109215058.png]]


## 五、Training
### 5.1 Training Data and Bathing
### 5.2 Hardware and Schedule
### 5.3 Optimizer优化器
* 使用Adam优化器，$\beta_1=0.9,\beta_2 = 0.98,\epsilon=10^{-9}$。
* 学习率通过公式动态变化
	* $lrate=d^{-0.5}_{model}\cdot min(step\_num^{-0.5},step\_num\cdot warmup\_steps^{-1.5})$ 
	* 作者将warmup_step设置为4000
	* 





## 六、Result


## 七、Conclusion
提出了Transforemr，第一个**完全基于注意力**的序列转换模型，用**多头自注意力**代替了在编码器-解码器架构中常用的循环层。
对于翻译任务，Transformer比与循环或卷积层的架构的**训练快**非常多。在两个数据集上都取得了最新的sota成绩。在WMT 2014 English-to-German翻译任务中Transformer最好的模型甚至超过了之前所有的集成模型。
对于基于注意力的模型的未来非常excited，并计划将它们用于其他任务中。计划将Transformer拓展到文本以外的，输入-输出模式的问题，并研究局部受限的注意力机制，来更有效的处理大规模输入和输出，例如图像、音频和视频。产生更少的序列也是我们的研究目标之一。
