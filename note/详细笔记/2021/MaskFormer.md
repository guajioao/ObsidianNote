
收录于：NIPS2021
Per-Pixel Classification is Not All You Need for Semantic Segmentation

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
			* F输入Transformer decoder，产生N个per-segment embeddings $Q$【queries是N个可学习的embeddings】
			* 这个$Q$独立地分别产生N个**类别预测**和N个对应的mask embeddinngs $\varepsilon_{mask}$
		* 二元掩码损失线：
			* F通过pixel decoder产生per-pixel embeddings $\varepsilon_{pixel}$
			* $\varepsilon_{pixel}$与$\varepsilon_{mask}$做点积，后面跟着一个Sigmoid激活，产生N个**二元掩码预测**
	* 对语义分割任务，直接将N个二元损失与他们的类别预测通过一个简单的矩阵乘法combine起来即可
Transformer decoder部分的query用CLIP的文本特征？这部分的目的是产生每个class对应的mask embeddings。

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

