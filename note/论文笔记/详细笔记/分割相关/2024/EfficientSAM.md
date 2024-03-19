EfficientSAM: Leveraged Masked Image Pretraining for Efficient Segment Anything
发表于：CVPR2024

## 结构
* Overview
	* ![[Pasted image 20240319153123.png]]
	* 第一阶段：SAMI(SAM-Leveraged)预训练，通过MAE与SAM的知识蒸馏MAE的得到轻量编码器
		* 对于输入图像，与MAE的步骤一样：
			* 先mask掉部分patches，
			* 使用轻量编码器对没有被遮住的区域提取特征
			* 使用提取的特征与masked token一区通过decoder还原为完整特征图
			* 完整特征图通过线性投影后与原图经过SAM 图像编码器提取的特征做重建损失
		* 最终得到一个轻量级编码器，SAMI中使用的的解码器会被丢弃
	* 第二阶段：EfficientSAM
		* 图像通过之前得到的轻量编码器提取特征，再使用SAM的解码器得到掩码
		* 在SA-1B数据集上微调

## 摘要：


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

