来自VNet(V-Net: Fully Convolutional Neural Networks for Volumetric Medical Image Segmentation)

Generalized Dice Loss is **a loss function specifically designed for handling imbalanced data in multi-class segmentation tasks**. It's an extension of the Dice coefficient (or Dice similarity index), a statistical measure widely used for comparing the similarity of two samples
该损失是专门为了解决多分类分割任务重数据不平衡问题的，是Dice coefficient(或Dice similarity index)的拓展，

### other前置定义
Dice coefficient定义：![[Pasted image 20231011200944.png]]
	其中其中 |X⋂Y| 是X和Y之间的交集， |X| 和 |Y| 分表表示X和Y的元素的个数，分子乘2为了保证分母重复计算后取值范围在 [0,1] 之间。
dice loss可以写成：![[Pasted image 20231011201042.png]]

* 对于二分类问题，一般预测值分为以下几种:
	* TP: true positive，真阳性，预测为阳性，实际也是正例，预测对了。
	* TN: true negative，真阴性，预测是阴性，实际也是负例，预测对了。
	* FP: false positive，假阳性，预测是阳性，实际是负例，预测错了。
	* FN: false negative，假阴性，预测是阴性，实际是正例，预测错了。
* 此时Dice coefficient为![[Pasted image 20231011201227.png]]，而
	* ![[Pasted image 20231011201256.png]]

* 因此此时**dice coefficient是等同F1 Score**，而**dice loss是优化F1 Score**

定义![[Pasted image 20231011201758.png]]，
	* 其中![[Pasted image 20231011201812.png]]为预测值，取值在(0,1)之间
	* ![[Pasted image 20231011201856.png]]为目标值，取值非0即1
### Dice loss
* **dice loss**有几种形式：
	* **形式1**: ![[Pasted image 20231011201952.png]]
	* **形式2(原论文形式)**:![[Pasted image 20231011202007.png]]
	* **形式3**:
		* **U**为加平方的方式获取: ![[Pasted image 20231011202026.png]]
	*  ![[Pasted image 20231011202129.png]]为一个极小的数，一般称为平滑系数，有两个作用:
		- **防止分母预测为0**。值得说明的是，一般分割网络输出经过sigmoid 或 softmax，是不存在输出为绝对0的情况。这里加平滑系数主要防止一些极端情况，输出位数太小而导致编译器丢失数位的情况
		- 平滑系数可以起到**平滑loss和梯度**的操作
- pytorch实现方式：
```
def dice_loss(target，predictive，ep=1e-8):
    intersection = 2 * torch.sum(predictive * target) + ep
    union = torch。sum(predictive) + torch.sum(target) + ep
    loss = 1 - intersection / union
    return loss
```
- 特点：
	-  **区域相关**，即某点的loss和梯度不仅与该点的label和预测值有关，还和其他点的label和预测值有关
	- [[单点输出]]的形式：
		- **dice损失函数**： ![[Pasted image 20231011202741.png]]
			- ![[Pasted image 20231011202754.png]]蓝色为ce loss（交叉熵），橙色为dice
			- t = 0 时，loss的值都很大，接近1。一般情况下，在正常范围内，预测不管为任何值，都无差别对待，loss 都统一非常大。
			- t = 1 时，x在0左右小范围内保持一定的线性，但是远离0点后loss呈现饱和现象
			- 
		- **梯度**：![[Pasted image 20231011202853.png]]
			- ![[Pasted image 20231011202935.png]]
			- 当 t=0 时，同样在 x 的正常范围内， x 的梯度值接近0 。实际上，由于平滑系数的存在，该梯度不为0，而是一个非常小的值 。该值过于小，对网络的贡献也非常有限。
			- 当 t=1 时， x 在0点附近存在一个峰值，此时 y 接近0.5。随着预测值 y 越接近1或0，梯度越小，出现梯度饱和的现象。
		- 一般神经网络训练之前都会采取权重初始化，不管是Xavier初始化还是Kaiming初始化(或者其他初始化的方法)， 输出 x 是接近于0的
		- 此时正样本( t=1 )的监督是远远大于负样本( t=0 )的监督，可以认为网络前期会重点挖掘正样本。而**ce loss 是平等对待两种样本**的。
	- **多点情况分析** :
		- 预测值变化( y 值，图上的数字为预测值区间):![[Pasted image 20231011203754.png]]
		- dice loss 对应 x 值的梯度:![[Pasted image 20231011203825.png]]
		- ce loss 对应 x 值的梯度:![[Pasted image 20231011203834.png]]
		- 一般情况下，dice loss 正样本的梯度大于背景样本的; 尤其是刚开始网络预测接近0.5的时候，这点和单点输出的现象一致。**说明 dice loss 更具有指向性，更加偏向于正样本，保证有较低的FN。**
		- 极端情况下，网络预测接近0或1时，对应点梯度值极小，dice loss 存在梯度饱和现象。此时预测失败(FN，FP)的情况很难扭转回来。不过该情况出现的概率较低，因为网络初始化输出接近0.5，此时具有较大的梯度值。而网络通过梯度下降的方式更新参数，只会逐渐削弱预测失败的像素点。
		- 对于ce loss，当前的点的梯度仅和当前预测值与label的距离相关，预测越接近label，梯度越小。当网络预测接近0或1时，梯度依然保持该特性。
		- 对比发现， 训练前中期，dice loss下正样本的梯度值相对于ce loss，颜色更亮，值更大。说明dice loss 对挖掘正样本更加有优势。
	- **dice loss为何能够解决正负样本不平衡问题?**
		- dice loss是一个区域相关的loss, 当前像素的loss不光和当前像素的预测值相关，和其他点的值也相关
		- dice loss的求交的形式可以理解为mask掩码操作，因此不管图片有多大，固定大小的正样本的区域计算的loss是一样的，对网络起到的监督贡献不会随着图片的大小而变化
		- 从上图可视化也发现，训练更倾向于挖掘前景区域，正负样本不平衡的情况就是前景占比较小
		- ce loss 会公平处理正负样本，当出现正样本占比较小时，就会被更多的负样本淹没
	- **dice loss 训练会很不稳定**
		- 在使用dice loss时，一般正样本为小目标时会产生严重的震荡
		- 在只有前景和背景的情况下，小目标一旦有部分像素预测错误，那么就会导致loss值大幅度的变动，从而导致梯度变化剧烈
		- 可以假设极端情况，只有一个像素为正样本，如果该像素预测正确了，不管其他像素预测如何，loss 就接近0，预测错误了，loss 接近1；对于ce loss，loss的值是总体求平均的，更多会依赖负样本的地方
## **总结**

* dice loss 对正负样本严重不平衡的场景有着不错的性能，训练过程中更侧重对前景区域的挖掘。
* 但训练loss容易不稳定，尤其是小目标的情况下。
* 另外极端情况会导致梯度饱和现象。
* 因此有一些改进操作，主要是结合ce loss等改进，比如: dice+ce loss，**dice + focal loss**等