论文名：CLIP-DINOiser: Teaching CLIP a few DINO tricks for open-vocabulary semantic segmentation
发表于：ECCV2024

## 结构
![[Pasted image 20241216110218.png]]

## 摘要：


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method



### 3.3 DINOising open-vocabulary features【推理时使用，Guided Pooling】
目标：利用已知的自监督特征中良好的位置原型，来改进MaskCLIP的开放词汇特征图
**提取自监督相关信息**。
* DINO最后一层注意力层可以帮助highlight图像中的目标。
* 使用value embeddings因为观察发现比key和query有更好的相关性。
* 丢弃CLS token，提取特征，计算patch之间的余弦相似性得到亲和图$A\in [-1,1]^{N\times N}$
* 发现自监督特征比CLIP的特征有更紧密、更准确的相关性
**通过引导池化来加强特征**
* 在亲和矩阵A的指导下对特征的每个patch进行一个concept-aware的线性合并combination
* 这个特征合并策略可以视为一种投票机制，强制相似的patches具有相似的CLIP特征(和预测)，同时衰减噪声
* 具体来说，计算一个新的特征图$F^+\in R^{N\times d}$ ，作为MaskCLIP特征$F$由A加权的平均值。如图2所示![[Pasted image 20241215213918.png]]
* 与[57,64,]一样，将$A^{\xi}$ 低于阈值的值设为0，并计算patch新特征$p \in \{1,\dots , N\}$:$$F^+_p=\frac{1}{\sum^N_{q=1}A^{\xi}_{p,q}}\sum^N_{q=1}A^{\xi}_{p,q}\cdot F_p$$
	* 【即每个patch与按照相似度图加权求和再求均值，重新计算得到一个新的值】
* 然后通过比较新特征图$F^+$与文本queries $\tau$ 来获得语义图$S\in [-1,1]^{N\times |\tau|}$ 

### 3.4 Teaching CLIP a first DINO trick: object correlations
训练阶段训练一个$3\times 3$的卷积，通过CLIP与DINO的对比BCE损失使得通过这个卷积能够将CLIP特征投影到一个更小的空间维度中。
计算投影后特征图的patch相关性$A^{\phi}\in [-1,1]^{N\times N}$  ，与二值化的$D=A^{\xi}>\gamma$ 计算二元交叉熵损失【BCE Loss】 
使用CLIP来产生关联图$A^{\phi}$，能够在MaskCLIP观察到类似的提升，说明良好的patch相关性可以从CLIP中提取出来。那么在推理中就可以丢弃DINO。将其命名为将CLIP-DINOiser命名为使用基于CLIP的相关性的guided-pooling策略。

### 3.5 Teaching CLIP a second DINO trick: background filtering
此外，如前面所述，可以将一个“背景”query添加到文本查询集合T中，以帮助过滤掉落在后台的、不对应于任何对象的patch。

作者认为仅仅依靠文本prompt的"background"来捕捉所有不显著的patch时表现不佳的，因此和[66]相似，建议使用一种非常轻量级的无监督前景背景分割方法，即FOUND[58]，它也依赖于DINO的自监督特征。
观察发现FOUND产生的显著图可能过于限制，丢弃部分显著目标或在杂乱中的目标。
为了减轻这种影响，作者提出添加一个额外的不确定约束来放松背景的选择：
* softmax函数后具有低置信度分数的patches和在掩码图M中处于背景的patch都被分配为"背景"prompt，从而融合两种情况下的背景信息
**Learning FOUND objectness.** 
* 训练一个$1\times1$卷积直接从CLIP特征学习FOUND预测，从特征中预测一个objectness map
* ![[Pasted image 20241215224115.png]]


## 四、实现细节


## 五、实验结果


## 六、结论

