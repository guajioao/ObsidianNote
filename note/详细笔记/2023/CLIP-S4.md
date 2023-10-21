# CLIP-S4:Language-Guided Self-Supervised Semantic Segmentation
收录于：CVPR2023
自监督！

# 摘要：
* 现有语义分割方法收到昂贵的像素级注释和预定义类的限制
* 本工作，CLIP-S4，提出利用**自监督像素表示学习**和视觉语言模型来实现各种语义分割任务（例如，无监督、迁移学习、语义分割），没有人工注释和未知类信息
	* 从不同的，增强后的图片views中通过pixel-segment 对比学习来学习**pixel embeddings** 
		* 不同模型生成的pixel embedding：![[Pasted image 20231009172203.png]]
	* 为了进一步改进pixel embeddings，并实现语言驱动的语义分割，设计了两种由视觉语言模型指导的**consistency**：
		1. **embedding consistency**. 将pixel embedding矫正到CLIP的joint特征空间中![[Pasted image 20231009172528.png]]
		2. **semantic consistency**. 强迫本模型作出与CLIP一致的推理
* CLIP-S4实现一种新的class-free的语义分割任务，训练过程中不需要unknown class信息
* 在未知类的识别方面大大优于其他方法
	* ![[Pasted image 20231009172330.png]]



# 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
结构图：![[Pasted image 20231009172656.png]]
	1. **a** 用增强后的多个同一图片进行聚类，然后对比学习
	2. **b** 通过Contrastive Loss强迫在视觉上一致的区域内pixel embedding也保持一致
	3. **c** 通过相似度计算的Embedding Consistent Loss 强迫b中处理后的pixel embedding与CLIP产生的embeddings对齐
	4. **d** 用argmax+cross-entropy交叉熵损失=Semantic Consistent Loss语义一致损失 来强迫本模型的预测结果与CLIP的类别预测结果保持一致
	5. **e** CLIP的预测结果和本模型的预测结果分别与[[Class Prototypes]]进行相似度计算，获得的计算结果进行**d** 。其中，Class Prototypes中的已知类在训练期间是预计算和固定的，位置类在训练过程中通过聚类来学习
**有好几个loss，同时训练还是多阶段训练？**
强迫预测结果保持一致的话，这样不可见类别的准确度上限不就是MaskCLIP的准确度了吗？
## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
* 通过自监督对比学习来学习一个pixel embedding function，在CLIP的指导下分割图像
* 通过自监督对比学习来强制视觉相关区域(如超像素[[superpixel]])和同一图像的不同增强视图之间的pixel embedding 保持一致
* 引入两个视觉-语言模型引导的consistency(即*embedding consistency and semantic consistency*)来进一步规范模型
* 这两个部分是互补的：
	* 一方面，对比学习减轻了CLIP引入的噪声
	* 另一方面，利用从CLIP中提取的知识，可以提高像素embedding的质量。
* 更重要的是，这样能够将精心设计的可知与不可知类的目标class prototypes应用于语言驱动的语义分割中

### 3.1 Pixel-Segment 对比学习
通过[[pixel-segment对比学习]]来产生 在视觉相关区域内一致的像素embeddings。具体来说：
* embedding函数通过**深度神经网络**将图像的每一个**pixel** p转换为d维的单位长度**embedding vector**向量![[Pasted image 20231009212805.png]]。
* 通过pixel embeddings聚类，将图像分成|**S**|个分段segments。
	* 每个分段s的embedding![[Pasted image 20231009213156.png]]为像素embeddings的平均值：![[Pasted image 20231009213237.png]]，然后被归一化为一个单位长度的向量![[Pasted image 20231009213355.png]]
* 对于每一个像素p，这些分段被分成两组：**positive set**![[Pasted image 20231009213510.png]]和**negative set**![[Pasted image 20231009213521.png]]
	* **positive set**![[Pasted image 20231009213510.png]]：包含在相同视觉相关区域内的分段，或者同一照片在不同增强视野下相同区域的分段
		* 视觉相关区域可以用[[super-pixels]]或[[contours]]来获得
		* 还使用数据增强(随机裁剪和颜色抖动)来产生同一图像不同增强视野的一致pixel embeddings
	* **negative set**![[Pasted image 20231009213521.png]]：图像中的其他区域的片段和其他图像增强后的片段被包含在![[Pasted image 20231009213521.png]]中。
	* pixel embedding![[Pasted image 20231009212805.png]]与![[Pasted image 20231009213510.png]]相吸，与![[Pasted image 20231009213521.png]]相斥，产生对比损失：![[Pasted image 20231009220844.png]]，其中κ是concentration常数，sim( )是相似度计算

### 3.2 视觉-语言模型引导的Consistency
使用CLIP来指导pixel embedding function的训练。关键思想是将pixel embedding function的输出空间与CLIP的特征空间保持一致。具体来说，是在训练过程中考虑两个consistency：**embedding consistency** and **semantic consistency**
* ***Embedding Consistency***. 目标是将自监督方法生成的pixel embeddings与CLIP的pixel embeddings对齐align。![[Pasted image 20231009222343.png]]图中绿色轮廓为自监督的结果，橙色轮廓为CLIP的。【我的理解是如果绿色轮廓与橙色区域不相交，那么损失会比较大，如果绿色区域完全在橙色区域里了，那么就损失比较小。目标是把绿色轮廓规整到橙色区域里】
	* 通过最小化两个像素嵌入空间之间的距离来实现
	* 首先，通过修改CLIP图像编码器的attention池化层，获得输入图像的像素embeddings。具体修改：
		* 移除 query 和key投影层
		* 将value投影层和最后的线性层变为两个连续的**全连接层**【和MaskCLIP的修改有点像，不过MaskCLIP是用两个1x1卷积投影】
	* 然后，使用原始图像来获得CLIP的pixel embeddings，然后进行增强。这样可以确保pixel embedding在不同增强视图之间是一致的
	* 最后，最小化**片段segments**之间的embeddings距离，而不是自监督的像素与CLIP的embeddings
		* 因为CLIP的pixel embeddings是有噪声的，这可以通过在segments聚合来缓解





## 四、实现细节


## 五、实验结果


## 六、结论

