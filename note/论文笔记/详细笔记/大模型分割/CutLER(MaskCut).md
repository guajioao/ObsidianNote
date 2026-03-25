论文名：Cut and Learn for Unsupervised Object Detection and Instance Segmentation
发表于：CVPR2023

## 结构


## 摘要：


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
### 3.1 Preliminaries
* Ncut为了最小化划分2个子图的代价，需要求解一个广义特征值系统：$$\begin{matrix} (D-W)x=\lambda Dx & (1) \end{matrix}$$，来**寻找与第二小特征值$\lambda$对应的特征向量$x$**。其中$D$是一个$N\times N$的对角矩阵，而$d(i)=\sum_i W_{ij}$。$W$是一个$N\times N$的对称矩阵

* TokenCut利用DINO进行NCut来获取图片中的前景/背景，而本文利用DINO特征空间的相似性作为NCut的相似度权重$W_{ij}$。具体来说，根据最近的多种方法【38,42,50】，使用来自dino预训练模型最后一个注意力层"key"特征的余弦相似度，即$W_{ij}=\frac{K_iK_j}{\left \| K_i  \right \|_2 \left \| K_j  \right \|_2 }$,并求解公式1中的第二小特征向量x
	* TokenCut每个图像只计算一个二值掩码，因此每张图片只能找到一个对象。
	* 作者发现使用其他N-2最小特征向量定位其他对象效果不佳
### 3.2 MaskCut for Discovering Multiple Objects
为了解决TokenCut和Ncut中只能发现一个mask的问题，提出MaskCut，通过迭代地将NCut用于一个 ***masked*** 相似矩阵
* 在阶段t通过NCut获得一个二值掩码$x^t$后，能够得到两个不相交的patches组，并构造一个二值掩码$M^t$:$$M_{ij}^t=\left\{ \begin{matrix}
  1, & if M^t_{ij} \ge mean(x^t) \\
  0, & otherwise.
	\end{matrix}  \right.$$
	* 为了确定哪一组对应前景，使用两个标准：
		1. 直观地看，前景patches应该比背景patches更突出。因此前景的掩码应该包含目标特征向量对应的patches
		2. 经验上的先验：前景集包含的图像四角应该少于两个
		* 如果二值掩码中的前景不满足上述任意一个条件，就反转前景背景的划分【即0变1,1变0】
	* 设置$W_{ij} < \tau^{ncut}$ 为$1e^{-5}$，$W_{ij} \ge \tau^{ncut}$ 为$1$【$\tau^{ncut}$是什么没讲？应该是预先设置的】
* 为获得$(t+1)^{th}$阶段的目标，屏蔽相似度矩阵$W_{ij}^{t+1}$中上一阶段前景区域对应的节点![[Pasted image 20241127141844.png]]，其中$\hat{M}^s_{ij}=1-M_{ij}^s$
* 使用更新后的$W_{ij}^{t+1}$再重复前两步操作，总共重复t次





## 四、实现细节


## 五、实验结果


## 六、结论

