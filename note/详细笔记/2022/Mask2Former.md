
收录于：CVPR2022
Masked-attention Mask Transformer for Universal Image Segmentation
[code](https://github.com/facebookresearch/Mask2Former)

## 摘要：
* 提出Masked-attention Mask Transformer(Mask2Former)
	* 可以处理任何图像分割任务（全景、实例、语义分割）
	* 核心组成部分是masked-attenntion：通过将交叉注意力约束在预测的掩码区域来提取局部特征
	* 不仅减少了至少三次研究工作，还在四个流行数据集上超过了专门的架构，均达到了SOTA的成果


## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 结构图
	* ![[Pasted image 20231122102044.png|450]]
	* 采用与MaskFormer相同的结构，由一个backbone，一个pixel decoder，一个Transformer decoder组成。
		* Transformer decoder做了改造
			* 用masked attention来替代原本的cross attention
			* 用pixel decoder中不同大小的特征图来分别输入Transformer decoder中的块，以此来更好的解决小物体问题
			* 交换了cross attetntion（masked attention）与self attention的位置，让query可学习，并移除了dropout以使得计算更加高效
			* 图中省略了位置嵌入与每一层的预测

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method

### 3.1 Mask classification preliminaries
基于[[Maskformer]]，介绍Maskformer的主要结构：
* backbone：提取低分辨率特征
* pixel decoder：上采样低分辨率特征，来产生高分辨率 per-pixel embeddings
* Transformer decoder：用图像特征来产生object queries
最后获得

### 3.2 Transformer decoder with masked attention
基于Maskformer相同的架构，但提出新的Transformer decoder替换原本的标准Transformer decoder部分
* 关键部分是 masked attention操作
	* 限制交叉注意力的范围，将其约束在每个query预测的mask中





## 四、实现细节


## 五、实验结果


## 六、结论

