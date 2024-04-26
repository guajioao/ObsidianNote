* 收录于：CVPR2023

* 应用领域：有监督训练，图像分割

* 总体方法：ZegCLIP
	* 结构图：![[Pasted image 20231006150721.png]]
	* 一阶段方法，将CLIP用于像素级zero-shot任务：分别用文本、图像编码器提取特征；经过处理后使用包含三个transformer层的解码器生成掩码。训练过程中使用NEL损失
	* 三个设计（DPT/NEL/RD）使得baseline保持性能的同时提高泛化性
	* DPT：图像编码器训练时，每层添加一组**提示token**作为参数，在每层输出时均被舍弃
	* NEL：改用**Sigmoid**和**二元交叉熵**损失BCE,使用BCE损失的**focal焦点损失**变化，并用其联合一个额外的**dice损失** 
	* RD：取出CLIP计算过程中代表图片与类名匹配程度的值RD，与原本提取出的文本特征T相连，以作为新的输出![[Pasted image 20231006213104.png]] 

* 实验结果
1. 相比两阶段方法ZegFormer![[Pasted image 20231008141019.png]]
	* 参数量更少，计算量更小，推理速度更快
2. 与其他方法
	* 实验结果表：![[Pasted image 20231008140341.png]]
	* 在"inductive"设置下性能优于之前的工作，尤其对于不可见类
	* 在"transductive"设置下也非常出色
* 详细笔记
[[ZegCLIP]]