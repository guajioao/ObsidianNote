
收录于：ICLR2021
AN IMAGE IS WORTH 16X16 WORDS: TRANSFORMERS FOR IMAGE RECOGNITION AT SCALE


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
结构图：![[Pasted image 20231122221309.png]]

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
因为标准的Transformer输入为1d的token序列。对于2d的图像，作者将$x\in \mathbb{R}^{H\times W\times C}$的图像reshape为一堆patchs拉直后的序列$x_p\in \mathbb{R}^{N\times (p^2\cdot C)}$，(P,P)是每个patch的分辨率，(H,W)是图像的分辨率，$N=WH/P^2$是patches的数量，也可以作为Transformer的输入序列长度

## 四、实现细节


## 五、实验结果


## 六、结论

* 将图像视为一系列patchs，并使用NLP的标准Transformer编码器对其进行处理。
* 这种简单但是可扩展的策略在大型数据集上的预训练效果出奇的好
	* 在很多图像分类数据集上持平甚至超过了SOTA，且训练更加便宜
