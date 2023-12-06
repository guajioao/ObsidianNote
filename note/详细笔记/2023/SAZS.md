Delving into Shape-aware Zero-shot Semantic Segmentation
收录于：CVPR2023


## 摘要：
* 提出利用自监督pixel-wise特征向量的拉普拉斯矩阵来提高shape-awareness
	* 这一技巧不再需要seen类的mask，并且性能超过sota的shape-aware公式（在训练中对齐GT与预测的边缘）
* 使用不同的backbone在不同的数据集上训练，挖掘性能的提升，并得到了一些有趣的观察结果
	* shape-awareness提高带来的好处高度关联于mask密度与语言embeddings的局部性

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* Overview：用特征图训练出mask的边界框，使得视觉编码器具有一定的定位能力【即能够定位文本类别对应的区域】
	* 结构图![[Pasted image 20231206201945.png]]
	* 训练时，(A) $V_{train}$被转换为Pixel-wise Visual Embedding，并在$M_{gt}$的监督下与Text embedding对齐
		* 文本特征作为特征空间的锚点，通过CLIP文本编码器获得
	* (B) 训练出边界约束，以此来利用输入图像中的形状先验
		* 比较GT边界和Boundary Head的预测
	* (C) 推理时，为了减少seen和unseen的gap，SAZS将神经网络的像素级预测与通过非基于学习的光谱分析得到的eigensegments相融合。
		* 


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

