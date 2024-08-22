论文名：AllSpark: Reborn Labeled Features from Unlabeled in Transformer for Semi-Supervised Semantic Segmentation
发表于：CVPR2024

## 总结
* 非开放类别，受限于K个类别标注的训练数据
* 使得每个通道关注不同的类别，而非相似的区域
	* ![[Pasted image 20240822145048.png]]
## 结构
![[Pasted image 20240728204203.png]]

## 摘要：
* 半监督语义分割为减轻像素标注的负担，使用有限的标注数据和大量的未标注数据
	* 当前方法使用GT训练已标注数据，用伪标注训练未标注数据
	* 但这两种训练是分别训练的，因此已标注数据会主导训练过程，导致伪标注质量低
* 本文提出的AllSpark能够通过通道交叉注意力机制更新未标注数据特征，从而缓解这个问题
* 引入语义记忆和通道语义分组策略，以确保未标注特征充分表示了标注特征（ensure that unlabeled features adequately **represent** labeled features）
* AllSpark是SSSS的新的架构(architecture)级设计，而非结构(framework)级别，这避免了越来越复杂的训练管道设计
* 它也可以视为一个灵活的瓶颈结构，可以无缝集成到一般的基于Transformer的分割模型中
* 

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
### 3.2 Channel-wise Cross-attention: the Core of AllSpark
使用未标注数据直接干预(intervene)已标注数据
* 通常不同特征通道编码了不同的语义信息。与patch token相比，这些通道特征包含了更丰富的contextual上下文信息，这些信息在不同的输入图像中更加通用
* 利用这些来自未标注数据的上下文信息来重建标注数据特征，作为一种使用通道智能(channel-wise)交叉注意力机制的鲁棒正则化。在这种机制中，已标注数据作为query，未标注数据作为key和value。
	* 具体来说，计算标注特征每个通道和未标注特征之间的相似性，高相似性的未标注通道对已标注特征的重构作用更为重要
	* 基本原理是，即使未标注的特征可能来自与已标注特征不同的类，它们仍然可以共享具有channel wise的通用信息，例如纹理
公式为：
$$\hat{h}^l=Mv^{\top}=\sigma[\psi(q^{\top}k)]v^{\top}w_{out}$$
其中$\sigma(\cdot)$与$\psi(\cdot)$分别为softmax与实例归一化，$w_{out}\in \mathbb{R}^{2C\times C}$
* 与传统的自注意力机制相反，通道智能的注意力可以捕捉通道之间的长期依赖关系。
* 为了进一步细化未标注数据的隐藏特征，还应用了一个通道智能的自注意。
	* 细化后的无标注特征为$\hat{h}^u_i$
* 重建的$\hat{h}^l_i$与$\hat{h}^u_i$被输入解码器，生成预测

### 3.3 用于扩大AllSpark特征空间的语义存储Semantic Memory
在单个小batch中直接利用无标注特征并不足以有效地重建已标注特征。因此，需要拓展无标注特征空间。
* 引入一个先入先出队列，Class-wise Semantic Memory（S-Mem），来存储大量的无标注特征，如图四底部所示。从而允许在重建过程中访问更广阔的无标注特征
	* S-Mem形状为$\mathbb{R}^{K\times C\times d}$，其中K为类别数
* 对每一个类别，S-Mem存储C个通道，每个通道由d个patches组成
* 在训练过程中，利用语义库来替换无标注特征中原本的key和value【即公式中的k和v】
* 3.4中将介绍如何使用包含特定类别语义信息的精确通道来更新每一个类别slot

### 3.4 Channel-wise Semantic Grouping
* 由于类别通常是不平衡的，以简单的方式存储未标注特征并不适用于语义分割任务
* 因此需要构建一个**类平衡**的语义记忆库，从而确保每个类别都有足够的语义信息
本文引入了一种基于通道的语义分组策略，来确定未标注特征中每个通道的语义特征，然后将其分组并添加到S-Mem对应类别的slot中，如图4所示
* 具体来讲，计算无标注特征$h^u\in \mathbb{R}^{C\times d}$与概率token $\hat{p} \in \mathbb{R}^{K\times d}$的相似性。
* 概率token是从概率图中resize并reshape为向量得到的
	* 概率图为语义网络中得到的soft预测，包含了整个$h^u$的语义信息
* 一旦每个通道的语义特征已经确定，就可以根据它们各自的语义类别存储在记忆库中
* 通过比较每个通道的语义信息和整个图像的语义信息，就可以确定该通道最有可能的语义类别
* 然后将表示相同语义类别的通道分组在一起，并将他们排入语义记忆库相应的类别slot中

**在推理阶段**，虽然也可以用S-Mem的交叉注意力机制，但计算负担较大，且性能只有微小的提升。因此为提高效率，在推理阶段选择删除S-Mem和CSG。因此，交叉注意力的两个输入变得相同，可以简化为自注意力




## 四、实现细节


## 五、实验结果


## 六、结论

