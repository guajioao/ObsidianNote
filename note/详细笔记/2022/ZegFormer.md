Decoupling Zero-Shot Semantic Segmentation
收录于：CVPR2022


## 摘要：
* 现有工作将ZS3(Zero-shot semantic segmentation)定义为像素级零样本分类问题，并借助仅经过文本预训练的语言模型，将语义知识从可见类迁移到不可见类。
	* 虽然简单，但是相对视觉-语言模型(即CLIP这样的)来说能力有限。
* 受到人类执行片段级语义标注行为的启发，作者将ZS3解耦为两个子任务：
	* 1）类别无关的分组任务，将像素分为多个段segments
	* 2）在这些段上进行零样本分类
	* 任务1不涉及类别信息，可以直接迁移到对不可见类的分组
	* 后一项任务在分段级别上进行，并自然地使用进过图像-文本对预训练的大规模视觉语言模型(例如CLIP)来进行
* 基于这样的解耦公式，提出ZegFormer

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 结构图
	* ![[Pasted image 20231014150308.png]]
	* 图像输入(图像分类)backbone生成视觉特征图
	* 视觉特征图与N个queries(哪来的？随机初始化？)一起通过Transformer解码器生成N个segment embeddings段嵌入
	* 段嵌入分别通过Mask投影和语义投影，生成N个mask嵌入和N个语义段嵌入**Semantic segment embedding**
		* Mask嵌入与特征图经过像素解码器的输出相乘，获得N个**class-agnostic masks**类别无关的掩码，并计算mask损失
		* 语义段嵌入与文本特征（计算相似度？矩阵乘法？），计算分类损失
	* N个类别无关的掩码与原图一起生成N个masked images，然后用预训练图像编码器生成特征并分类


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
### 3.1 ZS3的解耦公式
对于给定图像 *I*，其语义分割可被定义为( R, L )
	* R将图像分组为N个段，其中所有R的并集就是图像域，R之间交集为空
	* L将每个段R和语义标签 c ∈ C 联系在一起，其中类别C是预定义的集合
* 完全监督的语义分割从大规模语义标注数据集中学习，例如：$\mathrm {D} = {\left \{ I_k,\mathcal{R_k},\mathcal{L}_k \right \} }^K_{k=1}$ 
	* 通常假设类别集C是封闭的，即在测试图像中出现的类别被C很好地包含。但实际应用场景中并非如此
* 事实上，如果将注释数据集D的类别集表示为**S，即可见类**，而**E为在测试阶段出现的类**。有三种类型的语义分割设置：
	* 完全监督的语义分割：**E ⊆ S**
	* 零样本语义分割ZS3：**S ∩ E = Ø**
	* 广义GZS3问题：**S ⊂ E**
* 此文主要解决GZS3问题，并用**U** = E − E ∩ S代表**unseen类**
##### 与像素级零样本分类的区别
* 此前的工作将ZS3定义为一个像素级零样本分类问题，即从可见类S的像素级语义标签中学习并推广到不可见类U的像素中
* 这可以看作是本文解耦公式中的一个特殊情况：每个像素代表一个段Ri
* 由于R的学习不涉及语义类别，该公式将类不可知学习任务从ZS3中分离出来作为子任务
* **类不可知任务对不可见类有很强的概括能力**
* 建立从语义到片段视觉特征的连接，比到像素级视觉特征的连接更自然，因此本文提出的解耦公式比直接进行像素级零样本分类问题更加有效

### 3.2 ZegFormer
首先产生一系列段级嵌入，然后通过两个平行的分支分别将其投影，分别去做**类别无关的grouping**分组和**段级的分类**任务

##### Segment Embeddings
最近有很多方法能够产生段级embeddings。本文出于简单起见，选择Maskformer作为基础的语义分割模型
* 通过向一个Transformer解码器中投入N个queries和一个特征图，可以获得N个段级embeddings
* 然后将每一个段级嵌入分别通过一个语义投影和mask掩码投影层，获得每个段的语义嵌入和mask嵌入。
* segment-level semantic embedding (SSE)用$G_q \in \mathbb{R}^d$ 表示
* the segment-level mask embedding用$B_q \in \mathbb{R}^d$ 表示
* q为queru的序号index

##### Class-Agnostic Grouping
* 将特征图从像素解码器的输出表示为 $\mathcal{F}(I) \in \mathbb{R}^{d \times H \times W}$ 
* 通过将F(I)与段级掩码嵌入Bq相乘，获得N个对每一个query的二元binary掩码的预测结果 $m_q = \sigma(B_q \cdot \mathcal{F}(I)) \in [0,1]^{H \times W}$ 
* σ为sigmoid函数，N通常小于类别个数

##### Segment Classification with SSE(Semantic segment embedding)
* 如CLIP一般获得文本特征T，在训练时类别C = S，在推理时C = S ∪ U
* 在本文的pipeline中还需要一个"no object"类，来表示那些与任何一个GT的IoU都很低的情况
* 因此需要为"no object"加入一个额外的可学习的embedding $T_0 \in \mathbb{R}^d$
* 计算SSE与T的相似度，获得段与对应的最相似文本标签作为分类结果
##### Segment Classification with Image Embedding
* 使用预训练的视觉语言模型（例如CLIP）的图像编码器
* 为每一个段创建一个合适的子图像Iq（通过mask计算的masked 图像或cropped图像）
* 用Iq通过图像编码器获得图像嵌入。同样与文本特征计算相似度

##### Training
* 在训练中只有可见类S的标签被使用
* 在预测masks与GT masks之间计算a bipartite matching匹配损失




## 四、实现细节


## 五、实验结果


## 六、结论


## Question
1.语义段分类与Mask生成可以同时进行