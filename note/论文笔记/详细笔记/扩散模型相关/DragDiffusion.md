论文名：DragDiffusion: Harnessing Diffusion Models for Interactive Point-based Image Editing
发表于：CVPR2024

## 结构
* Overview，包括三个步骤 ![[Pasted image 20240903105426.png]]
	* (1) 首先，在diffusion上进行identity-preserving微调【直接用输入图像在Unet上进行重建损失微调】
	* (2) 其次，根据用户的拖动指令，对输入图像进行DDIM反演得到的latent进行优化【即$z_t$->$\hat{z_t}$】 ![[Pasted image 20240903110025.png]]
	* (3) 在$\hat{z_t}$上应用Reference-latent-control指导的DDIM去噪【如何指导，使得大部分地方不变化？】

## 摘要：

* 2023年Pan等人提出的DragGAN是一个基于点的交互式图象编辑框架，以像素级精度实现了很好的编辑结果。但它的编辑方式依赖于GANs结构。
* 在本文，作者将该编辑框架扩展到了扩散模型，并提出了一种新的方法DragDiffusion
	* 基于大规模预训练difusion模型，对真实图像和生成图像都有适用性
* 其他基于diffusion的编辑方法大多通过对多个时间step延迟引导，而本文方法仅优化一个时间step的latent，也能实现有效而准确的空间spatial控制
* 这种新颖的设计来自于一个观察到的现象：
	* 在一个特殊的时间step时的UNet特征能提供足够的语义和几何信息，以供基于拖拽的编辑
* 此外还引入了另外两种技术：identity-preserving微调和reference-latent-control，来进一步保持原始图像的特征
* 最后提出了一个具有挑战性的基准数据集，称其为DragBench，第一个用于评估交互式基于点的图像编辑方法性能的数据集




## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method

### 3.2 Identity-preserving Fine-tuning
在编辑图像前先使用lora微调扩散模型的unet，只需微调80步就足够了。在A100上需要25秒

### 3.3 Diffusion Latent Optimization
根据用户指令，并选择一个可编辑区域掩码

## 四、实现细节


## 五、实验结果


## 六、结论

