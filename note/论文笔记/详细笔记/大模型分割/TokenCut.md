论文名：
发表于：

## 结构
![[Pasted image 20241127100536.png]]
* 提取ViT特征，构造全连接图。其中，图节点是图像patches，边是图像块之间的相似性
* 使用NCut在全连接图上提取目标分割图，二值化，即得到掩码
	* Ncut的计算公式：
		* ![[Pasted image 20241127101210.png]]
		* ![[Pasted image 20241127101110.png]]
		* cut(A,B)与assoc(A,B)计算公式相同，只表示不同的目的
* 使用Bilateral Solver或CRF优化掩码

## 摘要：


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

