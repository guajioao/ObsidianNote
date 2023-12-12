$*$ 表示弱监督语义分割
$**$ 表示自监督
### Referring image segmentation
* [[CRIS]] **
* [[ZRIS]]

## mask分类
### 基于[[MaskFormer]]+[[SimSeg]]
* [[OpenSeg]] *
	* 2022
	* cross attention中使用HW大小的F【这个F是特征图还是mask?FPN产生的大分辨率特征图】
	* 使用文本特征与mask后的**特征图**相似度损失
* [[ZegFormer]]
	* 2022
	* 将maskformer中的class损失计算方式改为类别特征与文本特征的相似度损失，使class embeddings与文本特征对齐便于推理时的分类
	* 与maskformer中的mask loss相同的计算
	* mask patch分类的意义？
相同点：
* 都是基于MaskFormer生成mask区域
* 都通过mask后与文本特征对比的方式分类掩码
不同点：
* 监督方式的不同

### 改进对maskimage的识别
* [[OvSeg]] 

### 
* [[SAN]]

## 逐像素分类
* [[MaskCLIP]]
* [[DenseCLIP]]
* [[CLIP-S4]]
* [[SAZS]](暂定)
* [[ZegCLIP]]


