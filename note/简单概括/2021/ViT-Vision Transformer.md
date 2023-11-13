
收录于：ICLR2021


## 摘要：
* Transformer架构在自然语言处理里面普遍使用，但在计算机视觉里的使用依然有限
	* 要么与卷积网络结合使用，要么用于替换卷积网络的某些组成部分，同时保持其整体结构
* 我们证明了这种对CNN的依赖是不必要的，一个直接使用图像patchs序列的纯Transformer在图像分类任务上也可以获得非常好的表现
	* 当在大规模数据上预训练，并迁移到多个中型或小型图像识别基准测试（ImageNet、CIFAR-100、VTAB等）时，ViT获得了与SOTA卷积网络相比出色的成果，而只需要更少的计算资源进行训练



## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
![[Pasted image 20231113210611.png|500]]
* 将图像分割成固定大小的patchs
* 将所有patch线性嵌入
* 加入位置编码与额外的\[CLS]嵌入
* 加入标准的Transformer编码器

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
### 3.1 Vision Transformer(ViT)
* 将图形$x\in \mathbb{R}^{H\times W\times C}$Flatten成多个2d的图像patchs，每个patch$x_p\in \mathbb{R}^{N\times (P^2 \cdot C)}$
* 

## 四、实现细节


## 五、实验结果


## 六、结论

