Masked Autoencoders Are Scalable Vision Learners
收录于：CVPR2022/2021提交到arxiv

* scalable：可以做得很大
	efficient：可以很快
* Auto：x和y都来自图像

## 摘要：
* 随机的盖住图片里的一些块，用其他块预测这个块里的所有像素
	* 不对称的编码-解码器结构：
		* 编码器仅作用于未被遮盖的patchs
		* 解码器，轻量级的解码器，用于重建原图
	* 对输入图像遮盖很大比例（75%）对自监督任务很有用
* 基于上述两点使得能够高效并快速地训练大规模的模型
	* 提高了3倍的训练速度，也提高了准确度
* 通过MAE使得大模型能够用更少的数据训练
	* 普通的ViT可以只用imagenet-1k数据集就能达到87.8%的准确度
* 迁移到下游任务后表现甚至超过监督学习预训练模型

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* MAE结构图
	* ![[Pasted image 20231219145247.png]]
	* 在预训练过程中大量的随机patchs（75%）被遮盖掉
	* encoder只输入没被盖掉的图像，以减小计算量
	* 在encoder之后引入mask token，将patchs还原到原本的位置，再用decoder预测出mask token所在位置的所有像素
	* 在预训练之后，解码器被丢弃，只用编码器来进行识别任务

## 一、引言 Introduction
• 视觉和语言的Masked自编码器区别在什么地方？
• 卷积网络在过去十年里占主导地位，要将Mask tokens或位置编码集成到卷积网络中比较困难
• 语言与视觉的信息密度不同。
• 语言是人类产生的，具有高度的语义性。
• 相反，图像是有大量空间冗余的自然信号，因此一个缺失的patch可以从相邻的patch中恢复
• 因此**随机mask非常多的patches**(75%)这一策略在视觉中很有效，可以强迫模型学习语义信息来补全，而不是简单的插值

## 二、相关工作 Related Work


## 三、方法 Method
* MAE是一个简单的自编码器方法，通过给定信号的一部分还原成初始信号
	* 与所有的自编码器一样，包含一个编码器将可观察的信号提取为特征，一个解码器使用提取的特征重构为原始信号
	* 与其他自编码器不同的是，MAE采用了不对称的设计，使得编码器只在部分可见patchs上运作，而轻量级的解码器使用可见patchs和mask tokens重构原始信号
* **Masking**。像ViT一样将图像划分为很多个小patchs，然后随机采样
	* 高masking比的随机采样能够很好的去除冗余性，增加任务的难度，使其不容易从相邻块上直接采样获得
* **MAE encoder**。就是ViT，但是只输入未被mask的patchs。
	* 图像patch通过线性层并加入位置编码来转换为embedding【编码器也加入位置编码，fix还是learnable?】
	* 只处理一个全部patch集合的一个小的子集（约为25%），移除所有mask tokens
	* 全集由轻量级decoder处理
* **MAE decoder**。输入为所有tokens的集合，包括已被编码的visible patches和mask tokens
	* 每一个mask tokens都是一个共享的、可学习的向量，表示一个待推理的消失patch
	* 为所有tokens添加位置embeddings，使得tokens具有在图像上的位置信息
	* 只在训练时使用，在推理时只用编码器来为下游任务提供特征图
		* 因此可以使用比编码器更浅更窄的设计，更加轻量级，减少预训练时间
* **Recostruction target**。通过为每一个masked patch推理像素值来重建输入
	* decoder最后一层是一个线性层，其输出通道为一个patch的像素数量，随后会被reshape为一个重构的图像
	* 损失函数为重构后的图像与原始图像之间的MAE(mean squared error)
		* 与DETR相似，只在masked patches上计算损失
	* 作者还尝试了另一种重构目标，每个mask patch的归一化像素值
		* 即，计算一个patch中所有像素的均值
* Simple implementation
	* 为每个patch生成一个token，然后随机打乱这个令牌列表，并根据mask率随机删去列表的最后一部分。
	* 在经过编码器后向这个编码后的patch列表最后添加mask token列表，然后将它们还原回原来的位置。
	* 在添加位置编码后这个列表就可以作为解码器的输入了

## 四、实现细节


## 五、实验结果
* Imagenet分类
	* ![[Pasted image 20231225153642.png]]
* COCO目标检测
	* ![[Pasted image 20231225153724.png]]
* ADE20K语义分割
	* ![[Pasted image 20231225153759.png]]
* 

## 六、结论

