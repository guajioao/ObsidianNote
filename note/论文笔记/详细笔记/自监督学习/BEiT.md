BEIT: BERT PRE-TRAINING OF IMAGE TRANSFORMERS
收录于：ICLR2022


## 摘要：
* 提出自监督视觉特征模型BEiT, **B**idirectional **E**ncoder representation from **I**mage **T**ransformers
* 基于自然语言处理领域的BERT，为vision transformer预训练提出masked image modeling任务
* 每个图像在预训练中有两个视角：image patches和visual tokens
* 随机mask掉一些patch后喂入backbone Transformer
* 预训练的目标是基于错误的image patchs重建原始的视觉token

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* Overview
	* ![[Pasted image 20231225145433.png]]
	* 对于输入的图片分别将其打为patchs和使用tokenizer编码为visual token
	* 随机mask掉一些patch后用BEiT编码器还原mask tokens位置的visual tokens
	* 用visual tokens解码得到还原的图片，计算损失

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method
### 2.1 Image Representations
1. Image Patch
	* $224\times224$图像分为14x14个16x16大小的patchs
2. Visual Token
	* 与NLP相似，通过"image tokenizer"用连续tokens序列代表图像
	* 将图像$x\in R^{H*W*C}$转换为$z=[z_1,\cdots,z_N]\in V^{h*w}$，其中词汇表$V=\{1,\cdots,\left | V \right | \}$包含离散的令牌索引

## 四、实现细节


## 五、实验结果


## 六、结论
介绍了一个为ViT设计的自监督预训练架构，在下游任务中获得了很好的微调结果，如图像分类和语义分割。
结果表明与BERT相类似的预训练工作能很好的应用于image Transformer
还提出了自动获得语义区域知识的有趣属性【？】，不需要人为标注
希望在将来扩大在数据和模型规模上BEiT的训练规模，并用统一的架构进行多模态预训练