* 收录于：CVPR2023

* 应用领域：Open-Vocabulary Semantic Segmentation（开放词汇语义分割）

* 总体方法：
	* Overview of SAN![[Pasted image 20231008144145.png]]
		* SAN每一层的输入是上一层的输出加上对应CLIP层的输出，冻结CLIP模型参数
		* SAN训练最后一层后面接两个分支，一个提出Mask proposals，另一个提出attention bias
		* 推理时将proposals和proposal logits联合起来获得最终的推理结果
	* SAN的结构![[Pasted image 20231008195713.png]]
		* 与ViT相似，都是将图像分成patch然后线性投影成视觉特征。与可学习的N个输入Transformer
		* 
* 实验结果：

* 详细笔记：
* [[SAN]]