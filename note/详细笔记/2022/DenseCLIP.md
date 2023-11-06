DenseCLIP:Language-Guided Dense Prediction with Context-Aware Prompting
收录于：CVPR2022


# 摘要：
* CLIP这样使用图像-文本对进行大规模预训练
	* 从自然语言监督中学习视觉表征
	* 对下游任务和数据集的可转移性非常强
* 问题：如何将学到的知识转移到更复杂的密集预测任务
* 本文提出一个新的架构来完成密集预测：
	* 隐式和显式地利用预训练知识
		* 隐式方法：直接在下游数据集上微调模型
	* 具体步骤：
		* 将图像-文本匹配问题转换为**像素-文本匹配**问题
		* 使用**像素-文本得分图**来指导密集预测模型的训练
		* 使用图像的上下文信息来prompt语言模型，来使得模型更好地利用预训练知识
		* 本方法是模型无关的，可以用于任何密集预测系统和预训练的视觉骨干

# 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实验结果]]
* [[#五、结论]]
* [[#六、Question]]

## 结构
### 传统训练和微调方法与DenseCLIP的对比
* 传统方法：
	* ![[Pasted image 20231012153311.png]]
	* 训练：图像->图像编码器->标签
	* 微调：图像->图像编码器|图像解码器->下游任务
* DenseCLIP的方法：
	* ![[Pasted image 20231012153323.png]]
	* 视觉-语言模型的预训练：使用图像与文本编码器的结果对比学习
	* 视觉-语言模型的微调：用图像embedding提示文本embedding，由像素-文本分数图损失指导训练->用于下游任务
### DenseCLIP的架构
![[Pasted image 20231012153937.png]]
1. 输入为图像和文本，分别进入各自的编码器中提取特征
2. 计算像素-文本分数图。这个分数图由ground-truth labels监督（即**Pixel-Text Matching Loss**），并最后会喂给图像解码器，与图像embeddings一起生成掩码(Task loss)
3. 使用图像的contextual信息，通过Transformer模块来prompt语言模型


## 一、引言 Introduction
* “预训练+微调”的范式被认为是一个关键的发现，很大程度上推动了各种下游计算机视觉任务的发展
* 由于逐像素预测的高注释和高计算成本，预训练对密集预测任务尤为重要
	* 一般为在大规模数据集上通过监督或自监督学习，进行骨干网络**预训练**
	* 然后在backbone上添加一个特定任务的模块，比如探测器或分割解码器，然后用较少的训练数据在目标数据集上**微调**模型
* 与传统的只基于图像的训练方法不同，CLIP是一个新的架构，通过在noisy大规模图像-文本对上对比学习来学习高质量的视觉表征。
	* 得益于语言监督，通过预训练CLIP的模型在各种视觉分类任务上获得了非常好的结果，且只使用很少甚至没有的注释
* 最近有一些工作，通过采用NLP领域的**prompt engineering**来更好地将CLIP模型迁移到下游视觉**分类任务**中。
	* 一些基于学习的prompting方法提出，通过修改语言模型的输出来更好地适应新任务。但他们主要关注于分类任务，与预训练任务非常接近
	* 而如何将知识迁移到更复杂的密集预测任务，和更加通用的设置中，还没有人做出与此相关的工作。
* 针对上游对比学习预训练任务与下游的逐像素预测任务之间的gap问题，本工作提出DenseCLIP，隐式和显式地利用预训练知识
	* ![[Pasted image 20231012223423.png]]
	* 隐式方法：直接在下游数据集上微调模型。即上图的CLIP。虽然性能由于传统的ImageNet预训练模型，但是并没有很好的利用CLIP的潜力
	* 显式方法：本文提出将图像-文本匹配问题转换为**像素-文本匹配**问题，并使用**像素-文本得分图**来明确地指导密集预测模型的训练
		* 通过Transformer模块使用**图像上下文信息**来**prompt语言模型**，优化文本embeddings，使得模型能够更好地利用预训练知识

## 二、相关工作 Related Work


## 三、方法 Method
### 3.1 CLIP概述
* 上游的对比预训练任务与下游的逐像素预测任务之间是存在gap的，前者考虑的是对图像和文本的实例级预测，而后者只基于视觉信息，但需要像素级输出结果。

### 3.2 语言指导的密集预测
提出language-guided dense prediction framework，可以更好的利用CLIP预训练模型的语言先验知识。
* 作者发现，从CLIP图像编码器最后一层中不仅可以提取图像的全局特征，还可以抽象出语言兼容的特征图(**language-compatible feature map**)
	* 以ResNet编码器为例。CLIP对其做了一个小修改，即增加了一个全局注意力池化层：在最后一个阶段的特征图![[Pasted image 20231012162233.png]]上应用全局池化，获得全局特征![[Pasted image 20231012155852.png]]。将concatenated特征![[Pasted image 20231012155940.png]]输入多头自注意力层(MHSA),获得![[Pasted image 20231012160019.png]]。在CLIP的训练过程中，![[Pasted image 20231012160114.png]]会被作为图像编码器的输出，而z通常会被忽略
	* 作者发现这个z有两个属性：1. z依然还有充足的空间信息，可以作为特征图；2. MHSA均衡的对待每一个输入元素，因此z和![[Pasted image 20231012160114.png]]很可能会很相似，即它与语言特征也是对齐的
	* 基于上述两个属性，z就可以用作和语言特征兼容的特征图。而对于ViT这样的模型，z也可以通过排除输出中的class tokens得到【即抽象出来的图像特征】
* 使用抽象出的特征图z和文本特征t来计算像素-文本分数图
	* ![[Pasted image 20231012161104.png]]
		* ![[Pasted image 20231012161119.png]]和![[Pasted image 20231012161130.png]]是经过L2归一化后的z和t【为什么这样就能表示表示匹配结果？只是矩阵相乘了一下？】【A：CLIP利用cos函数进行余弦相似度计算，而这个函数实际上也是将x与y相乘之后除以各自的模，可视为做了一个归一化。因此这里归一化后再相乘，与原本的相乘后再归一化效果一致。】
	* 这个分数图：
		* 描述了像素-文本匹配的结果。
		* 可以被看作是分辨率较低的分割结果，因此可以用来计算一个辅助的分割损失
		* 可以将这个分数图concatenate到最后一个特征图上，来明确的融合语言先验，即![[Pasted image 20231012161514.png]]
* 这个架构是模型无关的，因为这个修改后的特征图经过一些小修改就可以直接用于分割或目标检测(例如作为FPN的输入)

### 3.3 Context-Aware Prompting
此前已有两个工作[13, 60]证明了缩小上下游任务之间视觉或语言的gaps有助于提高CLIP在下游任务性能的提高。因此作者希望探索一个能够提升文本特征t的方法
* **Language-domain prompting**. 
	* 此前的CoOp引入了learnable textual contexts，通过反向传播优化这个contexts，最终在下游分类任务中取得了更好的性能
	* 受此启发，作者也使用了learnable textual contexts可学习的文本上下文作为baseline，只包括语言领域的prompting。那么text encoder的输入就修改为![[Pasted image 20231012164433.png]](3)，其中p为可学习的文本上下文，e为第k个类别名的embedding
* **Vision-to-language prompting**. 引入对于视觉信息的描述能够让文本更准确，比如“a photo of a cat in the grass.”就比“a photo of a cat.”更加准确。因此，作者希望能够使用视觉上下文信息来细化文本特征。 ^8fa6bf
	* 使用Transformer解码器中的交叉注意力机制来模拟视觉和语言之间的相互影响
	* 两个策略：![[Pasted image 20231012170247.png]]
	* (a) **pre-language-model prompting**. 简称*pre-model prompting*，指在数据进入语言模型之前根据图像生成一个合适的图像描述prompt，以此提高识别准确度。比如可能变成"a photo of a white dog"。
		* 将![[Pasted image 20231012170449.png]]传进一个Transformer解码器来产生视觉上下文编码![[Pasted image 20231012193000.png]]，q是一组可学习queries，![[Pasted image 20231012193050.png]]是提取出来的视觉上下文。
		* 用v替换公式(3)中的p，作为新的text encoder输入。这个版本就称为**pre-model prompting**。
	* (b) **post-model prompting**. 在语言模型提取文本特征**t**之后再加上一个与t最相关的视觉线索的**Vpost** 
		* 使用[[CoOp]]来生成文本特征t，并直接将他们用作Transformer decoder的queries,生成![[Pasted image 20231012194300.png]]，这样能够寻找文本特征最相关的视觉线索
		* 通过残差连接更新文本特征：![[Pasted image 20231012194433.png]]，其中![[Pasted image 20231012195300.png]]是一个可学习的参数，来控制残差的大小。这个γ初始化为一个很小的值，来最大程度的保持文本特征的语言先验知识。
	* 作者更推荐post- model，原因：
		* post-model更有效率。pre-model在推理的时候需要文本编码器额外的的前向传递，因为它依赖于具体的图像。而post-model可以存储训练后的文本特征，从而减小文本编码器在推理时的开销
		* 实验结果表明，post-model比pre-model有更好的性能
	
### 3.4 Instantiations实例化
* **语义分割**。用于语义分割时，一个辅助目标来帮助其提高分割性能
	* 在score maps![[Pasted image 20231012204127.png]]上计算一个分割损失![[Pasted image 20231012204100.png]]，τ = 0.07是一个[[temperature coefficient]] ,![[Pasted image 20231012204316.png]]是ground truth标签。
	* 这个辅助的分割损失可以帮助特征图更快的恢复其locality，这对于密集预测任务很有帮助。
* **目标检测和实例分割**。在这个情况下没有ground truth分割标签。
	* 使用bbox和标签来构建一个二元目标![[Pasted image 20231012204952.png]]，最终损失为：![[Pasted image 20231012204934.png]]
* 在其他任何backbone模型的应用。
	* 作者发现可以将CLIP图像编码器换成任何视觉模型（比如用ImageNet预训练的模型和自监督模型）。即使**这些模型的输出与文本没有很强的关联性，但是依然可以在语言的指导下训练的更快、更好**。换句话说，可以利用预训练文本编码器的语言先验来提高任何预训练的图像backbone。
	* 这使得DenseCLIP成为一个更通用的框架，可以利用大规模预训练中学习到的自然语言先验知识来改进密集的预测。


## 四、实验结果

在多项密集预测任务上都做了实验，包括：语义分割、目标探测和实例分割。
### 4.1 语义分割
* 数据集：ADE20K
* 实现细节：在流行的[[Semantic FPN]]架构上实验，来评估DenseCLIP
	* 使用CLIP的图像编码器来作为分割backbone，并直接使用Semantic FPN作为解码器。考虑了三种图像backbone：ResNet-50，ResNet-101, 和 ViT-B
	* language-domain prompting，使用的文本长度为8
	* 用于提取视觉上下文的Transformer解码器包含6层，头数为4
	* 训练时固定文本编码器参数，来保护大规模预训练时学到的自然语言知识
	* 为减少计算成本，在Transformer模块前将图像和文本embeddings投影到低维(256)
	* 直接用默认的训练策略微调CLIP模型效果不好，因此进行了两个关键修改
		* 使用AdamW替代默认的SGD
		* 将图像编码器的学习率设置为其他参数的1/10，以保留预训练权值
* 主要结果：
	* Table 1. ![[Pasted image 20231012215418.png]]
	* 结果表明，对于相同的主干，在简单的Semantic FPN上使用DenseCLIP能够超过现有最先进的，使用更复杂解码器的方法。
	* 比在原始的ImageNet预训练baseline(Semantic FPN)的mIOU更高，而多出的计算量也在可接受范围内(227.1->269.2)
	* 比普通的微调策略 性能更高(CLIP + Semantic FPN)


## 五、结论
* 提出一个新的框架，DenseCLIP，将知识从预训练模型CLIP转移到了下游密集预测任务中。
* 是一个模型无关的架构，使用预训练视觉-语言知识和context-aware prompting 策略
* 可以用于各种密集预测任务，包括语义分割、目标检测和实例分割
* 大量实验证明性能优越
#### Limitations & societal impact
* 该方法在分割方面取得了很大的改进，但是在检测方面的改进并不显著
	* 猜测原因：预训练的CLIP图像编码器缺少locality，因为在预训练的时候是以对象为中心的，只能提供较少的密集监督dense supervision，没有相应的约束
	* 作者认为通过在预训练阶段引入dense supervision，或者在预训练之后更好地恢复the locality，能够提高DenseCLIP的能力
* 本文提出的方法是一个针对密集预测任务的一般方法，并不针对特定的应用程序，因此没有直接涉及社会问题

## 六、Question
* Q：语义分割任务的辅助分割损失为什么能够帮助特征图更快的恢复其locality？这个locality指的是什么?
	* A：局部性
* Q: Image Encoder生成的image embeddings的维度是？是否经过了全局池化？
	* MaskCLIP的修改是修改CLIP的图像编码器，直接输出掩码
	* DenseCLIP是用最后一层的特征图x4经过MHSA，得到z。![[Pasted image 20231012162233.png]]，因此z的尺寸也是![[Pasted image 20231013153021.png]]。
* Q:W4xH4的小分数图是如何获得HxW大小的掩码的？
	* 上采样层