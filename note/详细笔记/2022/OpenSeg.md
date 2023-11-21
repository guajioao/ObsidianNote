Scaling Open-Vocabulary Image Segmentation with Image-Level Labels
收录于：ECCV2022
需要类别无关的像素级标注

# 摘要：
* 设计了一个开放词汇的图像分割模型，将图像分为与任意文本相关的区域
* 最近的工作（CLIP与ALIGN）在图像级标签的分类上表现出色，但是无法分割像素级的视觉概念
* 作者认为这是因为缺少了一个，在学习视觉语义对齐之前少了一个将像素分组的步骤
* 提出OpenSeg来解决上述问题的同时依然使用了规模可变的图像及标题监督。
	* 首先，学习为可能的组织提出分割掩码
	* 然后，通过对齐标题中的每个单词与一个或多个masks来学习视觉-语义对齐
	* 发现

# 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 原论文结构图
	* ![[Pasted image 20231014163940.png|425]]
* 重制辅助理解结构图
	* ![[f9798c19e40a63231d4016179970e17.png|475]]


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method

### 3.1 学习分割掩码
1. 处理过程：
	* 使用FPN来多尺度提取特征，并使用一个交叉注意力模块来产生分割区域建议
	* 将FPN特征融入P2分辨率【按照[[Multi-task self-training for learning general representations|另一篇文章]]的做法】来产生图像特征**F**
	* 通过卷积和fc层，从F中获得![[Pasted image 20231014194927.png]]
	* 在Fs中加入可学习位置嵌入PE，获得![[Pasted image 20231014195310.png]]
	* 将![[Pasted image 20231014195410.png]]与一组随机初始化的queries![[Pasted image 20231014195504.png]]输入cross-attention交叉注意力模块，获得mask queries![[Pasted image 20231014195612.png]]
	* **计算q与位置增强的图像特征![[Pasted image 20231014195410.png]]之间的点积，获得推理的masks**【没有crop】
		* ![[Pasted image 20231014195811.png]]
2. 损失计算
	* 计算**s**与类别无关的掩码标注之间的Dice coefficient
	* 最大化每个已标注掩码与最匹配的mask之间的Dice coefficient
	* ![[Pasted image 20231014200141.png]]，在每个训练图像中N > M
### 3.2 使用Masks来进行视觉-语义对齐
1. 使用与Fs相同的架构生成图像特征**Fz**
2. 通过用mask来池化图像特征->获得每个mask的特征？
	* ![[Pasted image 20231014201031.png]]
3. 计算图像与标题的相似度
	* ![[Pasted image 20231014201314.png]]
	* σ(x)i为Softmax计算，g(z, wj )为区域**z**与单词wj之间的相似度计算
	* 上述相似度计算函数鼓励每个单词对应到一个或多个区域，也避免了惩罚找不到任何相似单词的区域
	* 对每一个小批次**B**计算grounding loss
		* grounding loss的目的是**最大化每一个标记后的图像-标题对的分数**
		* ![[Pasted image 20231014201908.png]]
	* 训练OpenSeg的过程中将两个损失简单的用权重α相加
		* ![[Pasted image 20231014201959.png]]
		* 

### 3.3 Learning from Caption Only Data



## 四、实现细节


## 五、实验结果


## 六、结论

