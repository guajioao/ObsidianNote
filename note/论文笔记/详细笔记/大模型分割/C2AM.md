论文名：Contrastive learning of Class-agnostic Activation Map for Weakly Supervised Object Localization and Semantic Segmentation
发表于：

## 结构
![[Pasted image 20241126154326.png]]
* 编码器提取特征$Z_i$，经过激活头$\varphi(\cdot)$产生类别无关的激活图$P_i$【只区分前景背景】
* 前景与背景之间计算对比损失
	* 作者认为对于给定图像，前景和背景包含不同语义信息，因此在特征空间中应该有较大的距离
	* 最终前景-背景损失计算公式为：$$\mathcal{L}_{NEG}=-\frac{1}{n^2} \sum_{i=1}^n\sum_{j=1}^n log(1-s^{neg}_{i,j})$$，其中前景与背景之间计算余弦相似度：$s^{neg}_{i,j}$，该损失考虑了图像内和交叉图像【即所有前景与背景之间计算对比损失】
	* 前景-前景，背景-背景之间的损失
		* 只有相似的前景-前景，背景-背景在特征空间的距离较小应该拉进
		* 设计基于特征相似度的秩加权，减小

## 摘要：


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

