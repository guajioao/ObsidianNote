Dinov2: Learning robust visual features without supervision
收录于：2023


## 摘要：
现有工作表明，如果现有的预训练方法，特别是自监督的方法，如果在来自足够的**不同来源数据**上训练，是可以产生**无需微调**就可以直接应用在下游任务上的模型的
作者扩大数据和模型方面的预训练规模，尽力加速训练并保持稳定
* 在数据方面，作者提出了一个自动pipeline来构建一个专用的、多样化的curated图像数据集
* 模型方面，训练了一个具有1B参数的ViT模型



## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 数据处理的pipeline
	* ![[Pasted image 20240107195047.png]]
	* Embedding
		* 未经curaterd的数据和已经curated的数据都被映射为embeddings
	* Deduplication【去重】：
		* 只应用于未被curated的数据，删除接近的、重复的图片。减少冗余性，增加图像间的多样性
		* 删除与测试或验证集中包含的图片接近的图片
	* Self-supervised image retrieval【自监督图像检索】
		* 使用在ImageNet-22K上与训练的自监督网络计算图像embedding，并使用余弦相似度计算图像之间的距离。
		* 对未curated的图像进行k-means聚类。
		* 对于用于检索的query数据:
			* 如果足够多，就为每个图像检索N(通常为4)个最近邻
			* 如果不够，就从每个query图像对应的聚类中抽取M个图像（M由人工视觉检查选择决定）
			* 如果聚类得到的图像与query图像相似度够高，就可以增加N，减少M；反之则减少N，增加M
	* 最后将相似图片与query图片一起用于预训练，得到一个更优质，精心筛选过的大规模预训练数据集
* 学习特征的方式：可以看作是DINO和iBOT的结合，并引入SwAv的centering方法


## 一、引言 Introduction
文本引导预训练

## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

