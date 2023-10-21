# Open-Vocabulary Semantic Segmentation with Mask-adapted CLIP
收录于：CVPR2023

# 摘要：
* 开放词汇语义分割的目的：根据文本描述将图像分割为语义区域。文本描述在训练过程中可能是不可视的
* 两阶段方法首先生成不可知类的mask proposl，然后利用预训练的视觉语言模型（例如CLIP）来对掩蔽区域分类。性能瓶颈为CLIP模型，因为它在Masked图像上表现不佳
* 为了解决问题，提出方法mask prompt tuning：在一批masked图像区域和相关的文本描述上微调CLIP

# 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 方法示意图：![[Pasted image 20231008214039.png]]
	* 输入为（图像，Mask prompt）和与之对应的文本
	* 右侧为具体的图像编码器，在输入图像时将masked patch替换为可学习的mask prompt再进入Transformer中进行训练

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
### 3.1 两阶段开放词汇表分割方法
* 两阶段方法示意图![[Pasted image 20231008214558.png]]
	* 由一个分割模型和一个CLIP组成
	* 首先利用CLIP的文本嵌入来训练改良后的MaskFormer，从而执行开放词汇分割
	* 使用预训练的分割模型生成不可知类的proposals，并将proposals与相应名词对齐
	* 收集掩码类别对后用提出的mask提示调优来微调CLIP
* ***NxC*****的分支**：MaskFormer并非对每个像素逐个预测，而是预测一组掩码proposals和对应的类别推测，每个proposals都用HxW二进制掩码表示。
	* 按照【40】对MaskFormer进行修改：对每个掩码生成一个C维的proposal embedding，C是CLIP模型的embedding维度。
		* 这一改进允许MaskFormer进行开放词汇分割
		1. 使用CLIP文本编码器为每个类生成K个文本嵌入
		2. 将每个掩码embedding与文本embedding进行比较，并预测是k个类的概率
		3. 此外还附加了一个可学习的embedding来表示“no object”类
		* 这种方式生成的mask proposals并不是严格不知道类别的，因为定义的对象是由训练集中的类而来。例如，如果训练集只包含人作为一个类，那么模型很难自动将一个人分割成脸、手、身体或更精细的部位。如何生成一个通用的和类不可知的模型来生成掩膜是一个重要的课题，但这超出了本文的范围
* ***NxHxW*****的分支**：MaskFormer生成一组掩码提议，其中1和0分别表示前景和背景。对每一个mask，选择一个包含所有前景像素的最小边界框，裁剪出图像，将背景遮住，然后re-size到CLIP的分辨率
* 将上述两个预测**集成**起来，计算出最终的预测
* 使用MaskFormer的fusion模块将这个对mask智能的预测融合到语义分割中

### 3.2 从caption中收集多个mask-类别对
在由masked图像和文本对组成的数据集上对CLIP进行微调。
* 首先，尝试直接用COCO-Stuff数据集中手动标注的分割标签。但是实验表明这样对于171个类过拟合，失去了对不可见类的能力
* 改进，使用图像captions，如"There are apple and orange and teapot"
	* 为此提出一种自标注策略来获取mask-category对，如下图
	* ![[Pasted image 20231009095948.png]]
	* 首先用预训练的Mask-Former来生成masked proposals。同时从对应的图像标题中使用现成的语言解析器来提取所有的名词，作为潜在的类别
	* 使用CLIP计算将掩码proposals最匹配的类
		**这样收集的数据集准确度还是依赖CLIP文本和掩码的准确度？**

### 3.3 掩码提示调优
masked图像中用0像素取代区域原本的像素，会导致很多空区域，这样的空区域称为零tokens。这些tokens并不包含有用的信息，反而会给模型带来**domain distribution shift**（因为这些标记在自然图像中不存在），并导致性能下降
* 解决方式：mask prompt tuning
	* masked图像将被标记为一个tensor![[Pasted image 20231009112613.png]]，Np为patch数、E为token维度。此外还有一个压缩的二进制掩码![[Pasted image 20231009141143.png]]，
	* 引入prompt tokens![[Pasted image 20231009141523.png]]，学来分辨在masked patches中的边界像素
	* 最终公式为![[Pasted image 20231009142203.png]]，⊗表示元素乘法
* 优点：
	* 输入图像有部分被masked
	* 可训练参数量更小
	* CLIP的参数可能不能调整，但mask prompt tuning不需要改变CLIP的权重
	* 单独mask prompt tuning就能会显著提高性能。如果结合全模型微调，能更加提高对开放词汇分割的表现


## 四、实现细节


## 五、实验结果


## 六、结论


## Question
* Q: 解决的是什么问题？
	A: 两阶段模型的性能瓶颈：CLIP在masked图像上性能不佳。即，以某种方式让CLIP对masked图像识别准确率更高。这里作者用了prompt tuning的方式，提出mask prompt tuning
* Q: 每个masked图像被掩盖区域不同，难道对每一个图像都训练一个prompt tuning吗？不是，训练的是Mask prompt矩阵，类似于权值矩阵，但是这个矩阵的patch会在输入patch为blank areas的时候替换掉原来的patch。为什么这样会比原来更好？这个prompt学习的是什么信息？
	A:这个操作是希望fine-tuning the blank areas while keeping te entire clip frozen.因为希望CLIP保持权重不变，那么就fine-tune mask prompt the clip adapted to mask images
作者在youtube上有一个讲这篇论文的视频，他提到这个操作的目的是fine-tuning the blank areas同时保持CLIP权重不变，用微调mask prompt的方式来让CLIP适应mask images。然后我去看了最早提出这个方法的文章Visual Prompt Tuning，这个方法作用我的理解就是，用prompt记录并提示当前数据集跟transformer层预训练的数据不一样的地方。感觉有点像之前另一篇文章的attention bias的作用？
我之前想问为什么这样就能比直接设置成0像素更好，现在我的理解是，这个mask prompt的作用就是训练的时候记录masked区域的特点，然后也是让模型能够知道这些符合masked区域特点的patch没那么重要，不需要考虑？嗯我目前大致是这么理解的


	
* Q: 解决的问题是对什么样的图形？裁剪下来之后的小块，还是直接原本大小图像加上掩膜？
	A:原本的图像中抠出包含目标物体的小图，加上掩膜，背景部分像素被设置为0
* **domain distribution shift**是指什么？
	