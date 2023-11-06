# Side Adapter Network for Open-Vocabulary Semantic Segmentation
收录于：CVPR23

# 摘要：
* 提出Side Adapter Network(SAN)，一个使用预训练视觉-语言模型来完成开放词汇语义分割任务的架构
* 将语义分割任务建模为一个**区域识别**任务
* side network在一个**冻结的CLIP模型**后面连接两个分支：
	* 一个用于预测**掩码proposals**
	* 另一个用于预测CLIP模型识别类掩码的**注意力偏移**
* 网络进行**端到端训练**
	* 使得侧网适应冻结的CLIP模型，因此预测的到的proposals具有CLIP的感知能力(CLIP-aware)
* 本方法比其他方法训练参数减少了18倍，推理速度更快提高了19倍

# 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]
* [[#Question|问题]]

## 结构
* ![[Pasted image 20231008144145.png]]
	* 红色虚线是训练过程中的梯度流,
	* SAN两个分支：mask proposals，attention bias。这样的解耦设计提高了分割性能，因为CLIP用于识别mask的区域和mask区域本身
	* 将浅层CLIP块的特征融合到SAN中，更深的块与attention bias结合
* SAN的结构![[Pasted image 20231008195713.png]]
	* 与ViT相似，都是将图像分成patch然后线性投影成visual token。与N个可学习的query token连起来后输入Transformer
	* 输出：mask proposals与相应的attention biases，attention bias用于掩膜识别
	* 在生成mask时
		* 公式： ![[Pasted image 20231008201016.png]]$M = V_{mask}Q_{mask}^T$
		* $Q_{mask} \in \mathbb{R}^{N \times 256}$ 为**query tokens**经过三层MLP(多层感知机)得到，$v_{mask} \in \mathbb{R}^{\frac{H}{16} \times \frac{W}{16} \times N}$ 为**visual tokens**经过三层MLP得到，H和W是输入图像的高和宽，得到的 $M \in \mathbb{R}^{\frac{H}{16} \times \frac{W}{16} \times N}$
	* 在生成attention bias时
		* 公式： $B = V_{attn}Q_{attn}^T$
		* $Q_{attn} \in \mathbb{R}^{N \times 256}$ 也为**query tokens**经过三层MLP得到，$V_{attn} \in \mathbb{R}^{\frac{H}{16} \times \frac{W}{16} \times K \times 256}$ 为**visual tokens**经过三层MLP得到，K是ViT CLIP模型的注意力头个数，得到的 $B \in \mathbb{R}^{\frac{H}{16} \times \frac{W}{16} \times K \times 256}$
		* 实际上$Q_{mask}$和$Q_{attn}$可以共享
		* **attention bias用于CLIP的多个自注意力层** [[#^c1f508|问题1]]
	* visual token的特征融合：
		* ViT由visual token和【CLS】token组成，但SAN只融合了visual token
		* ---融合特征的具体操作
		* 将CLIP的{stem, 3, 6 , 9}层与SAN的{stem, 1, 2, 3}层融合
	* 结合attention bias进行mask recognition：
		* 示意图：
			* ![[Pasted image 20231014204654.png]]
		* CLIP只能通过【CLS】token来进行图像级识别，该工作的思路是通过【CLS】token在感兴趣区域的attention map来指导准确的mask识别。
		* 创建一组【SLS】tokens，被视觉token单向更新，不影响视觉token和【CLS】token。
		* SLS更新公式：![[Pasted image 20231008203657.png]]
			* $B_k \in R^{\frac{H}{16}\times \frac{W}{16} \times N}$为第L层第k个头的注意力偏移attention bias
			* ![[Pasted image 20231008204155.png]]，
			* ![[Pasted image 20231008204208.png]]![[Pasted image 20231008204215.png]]，
			*  ![[Pasted image 20231008204312.png]]
			* 来自代码：$X \in R^{K*N*C}$ 
		* **因为加入了注意力偏移Bk，SLS的特征逐渐演变为适合mask预测**。【Prompt？】
			* ![[Pasted image 20231016220019.png]]
			* 注意力与Masks来自同一个Query token，所以有着对应关系
	* 通过比较【SLS】token【尺寸为1xN】和CLIP文本embedding【尺寸为1xC】之间的距离/相似性，获得mask的类预测，计为 $P \in \mathbb{R}^{C \times N}$，C是类别数。
	* 利用M和P可以计算出分割图$S = M \times P^T$。$S \in \mathbb{R}^{\frac{H}{16} \times \frac{W}{16} \times C}$，即语义分割的标准输出
	* 损失函数：
		* mask生成：dice loss$L_{mask\_dice}$ 和二元交叉熵损失BCE $L_{mask\_bce}$
		* mask识别：交叉熵损失 $L_{cls}$
		* 总损失：$$L_{seg} = \lambda_1L_{mask\_dice} + \lambda_2L_{mask\_bce} + \lambda_3L_{cls}$$，$\lambda_1, \lambda_2, \lambda_3$分别为为5.0,5.0,2.0

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论


## Question:
attention bias与CLIP层到底做了什么操作？ ^c1f508