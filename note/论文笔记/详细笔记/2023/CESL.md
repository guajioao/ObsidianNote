Category-aware Saliency Enhance Learning based on CLIP for Weakly Supervised Salient Object Detection
收录于：

## 摘要：
* 弱监督显著目标检测(SOD)
	* 使用图像级的类别标签
	* 为了减少像素级标签的标注成本
	* 现存方法大多数训练一个分类网络来产生类激活图CAM，存在定位粗糙和伪标签更新困难等问题
* 本文提出一个具有类别意识的(Category-aware)显著性增强学习(**CSEL**)方法：
	* 基于视觉-语言对比预训练模型CLIP，此模型可以同时进行图像-文本分类和伪标签更新。
	* 将图像-文本分类转换为像素-文本匹配，生成一个**具备类别意识的显著图category-aware saliency map**，通过分类准确率来评估
	* 评估了category-aware显著图和**pseudo显著图**，使用质量置信度分数作为权重来更新伪标签
	* 通过两个map的相互增强来指导**伪显著图**向正确方向提升
	* SOD网络可以在更新后的伪显著图监督下联合地进行训练
* 在各种著名的RGBD和RGB SOD数据集上测试模型
	* S-measure
	* E-measure
	* F-measure

## 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
### 传统WSOD与CLIP指导的WSOD对比
* 传统的WSOD
	* ![[Pasted image 20231013143435.png]]
		* 用类别标签训练一个图像分类编码器，
		* 转换分类网络的特征，生成CAM(Class Activation Map)
		* 使用 conditional random fields（CRF）来优化这些CAMs
		* 利用优化后的CAMs来训练一个比较显著性网络
	* 缺点：CAM作为伪标签是不准确的，因为可能只关注了大多数对分类有帮助的区域，而不是整个物体
* CLIP指导的WSOD
	* **CSEL**:![[Pasted image 20231013144240.png]]
		* 图像被输入SOD-CLIP和编码器解码器（即SOD网络）中
		1. SOD-CLIP由类别标签监督，生成category-aware saliency map类别显著图(**cm**)；生成的cm再次经过SOD-CLIP评估，生成pseudo saliency map伪显著图(**pm**)
			* **cm**与**pm**通过CSEL分类头产生的两个置信度分数，相互监督，来更新伪标签。此处pm被用作伪标签
		2. 在获得更新后的pm之后，再作为伪标签用于SOD网络的训练
		* 推理阶段只使用SOD网络来推理结果
	
### CLIP指导的弱监督SOD模型
包括两个弱耦合的网络：伪标签更新网络；弱监督SOD网络。前者的结果被用来监督后者。两个网络同时进行训练。
* Overview：![[Pasted image 20231013150449.png]]
* （a） **SOD-CLIP**
	1. 分类头![[Pasted image 20231013151340.png]]
		* GAP即全局注意力池化，MHSA即多头自注意力。最后一层的特征图经过全局池化被提取为特征值用于分类。
		* 红色框内为图像特征和文本特征提取，然后进行匹配。即将**CLIP用于图像分类**
		* TransDecoder:**DenseCLIP的操作**。即使用图像的上下文信息prompt文本特征，然后与原本的文本特征进行相加
	2. 分割头![[Pasted image 20231013152045.png]]
		* 与DenseCLIP一样最后一层的特征图直接经过MHSA得到依然和语言特征对齐的特征图z。
		* z与prompt后的文本特征t计算相似度，获得相似度图(**sm**)，然后计算出伪标签(**pm**)
		* z与原本没经过MHSA的特征图进行**c**操作（应该是残差相加？），再**经过解码器生成具有类别意识的显著性图(cm)**
		* pm,sm与cm？只能看出是一个相互的关系，应该是相互监督的关系？具体操作细看methods
1. 用pm来监督sm的获取，使得分数图score能够更准确，即使得图像特征的提取和文本特征的prompt更好【**优化Image Encoder、Trans Decoder和MHSA**】
2. 用pm来监督cm，提高解码器生成显著图的准确度【**优化Decoder**】【**也起到优化1中3各部分的作用？**】
3. 用cls来监督相似度向量csv，即让分类准确度更高【**对齐文本和图像特征**】
* （b） **伪标签更新** 

## 一、引言 Introduction
现有的WSOD方法一般在ImageNet或COCO数据集上训练一个分类网络，然后转换分类网络的特征生成类激活图CAMs。然后应用Conditional Random Field（CRF）对CAMs进行优化，最后利用优化后的CAMs训练一个显著网络。然而，cam作为伪标签是不准确的，因为它们可能只突出显示最具区别性的区域，而不是整个对象



* CLIP指导的WSOD
	* 用CLIP生成category-aware saliency map类别显著图(**cm**)
	* 用CLIP评估pseudo saliency map伪显著图(**pm**)和类别显著图(**cm**)的质量来更新为标签
	* 使用伪显著图作为伪标签
## 二、相关工作 Related Work


## 三、方法 Method

### 3.1 Motivation and Overview
为了获得更好的伪标签，受DenseCLIP启发，设计了一个相似的具有类别意识的(Category-aware)显著性增强学习(**CSEL**)方法，同时执行分类和分割任务。

* 用CSEL同时对图像-文本相似度和像素-文本匹配关系进行建模
* 在训练阶段：
	1. 用传统手工方法([[traditional handcrafted method|->架构]])制作初始的显著图作为伪标签pm1，然后用这个显著类别作为弱监督信号来训练CSEL
	2. CESL在(a)模块生成cm1，会受（1）生成的pm1监督。
		* 这个cm1比初始化的pm1更好，因为它与显著类别的语言特征有一个很好的对齐关系(CLIP)
		* 手工制作的显著图pm1擅长感知低级线索
	3. 将cm1与pm1结合并使用具有类别感知的置信度分数，来更新获得pm2和cm2。
		* 置信度分数从CSEL的分类结果推理获得：
			* 用cm2和pm2分别mask input图片。这个显著图的质量越高，那么masked图像分类结果就越准确
			* 分类结果的准确度就作为置信分数来与pm和cm加权
	4. 将cm2和pm2结合(combine)起来,结合结果pm3用于更新原有的pm1。这样就能随着训练轮次的增加逐渐提高伪显著图pm的质量
	5. cm使得pm越来越好，然后更好的pm能够监督生成一个更好的cm。两个map一起越来越好，形成了SOD网络的最优监督信号
### 3.2 CSEL 
* 输入[[ROG-D图像对]] $\{r,d\} \in R^{ H \times W \times 4}$ ，将其concatenated起来，并卷积成一个三通道的输入$x \in R^{H \times W \times 3}$ 。即 $x = Conv(Concat(r, d)$ 
* 对CLIP图像编码器的操作**与DenseCLIP描述一致**，详见[[DenseCLIP#3.2 语言指导的密集预测|DenseCLIP#3.2 语言指导的密集预测]]
*  对CLIP提取的文本特征prompt操作也与DenseCLIP一致，详见[[DenseCLIP#^8fa6bf|DenseCLIP#3.3 Context-Aware Prompting中的Vision-to-language prompting]] 

	* 分别计算类别相似向量$csv \in R^{1 \times K}$ 和像素文本匹配分数矩阵$score \in R^{H_4 \times W_4 \times K }$ ，K为显著类别个数，与DenseCLIP中的类别个数C对应
	* 用匹配分数矩阵score通过一个卷积层和Sigmoid函数生成匹配分数图**sm** $sm = Sigmoid(Conv(score)$ 
	* 将图像编码器最后一层的特征f4与score连接起来(concat)，然后通过Decoder生成category-aware saliency map **cm:** $cm = Decoder(Concat(f_4, score)$ 
		* Decoder( * )是指通过progressive反卷积和连接(concatenation)来进行解码操作
	* 在训练过程中，使用显著类别cls来监督类别相似度向量csv，同时使用伪显著图pm来监督sm和cm
		* $loss_T = loss_{ce}(csv, cls)$
		* $loss_I^{high} = loss_{ppa}(sm,pm)$
		* $loss_I^{low} = loss_{ppa}(cm, pm)$
			* $loss_{ce}$ 是交叉熵损失，$loss_{ppa}$是像素位置aware损失[[pixel position aware loss]]。
		* 整个损失为上面三个损失的平均值：$loss = (loss_T + loss_I^{high} + loss_I^{low})/3$ 
* DenseCLIP:像素-文本分数图
* CESL: 特征-文本分数图
* CSEL利用CLIP的图像-文本对齐能力来将类别线索迁移到cm图上
	* 这个对类别具有感知力的和对空间敏感的特征图z会被用于密集预测任务
	* 同时全局信号 $\hat{z}$ 也被用于计算类别相似度
	* 这与**DenseCLIP只使用z**来在全监督语义分割任务中建立像素与类别的关系**不同**
### 3.3 伪标签更新

1. 用传统手工方法[[traditional handcrafted method]]制作初始的显著图作为伪显著图pm1
2. 从上一节的CSEL中获得了类别显著图cm，这个类别aware显著图聚合了类别知识，在直觉上比无监督手工显著图更好。
	* handcrafted saliency map对于感知低级别线索的能力很强
3. 因此，使用cm来逐渐更新pm
* 因为在弱监督方法中没有像素级的ground truth，所以无法评估cm和pm的质量。但是如果将这两个二元显著图视作masks，那么可以视为越好的masked图像分类结果越正确。
	* 因此，可以使用CLIP出色的零样本分类能力，来直接的评估两个显著图的质量，即计算置信分数。
	* **基于置信分数来融合两个显著图**，并更新原来的伪标签
* 在将pm和cm用作掩膜之前先进性Smooth操作。然后与输入图片结合，使显著部分可见，非显著部分不可见。生成的masked输入为 $x_{pm}$和 $x_{cm}$。
	* $x_j = Conv(x \times Smooth(j))$ ，$j \in {pm, cm}$，Smooth（·）是高斯平滑操作，“ $\times$ ”是元素乘法
* 这两个masked图像会输入CSEL分类部分来产生两个置信分数【CSEL文本编码器是frozen的】
* 综合置信分数，将pm与cm相加，更新pm
	* $pm \gets CRF(score_{pm} \times pm + score_{cm} \times cm)$ 
	* [[CRF]]是全连接条件随机场运算fully-connected conditional random field operation
	* 每一训练轮次的最后，都会执行这个策略生成一个最新的pm

### 弱监督SOD
理论上，可以采用任何显著的目标检测网络。它通过逐步更新上一节中描述的伪标签来监督。
本文使用的显著目标探测网络：
* 使用分段器Segformer作为编码器，来获得4层特征【即共有4个layer，每个layer都是一个Segformer】
* 第2、3、4层使用了global contextual modules (GCMs)来扩大接受野
* 为提高特征的表现能力，使用了金字塔乘法策略，来用高层特征增强低层特征
	* ${G_i}'' = {G_i}' \times \prod_{k=i+1}^{4}Up({G_k}')$ 
	* ![[Pasted image 20231013221804.png]]
	* Up（·）是上采样操作
* 解码过程采用连续的上采样([[插值算法]])，连接和卷积操作
	* $$P_i =  \begin{Bmatrix}BConv(Concat(Up(P_{i+1}),{G_i}''), & i = 1, 2, 3
 \\{G_i}'', & i = 4 \end{Bmatrix}$$
	* BConv(·)是3 x 3 卷积核的卷积操作，跟着一个批归一化层和ReLU激活函数
	* 在最后，用P1进行卷积核sigmoid操作来产生推理的显著图m
		* $$m = Sigmoid(Conv(P_1))$$
* 这个弱监督SOD的损失函数定义为
	* $loss_{saliency} = loss_{ppa}(m, pm)$



## 四、实现细节


## 五、实验结果


## 六、结论

