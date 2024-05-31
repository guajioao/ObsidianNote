Conditional Prompt Learning for Vision-Language Models
发表于CVPR2022

一张图其实可能有多种描述，比如一张猫的图像可能的描述：“一个猫。”，“一张猫的照片。”，“这是一只猫。”等。其实CLIP原文中，其作者发现了这个问题，并且发现prompt对预测性能的影响还挺大，于是还做了prompt ensembling。
CoOp其实就是为了研究这个问题，希望**不再手工设计prompt了，直接learn一个最优的prompt**
下图为各种prompt对识别结果的影响。最后一行是CoOp采用learnable prompt的结果

![[Pasted image 20231012195749.png]]

* 在CoOp中，输入的text是learnable的，随着在下游任务的few-shot样本而更新：
![[Pasted image 20231012195929.png]]