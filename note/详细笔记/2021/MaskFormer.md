
收录于：NIPS2021
Per-Pixel Classification is Not All You Need for Semantic Segmentation
[code](https://github.com/facebookresearch/MaskFormer)

## 摘要：
* 语义分割被视为逐像素分类问题，实例分割在此基础上被视为mask分类
	* 作者认为，mask分类对于语义分割和实例分割都足够有效
	* 二者可以用同样的模型、损失与训练步骤
* 提出MaskFormer，即在这个思想上提出的mask分类模型
	* 对于每一个类预测一个二元掩码
* 结果SOTA

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* per-pixel vs mask 分类
	* ![[Pasted image 20231121215242.png]]
	* 每一个mask都单独计算mask损失和分类损失
	* 这样成组的进行匹配可以通过[[DETR]]中采用的bipartite matching或者通过fixed matching，即直接使用mask的index（当预测结果个数K与类别个数N相同时:$K=N$）
* Overview
	* ![[Pasted image 20231121220910.png]]
	* 用backbone提取出特征图$F$
	* 两条线：分别计算分类损失与二元掩码损失
		* 分类损失线：
			* F输入Transformer decoder，产生N个per-segment embeddings $Q \in \mathbb{R}^{C_Q \times N}$【queries是N个可学习的embeddings】
				* queries是N个$C_Q \times 1$大小的向量
				* 每一个query在Transformer 解码器中都独立的对$F$进行交叉注意力查询
			* 这个$Q$独立地分别产生N个**类别预测**和N个对应的mask embeddinngs $\varepsilon_{mask}$
		* 二元掩码损失线：
			* F通过pixel decoder产生per-pixel embeddings $\varepsilon_{pixel}$
			* $\varepsilon_{pixel}$与$\varepsilon_{mask}$做点积，后面跟着一个Sigmoid激活，产生N个**二元掩码预测**
	* 对语义分割任务，直接将N个二元损失与他们的类别预测通过一个简单的矩阵乘法combine起来即可
Transformer decoder部分的query用CLIP的文本特征？这部分的目的是产生每个class对应的mask embeddings。 ^9af7dd


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
* 先描述语义分割在逐像素分类和掩码分类下的公式
* 介绍作者提出的掩码分类模型，以及使用的Transformer decoder在其中的作用
* 提出一种简单的将mask分类输出结果转换为其他任务依赖的输出格式
### 3.1 逐像素分类公式
对于一个HxW的图像，总共有K个类别，需要预测图像的每个像素$y=\{p_i|p_i \in \Delta^{K}\}$，其中$\Delta^{K}$是一个K维的概率向量。
训练非常直接，直接用ground truth的类别标签$y^{gt}=\{y^{gt}|y^{gt} \in  \{1,\cdots ,K\}\}^{H\cdot W}_{i=1}$来计算每个像素的交叉熵损失 $\mathcal{L}_{pixel-cls}(y,y^{pt})=\sum^{H\cdot W}_{i=1}-\log p_i(y^{gt}_{i})$

### 3.2 掩码分类公式
将语义分割任务分解为：划分区域获得二元掩码；对掩码进行分类
* 将图像划分/分组为N个区域(N不一定与K相等)，用二元掩码表示$\{m_i|m_i \in [0,1]^{H\times W}\}^N_{i=1}$
* 用在K个类别上的分布将每个区域联系成一个整体
* 对每一个segment进行联合分组和分类，即进行掩码分类
	* 定义了目标输出$z$，是一组N概率-掩码对，即$z=\{(p_i,m_i)\}^N_{i=1}$
	* $p_i \in \Delta^{K+1}$还包含一个"no object"标签($\phi$)，用于推理不属于K中任何一个类的mask
	* 允许使用相同的class预测多个掩码，使得它可以同时用于语义分割和实例分割任务
训练的时候，掩码分类模型需要在一组预测$z$与一组GT段$z^{gt}$之间进行匹配matching $\sigma$
$z^{gt} = \{(c_i^{gt},m_i^{gt})|c_i^{gt}\in\{1,\cdots,K\},m_i^{gt}\in \{0,1\}^{H\times W}\}_{i=1}^{N^{gt}}$，其中$c_i^{gt}$是第i个类的GT掩码。
* 对于语义分割任务，普通的fixed matching就足够了，因为预测数量N与类别标签K是匹配的。在实验中，作者发现基于bipartite matching的赋值比fixed matching效果更好。
* 与DETR不同，DETR使用bbox来计算在预测$z_i$与GT$z_j^{gt}$之间对于匹配问题的的assignment costs，而作者的工作MaskFormer中直接使用class和mask预测，即$-p_i(c_j^{gt})+\mathcal{L}_{mask} (m_i,m_j^{gt})$，其中$\mathcal{L}_{mask}$是二元mask损失
* 训练时的损失是：![[Pasted image 20231122210319.png]]
* 

### 3.3 MaskFormer
* 计算得到N个概率-mask对$z=\{(p_i,m_i)\}^N_{i=1}$
* 包括三个模块：
	* a pixel-level module：提取出per-pixel embeddings来产生二元掩码预测结果
	* a transforemr module：用一组Transformer decoder layers计算N个per-segment embeddings
	* a segmentation module：从之前的输出中产生预测结果$\{(p_i,m_i)\}^N_{i=1}$
* 在推理的时候，由$p_i$与$m_i$来组装成最终的预测结果

**Pixel-level module**：以$H\times W$大小的图像为输入
* backbone产生低分辨率图像特征图![[Pasted image 20231123203654.png|192]]
		其中$C_{\mathcal{F}}$是通道数，S是特征图的stride(作者使用$S=32$的设置)
* 逐渐上采样特征图，产生per-pixel embeddings $\varepsilon_{pixel}$ ![[Pasted image 20231123204631.png|149]]
		其中$C_{\varepsilon}$是embedding的维度
* 当时的任何基于per-pixel 分类器的分割模型均符合这个像素级模块的设计，包括基于Transforemr的模型
* MaskFormer能将所有这样的模型转换为mask分类模型

**Transformer module**
* 使用标准的Transformer decoder，来从**图像特征图** $\mathcal{F}$和N个可学习的位置编码(即**queries**)计算输出，即N个per-segment embeddings $Q\in \mathbb{R}^{C_Q\times N}$
	* $C_Q$对每一个segment的全局信息进行编码
	* 与[[DETR]]一样，decoder平行的产生输出

**Segmentation module**


## 四、实现细节


## 五、实验结果


## 六、结论
* 语义和实例分割范式的差异导致两个任务的模型完全不同，阻碍了图像分割整体的发展
* 作者提出的简单掩码分类模型可以超过SOTA的逐像素分类模型，尤其是在大量类别的情况下。
	* 在全景分割上也很有竞争力，并且不需要改变模型架构、损失、或训练流程
* 作者希望这种统一范式能激发语义分割和实例分割之间跨任务的联合工作