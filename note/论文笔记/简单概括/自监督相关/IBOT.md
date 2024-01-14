* 论文全名
* 发表于：
* 结构图
	* ![[Pasted image 20240110104719.png|750]]
	* 图片x有两个视角u和v，两个视角都会通过techer网络和student网络
	* 计算两个损失：
	* 第一个损失是用两个网络的CLS token自蒸馏
		* student网络中有部分patch被掩码盖住了，teacher中的没有。
		* 如果这两个的cls token能够相似，说明student经过学习学到了如何能够提取到比较正确的语义信息，从而能够判断类别
	* 第二个损失是student被mask的patchs与teacher对应位置的patchs自蒸馏
		* 

* 大致思路：
	* 创新点
* 实验结果

* 详细笔记