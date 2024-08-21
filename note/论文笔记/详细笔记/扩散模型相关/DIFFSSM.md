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
SSMs是一类用于处理时间序列的架构。这些模型表现的像是一个线性循环神经网络（RNN），通过下列公式将输入的一组标量的输入序列$u_1,\dots,u_L$，处理为输出$y_1,\dots,y_L$。
$$x_k=\bar{A}x_{k-1}+\bar{B}u_k, \quad y_k=\bar{C}x_k$$
其中$\bar{A}\in \mathbb{R}^{N\times N}, \bar{B}\in \mathbb{R}^{N\times 1}, \bar{C}\in \mathbb{R}^{1\times N}$。
* 相比其他结构如Transformers和标准RNNs，这种方法的好处是它的线性结构允许使用**卷积**来实现，而非循环。
	* 具体来说，$y$可以通过在$u$上应用一个FFT(快速傅里叶变换)来生成，产生$O(L\log L)$的复杂度，使其能够应用于一个非常长的序列。处理向量输入时可以堆叠D个不同的SSMs，并应用D个batched FFTs。
* 然而如果仅有线性RNN，并非一个有效的序列模型。过去的观点认为，如果$\bar{A},\bar{B},\bar{C}$是从一个合适的连续时间状态空间模型中获得的，线性RNN方法才能做到稳定而有效。
* 因此，作者学习了一个连续时间SSM参数$A,B,C$以及一个离散化比率$\Delta$，用于产生必要的离散时间参数
	* 这种转换原本实现起来非常困难，但最近有研究通过引入简化的对角化版本的SSM神经网络，通过连续时间参数的简单近似实现了类似的结果。
	* 作者选择了其中之一，S4D，作为骨干模型
与标准RNNs一样，SSM可以通过连接两个SSM层的输出并输入MLP层来产生一个$L \times 2D$ 输出，从而实现bidirectional双向性？。此外，过去的工作表明这一层可以与乘法门控相结合，以产生一个改进的双向SSM层，来作为编码器的一部分。这是本文结构的动机。

### 3.2 DIFFUSSM Block
DiffuSSM的核心部分是一个门控双向SSM，旨在优化长序列的处理
为提高效率，在MLP层中加入了沙漏化结构，以减少MLP中的序列长度。
每一个沙漏结构收到的都是一个缩短、展平的输入序列$I \in \mathbb{R}^{J\times D}$ ，其中$M = L/J$是下采样与上采样比例
同时，整个DIFFUSSM块又是在原始长度上计算的，从而完全利用全局上下文信息。

## 四、实现细节


## 五、实验结果


## 六、结论

