
发表于：

## 结构
* 结构图
	* ![[Pasted image 20240304111123.png]]

## 摘要：
* 提出LayerDiffusion，微调类似SD这样的Latent diffusion models来产生透明图片
* 在1M张透明图像上训练
* 可以实现
	* 前景/背景条件的层生成（foreground/background-conditioned layer generation）
	* joint layer generation
	* 涂层内容的结构控制等


## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]


## 一、引言 Introduction
* 当前缺少开源的高质量透明图像数据库，最大的开源数据集通常小于50K【缺少训练数据】
* 大多数开源图像生成模型，例如SD，都对其潜在空间数据表征很敏感。即使只对其latent distribution进行了很细微的改变，也会导致严重降低推理或微调表现
* 本文提出“潜在透明度”方法，使得大规模预训练LDM能够产生透明图像与多个透明图层

## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

