SimMIM: A Simple Framework for Masked Image Modeling
收录于：CVPR2022


## 摘要：
* 为掩码学习提出一个简单的架构SimMIM
* 研究如何让掩码学习任务学到更好的特征后，让每个组件设计简单又能和好的学习特征
	* 中等大小(如32)的随机mask patch
	* 直接回归预测像素颜色性能上不比复杂设计的patch分类方法差
	* prediction head可以是轻量级的，比如只有一个线性层。不会比更大的头表现更差
	* 使用ViT-B在ImageNet-1K获得了 **83.8%** top-1微调准确度
	* 使用更大的SwinV2-H，达到了87.1%
	* 用该方法解决数据饥饿问题，成功训练3B的模型（SwinV2-G）并SOTA

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* SimMIM
	* ![[Pasted image 20231225154548.png]]
	1. 图片打成patch
	2. mask掉其中一些patch，用learnable向量替代
	3. 编码器提取特征
	4. 预测头回归预测masked patch中所有像素值

## 一、引言 Introduction
NLP领域自监督学习基于masked语言学习任务已经占统治地位，通过大规模无标注数据来学习大规模语言模型，已被证明可以很好的推广到广泛地NLP任务中
CV领域虽然也有利用自监督表征学习方法，但前些年几乎都是对比学习的天下。
掩码学习应用于语言和视觉的领域的方式存在差异。
* 一个不同就是图像存在强烈的***locality***【局部性】，相邻像素具有强相关性，所以该任务可以通过复制相近的像素、而非语义推理完成。问题：可能走捷径，直接插值就能填充了
* 另一个不同是，视觉信号是原始而低维的（***raw and low-level***）的，而文本token是人造的高级概念。这就产生了一个问题：低维信号的预测是否能用于高维视觉识别任务
* 第三个不同是，视觉信号是连续(***continous***)的，而文本token是独立的。问题：基于分类的掩码学习如何很好的用于连续的视觉信号上
最近有一些工作试图通过引入一些特殊设计拟合这些差距。例如将连续的信号转变为color cluster；通过一个附加网络将patch token化；或通过block-wise的mask策略来打破locality。这些设计证明mask学习任务可以很好的转移到下游任务中
本文提出一个简单框架，不需要这些复杂设计。它与视觉信号的本质非常一致，比之前的复杂方法更能学到好的特征。
* 随机遮盖
	* 用vision Transformers实现很简单方便
	* 更大的patch size和更高的masking ratio都能使的从相近像素找到像素值的机会变小【让任务更难，防止模型直接使用插值就能完成任务】
	* 大尺寸patch size（32）有更广的masking ratio选择10%~70%，都能获得好的性能
	* 小尺寸patch（8）需要高于80%以上才能表现的好
	* 这与NLP采用的遮盖比非常不同，其默认使用0.15的遮盖比
	* 作者认为这是因为NLP与CV信息冗余程度不同【图像相邻像素之间非常相似。冗余程度很高】
* 线性层回归原始的像素值
	* 回归任务与视觉信号的连续性质很一致，具有有序性
	* 这一简单任务的表现不弱于使用tokenization、聚类或离散化的定制分类方法
	* 使用极度轻量级的预测头（一个线性层），与较重的预测头具有类似或略好的迁移性能，又能显著提高训练速度
	* 更小的target 分辨率($12^2-96^2$)与最高的$192^2$性能相当
	*  更重的头或更高的分辨率虽然会带来更好的生成能力，但这样的能力并不一定有利于下游任务的微调
* 使用$l_1$损失
* 

## 二、相关工作 Related Work
* Maked image modeling(MIM) ，iGPT/BEiT
* Reconstruction based methods基于重建的方法，
* Image inpainting methods图像生成方法，能够生成更高质量的图片不一定能够在下游任务上具有更强的微调性能
* Compressed sensing压缩感知，这一方法确认了大多数数据都可以被丢弃，而几乎没有感知损失。最近的稀疏推理工作显示，在抛弃大量图像特征后识别精度几乎没有下降。因此本文即使只有10%的输入块也可以通过补全任务的学习获得良好的视觉特征
* 其他自监督学习方法。其他的代理任务：灰度图像着色、拼图游戏、旋转预测、聚类学习等。
	* 虽然与MIM非常不同，但其中一些也遵循了预测不可见部分的思想，例如使用一个或两个颜色通道来预测另一个颜色通道的值。
	* 另一个大部分是对比学习，这是以前的主流。作者希望他们的工作能够推进将掩码学习作为自监督视觉表征学习代理任务饿的研究


## 三、方法 Method
### 3.1 A Masked Image Modeling Framework
SimMIM架构通过掩码图像建模任务学习特征，即mask输入图像信号的一部分然后预测mask区域的原始信号。
由四部分组成：
* **Masking** strategy。该组件用于选择mask区域并实现mask操作。mask后的图像将被作为输入
* **Encoder** architecture。该组件从masked图像中提取特征，然后用于推理masked 区域的原始信号。学得的encoder用于下游任务。
* Prediction **head**。解码得到原始信号【即生成原图】
* Prediction target。定义要预测的信号形式和损失计算方式。信号形式可以是像素值，也可以是原始像素的转换。损失计算可以是交叉熵分类损失，也可以是L1和L2回归损失
### 3.2 Masking Strategy
* 用可学习mask token向量代替每个masked patch
* 尝试mask区域的选择有两个：
* Patch-aligned random masking。即patch要么全被遮住要么全都没被遮住
* Other masking strategies。
1. 盖住中心区域。作者将其修改为随机移动遮盖某一块区域
2. BEiT使用的block-wise遮盖策略
![[Pasted image 20231226151200.png]]

### 3.3 Prediction Head
预测头可以非常轻，只使用一个线性层。
也尝试了较重的头部，如2层MLP, 逆Swin-T和逆Swin-B

### 3.4 Prediction Tartget
Raw pixel value regression原始像素值回归。将小尺寸特征图对应patch位置的特征向量用$1\times1$卷积映射回原始的大小，然后用这个向量负责预测原始像素值。
例如，在32倍下采样的特征图上使用$1\times1$卷积将输出维度改为$3072=32*32*3$，代表$32*32$个像素的RGB值。
即，原图$224*224$，原特征图=$7*7*128$，用$1*1$卷积修改为$7*7*(32*32*3)$
* $L_1$损失计算如下：
	* ![[Pasted image 20231226154132.png]],
	* 其中$\Omega(x_M)$为元素数量

* Other prediction targets。
	* Color Clustering。iGPT的做法
	* Vision tokenization。BEiT的做法
	* Channel-wise bin color discretization。

### 3.5 Evaluation protocols
与BEiT相同，通过在ImageNet-1K上微调后进行图像分类来评估学到的特征的质量。
主要目标是衡量特征在所有下游任务上的表现



## 四、实现细节


## 五、实验结果


## 六、结论

