DENOISING DIFFUSION IMPLICIT MODELS
发表于：2022


## 摘要：
* Denoising diffusion probabilistic models(DDPMs)去噪扩散概率模型无须对抗训练就能生成高质量图片，但是需要为非常多的steps计算一个Markov链来产生一个sample
* 为加速sampling采样，本文提出denoising diffusion **implicit** models (DDIMs)去噪扩散隐式模型
	* 更有效率的迭代隐式概率模型
	* 与DDPMs训练过程相同
* 在DDPMs中，生成过程被定义为一个特定Markovian扩散过程的反演
	* 作者通过**非马尔可夫**（non-Markovian）扩散过程推广DDPMs，从而得到与训练图像相同的目标
	* These non-Markovian processes can correspond to generative processes that are deterministic, giving rise to implicit models that **produce high quality samples much faster**
	* 
【即，如果有一个已经训练好的DDPM模型，用DDIM的采样方法能够加速推理。其实并没有改变DDPM的训练过程】
* 是一个确定的过程，因此多样性不如DDPM



## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 扩散模型与非马尔可夫推理模型的对比
	* ![[Pasted image 20240113184100.png]]
	* DDPM是逐个预测噪声的过程，链式结构，因此无法并行加速
	* DDIM同时使用$x_{t-1}$与$x_0$的信息来产生$x_t$的正向噪声

## 一、引言 Introduction
深度生成模型（Deep generative models）已经证明了在许多领域产生高质量样本的能力。在图像生成领域，GANs比基于可能性的模型（例如VAE，自回归模型，normalizing flows等）更能产生高质量图像。然而，为了稳定训练，GANs在优化和架构方面需要非常具体的选择，并且可能无法涵盖数据分布模式。【GANs存在迁移性不好的缺陷】
迭代生成模型，例如DDPM、NCSN，已经能够在不进行对抗训练的情况下产生与GAN相当的样本。
* 需要训练去噪自编码器模型来对不同水平的高斯噪声去噪
* 由一个马尔可夫链产生样本，再从噪声图像逐渐去噪为一个图像
* 缺点：需要多次迭代来产生高质量的样本，生成过程太慢
	* 对于DDPM，这是因为去噪过程近似于正向过程，而这可能有上千步，需要迭代所有步骤才能生成一个样本。这比GAN要慢得多，因为它只需要通过一次网络
	* 例如，DDPM需要20个小时左右才能采样出50k张32\*32大小的图像，而GAN只需要不到一分钟。如果需要生成更大的图像，比如256\*256大小，同样的硬件需要甚至1000小时
* 因此作者提出DDIM，一种隐式概率模型。
	* 与DDPM训练中使用的目标函数相同
	* DDPM使用的前向扩散过程是马尔可夫的，而对于非马尔科夫的过程，作者设计了一个合适的反向生成马尔可夫链
	* 

## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

