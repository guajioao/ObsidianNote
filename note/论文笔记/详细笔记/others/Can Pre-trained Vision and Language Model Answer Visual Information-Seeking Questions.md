Can Pre-trained Vision and Language Model Answer Visual Information-Seeking Questions?
发表于：emnlp

## 结构


## 摘要：
* 与训练文本语言模型在视觉问题回答上已经展示了sota的能力，但不清楚这些模型是否能够不仅查询视觉内容，还能够回答知识密集型和信息寻求的问题
* 本研究提出数据集INFOSEEK，一个数据集，里面只有无法仅通过普通感官无法回答的问题
* 在这个数据集上发现现有多模态模型面对这些问题表现不佳，但在微调后能够引出模型使用在于训练过程中得到的细粒度知识的能力
* 此外，论文还发现精确的视觉实体识别可以通过检索相关文档来提高信息搜索的性能，说明在此有很大的提升空间

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、The Need for a New Visual Information-seeking Benchmark]]
* [[#三、INFOSEEK A VQA Benchmark of Visual Information-seeking Questions]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]


## 一、引言 Introduction
* 大模型对于INFOSEEK中问题表现不佳
* 大语言模型需要一些微调才能完全唤醒使用预训练获得的知识的能力
* 在INFOSEEK微调的模型可以推广到在微调过程中完全unseen的问题和实体类型

* 能够访问知识库的模型总体上比依赖预训练学习到的知识的模型表现更好，
* 但是没有知识库的端到端模型在某些需要细粒度答案的问题类别甚至tail entities上表现得更好（）
	* 例如“Which continent is this building located on?这座建筑位于哪个大陆上？”
* 提高视觉实体的识别可以大幅提高模型回答视觉信息寻找问题 visual infoseeking questions的能力

## 二、The Need for a New Visual Information-seeking Benchmark
以往数据集的局限：
* **Information Seeking Intent.** 信息寻求的意图
	* 评估模型回答信息寻求问题的能力需要细粒度的知识，需要人们不太可能知道的
	* 然而作者发现70.8%的**OK-VQA**问题可以在不使用搜索引擎的情况下得到回答，这表明数据集主要集中于人们已知的知识。大多数OK-VQA问题都是关于许多人已经知道的粗粒度知识的
		* 例：What days might I most commonly go to this building? Sunday.
		* 人们只需要知道建筑的类型（教堂）而非特定的建筑（Dominus Flevit Church）
	* 这使得它不适用于评估long-tailed knowledge长尾知识，这是这些模型显示出来的弱点所在
* **Reliance on Visual Understanding.** 依赖于视觉上的理解
	* 与OK-VQA相比，ViQuAE数据集的目标是通过将从TriviaQA中提取出的问题与图像对来测试视觉实体的细粒度知识
	* 但是ViQuAE很大一部分问题不需要看图像就能回答，因为这些问题往往揭示了足够的信息来确定答案
		* 例如：Who betrayed him for 30 pieces of silver?"
				* “是谁为了30块银币出卖了他？”
	* 为了量化这一观察结果，作者从大模型PaLM说的评估集中提出了一些问题。
		* PaLM只需要读取问题就可以产生31.%准确度的回答，比SOTA的基于检索的模型还要高（该模型可以检索图片），它在这个数据集上只有9.4%
		* 虽然PaLM是一个更大的模型，但是这个实验表明即使不使用图象中的信息，也可以在ViQuAE数据集上获得非常好的性能
* **Entity Coverage.** 实体覆盖范围。
	* 当前的VQA数据集覆盖的视觉实体类别通常非常有限。
		* 例如，K-VQA只关注人类主题的实体
	* 这些限制阻碍了模型跨实体类别的知识的评估，并可能导致任务复杂性降低
		* 因为评估可能仅限于面部识别
* 为了解决上述限制，作者提出INFOSEEK，一个在视觉信息寻找问题上新的跨模态模型预训练数据集
	* 基于一个视觉实体识别数据集之上OVEN，它旨在回答与视觉实体识别相关的问题
* 通过对关于视觉实体的信息寻求问题来进行基准测试，进一步寻求视觉信息，这允许我们测试模型的预训练知识，而不仅仅是简单地识别一个实体。

## 三、INFOSEEK: A VQA Benchmark of Visual Information-seeking Questions
INFOSEEK数据集由两部分组成：
（1）$INFOSEEK_{Human}$：一组人写的视觉信息寻求问题（8.9K）来模拟信息寻求意图
（2）$INFOSEEK_{Wikidata}$：一个自动数据集，涵盖了大量实体。用于大规模训练的评估目的
分割数据集以确保记住训练集是无用的，从而强调预训练对获取知识的重要性
**Image Sources for Diverse Entity Coverage.** 从9个图像分类和检索数据集中获取图像，包括地标建筑（17%），动物（13%），食物（5%），飞机（3%）等
### 3.1 $INFOSEEK_{Human}$：  Natural Info-Seeking VQA Data Annotated by Humans
为确保信息搜索问题依赖于视觉理解，防止模型走捷径不使用图像就回答问题，采用了一种受TyDiQA启发的两阶段注释方法
这使得提问者不能事先知道答案，从而确保问题有寻求信息的意图
* **Question Writing.** 
	* Annotators标注者需根据自己的好奇心和信息需求写3-5个关于视觉实体的问题。
	* 在编写问题的过程中会给一些关于视觉实体的提示：一段简短的描述（15词），以及一组维基百科的章节标题。这确保了问题反应对学习实体的重要方面但又不能看到答案
	* 使用一组注释规则来防止问题太琐碎，比如关于视觉attributes的问题
* **Answer Labeling.**
	* 每个实体收集到的问题随机分配给不同的标注者，让他们根据维基百科来标注答案
	* 标注者查看维基百科上关于这个实体的文章，并被要求找到这个问题的简洁答案：一个尽可能短的文本span，同时仍能形成一个令人满意的回答
	* 此外，标注者还需要将问题分为三种类型：
		* 时间TIME，例如year
		* 数值NUMERICAL，例如height
		* 字符STRING，例如location
	* 最终为标注好的QA对分配图片，构造{image, question, answer}的三元组。如果在图像中出现多个物体，则进行人工验证和问题澄清clarification
	* 根据TyDiQA，测量注释的正确性，并获得了很高的精度95%，以此证明数据集质量是可靠的，足以用于评估视觉信息检索模型

### 3.2 $INFOSEEK_{Wikidata}$ 1 Million Automated VQA Data from Wikipedia
使用半自动化程序拓展数据集，将Wikidata（2022-10-03）中的知识三元组转换为使用人类编写模板的自然语言问题，从而得到1.3M个examples，包含超过11K视觉实体，覆盖了2.7K种实体类别
* **QA Generateion.**
	* 将Wikidata中的知识三元组(subj, relation, obj)根据一个挑选出的包含300个关系的列表，转换为自然语言处理问题-回答对。
	* 对每一个关系，标注者写1-2个问题模板。模板中包含1个用于视觉实体的占位符（例如car），并在数值问题中设置1个用于测量单位的占位符（例如inches英尺）避免混淆
	* 构造IQA三元组
* **QA Pair Filtering and Subsampling.**
	* 为了确保问题是多样化的，并且答案可以从维基百科上引用
	* 当来自Wikidata的answer无法在Wikipedia文章和subsample问题中找到时这个QA对会被过滤
	* 以平衡实体和关系的分布
### 3.3 Evaluation of INFOSEEK
* **Dataset Split.**
* **Evaluation Metric.**
	* STRING和TIME类型计算VQA accuracy准确度
	* NUMERICAL计算Relaxed Accuracy

## 四、Protocols and Models for INFOSEEK


## 五、实验结果


## 六、结论

