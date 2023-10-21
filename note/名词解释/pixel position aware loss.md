Wei, J., Wang, S., Huang, Q.: F3Net: Fusion, Feedback and Focus for Salient Object Detection. In: Proceedings of the **AAAI** Conference on Artificial Intelligence, pp. 12321–12328 (**2020**)

BCE有三个缺点：
1. 独立计算每个像素的损失，忽略了图像的全局结构。
2. 在以背景为主的图片中，前景像素的损失会被稀释
3. 对所有像素权重相同

* PPA损失并**不平等对待像素**，它可以综合像素的局部结构信息来引导网络**更多地关注局部细节**
* 来自边界或容易出错的部分的硬像素将得到更多关注，以强调它们的重要性
* PPA损失由加权BCE损失和加权IoU损失组成
	* ![[Pasted image 20231013194527.png]]
	* 
* 加权BCE损失：关注局部结构信息，更关注hard pixel
	* 定义：![[Pasted image 20231013194623.png]]
	* 其中 1(⋅) 是[[指示函数]]，γ是超参。这里每个像素被赋予一个权重α，**更难预测的像素应该对应于更大的权重**，反之亦然
	*   α定义为：![[Pasted image 20231013195023.png]]
	* 权重的实现如下：
	```
		 weit  = 1+5*torch.abs(F.avg_pool2d(mask, kernel_size=31, stride=1, padding=15)-mask)
	```
	* 可以看出，是选取上下左右15个像素范围的像素作为周围像素。若 α 越大，代表该像素和周围越不同
	* 和BCE相比，加权BCE更关注于难像素，同时加入了局部结构信息
* 加权IoU损失：扩大模型感受野，使其更关注全局信息而非单个像素
	* 为了进一步使网络关注全局结构,引入wIoU损失。其目的是优化全局结构，而不是专注于单个像素，且不受不平衡分布的影响
	* ![[Pasted image 20231013200955.png]]

综上，PPA损失综合了局部结构信息，为所有像素生成不同的权重，并引入像素限制wBCE Loss和全局限制wIoU Loss，使得模型能够更好的学习和产生更清楚的细节

![[Pasted image 20231013203020.png]]