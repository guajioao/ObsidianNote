DIFFUSION MODELS ALREADY HAVE A SEMANTIC LATENT SPACE
收录于：ICLR2023


## 摘要：
扩散模型在很多领域表现出色，但是缺乏semantic latent space。这个与语义潜在空间对于控制生成过程是至关重要的
* 本文提出asymmetric reverse process（Asyrp）不对称反向过程，在冻结的预训练扩散模型中发现了语义潜在空间，作者将其命名为h-space。
	* h-space具有很好的属性：同质性，线性，鲁棒性和连贯性，使其能够适用于图像的语义操作：
* 针对通用编辑（versatile editing）和提高质量引入了一个产生处理的原则设计的量化措施
	* 时间间隔的编辑强度(:editing strength)与一个时间步长的质量缺陷(quality deficiency)
* 




## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、背景BACKGROUND]]
* [[#三、发现扩散模型中的语义潜在空间]]
* [[#四、生成过程设计]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 结构图
	* ![[Pasted image 20240110193245.png]]
	* 经过编码器后的$h$在输入解码器之前先进行$f_t$的处理并以$\Delta h_t$为参数加回到原来的$h$上
	* 未经处理的$h$和经过处理的$h'$都输入到解码器中，在第$x_{t-1}$步时用h解码得到的$\epsilon_t$，用$h'$解码得到$\hat{\epsilon_t}$
		* $\epsilon_t$经过【？】得到$P_t(\epsilon_t)$与$D_t$，
		* $\hat{\epsilon_t}$得到$P_t(\hat{\epsilon_t})$
	* 下一个时间的输入$x_{t-1} =D_t +P_t(\hat{\epsilon_t})$
	* 不断重复上述步骤
Q：smileing等控制是如何来的，在哪一步加入了什么？

## 一、引言 Introduction
* 扩散模型在图像生成上效果很好，且由于它是能够完美地生成原图像的，因此是适用于图像编辑的
	* 然而，直接编辑潜在变量(即中间噪声图像)并不能达到这一目的。相反，它需要复杂的过程：
	* 在反向过程中提供指导或属性微调模型
* 下图简单展示了现有的方法：
	* ![[Pasted image 20240110194915.png]]
	* **图像引导**是通过将指导图像的潜在变量与无限制的潜在变量混合
		* 虽然提供了一些控制，但是对于guide图片中哪些属性需要表达在目标图像中是不确定的
		* 对于变化的幅度缺乏直观的控制
	* **分类器指导**通过在反向过程中对潜在变量施加分类器的梯度来匹配目标类别
		* 需要为潜在变量（比如噪声图像）训练一个额外的分类器
		* 在采样过程通过分类器计算梯度是昂贵的
	* 微调整个模型可以控制结果向目标属性改变且没有上述问题，但仍需要对每一个描述训练一个模型
* GAN在他们的潜在空间中提供了直接的图像编辑
	* 对于给定图像的潜在向量，让其最大化的贴近目标描述的CLIP向量
	* 然而，给定一张真实图像，如何找到它确切的潜在向量往往非常具有挑战性，并会导致意想不到的外观变化
* 如果近乎能够完美反推出原图的扩散模型也具有这样的语义潜在空间，那么他将能实现出色的图像编辑
	* Preechakul等人在2022的[[Toward a meaningful and decodable representation|一篇文章]]中提出一个方法：在反向扩散过程中引入一个额外的输入：由另一个编码器得到的原始图像的潜在向量
本文中作者提出Asyrp，在冻结的扩散模型中找到了这个语义潜在空间，这样就可以在这个空间中编辑原图的特定属性
作者将找到的这个语义潜在空间命名为h-space，

## 二、背景BACKGROUND
### 2.1 DDPM
* 【公式1】从$x_{t-1}$生成$x_t$的公式，正向加噪
	* ![[Pasted image 20240110205524.png]]
* 【公式2】从$x_t$生成$x_{t-1}$的公式，反向去噪
	* ![[Pasted image 20240110205504.png]]
	* 
### 2.2 DDIM
* 将公式1修改为：
	* ![[Pasted image 20240110205740.png]]
	* 将原图加入到去噪过程中
	* 因此反向过程就变为了：
		* ![[Pasted image 20240110205901.png|775]]
		* 推理的$x_0$+$x_t$的方向指向+随机噪声
		* 其中，![[Pasted image 20240110210107.png]]
		* 若每个时刻$\eta=1$，就是DDPM。
		* 若$\eta=0$，这个过程就是确定的，是几乎完美的反向推演
### 2.3 用CLIP进行的图像操控
与直接最小化编辑图像与目标描述之间的余弦距离【直接对比图像特征与文本特征】相比，用余弦距离的方向损失实现的同质编辑不会出现mode collapse【只比较方向更好】
![[Pasted image 20240110210711.png]]
$\Delta T$是target与source之间文本特征的方向差值
$\Delta I$是target与source之间图像特征的方向差值
$x^{edit}$是edited图像
$y^{target}$是目标描述
$x^{source}$是来源(source)图像
$y^{source}$是原(source)描述



## 三、发现扩散模型中的语义潜在空间
DISCOVERING SEMANTIC LATENT SPACE IN DIFFUSION MODELS
* 本文中这个新的可控反向过程将公式3重新表示为：
	* ![[Pasted image 20240110211240.png]]
	* 其中$P_t(\epsilon_t^{\theta}(x_t))$代表预测的$x_0$，
	* $D_t(\epsilon_t^{\theta}(x_t))$表示$x_t$的direction pointing方向
	* 并进一步用$P_t$和$D_t$简短表示
		* $\epsilon_t$经过【？】得到$P_t(\epsilon_t)$与$D_t$，
		* $\hat{\epsilon_t}$得到$P_t(\hat{\epsilon_t})$
### 3.1 问题


### 3.2 ASYMMETRIC REVERSE PROCESS（Asyrp）
* 本文提出的的不对称反向过程公式表示为【公式5】：
	* ![[Pasted image 20240110211814.png]]
	* 只修改了$P_t$，将 $\epsilon_t$换成了$\hat{\epsilon_t}$，保留了$D_t$
* 直观地说，它根据$\Delta\epsilon_t= \hat{\epsilon_t} - \epsilon_t$修改了反向过程，同时没有改变指向$x_t$的方向$D_t$，因此$x_{t-1}$在每个采样步骤中遵循original flow Dt【一定程度上这个$D_t$还是有变化的吧？毕竟是会加上$P_t$后经过一系列decoder输出的】
* 使用修改后的$P_t^{edit}$和原本的$P_t^{source}$作为[[#2.3 用CLIP进行的图像操控]]中的视觉输入，并regularize二者之间的不同
* 作者发现$\Delta\epsilon_t=arg min_{\Delta\epsilon_t}\mathbb{E}_t\mathcal{L}^{(t)}$这一计算方法，缺乏之前描述的四个必要的属性
	* 其中【公式7】![[Pasted image 20240110213222.png]]
### 3.3 h-space
在所有SOTA扩散模型中$\epsilon_t$是用U-Net实现的。
作者选择它的bottlenect瓶颈，即最深的特征图$h_t$。根据设计， $h_t$比$\epsilon_t$具有更小的空间分辨率和更高级的语义
* 因此，采样公式就修改为【公式8】：
	* ![[Pasted image 20240110214459.png]]
	* 其中$\epsilon_t^{\theta}(x_t|\Delta h_t)$将$\Delta h_t$加入到原本的$h_t$中
	* $\Delta h_t$最小化公式7中的损失，但用$P_t(\epsilon_t^{\theta}(x_t|\Delta h))$代替了$P_t(\hat{\epsilon}_t^{\theta}(x_t|\Delta h))$

### 3.4 IMPLICIT NEURAL DIRECTIONS
即使$\Delta h$能够成功操控图像，直接在多个时间步长上优化$\Delta h_t$需要很多训练轮次，且需要很小心的选择学习率和它的scheduling。
因此作者定义了隐函数（implicit function）$f_t(h_t)$，这个函数对于给定的$h_t$和$t$能够直接产生$\Delta h_t$。
* $f_t$用一个很小的卷积网络来实现
	* 只有两个$1\times1$卷积连接时间步长t
* 优化与公式7中相同的损失，其中$P^{edit}_t = P_t(\epsilon_t^{\theta}(x_t|f_t))$
* 学习$f_t$对学习率的设置更佳鲁棒，并且比学习每一个$\Delta h_t$要收敛更快
* 此外，由于$f_t$学习了一个给定时间步长和瓶颈特征的隐函数，他**能够推广到不可见**的时间步长和瓶颈特征
* 【\*】
* 在一个$[1,T]$的子序列$[1,S]$上定义的子序列$\{x_{\tau_i}\}_{\forall i\in [1,S]}$训练

* 因此，我们可以在生成过程的任何子序列上训练$f_t$。


## 四、生成过程设计 
GENERATIVE PROCESS DESIGN
描述了整个编辑过程，包括三个阶段：Asyrp编辑、传统的去噪和质量提高.
我们设计了公式来通过可量化的措施确定每个阶段（phase）的长度

### 4.1 Asyrp编辑过程
* 【根据另一篇论文】扩散模型在早期产生高水平的背景，在后期产生细节
	* 因此，需要在早期修改产生过程来达成语义的改变
	* 将早期阶段称为editing interval $[T, t_{edit}]$
* $LPIPS（x，P_T）$和$LPIPS（x，P_t）$分别计算时间步长T和t下，原始图像与预测图像之间的感知距离（perceptual distance）
* 直观地说，high-level内容已经由predicted terms决定了，LPIPS衡量的是在剩余反向过程中剩下的待编辑内容。【总之就是LPIPS衡量的是后期的细节？】
* 定义了一个时间间隔$[T,t]$的编辑强度
	* $\xi_t=LPIPS(x,P_T)-LPIPS(x,P_t)$
	* 表示在原本产生过程中时间T到t的perceptual change感知变化
* 时间间隔越短，编辑强度$\xi_t$越小。而更长的间隔一般来说会给图片带来更有辩识力的改变
* 实验找到了有足够编辑强度的最短编辑间隔0.33
* 一些属性需要更多的视觉变化，比如pixar > smile【整体风格的变化>人物情绪的变化】。对于这样的属性，需要根据下列公式提高编辑强度
	* ![[Pasted image 20240111143241.png]]
	* $E_T(\cdot)$产生CLIP文本embedding【即文本特征提取器】
	* $y(\cdot)$代表描述文本
	* $d(\cdot,\cdot)$计算余弦距离
### 4.2 利用随机噪声注入技术提高质量
QUALITY BOOSTING WITH STOCHASTIC NOISE INJECTION
DDIM通过去除随机性实现了近乎完美的反演，但是2020年的[[Training generative adversarial networks with limited data|一篇文章]]证明随机性(stochasticity)能够提高质量。因此，作者在boosting interval提高间隔中注入了随机噪声$[t_{boost},0]$
* 增长时间间隔会获得更高的质，但是过长会导致内容改变
* 因此需要找到足够提高质量的最小间隔，使得内容尽量不要变化
* 作者提高质量的能力与图像噪声有关，并定义了t时刻的quality deficiency：
	* $\gamma_t = LPIPS(x,x_t)$
	* 表示$x_t$中与原始图像相比的噪声量。
	* 这里用$x$与$x_t$是因为考虑的是实际的图像而非语义信息
* 实验找到了能够让质量提升的最小内容变化



## 五、实验结果


## 六、结论
* 提出一个新的生成过程，Asyrp，促进在扩散模型语义潜在空间h-space上的图像编辑
* 像GANs的潜在空间一样，h-space有很好的属性：homogeneity（同质性）, linearity（线性）, robustness（鲁棒性）, and consistency across timesteps（时间步长上的连贯性）
* 整个编辑处理的设计目的是为了通过在时间步长上测量编辑强度和质量缺陷，实现通用和高质量的编辑。
* 作者希望他们的方法和详细的分析能够帮助产生一种新的图像编辑范式来应用于扩散模型的语义潜在空间中
	* 结合此前的微调或指导技巧或许是一个有趣的研究方向
