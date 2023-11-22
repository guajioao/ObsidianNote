
收录于：CVPR2022
Masked-attention Mask Transformer for Universal Image Segmentation
[code](https://github.com/facebookresearch/Mask2Former)

## 摘要：


## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 结构图
	* ![[Pasted image 20231122102044.png|450]]
	* 采用与MaskFormer相同的结构，由一个backbone，一个pixel decoder，一个Transformer decoder组成。
		* Transformer decoder做了改造
			* 用masked attention来替代原本的cross attention
			* 用pixel decoder中不同大小的特征图来分别输入Transformer decoder中的块，以此来更好的解决小物体问题
			* 交换了cross attetntion（masked attention）与self attention的位置，让query可学习，并移除了dropout以使得计算更加高效
			* 图中省略了位置嵌入与每一层的预测

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

