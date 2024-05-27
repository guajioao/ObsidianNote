Null-text Inversion for Editing Real Images using Guided Diffusion Models

发表于：CVPR2023

## 结构
* NULL-text Inversion overview
	* ![[Pasted image 20240527200835.png]]
	* 输入一张真实图像，使用DDIM反演每一步都会有一点微小的错误。如果没有condition控制条件，这样的累积误差是可以忽略不计的，因此DDIM能够反演成功
	* 但是Stable Diffusion需要使用无分类器引导，且w需要大于1。在这种情况下进行DDIM反演过程不仅会产生视觉伪影，得到的噪声向量还可能脱离高斯分布。因此最终反演得到的图像与原图会有偏差
		* 当噪声向量脱离高斯分布会降低可编辑性【因为现有方法都是基于去噪的，而去噪方法预测的都是高斯噪声】
	* 因此DDIM反演只能提供一个粗略的原始图像近似，但并不准确。称初始的DIM反演轨迹为pivot trajectory支点轨道
	* 围绕支点轨道优化。
		* 在实践中，我们按照扩散过程的顺序对每个时间戳t分别进行优化，使其尽可能接近initial trajectory【即最上面那条直线,$z_T^*,\cdots,z_0^*$】
		* 计算 $min||z_{t-1}^*-z_{t-1}||^2_2$ 
		* 因为DDIM的反演过程提供了一个很好的起点，因此这种优化相比使用随机向量是高效的
	* 不随机初始化一个噪声直接反演到图像，而是来优化一个关键的噪声向量
* 【idea】
	* 作者优化了一个null embedding来优化反演原图
	* 那么是不是也可以学习一个learnable prompt，像下图一样除了class以外的embedding都由模型来学。这样比自己设计prompt更符合描述
		* ![[Pasted image 20240527212430.png]]

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
### 3.1 Background
* 输入一张真实图像，使用DDIM反演每一步都会有一点微小的错误。如果没有condition控制条件，这样的累积误差是可以忽略不计的，因此DDIM能够反演成功
* 但是Stable Diffusion需要使用无分类器引导，且w需要大于1。在这种情况下进行DDIM反演过程不仅会产生视觉伪影，得到的噪声向量还可能脱离高斯分布。因此最终反演得到的图像与原图会有偏差
	* 当噪声向量脱离高斯分布会降低可编辑性【因为现有方法都是基于去噪的，而去噪方法预测的都是高斯噪声】
* 因此DDIM反演只能提供一个粗略的原始图像近似，但并不准确。
### 3.2 Pivotal Inversion
* 称初始的DIM反演轨迹为pivot trajectory支点轨道
* 围绕支点轨道优化。
	* 在实践中，我们按照扩散过程的顺序对每个时间戳t分别进行优化，使其尽可能接近initial trajectory【即最上面那条直线, $z_T^*,\cdots,z_0^*$ 】
	* 计算 $min||z_{t-1}^*-z_{t-1}||^2_2$ 
	* 因为DDIM的反演过程提供了一个很好的起点，因此这种优化相比使用随机向量是高效的

### 3.3 Null-text optimization
* 直接对文本embedding优化会导致一个不可解释的表示，因为优化后的标记不一定匹配已存在的单词
* 因此直接prompt-to-prompt的图像编辑会很困难
* 因此利用无分类器引导的特点——预测结果受unconditional prediction的影响很大，因此将默认的nul-text embedding替换为一个优化后的embeding，称其为null-text optimization空文本优化
* 即对每一个输入的图像都优化一个初始化为null-text embedding的Unconditional embedding $\emptyset$ 
* 模型和条件文本embedding均保持不变
* 单个的无条件embedding被称为全局空文本优化，二对每一个时间戳t优化一个null embedding $\emptyset_{t}$ ,用上一步优化好的 $\emptyset_{t+1}$来初始化


## 四、实现细节


## 五、实验结果


## 六、结论

