Extract Free Dense Labels from CLIP
收录于：ECCV2022
# 摘要：

```
对比语言-图像预训练（CLIP）在开放词汇zero-shot图片识别方面取得了显著突破。很多最近的研究将预训练的CLIP模型用于图像级别的分类和控制（manipulation）。在本文中，我们希望实验CLIP在像素级稠密推理的内在潜力，尤其是在语义分割方面。用最小的修改，也没有注释和微调，MsakCLIP的分割结果非常好。通过加入伪标签和自训练，MaskCLIP+大大超过了SOTA转换zero-shot分割方法。我们还测试了MaskCLIP在输入不好的情况下的鲁棒性，以及评估了他在区分细粒度对象和新概念的能力。我们发现，MaskCLIP可以作为一种新的可靠的监督来源，以实现无注释分割。
```
* 将CLIP用于语义分割->MaskCLIP
* MaskCLIP+伪标签(pseudo labeling)+自训练(self-training) => MaskCLIP+
# 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
### 结构图：

![[MaskCLIP_Overview.png]]
* 图中只有黄色的块需要训练。
* 保持CLIP的预训练权重frozen冻结，尽量不修改
* MaskCLIP+使用MaskCLIP的输出作为伪标签来训练更好的分割网络


## 一、引言 Introduction


## 二、相关工作 Related Work



## 三、方法
### 3.1 CLIP的独特性
使用图片-文本对进行训练，因此能够将图像内容与自然语言联系起来，而自然语言包含了复杂而密集的语义，跨越了多个粒度。
### 3.2 传统的微调方法阻碍了CLIP的Zero-shot
当下训练分割网络的pipeline：
	* 使用ImageNet预训练权值初始化骨干网络
	* 加入分割网络，并随机初始化
	* 联合骨干网络与新增模块在数据集上微调
* 按照这种方式，用CLIP图像编码器来初始化骨干网络，用CLIP文本编码器通过mapper映射到DeepLab的分类器（最后的1x1卷积层），最终分类性能虽然不错，但是失去了CLIP特有的zero-shot能力
* 作者分析可能的原因：
	* 主干网络的架构与图像编码器稍有不同
	* 图像编码器初始化的权重在微调时被更新了
	* 映射使用的mapper，只对特定的类进行了训练，因此泛化性不足
### 3.3 MaskCLIP
图为CLIP中的注意力池化：
![[Pasted image 20231005152840.png]] 
* 左列的Attention Pooling：在这个Transformer式的多头注意力层中，全局平均特征作为query，每个空间位置生成一个key-value对。因此该层输出为输入特征图的空间加权和，后面跟一个线性层F。这一层的输出可以作为整个图像的综合表示，因为每个空间位置计算的**F(v)** 已经包含了丰富的局部语义，可以与CLIP文本嵌入的token很好的对应
* 右列的**Our Adaptation**：作者进行的修改：
	* 移除embedding层中的query和key
	* 将value嵌入改为1x1卷积，也将embedding最后一层的线性层改为1x1卷积
	* v是对每一个位置通过嵌入向量X与Wv计算得出的值，而这里直接改为1x1卷积
* 文本编码器保持不变，每个类的结果embedding用于分类
* 将修改后的模型命名为MaskCLIP，因为其生成像素级的掩码预测
* 问题：为什么不直接使用attention pooling的自注意力结果，而只使用value？
MaskCLIP的好处：
	* 作为一个free分割注释器，为标签有限的分割方法提供监督信号
	* 保留了CLIP的视觉语言联系，因此能够分割自由形式的短语类，例如白色汽车、红色巴士
	* CLIP对于位移和不好的输入也有很强的鲁棒性,而MaskCLIP在一定程度上保持了这种鲁棒性
**Key Smoothing and Prompt Denoising**
->为了进一步提高MaskCLIP的性能，提出的两种细化策略
* CLIP中的key在之前的MaskCLIP中只是简单的被抛弃，此处想办法将其利用
	* key特征可以视为相应patch的描述符，因此相似的patch会产生相似的key
	* 基于上述假设，提出一种平滑预测的策略，即**key smoothing**：![[Pasted image 20231005192013.png]] k_i和pred_i是位于i的key特征和类别置信度预测，∥·∥2 和 cos(·)为L2归一化和余弦相似度
* 当处理多个目标类的时候，一个目标类只占一小块区域，那么其他区域就是干扰项会降低性能
	* 提出了**prompt denoising**，如果目标类在所有位置的置信度都小于阈值t=0.5，那么就不认为存在该目标类，去除具有目标类的提示
### 3.4 MaskCLIP+
虽然MaskCLIP不需要训练，但是这也限制了其结构不能进行过多修改。因此为了能够适应更加先进的、为图像分割任务定制的架构（例如DeepLab与PSPNet），提出**MaskCLIP+**。
* 将MaskCLIP的预测结果视为训练的伪真值标签
* 采用自训练策略，可以使用任意的主干架构（因为MaskCLIP只是作为输入的伪真值使用）
* 结构图如下：![[Pasted image 20231005193257.png]]
	* 使用DeepLabv2作为MaskCLIP+的主干
**MaskCLIP-Guided Learning** ：
* 使用CLIP的预测结果来指导目标网络的训练
	* 将目标网络的分类器替换为MaskCLIP的分类器，以保持开放词汇预测的能力
	* 当需要zero-shot时，使用MaskCLIP来为无标记的像素生成伪标签
	* 与当下最先进的方法相比，在三个标准数据集（PASCAL VOC 2012、PASCAL Context、COCO Stuff）上都有更好的效果，甚至与完全监督的基线相当
* 没有使用目标物体检测和知识蒸馏方法，这些是特征级的指导，而是采用了伪标签的方式来指导训练
	* 因为目标网络是为分割任务定制的，在结构上与CLIP的图像编码器不同。因此通过特征匹配的蒸馏不合适
	* 已有研究表明这种特征级的指导会导致在零样本的情况下可视类和未知类的性能冲突
**Self-Training** : 在经过一定训练迭代之后，MaskCLIP+的性能会优于MaskCLIP。此时令MaskCLIP+替换MaskCLIP，自己生成伪标签。即自训练。

## 四、实现细节
* 数据集。PASCAL VOC 2012、PASCAL Context、COCO Stuff
* 文本嵌入。方法与[[#^0d565b|GU]]等人提出的方法相同。
	* 将提示文本通过85个prompt templates生成对应句子后输入CLIP的编码器再取平均
* 具体细节。
	* 在MMSegmentation码库上实现，并继承了其训练配置
	* 使用ViT时，预训练的位置嵌入采用bicubic interpolation
	* 无注释分割时，采用DeepLabv2-ResNet101为骨干分段，对 PASCAL Context或COCO Stuff进行4k/8k个iterations，进行maskclip引导的学习，且没有使用自训练
	* Zero-shot分割时，选择MMSegmentation提供的最轻量级的训练schedule，即在PASCAL VOC、PASCAL Context或COCO Stuff上进行20k/40k/80k的训练。前1/10次训练迭代采用maskclip引导的学习，其余的采用自我训练
	* 

## 五、实验结果
* 无注释分割的mIoU结果：
![[Pasted image 20231005201740.png]]
* Zero-shot分割的表现
![[Pasted image 20231005202007.png]]
* 效果示例：
![[Pasted image 20231005202757.png]]
## 六、结论
* 本文尝试将CLIP应用在语义分割任务中。传统的微调范式不能从CLIP中获益，但作者发现CLIP的图像编码器已经有直接为分割模型工作的能力。
* 作者将模型命名为MaskedCLIP，不需要重新训练。
* 在MaskCLIP成功的基础上进一步提出MaskCLIP+来适应现有的分割架构。
* 在标准的zero-shot分割数据集上，MaskCLIP+显著提高了SOTA结果。
* 更重要的是，MaskCLIP+可以很容易地用于分割更具挑战性的看不见的类，比如名人和动画角色。



Gu, X., Lin, T.Y., Kuo, W., Cui, Y.: Open-vocabulary object detection via vision and language knowledge distillation. arXiv preprint (2021) ^0d565b

## Question
MaskCLIP到底是如何生成掩码的？