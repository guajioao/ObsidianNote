
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
对于一个HxW的图像，总共有K个类别，需要预测图像的每个像素$y=\{p_i|p_i \in \triangle^{K}\}$，其中$\triangle^{K}$是一个K维的概率向量。
训练非常直接，直接用ground truth的类别标签$y^{gt}=\{y^{gt}|y^{gt} \in  \{1,\cdots ,K\}\}^{H\cdot W}_{i=1}$来计算每个像素的交叉熵损失 $\mathcal{L}_{pixel-cls}(y,y^{pt})=\sum^{H\cdot W}_{i=1}-\log p_i(y^{gt}_{i})$

### 3.2 掩码分类公式
将语义分割任务分解为：
* 将图像划分/分组为N个区域(N不一定与K相等)，用二元掩码表示$\{m_i|m_i \in [0,1]^{H\times W}\}^N_{i=1}$
* 用在K个类别上的分布将每个区域联系成一个整体
* 对每一个segment进行联合分组和分类，即进行掩码分类
	* 定义了目标输出$z$，是一组N概率-掩码对，即$z=\{(p_i,m_i)\}^N_{i=1}$




## 四、实现细节


## 五、实验结果


## 六、结论
* 语义和实例分割范式的差异导致两个任务的模型完全不同，阻碍了图像分割整体的发展
* 作者提出的简单掩码分类模型可以超过SOTA的逐像素分类模型，尤其是在大量类别的情况下。
	* 在全景分割上也很有竞争力，并且不需要改变模型架构、损失、或训练流程
* 作者希望这种统一范式能激发语义分割和实例分割之间跨任务的联合工作