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

#### 3.1 Task Definition
将训练集定义为$D_{train}=\{(I,M,S)\}$,测试集定义为$D_{test}=\{(I,M,U)\}$。
* 其中，$I \in R^{H\times  W\times 3}$，$M\in R^{H\times W\times C}$分别代表输入图像和对应的语义分割GT。
* S代表I中K个潜在标签的集合。
* U代表测试过程中的unseen类
* 


#### 3.2 Pixel-wise Vision-Language Alignment

* Visual Encoder
	* 
* Text Encoder
	* 
* Vision-Language Alignment
	* 最小化pixels与对应语义类别的距离，最大化与其他类别的距离
	* 损失计算公式:
		* ![[Pasted image 20231206214640.png]]
		* 分子：位置(i,j)上视觉特征与真实标签类别对应的文本特征之间的相似度
		* 分母，视觉特征与所有文本特征之间的相似度
		* -log(Softmax($<F_V[i,j],F_T>$))
#### 3.3 Shape Contraint
引入边缘探测作为限制任务，则视觉编码器能够更细粒度的获取图像信息【有没有更好的办法？同时训练两个任务比较复杂。能不能把Mask2Former的mask attention思想用在这里？】

## 四、实现细节


## 五、实验结果


## 六、结论

