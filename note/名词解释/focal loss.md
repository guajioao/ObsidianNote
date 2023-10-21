Focal loss是最初由何恺明提出的，最初用于图像领域解决**数据不平衡**造成的模型性能问题
[Focal Loss for Dense Object Detection.pdf](https://arxiv.org/abs/1708.02002)
### 交叉熵损失函数
![[Pasted image 20231011204902.png]]
其中p^ 为预测概率大小,
y为label，在二分类中对应0或1：![[Pasted image 20231011205003.png]]

### 样本不均衡问题
* 对于所有样本，损失函数为：![[Pasted image 20231011204752.png]]
* 对于二分类问题，损失函数可以写为：![[Pasted image 20231011204806.png]],其中m为正样本个数，n为负样本个数，N为样本总数，m+n=N
* 当样本分布失衡时，在损失函数L的分布也会发生倾斜，如m<<n时，负样本就会在损失函数占据主导地位。由于损失函数的倾斜，模型训练过程中会倾向于样本多的类别，造成模型对少样本类别的性能较差

### 平衡交叉熵函数(balanced cross entropy)
基于样本非平衡造成的损失函数倾斜，一个直观的做法就是在损失函数中添加权重因子，提高少数类别在损失函数中的权重，平衡损失函数的分布。如在上述二分类问题中，添加权重参数 α∈[0,1] 和 1−α
![[Pasted image 20231011205134.png]]，其中![[Pasted image 20231011205151.png]]，即权重的大小根据正负样本的分布进行设置

### focal loss
focal loss也是针对样本不均衡问题，从loss角度提供的另外一种解决方法
* **focal loss的具体形式**：
	* ![[Pasted image 20231011205239.png]]
	* 令![[Pasted image 20231011205303.png]]，将focal loss的表达式统一为一个表达式：
* ![[Pasted image 20231011205333.png]] 
	* 同理**交叉熵**表达式可统一为：![[Pasted image 20231011205455.png]]
* ![[Pasted image 20231011205503.png]]反映了与ground truth即类别y的接近程度，越大说明越接近类别y，即分类越准确
	* 对比fl和ce可以发现，focal loss相比交叉熵多了一个modulating factor，即![[Pasted image 20231011205629.png]]。
		* 对于分类准确的样本，![[Pasted image 20231011205503.png]]趋向于1，modulating factor趋近于0
		* 对于分类不准确的样本，![[Pasted image 20231011205503.png]]趋向于0，modulating factor趋近于1
		* 即相比交叉熵损失，focal loss对于分类不准确的样本，损失没有改变，对于分类准确的样本，损失会变小。
	* **相当于增加了分类不准确样本在损失函数中的权重**
* ![[Pasted image 20231011205503.png]] 也反映了分类的难易程度，越大说明分类置信度高，代表样本越容易分；越小则说明越难分
	* 因此focal loss相当于增加了难分样本在损失函数的权重，使得损失函数倾向于难分的样本，有助于提高难分样本的准确度
* focal loss与交叉熵的对比，可见下图：
	* ![[Pasted image 20231011210009.png]]



https://zhuanlan.zhihu.com/p/266023273