论文名：From SAM to CAMs: Exploring Segment Anything Model for Weakly Supervised Semantic Segmentation
发表于：CVPR2024

## 结构
1. SSC：![[Pasted image 20241105114358.png]]
2. CPM:![[Pasted image 20241106094002.png]]

## 摘要：
* 弱监督语义分割，有图像类别标签监督
* 最近的工作在推理阶段使用SAM取得了不错的进展，但是作者观察到这些方法仍然很容易受到作为初始种子的类激活映射CAMs的噪声的影响
* 针对这一问题本文提出了一个补救措施，From-SAM-to-CAMs(S2C)，一种新的WSS架构，在训练过程中直接将SAM的知识转移到分类器，提高CAM本身的质量
* S2C包括SM-segment Contrasting(SSC)和CAM-based prompting module(CPM)
	* SSC用SAM的everything掩码来基于原型对比【聚类】，限制每个特征接近其原型，远离其他原型
	* 同时，CPM从每个类的CAM在提取prompt【点标注】，并通过SAM生成特定类别的分割掩码。这些mask根据置信度被聚合成统一的自监督
* SOTA

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、Exploring the Use of SAM for WSSS


## 四、.Method
### 4.1 获取CAMs【训练分类模型】
* 定义一个分类器$C$, 作为CAMs生成器。由一个编码器$C_E$和一个分类头$C_H$组成
	* 编码器负责从输入图像$I\in R^{3×H×W}$中**提取特征图**$F\in R^{D×H×W}$: $$F=C_E(I)$$
	* 然后，利用分类头$G_H$，即1x1卷积层，我们**生成CAMs** $A\in R^{C×h×w}$:$$A=C_H(F)$$其中C是类别数，indices=$\{1,2,...,C\}$ 
	* 最后，通过沿空间轴在CAMs上应用一个**全局平均池化**Global Average Pooling(GAP)，得到一个图像级的预测logit $y\in R^{C}$:$$y=GAP(A)$$
	* 对于多标签分类，通过**交叉熵最小化损失** $L_{CLS}=l_{bce}(y, t)$，其中t是一个图像级的分类标签

### 4.2 SAM-Segment Contrasting(SSC)
* SAM segmeng-everything给定的掩码可以视作是一个可靠掩码，但由于输入的prompt是一系列没有语义的位置信息，得到的掩码也缺乏明确的语义信息。
* 这些图像通常包含不止一个相同类别的对象。
* 此外，点的网格状分布导致合并过程后图像被过度分割。例如，由各种组件组成的物体，如自行车或摩托车通常被分开分割而非作为一个整体
	* 综上所述，位于segment-everything的不同segemnt并不总是属于不同的类
* 因此，本文并不是在logit级别上直接使用segment-everything来对比，而是专注于**指导分类器**在**特征级别**上学习segmentation的概念
* 具体来说，提出 **SAM-Segment Contrasting(SSC)** 来将SAM的分割潜力在特征级别上转移到分类器中
* SSC主要是基于一个区域原型的对比方法，目标是帮助分类器理解图像的哪些像素应该被分组到一个部分
* 具体来说，在SSC中，从聚类的角度利用SAN，根据segment-everything给定的sgments来对比分类器特征
![[Pasted image 20241105114358.png]]
图3说明了提出的SSC。
* 首先将图像I输入到SAM中，利用segment-everything选项来生成segment。
	* 考虑到预测的segment可能会重叠，现根据面积进行从小到大排序。即，当一个像素属于多个segments时，选择面积最小的segment
	* 这个过程产生了一个单个的分割图，在本文中将其称为SE map，SE map的第i个segment称为$SE_i$
* 同时，分类器产生一个特征图$F$作为分类的中间结果
	* 由于特征图空间维度较小，使用双线性插值来调整匹配SE map的大小
* 随后，通过求位于每一个segment的像素平均值为每一个segment$SE_i$生成一个原型：$$pt_i = \frac{1}{SE_i}\sum_{(x,y)\in SE_i}F_{x,y}$$
	* 其中$pt_i$是第i个segment的原型
	* 在平均前后都会沿通道进行规范化，以保证被限制在单位超球层上
* 接着，强制每个特征接近它所属的段的原型，并远离其他段的原型
* 该策略鼓励一个segment内的像素特征形成聚类，便于分类器将其与其他片段中的像素特征区分开来
* 本质上SSC方法将分割知识转移到了分类器中
* 通过infoNCELoss来进行对比过程：$$L_{SSC}=-\sum_{i=1}^N\sum_{(x,y)\in SE_i}\frac{F_{x,y}\cdot pt_i/T}{\sum_{j=1}^{N}F_{x,y}\cdot pt_j/T}$$，其中N是SEmap中的segment总数，T是temperature温度系数
* 由于WSSS中没有像素级GT，本文会像[63]那样指导每个像素的特征，而不会像ReCo那样采样hard negative像素

### 4.3 CAM-based Prompting Module (CPM)
用每个类别的CAM作为SAM的提示，获得相应类别的掩码





## 五、实验结果


## 六、结论

