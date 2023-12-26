BEIT: BERT PRE-TRAINING OF IMAGE TRANSFORMERS
收录于：ICLR2022


## 摘要：
* 提出自监督视觉特征模型BEiT, **B**idirectional **E**ncoder representation from **I**mage **T**ransformers
* 基于自然语言处理领域的BERT，为vision transformer预训练提出masked image modeling任务
* 每个图像在预训练中有两个视角：image patches和visual tokens
* 随机mask掉一些patch后喂入backbone Transformer
* 预训练的目标是基于错误的image patchs重建原始的视觉token

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、方法 Method]]
* [[#三、实现细节]]
* [[#四、相关工作 Related Work]]
* [[#五、结论]]

## 结构
* Overview
	* ![[Pasted image 20231225145433.png]]
	* 对于输入的图片分别将其打为patchs和使用tokenizer编码为visual token
	* 随机mask掉一些patch后用BEiT编码器还原mask tokens位置的visual tokens
	* 用visual tokens解码得到还原的图片，计算损失
* 最上面一条线路是dVAE，下面是BERT
* 

## 一、引言 Introduction



## 二、方法 Method
### 2.1 Image Representations
1. Image Patch
	* $224\times224$图像分为14x14个16x16大小的patchs
2. Visual Token
	* 与NLP相似，通过"image tokenizer"用连续tokens序列代表图像
	* 将图像$x\in R^{H*W*C}$转换为$z=[z_1,\cdots,z_N]\in V^{h*w}$，其中词汇表$V=\{1,\cdots,\left | V \right | \}$包含离散的令牌索引
	* 通过离散变分自编码器dVAE学习image tokenizer
		* 由tokenizer和decoder组成
		* 直接用了DALL-E(text-to-text)的tokenizer

### 2.2 Backbone : image Transformer
* 输入为一个patches序列$\{x_i^p\}^N_{i=1}$
* patches经过线性投影得到patch embedding:$Ex^p_i$，其中$E\in R^{(P^2C)\times D}$
* 加入特殊token$[S]$和1D可学习位置嵌入$E_{pos}\in R^{N\times D}$
* 输入向量$H_0=[e_{s},Ex_0^p,\cdots,Ex_N^p]+E_{pos}$
* 最后一层编码器输出$H^L=[h^L_{[S]},h^L_1,\cdots,h^L_N]$，其中$h_i^H$是第i个图像patch的vector

### 2.3 Pre-Training BEIT: Masked Image Modeling
提出masked image modeling(MIM)任务。
* 随机Mask约40%的patches
* 用可学习的embedding替换masked patches
* 使用 **block-wise masking**，根据M而非随机选择
	* ![[Pasted image 20231225212511.png|400]]
	* 每次mask一个block的patches，每个block的patch数最小设置为16，随机选择masking block的高宽比(aspect ratio)
	* 不断重复，直到获得足够的masked patches（0.4N）


## 三、实现细节
### 3.1 Image Classification
* 图像分类的top-1 acc
	* ImageNet-1K
		* ![[Pasted image 20231225202807.png]]
* 语义分割
	* ADE20K
		* ![[Pasted image 20231225202832.png]]

### 3.4 自注意力Map的分析
作者发现BEiT的自注意力图可以分离对象，且这一现象即使迁移到其他数据集上也能出现
通过计算qk产生分数图
例：![[Pasted image 20231225202104.png]]

## 四、相关工作 Related Work



## 五、结论
介绍了一个为ViT设计的自监督预训练架构，在下游任务中获得了很好的微调结果，如图像分类和语义分割。
结果表明与BERT相类似的预训练工作能很好的应用于image Transformer
还提出了自动获得语义区域知识的有趣属性【？】，不需要人为标注
希望在将来扩大在数据和模型规模上BEiT的训练规模，并用统一的架构进行多模态预训练