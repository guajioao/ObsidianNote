
发表于：

## 结构
* 结构图
	* 潜在透明图的编码解码器训练
		* ![[Pasted image 20240304214600.png]]
	* 使用潜在透明图的扩散模型训练
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

定义：$I_t \in R^{h*w*4}$为RGBA图片，前三个RGB颜色通道定义为$I_c \in R^{h*w*3}$，Alpha通道图片定义为$I_{\alpha} \in R^{h*w*3}$
作者将$I_c$称为“padded RGB图片”，$I_t$可以被转化为"premultiplied image"，即$I = I_c*I_{\alpha}$ ，其中$*$代表像素乘法
* RGB值的值域为$[-1,1]$,alpha值域为$[0,1]$
### 3.1 Latent Transparency
训练编码解码器$\varepsilon$与$\mathcal{D}$，希望让$\varepsilon$提取出的$x_{\epsilon}$加入扩散模型编码器提取出的$x$得到$x_a$后对扩散模型生成图像的质量影响尽可能降低，同时希望$\mathcal{D}$能够从$x_a$中尽可能的还原出原本的RGB图像和Alpha图像:
* 四通道图片$I_t$先被分为$I_c$和$I_{\alpha}$，$I_c$和$I_{\alpha}$都作为编码器$\varepsilon$的输入,提取得到潜在透明度Latent Transparency $x_{\epsilon}=\varepsilon(I_c,I_{\alpha})$
* $I_t = I_c*I_{\alpha}$输入冻结参数的sd编码器，提取出特征$x$
* $x$与 $x_{\epsilon}$相加后得到$x_a$，用于SD等LDM的训练或微调
* $x_a$经过SD的解码器得到解码的乘积图$\hat{I}$
* $\hat{I}$经过编码解码器$\mathcal{D}$还原为解码的$\hat{I}_{\alpha}$和$\hat{I}_c$，并重建
* 重建后的图像与原图计算损失，训练$\varepsilon$与$\mathcal{D}$ 
	* 评价偏移量$x_{\epsilon}$的有害程度
		* 公式一：
		* ![[Pasted image 20240304210836.png]]
	* 评价重建的效果
		* ![[Pasted image 20240304211513.png]]
	* 此外，实验发现引入PatchGAN discriminator loss可以进一步提高结果的质量
		* ![[Pasted image 20240304211624.png]]
		* 其中$\mathbb{L}_{disc}(\cdot,\cdot)$是一个来自一个5层patch discriminator的GAN目标；
	* 最终的目标可以写成上述损失的加权和
		* ![[Pasted image 20240304211839.png]]
		* 作者使用$λ_{recon} = 1, λ_{identity} = 1, λ_{disc} = 0.01$ 这一设置
* 经过这样的训练后，调整后的latent $x_a$可以从透明图像中编码得到；反之，这些latent图像可以用于微调SD

总结：将透明图像提取成特征图，通过SD在透明特征图上的微调让SD记住透明特征图的表征，从而使其也能生成其他透明特征图。
SD生成透明特征图之后用预训练好的编码解码器还原成RGB图像和Alpha图像
### 3.2 扩散模型与潜在透明度(latent)
由于预训练的时候约束了透明度特征，其对扩散模型的生成效果影响被尽量的降低，因此可以直接用于SD的微调。
给定调整过的latent $x_a$，扩散模型在$x_a$上进行加噪和去噪的流程，并正常的加入控制条件和计算损失
![[Pasted image 20240304215127.png]]

### 3.3 生成多层图像
将前景的latent记为$x_f$，背景的latent记为$x_b$ 
训练两个LoRA，前景的LoRA参数记为$\theta_f$，背景的LoRA记为$\theta_b$，分别对两个图像进行加噪去噪
在这个过程中，两组模型中的扩散模型参数被冻结，且注意力共享(attention sharing)


### 3.4 数据集准备与训练细节
1. Base Dataset
	* 收集20k高质量透明图像
	* 训练包含潜在透明度的SDXL VAE（即之前的$\varepsilon$）
	* 使用SDXL VAE提取出的，包含潜在透明度的$x_a$训练SDXL扩散模型
	* 重复下述步骤25次：
		* 生成10k随机采样的图像，用LAIONPOP生成随机的prompts
		* 手工挑出1000张采样的图像，加入数据集
			* 新添加的样本在下一轮的训练批次中出现的概率高出2倍
		* 再次训练潜在透明度编码解码器和扩散模型
	* 数据集大小达到了45K
	* 没有人类交互地生成5M sample pairs，



## 四、实现细节


## 五、实验结果


## 六、结论

