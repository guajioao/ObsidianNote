
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
* 为了处理小目标，提出多尺度策略来利用高分辨率的特征图
	* 从像素解码器的特征金字塔，以循环的方式将特征图连续喂输入Transformer解码器的各层里
* 提高性能，而没有引入额外的计算

#### 3.2.1 Masked attention
上下文特征在图像分割中的重要性显而易见，但是，最近的研究认为Transformer-based模型收敛慢是由于交叉注意力层中的全局语义，因为需要许多训练轮次来学习注意物体的周围区域。
* 作者假设局部特征已足以更新query特征，且上下文信息可以通过自注意力来汇集。
* 因此提出masked attention，一个交叉注意力的变体
	* 只在每个query对应推理得到的mask的前景区域做注意力
* 标准的交叉注意力计算$$ X_l=softmax(Q_lK_l^T)V_l+X_{l-1} $$
* 其中，$l$是当前层序号，$X_l\in \mathbb{R}^{N\times C}$指第$l$层的N个C维query特征，且$Q_l=f_Q(X_{l-1})\in \mathbb{R}^{N\times C}$。
	* $X_0$指输入Transformer decoder的query特征。
	* $K_l,V_l\in \mathbb{R}^{H_lW_l\times C}$是分别通过$f_K(\cdot)$和$f_V(\cdot)$变换后的图像特征
	* $H_l,W_l$是图像特征的空间分辨率
	* $f_K(\cdot)$和$f_V(\cdot)$是线性变换
* 作者提出的masked attention将注意力矩阵体征为:$$ X_l = softmax(\mathcal{M}_{l-1}+Q_lK_l^T)V_l+X_{l-1} $$
	* 此外，注意力mask$\mathcal{M}_{l-1}$在(x,y)位置的特征为$$\mathcal{M}_{l-1}=\begin{cases}0  & \text{ if } M_{l-1}(x,y)=1 
		 \\-\infty  & \text{otherwise}\end{cases}$$
		 * 其中，$M_{l-1}\in \{0,1\}^{N\times H_kW_l}$是上一层Transformer decoder layer resize后mask的二元输出(阈值设置为0.5)【？】
		 * 







## 四、实现细节


## 五、实验结果


## 六、结论

