
收录于：ICLR2021
AN IMAGE IS WORTH 16X16 WORDS: TRANSFORMERS FOR IMAGE RECOGNITION AT SCALE


## 摘要：


## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
结构图：![[Pasted image 20231122221309.png]]

## 一、引言 Introduction
在中等大小的数据集（imagenet）上是比不过相同大小的卷积模型的，比如ResNets。并且这也是可以expected的，因为Transformer缺少一些inductive biases


## 二、相关工作 Related Work


## 三、方法 Method
因为标准的Transformer输入为1d的token序列。对于2d的图像，作者将$x\in \mathbb{R}^{H\times W\times C}$的图像reshape为一堆patchs拉直后的序列$x_p\in \mathbb{R}^{N\times (p^2\cdot C)}$，(P,P)是每个patch的分辨率，(H,W)是图像的分辨率，$N=WH/P^2$是patches的数量，也可以作为Transformer的输入序列长度。
* 因为Transforemr使用固定的向量大小D【因为是相同的block叠在一起，且BLOCK不改变输入输出的形状】，所以在patches输入之前要先经过一个线性投影将patchs投影到D维上。作者将这个投影的输出称为**patch embedding**。
* 与BERT的$[class]$ token相似，作者在序列的最前面添加了一个可学习的embedding($z_0^0=x_{class}$),它在Transformer encoder的输出状态($z^0_L$)可以作为图像特征图**y**。
	* 在预训练和微调时，$z^0_L$都连着一个分类头
	* 
* 使用可学习的1d位置embeddings。作者也尝试了2d-aware position embeddings，但并没有明显提升。
* **inductive bias**【一种先验知识】。在卷积中有一些image-specific inductive bias，比如：
	* locality：假设相邻的区域上会有相同的特征
	* translation equivariance平移等变性：f(g(x))=g(f(x)),无论是在卷积之前平移还是在平移之前卷积，结果是不变的
	* 在Transformer里面是没有的，对Transformer来说都需要重新学习，因此必须要大量的数据。
* Hybrid Architecture.可以用特征图来作为flatten与投影的对象，而不是整张图。

## 四、实验


## 五、实验结果


## 六、结论

* 将图像视为一系列patchs，并使用NLP的标准Transformer编码器对其进行处理。
* 这种简单但是可扩展的策略在大型数据集上的预训练效果出奇的好
	* 在很多图像分类数据集上持平甚至超过了SOTA，且训练更加便宜
