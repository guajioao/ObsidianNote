论文名：Diffusion Models Without Attention
发表于：CVPR2024

## 结构
* 结构图
	* ![[Pasted image 20240820155107.png]]
	* noisy特征图flatten为序列，输入n个重复的DiffuSSM块中
	* 

## 摘要：
* DDPMs在高分辨率特征上会产生很高的计算开销，当前方法，例如patchifying加快了Unet和Transformer结构中的处理进程，但是以representational能力为代价的【？】
* 提出DIFFUSSM(Diffusion State Space Model)模型，将注意力机制替换为一个更灵活的状态空间骨干
	* 无需全局压缩也能有效解决高分辨率问题，因此在扩散过程中能够保护图像特征的细节
	* 是一个FLOP-efficient架构

## 一、引言 Introduction
DDPMs拓展到高分辨率上时会遇到显著的计算量挑战。
一个主要的瓶颈是在高保真生成时对自注意力的依赖。
* Unet结构下，这一瓶颈来源于Resnet与注意力层的合并。需要多头注意力层
* 在Transformer结构中，注意力是核心成分，因此对于sota的图像合成结果至关重要
* 在这两种结构中，当处理高分辨率图像时注意力的复杂度就令人望而却步
现有高分辨率结构主要是使用patchfying，或多尺度分辨率
* Patchfying创建粗粒度特征图，从而减小计算开销，但这以降低关键高频空间信息和结构完整性为代驾
* 多尺度分辨率能够在降低注意力层的计算。但同时通过下采样会减少空间细节，并会在上采样时引入伪影
DiffuSSM是一个无注意力的duffusion结构，旨在避免高分辨率图像生成过程中的注意力应用问题
* 在扩散过程中使用一个gated state space model (SSM)骨干
基于SSMs的序列模型在先前的工作中已被证明了是一种高效通用的卷积序列模型
* 通过使用这个架构，我们可以通过删除全局patchfication或多尺度层，使SSM核心能够处理更细粒度的图像表示。
为进一步提高效率，DIFFUSSM在计算密集部分使用了一个hourglass沙漏结构。
这两种方法均是针对随着长度增长的复杂度以及在网络的position-wise部分的实际效率。

## 二、相关工作 Related Work
* State space models (SSM)-based architectures\[16–18] have yielded significant advancements over contemporary state-of-the-art methods on the LRA and audio benchmark\[13].
* 此外，Dao等人[6]，Peng等人[41]，Poli等人[44]，Qin等人[45]已经证实了非注意架构在语言建模中获得值得称赞的性能方面的潜力

## 三、方法 Method
### 3.1 SSMs

### 3.2 DIFFUSSM Block
DiffuSSM的核心部分是一个门控双向SSM，只在优化长序列的处理
为提高效率，在MLP层中加入了沙漏化结构，以减少MLP中的序列长度。
每一个沙漏结构收到的都是一个缩短、展平的输入序列$I \in \mathbb{R}^{J\times D}$ ，其中$M = L/J$是下采样与上采样比例
同时，整个DIFFUSSM块又是在原始长度上计算的，从而完全利用全局上下文信息。

## 四、实现细节


## 五、实验结果


## 六、结论

