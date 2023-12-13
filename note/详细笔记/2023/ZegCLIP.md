# 
收录于：CVPR2023
是有监督训练
# 摘要：
最近CLIP已经通过一种两阶段的方案应用于像素级zero-shot学习任务。其主要思想：
	* 生成不可知类的区域建议
	* 将该区域裁剪出来，投入CLIP，以利用其图像级zero-shot分类能力
	* 这样的方案虽然有效，但他需要两个图像编码器，导致其pipeline复杂，也导致了计算成本高。
该工作希望直接将CLIP的zero-shot预测能力从图像级扩展到像素级
	* baseline：通过比较从CLIP中提取的文本和通过CLIP提取出的patch嵌入
	* 然而这样的做法会导致严重的过拟合可视类，且不能推广到不可视类。(why?)
	* 因此提出三种简单但有效的设计(**DPT、NEL、RD**)，不仅能保留CLIP的zero-shot能力，还能提高像素级的泛化能力
	* 综合这些修改的zero-shot语义分割系统称为**ZegCLIP**
	* 

# 目录：
* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
结构图：![[Pasted image 20231006150721.png]]
总体还是将文本编码器提取的特征与图像编码器提取的特征进行比较，新增的部分是：
	1.**Deep Prompt Tuning, DPT** ：深度提示调优【防止微调时丢失unseen类信息】
	2.**Relationship Descriptor, RD**：关系描述符 【使得模型能够匹配unseen类的label和patch】与SAN的【SLS】作用类似？
	3.**Non-mutually Exclisive Loss**：非互斥损失 
![[Pasted image 20231023155309.png]]
## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
### 3.1 Problem Definition
* 遵循广义的零样本语义分割，只在具有可见部分像素的数据集上训练后，就可以对可见类和不可见类进行分割。
	* 在训练阶段，模型从所有可见类的语义描述中生成每个像素的分类结果
	* 在测试阶段，模型产生对已知类和新类的分割结果
	* 可见类与不可见类不能有交集，且不可见类不参与训练
	* 关键问题：仅对可见类进行训练，就不可避免的导致对已知类别的过度偏见
	* 该方法对应“inductive”零样本分割，即在训练中无法访问不可见类的类名和图像
* 与上述方法对应的是"transductive"零样本学习方法，即使得不可见类的类名在测试阶段之前是已知的。
	* 训练样本包含不可见类的图像，但不可见类的GT不可用于训练
### 3.2 Baseline: One-stage Text-Patch Matching
* 现有CLIP用于零样本分割的方法为两阶段范式：
	* 阶段1：训练一个不可知类生成器
	* 阶段2：将CLIP作为一个零样本图像级的分类器匹配文本与1中图像区域
	* 有效但开销大
* 最近的一个研究发现，文本嵌入可以隐式地与patch级图片嵌入匹配。
	* 本工作受其启发，构建了一个一阶段的基线
	* 添加了一个普通的轻型transformer作为**解码器**
	* 将语义分割问题转化为**代表类查询**和**图像patch特征**的**匹配问题** 
* 用公式表示转化后的问题：
	* 使用线性投影产生不同维度的产生Q, K, V。Q从C个class的Truth中降维获得，K和V从N个图片patch中降维获得：
		* ![[Pasted image 20231006163143.png]]
		* $\mathrm{Q} = \phi_q(\mathrm{T}) \in \mathbb{R}^{C \times d}$ 
		* $\mathrm{K} = \phi_k(\mathrm{H}) \in \mathbb{R}^{N \times d}, \mathrm{V} = \phi_v(\mathrm{H}) \in \mathbb{R}^{N \times d}$ 
		* $\phi$ 为线性投影
		* 将C个类作为T嵌入，表示为$\mathrm{T = [t^1,t^2,\dots,t}^C]  \in \mathbb{R}^{C \times d}$ , d是CLIP模型特征的维度。$\mathrm{t}^i$ 代表第i个类。
		* 图片的N个patch被表示为$\mathrm{H = [h_1,h_2,\dots,h}_N]  \in \mathbb{R}^{N \times d}$ 
	
	* 上述scaled dot-product注意力的计算结果QK可以用于生成语义掩码**Masks**：
		* $\mathrm{Masks} = \frac{\mathrm{QK}^T}{\sqrt{d_k}} \in \mathbb{R}^{C \times N}$ 
		* $\sqrt{d_k}$ 是keys的维度，作为缩放因子
	* 最终的分割结果通过对Masks进行**Argmax**操作得到
	* 解码器的详细结构在结构图右侧，由**三层transformer**组成
* **更新CLIP图像编码器**：由CLIP图像编码生成patch特征。因此如何修改CLIP的图像编码器、计算**H**，就是一个重要的因素。
	* 在baseline方法中，H被认为由CLIP得到，CLIP的参数可能是固定的，或者可调的。分别表示为**Baseline-Fix**和**Baseline-FT**
	* 在3.3节的**DPT**中将提出一个更好的方法来适应CLIP的零样本分割
* **训练分割模型**：为了正确的训练解码器（或选择性的训练CLIP模型），
	* baseline：
		* 使用常见的softmax操作来将公式2的计算结果Masks转换为后验概率
		* 使用如交叉熵损失这样的排他性损失**Exclusive Loss (EL)** 作为目标函数
	* 在3.4节**NEL**中将指出baseline这种看似直接的策略会对泛化有害
* **设计查询嵌入(query embedding) T**：这是论文中方法的关键
	* 在baseline中直接使用CLIP文本编码器的特征
		* 这样会导致严重的过拟合
	* 因此建议使用文本和图像token之间的关系作为类查询
		* 在4.5节中还探讨了其他T的选择
### 方法比较：
图中展示从Baseline逐步加入本文提出的改进方法，泛化性和准确度逐渐提高![[Pasted image 20231006170657.png]]
### 3.3第一个设计：Deep Prompt Tuning (DPT)
对CLIP的backbone使用**DPT深度提示调优**，而不是微调
* **prompt tuning**提示调优是最新提出的策略，用于将预训练的Transformer模型适应到目标领域。它是迁移学习中微调方法的一个很有竞争力的备选手段
* 提示调优固定了CLIP的原始参数，添加可学习的**提示令牌**来作为每一层的额外参数
	* 微调会使得模型被修改的偏向可见类，不可见类的参数可能会被丢弃
	* 提示调优保留原本的参数，能缓解这个问题
* DPT的具体设计：
	* 结构图： ![[Pasted image 20231006213356.png]] 输出结果为g和H，每一层的Learnable prompts在输出时都被舍弃了，不作为下一层的输出(**这个设计作用是？**)
	* 第l层MHA的输入为 $\left \{\mathrm{g}^l,\mathrm{h}^l_1,\mathrm{h}^l_2,\dots,\mathrm{h}^l_N \right \}$，g为$[CLS]$token，H为N个图片patch
	* 深度提示调优附加的可学习的token表示为 $\mathrm{P}^l = \left \{ \mathrm{p}^l_1,\mathrm{p}^l_2,\dots,\mathrm{p}^l_M \right \}$，**每层的输入序列都附加这样一组token** 。则第L层MHA的处理就修改为 $[\mathrm{g}^l,\_,\mathrm{H}^l] = \mathrm{Layer}^l([\mathrm{g}^{l-1},\mathrm{P}^{l-1},\mathrm{H}^{l-1}])$ 其中p的输出直接被舍弃，即在输出中用下划线_代替，这样就不会被送入下一层。通过这种方式使得 $\mathrm{P}^l = \left \{ \mathrm{p}^l_1,\mathrm{p}^l_2,\dots,\mathrm{p}^l_M \right \}$ 仅作为一组可学习参数来适应MHA模型
	* 实验证明DPT可以在性能相似的情况下提高泛化性

### 3.4 第二个设计：Non-mutually Exclusive Loss (NEL)
语义分割模型一般将每个像素**视为多路分类问题**，采用softmax运算来计算后验概率，然后使用交叉熵等互斥损失EL作为损失函数。然而，Softmax本质上假设待分类类之间存在互斥关系：**每个像素必须且只能属于一个interest的类**。因此只有对数的相对强度，即对数的比值，对后验概率的计算重要。但是，当将模型用于不可见类时，类空间与训练场景不同，使得不可见类的预测效果不佳
因此本文提出使用非互斥损失（NEL），避免在训练时使用互斥机制。
* 使用**Sigmoid和二元交叉熵（BCE）损失**，确保每个类的分割结果都是独立生成的
* 使用BCE损失的[focal loss]]焦点损失变化，并用其联合一个额外的[[dice loss]] 损失
* $\mathcal{L}_{\mathrm{focal}} = -\frac{1}{\mathrm{hw}}\sum_{i=1}^{hw}{(1-y_i)^{\gamma} \times \hat{y}log(y_i)+y_i^{\gamma}\times(1-\hat{y})log(1-y_i)}$
* $\mathcal{L}_{\mathrm{dice}} = 1 - \frac{2\sum_{i=1}^{\mathrm{hw}}y_i\hat{y}_i}{\sum_{i=1}^{\mathrm{hw}}y_i^2 + \sum_{i=1}^{\mathrm{hw}}\hat{y}_i^2}$
* $\mathcal{L} = \alpha \cdot \mathcal{L}_{\mathrm{focal}} + \beta \cdot \mathcal{L}_{\mathrm{dice}}$
* 令$\gamma = 2$来平衡hard和easy样本，${\alpha, \beta}$ 为联合focal和dice损失的系数 [[#^bfba76|question]] 

### 3.5 第三个设计：Relationship Descriptor (RD)
在上述设计中，从CLIP文本编码器提取的类将直接与CLIP图像编码器提取的补丁进行匹配。这样虽然很直观，但会导致严重的过拟合。作者认为这是因为只在可见类数据集上训练了文本和图像patch之间的匹配能力。
作者观察CLIP计算匹配分数的公式：
	* ![[Pasted image 20231006205857.png]] ， ![[Pasted image 20231006205957.png]]代表第c个类的文本，![[Pasted image 20231006210028.png]]代表第j维。
	* g 是图像嵌入（【CLS】token）
	* ![[Pasted image 20231006210415.png]]，作者假定r代表了**图片与**类c文本提示符（即**类名**？）的**匹配程度**
* 将上述的![[Pasted image 20231006211759.png]]称为**文本-图像Relationship Descriptor (RD)**，表示为![[Pasted image 20231006211036.png]] 。
	* 然后将这些RD与原本的文本嵌入![[Pasted image 20231006211843.png]] concatenate连接起来，作为transformer解码器中的图像-特定文本queries![[Pasted image 20231006212000.png]]。
	* transformer解码器每个类输入的文本问询（**query**）就变成了![[Pasted image 20231006212204.png]] ，![[Pasted image 20231006212225.png]]是哈达玛积
	* 在![[Pasted image 20231006212530.png]]和**H**做了可学习的线性投影层，使其具有相同特征维数
**总之**，作者将CLIP计算匹配程度公式中，代表图片与类名匹配程度的值（**即RD**）取出来，与原本提取出来的文本特征T连接起来，表示为![[Pasted image 20231006213104.png]]作为后续Transformer解码器的输入之一
从结构图中可知![[Pasted image 20231006213134.png]]和**H**都是text-patch匹配解码器的输入，因此T和H需要做一个投影，使得其特征纬度相同。

## 四、实现细节
* 实验设置
	* 开源toolbox MMSegmentation，PyTorch1.10.1
	* CLIP ViT-B/16
	* batchsize：16，图像分辨率：512x512
	* 在训练迭代的前半部分在seen classes上训练ZegCLIP模型，然后在剩下的迭代中通过生成伪标签来自我训练。
	* 优化器：MMSeg toolbox的默认设置：AdamW

## 五、实验结果
1. 相比两阶段方法ZegFormer![[Pasted image 20231008141019.png]]
	* 参数量更少，计算量更小，推理速度更快
2. 与其他方法
	* 实验结果表：![[Pasted image 20231008140341.png]]
	* 在"inductive"设置下性能优于之前的工作，尤其对于不可见类
	* 在"transductive"设置下也非常出色
3. 消融实验

## 六、结论

在该工作中，基于CLIP提出一个有效的一阶段直通的zero-shot语义分割方法。为了将图像级的分类能力迁移到密集的预测任务中，同时保持先进的零样本知识，作者提出了三种设计，使得模型不仅在可见类上取得了颇有竞争力的成功，还极大的提高了对新类的表现。
* 提出基于CLIP的一阶段zero-shot语义分割方法
* 提出三种设计，使得模型在可见类上的性能好，同时泛化能力也不错
* 将文本嵌入作为query，使得对于“inductive” 和 “transductive”零样本设置都能很好的处理。
* 单阶段框架比两阶段框架推理快5倍
总的来说，我们的工作探索了如何利用预训练好的CLIP模型进行语义分割，并成功地将其零样本知识利用在下游任务中，这可能为未来的研究提供灵感。

## Question:
* 这个{α, β}是超参数还是学出来的系数？ ^bfba76