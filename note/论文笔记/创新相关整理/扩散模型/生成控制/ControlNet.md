Adding Conditional Control to Text-to-Image Diffusion Models

发表于：

## 结构
* 结构图
	* ![[Pasted image 20240302204145.png]]
	* 详细版本
		* ![[Pasted image 20240302204202.png]]
	* 复制encoder；对Condition c使用零初始化卷积(zero conv)；decoder部分使用zero conv代替

## 摘要：
* ControlNet作用：将**空间控制-spatial conditioning controls**加入到大规模预训练文生图扩散模型中
	* 锁定已训练好的扩散模型，重用大规模预训练过的编码层
	* 使用"zero convolutions"，即0初始化的卷积层
		* 参数从零开始逐渐增大，避免噪声对微调的影响
	* 

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
### 3.1 ControlNet
* 冻结原始block的参数，同时clone block到另一个可训练的相同结构(trainable copy)
	* 锁定参数保护了预训练的结果
	* 可训练的copy即使用了预训练模型，又能够处理复杂的输入条件控制
* 这个trainable copy有一个额外的输入，即条件向量 $c$ 
	* c来自于：conditioning图像经过一个tiny network的编码，从一个image-space condition 编码为一个feature space conditioning vector向量
	* $c$ 在输入ControlNet之前先进入1个zero conv，记为$Z_1$，其参数即为$\theta_{z_1}$，且初始化为0
	* 0初始化保证trainable copy在训练的时候不会受到有害噪声影响
* ControlNet的输出为：
	* ![[Pasted image 20240302212858.png]]
	* 由于$\theta_{z_1}$的0初始化，在最开始$y_c = y$
	* 
### 3.3 Training
* 输入图像$z_0$，加噪为$z_t$
* 给定一组条件，包括time step $t$，文本prompts $c_t$，与task-specific的条件$c_f$
* 损失依然是噪声损失

## 四、实现细节


## 五、实验结果


## 六、结论

