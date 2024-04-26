* 收录于：ECCV2022

* 应用领域：语义分割

* 总体方法：
	* ![[MaskCLIP_Overview.png]]
	* 修改CLIP的注意力池化层，只保留value，并输出掩码
	* 用MaskCLIP的预测结果作为MaskCLIP+的伪标签，使MaskCLIP+可以使用任何分割定制的模型作为骨干网络
	* MaskCLIP的分类器直接替换MaskCLIP+使用的骨干网络的分类器
	* 当MaskCLIP+的结果比MaskCLIP好时进行自训练

* 实验结果
	* 无注释分割的mIoU结果：![[Pasted image 20231005201740.png]]
	* Zero-shot分割的表现![[Pasted image 20231005202007.png]]
	* 效果示例：![[Pasted image 20231005202757.png]]
* 详细笔记
[[MaskCLIP|MaskCLIP]]