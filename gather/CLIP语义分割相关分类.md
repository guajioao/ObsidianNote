$*$ 表示弱监督语义分割
$**$ 表示自监督
### Referring image segmentation
* [[CRIS]] **
* [[ZRIS]]

## mask分类
baseline：[[SimSeg]]
### 基于使用Transformer decoder来区分区域
* [[OpenSeg]] *
	* 2022
	* cross attention中使用HW大小的F【这个F是特征图还是mask?FPN产生的大分辨率特征图】
	* 使用文本特征与mask后的**特征图**相似度损失
* [[ZegFormer]]
	* 2022
	* 将maskformer中的class损失计算方式改为类别特征与文本特征的相似度损失，使class embeddings与文本特征对齐便于推理时的分类
	* 与maskformer中的mask loss相同的计算
	* mask patch分类的意义
		- 在推理阶段与class分类一起综合的分类
相同点：
* 都是基于MaskFormer生成mask区域
* 都通过mask后与文本特征对比的方式分类掩码
不同点：
* 监督方式的不同
### 使用Transformer encoder产生区域 
* [[SAN]]
	* 直接转换思路，Maskformer是用decoder来做n个query的查询学习，SAN使用encoder，使区域query与class同时训练
			* maskformer用MLP对同一个Q做计算来使得class prediction与mask ermbeddings有一个对应关系
			* SAN直接用同一个Q分别与不同的V相乘，对应关系无疑更加深入【因为来自同一个Q】（反过来用在目标检测中或许能比DETR效果更好？）（可能所有需要对一个class做不同的查询的任务都可以用这种同一个Q对多个V做查询的方式，那么重要的就是对Q的训练）
### 思考
* 虽然长得很不一样，但是SAN和MaskFormer核心思想是一样的，都是用query来区分区域。一个是用Decoder做查询，一个用Encoder做查询。我之前本来想不出来SAN到底怎么突然想到的这个结构，但是跟Maskformer一比较，就觉得这两个是同一个思想的不同实现。
	Maskformer是通过Transformer Decoder的交叉注意力来用N个query在特征图上做查询，然后再分别转换为mask和class的预测。很多其他工作比如ZegFormer这些也是基于Maskformer的。
	但是SAN直接改换思路，不用Decoder先查询再区分了，而是在Encoder的输入额外添加N个类似CLS token的token，这些token学出来之后用同样的token与不同的Vmask和Vclass相乘来做查询。
	我觉得这样改造的优势在于加强了mask和class的对应关系，让V的MLP更加专注于提取特征，二者的对应关系由Q的MLP来学习。这样的结构感觉反回去像DETR一样用在目标检测里效果应该也挺好。然后感觉浙大那个工作里将CLIP文本特征添加到query token里来实现open voculabury的做法也可以用在SAN里
* 既然一个是用encoder，一个用decoder，那是不是可以两个都用？
#### 改进对mask image的识别
* [[OvSeg]] 
	* 引入[[VPT]]方法,使用的是VPT:Deep
	* 缺点：需要额外制作mask数据集
	* 训练一个与图像等大的mask visual prompt，这个mask prompt训练目的是记住mask区域的特征
* 思考：
	* Mask attention是否可以用于忽视mask区域？
## 逐像素分类
* [[MaskCLIP]]
	* 用文本embedding作为$1*1$卷积的权重【为了能够进行相似度计算，视觉特征的维度与文本的维度一定是相同的】，直接在特征图上卷积获得粗糙的mask作为伪标签
	* 用伪标签训练传统分割网络
	* 直接改造CLIP的输出，利用其特征图
* [[DenseCLIP]]
	* 利用CLIP的副产物z
	* 使用**可学习的文本prompt**，并利用视觉prompt提示文本【加强文本与视觉特征之间的关联】
	* 从视觉**特征图**与文本特征相似度产生掩码
* [[CLIP-S4]]
	* 
* [[SAZS]](暂定)
	* 
* [[ZegCLIP]]
	* 利用Attention层中的Scale层产生Mask【即$QK^T$】【与SAN不约而同的使用了QK乘积产生mask的思路】
	* 三个trick改进对unseen类的识别


