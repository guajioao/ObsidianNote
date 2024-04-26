#自监督学习 #掩码学习

发表于：CVPR2023
MAGE: MAsked Generative Encoder to Unify Representation Learning and Image Synthesis
# 总结
将生成模型提取出的特征用于掩码学习

## 结构
* Framework
	* ![[Pasted image 20240426101823.png]]
	* 使用VQGAN 将输入图像编码为一系列语义tokens
	* 采样一个mask比率，随机mask掉一些tokens
	* 将其他没被mask掉的tokens输入编码器提取特征，解码器解码得到的特征与未被mask的完整tokens计算交叉熵损失
	* 【optional】【类似SimCLR】在对Encoder输出进行全局平均池化后增加一个两层的MLP，对其输出计算对比损失
		* 正样本对为同一个样本的不同视角（不同的图像增强）
		* 负样本对为同一个batch的其他样本

## 摘要：
* 生成式建模与表征学习一般是被分别训练的，忽略了潜在的一般关系
* 提出Masked Generative Encoder，第一个统一SOTA图像生成与自监督表征学习的框架
	* 在输入输出时使用语义tokens，这个tokens是在向量量化(vector-quantized)的GAN上学习到的
	* 语义tokens与掩码结合
	* 在编码器的输出中增加一个对比损失，提高表现
	* 

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

