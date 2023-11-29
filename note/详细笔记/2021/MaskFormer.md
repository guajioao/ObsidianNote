
收录于：NIPS2021
Per-Pixel Classification is Not All You Need for Semantic Segmentation
[code](https://github.com/facebookresearch/MaskFormer)

## 摘要：
* 语义分割被视为逐像素分类问题，实例分割在此基础上被视为mask分类
	* 作者认为，mask分类对于语义分割和实例分割都足够有效
	* 二者可以用同样的模型、损失与训练步骤
* 提出MaskFormer，即在这个思想上提出的mask分类模型
	* 对于每一个类预测一个二元掩码
* 结果SOTA

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* per-pixel vs mask 分类
	* ![[Pasted image 20231121215242.png]]
	* 每一个mask都单独计算mask损失和分类损失
	* 这样成组的进行匹配可以通过[[DETR]]中采用的bipartite matching或者通过fixed matching，即直接使用mask的index（当预测结果个数K与类别个数N相同时:$K=N$）
* MaskFormer Overview
	* ![[Pasted image 20231121220910.png]]
	* 用backbone提取出特征图$F$
	* 为什么在MaskFormer中要直接用F，而不像DETR中一样通过encoder之后再输入decoder
	* 两条线：分别计算分类损失与二元掩码损失
		* 分类损失线：
			* F输入Transformer decoder，产生N个per-segment embeddings $Q \in \mathbb{R}^{C_Q \times N}$【queries是N个可学习的embeddings】
				* queries是N个$C_Q \times 1$大小的向量
				* 每一个query在Transformer 解码器中都独立的对$F$进行交叉注意力查询
			* 这个$Q$独立地分别产生N个**类别预测**和N个对应的mask embeddinngs $\varepsilon_{mask}$
		* 二元掩码损失线：
			* F通过pixel decoder产生per-pixel embeddings $\varepsilon_{pixel}$
			* $\varepsilon_{pixel}$与$\varepsilon_{mask}$做点积，后面跟着一个Sigmoid激活，产生N个**二元掩码预测**
	* 对语义分割任务，直接将N个二元损失与他们的类别预测通过一个简单的矩阵乘法combine起来即可
Transformer decoder部分的query用CLIP的文本特征？这部分的目的是产生每个class对应的mask embeddings。 ^9af7dd


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
* 先描述语义分割在逐像素分类和掩码分类下的公式
* 介绍作者提出的掩码分类模型，以及使用的Transformer decoder在其中的作用
* 提出一种简单的将mask分类输出结果转换为其他任务依赖的输出格式
### 3.1 逐像素分类公式
对于一个HxW的图像，总共有K个类别，需要预测图像的每个像素$y=\{p_i|p_i \in \Delta^{K}\}$，其中$\Delta^{K}$是一个K维的概率向量。
训练非常直接，直接用ground truth的类别标签$y^{gt}=\{y^{gt}|y^{gt} \in  \{1,\cdots ,K\}\}^{H\cdot W}_{i=1}$来计算每个像素的交叉熵损失 $\mathcal{L}_{pixel-cls}(y,y^{pt})=\sum^{H\cdot W}_{i=1}-\log p_i(y^{gt}_{i})$

### 3.2 掩码分类公式
将语义分割任务分解为：划分区域获得二元掩码；对掩码进行分类
* 将图像划分/分组为N个区域(N不一定与K相等)，用二元掩码表示$\{m_i|m_i \in [0,1]^{H\times W}\}^N_{i=1}$
* 用在K个类别上的分布将每个区域联系成一个整体
* 对每一个segment进行联合分组和分类，即进行掩码分类
	* 定义了目标输出$z$，是一组N概率-掩码对，即$z=\{(p_i,m_i)\}^N_{i=1}$
	* $p_i \in \Delta^{K+1}$还包含一个"no object"标签($\phi$)，用于推理不属于K中任何一个类的mask
	* 允许使用相同的class预测多个掩码，使得它可以同时用于语义分割和实例分割任务
训练的时候，掩码分类模型需要在一组预测$z$与一组GT段$z^{gt}$之间进行匹配matching $\sigma$
$z^{gt} = \{(c_i^{gt},m_i^{gt})|c_i^{gt}\in\{1,\cdots,K\},m_i^{gt}\in \{0,1\}^{H\times W}\}_{i=1}^{N^{gt}}$，其中$c_i^{gt}$是第i个类的GT掩码。
* 对于语义分割任务，普通的fixed matching就足够了，因为预测数量N与类别标签K是匹配的。在实验中，作者发现基于bipartite matching的赋值比fixed matching效果更好。
* 与DETR不同，DETR使用bbox来计算在预测$z_i$与GT$z_j^{gt}$之间对于匹配问题的的assignment costs，而作者的工作MaskFormer中直接使用class和mask预测，即$-p_i(c_j^{gt})+\mathcal{L}_{mask} (m_i,m_j^{gt})$，其中$\mathcal{L}_{mask}$是二元mask损失
* 训练时的损失是：![[Pasted image 20231122210319.png]]
* 

### 3.3 MaskFormer
* 计算得到N个概率-mask对$z=\{(p_i,m_i)\}^N_{i=1}$
* 包括三个模块：
	* a pixel-level module：提取出per-pixel embeddings来产生二元掩码预测结果
	* a transforemr module：用一组Transformer decoder layers计算N个per-segment embeddings
	* a segmentation module：从之前的输出中产生预测结果$\{(p_i,m_i)\}^N_{i=1}$
* 在推理的时候，由$p_i$与$m_i$来组装成最终的预测结果

**Pixel-level module**：以$H\times W$大小的图像为输入
* backbone产生低分辨率图像特征图![[Pasted image 20231123203654.png|192]]
		其中$C_{\mathcal{F}}$是通道数，S是特征图的stride(作者使用$S=32$的设置)
* 逐渐上采样特征图，产生per-pixel embeddings $\varepsilon_{pixel}$ ![[Pasted image 20231123204631.png|149]]
		其中$C_{\varepsilon}$是embedding的维度
* 当时的任何基于per-pixel 分类器的分割模型均符合这个像素级模块的设计，包括基于Transforemr的模型
* MaskFormer能将所有这样的模型转换为mask分类模型

**Transformer module**
* 使用标准的Transformer decoder，来从**图像特征图** $\mathcal{F}$和N个可学习的位置编码(即**queries**)计算输出，即N个per-segment embeddings $Q\in \mathbb{R}^{C_Q\times N}$
	* $C_Q$对每一个segment的全局信息进行编码
	* 与[[DETR]]一样，decoder平行的产生输出

**Segmentation module**
* 在Q上用一个线性分类器，跟着一个softmax激活，来对每个segment都产生一个类别概率预测$\{p_i \in \Delta^{K+1}\}^N_{i=1}$
	* 加入了一个"no object"类别，因此是(K+1)
* 为了预测掩码：
	* 用一个有2个隐层的多层感知机(MLP)将Q转换为N个mask embeddings ![[Pasted image 20231123215617.png]]
	* 最后通过第i个mask embedding与per-pixel embedding $m_i$做点积，来获得每一个二元掩码的结果。
	* 点积后面跟着一个sigmoid激活函数，即![[Pasted image 20231123215902.png]]
* 作者发现不使用softmax而是使用sigmoid，即不让各个掩码互相排斥是更有利的
* 在训练中，最后的损失结合了交叉熵分类损失与二元掩码损失
* 为了简便，使用了DETR中相同的mask损失，即一个focal loss与dice loss的线性组合，系数分别为超参数$\lambda_{focal}$和$\lambda_{dice}$

### 3.4 Mask-classification inference
作者发现需要根据评估度量、而不是任务，来选择推理策略。
* 简单的*general inference*，能够将mask分类结果 $\{(p_i,m_i)\}^N_{i=1}$ 转变为全景或者语义分割的标准输出格式
* *semantic inference*，特别为语义分割设计的

**General inference**：通过![[Pasted image 20231123221447.png|350]]将每个像素分配给N个预测的概率-掩码对来将图像分割成块。其中，$c_i$是在每i个概率-掩码对中最可能的类别标签。
* 直觉地，只有在类别概率$p_i(c_i)$和掩码推理概率$m_i[h,w]$都高的情况下才会将位置$[h,w]$分配给概率-掩码对$i$
* 分配给同一个概率掩码对$i$的像素组成一个segment，其中所有的像素类别标签都为$c_i$
	* 语义分割任务中所有$c_i$相同的像素被合并为同一个区域
	* 实例分割中，可以用概率-掩码对的index $i$来区分同一类别的不同实例
	* 为了减少假阳率(FP rate)，在全景分割中采用与DETR和【参考文献24】相同的推理策略
	* 在推理之前先过滤出低置信度的推理结果，并删除了那些有大量掩码被其他预测结果遮挡$(m_i>0.5)$的预测segments

**Semantic inference**是专门为语义分割任务设计的，通过矩阵乘法来进行。
* 作者发现概率-掩码对的边缘，即![[Pasted image 20231123223848.png]]，能够比general inference策略获得更好的结果。
* the argmax不包括"no object"类，因为标准的语义分割结果要求每个像素都取一个标签
* 这一策略返回一个per-pixel class probality![[Pasted image 20231123224202.png]]
* 然而作者观察到直接的最大化每个像素的类别可能会导致结果变差。我们分析这是因为梯度均匀的分布到每一个query中，使得训练变复杂。

MaskFormer这篇文章里3.4讲的两个推理方法
* general inference是对每一个概率-掩码对 $i$ 找到每一个 $c_i$ 中包含的一组概率$p_i(c)$中的最大值，记为 $p_i(c_i)$，然后乘以 $m_i$。找最大的 $p_i\cdot m_i$
* semantic inference对每一个概率-掩码对 $i$ 不找$c_i$中的最大概率了，直接每一组$p_i$都乘以相应的$m_i$后求和，最大化这个求和结果


## 四、实现细节


## 五、实验结果


## 六、结论
* 语义和实例分割范式的差异导致两个任务的模型完全不同，阻碍了图像分割整体的发展
* 作者提出的简单掩码分类模型可以超过SOTA的逐像素分类模型，尤其是在大量类别的情况下。
	* 在全景分割上也很有竞争力，并且不需要改变模型架构、损失、或训练流程
* 作者希望这种统一范式能激发语义分割和实例分割之间跨任务的联合工作