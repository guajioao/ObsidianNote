Can Pre-trained Vision and Language Model Answer Visual Information-Seeking Questions?
发表于：emnlp

## 摘要：
* 预训练文本语言模型在视觉问题回答上已经展示了sota的能力，但不清楚这些模型是否能够不仅查询视觉内容，还能够回答知识密集型和信息寻求的问题
* 本研究提出数据集INFOSEEK，一个数据集，其中只包含无法仅依靠常识来回答的问题
* 在这个数据集上发现现有多模态模型面对这些问题表现不佳，但在微调后能够引出模型使用在于训练过程中得到的细粒度知识的能力
* 此外，论文还发现精确的视觉实体识别可以通过检索相关文档来提高信息搜索的性能，说明在此有很大的提升空间

## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、The Need for a New Visual Information-seeking Benchmark]]
* [[#三、INFOSEEK A VQA Benchmark of Visual Information-seeking Questions]]
* [[#四、Protocols and Models for INFOSEEK]]
* [[#五、Experiments]]
* [[#六、Related Work]]
* [[#七、 Conclusion]]
* [[#八、 Limitation]]


## 一、引言 Introduction
* 此前研究已经分析了模型回答文本信息寻求（或信息寻求）问题的能力，但对视觉信息寻求问题却知之甚少。
* 大模型对于INFOSEEK中问题表现不佳
* 大语言模型需要一些微调才能完全唤醒使用预训练获得的知识的能力
* 在INFOSEEK微调的模型可以推广到在微调过程中完全unseen的问题和实体类型

* 能够访问知识库的模型总体上比依赖预训练学习到的知识的模型表现更好，
* 但是没有知识库的端到端模型在某些需要细粒度答案的问题类别甚至tail entities上表现得更好（）
	* 例如“Which continent is this building located on?这座建筑位于哪个大陆上？”
* 提高视觉实体的识别可以大幅提高模型回答视觉信息寻找问题 visual infoseeking questions的能力
Entity-focused dense passage retrieval for outside

knowledge visual question answering

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
为确保信息搜索问题依赖于视觉理解，防止模型走捷径，不使用图像就回答问题，采用了一种受TyDiQA启发的两阶段注释方法
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
	* 设计评估分割，以防止过拟合，并重点评估预训练模型的泛化能力
		* 包括回答新实体的问题和在未见过的问题的能力
	* 定义了两个evaluation splits：
	1. UNSEEN ENTITY。一部分实体在不参与训练，只在评估中使用
	2. UNSEEN QUESTION。一部分问题只在评估时使用
* **Evaluation Metric.**
	* STRING和TIME类型计算VQA accuracy准确度
	* NUMERICAL计算Relaxed Accuracy

## 四、Protocols and Models for INFOSEEK
* 提出两种protocol，分别用于评估获取不同信息的模型。
	* 这一设计是为了鼓励来自不同families的模型对比概念，什么信息是可获取的
	* No KB协议比With KB 协议更有挑战性
* **The No-KB protocol.** 
	* 通过根据图像和问题来直接预测答案，类似于传统的VQA系统
	* 要求模型在参数中直接存储世界知识，以便有效的回答问题
	* 研究问题的一个重点是一个端到端模型在预训练中能记忆多少知识，以及在微调后对这些知识能够多好地利用
	* 使用标准的VQA格式数据，即{Image(I), Question(Q), Answer(A)}三元组
* **The With-KB protocol.** 
	* 目标是提供明确可行的推理链时，分析改进的headroom净空间
	* 因此该协议鼓励一个额外的实体识别步骤，并将任务建立在一个知识库上
	* VQA任务被转换为一个two-step pipeline
		1. 视觉实体识别
		2. 在有实体信息的情况下进行语言QA
			* 利用识别的实体信息查询一个大模型的答案
			* 或识别相应的维基百科文章来提取答案
	* 提供了一个100K的维基百科KB(文章和infobox图像)，其中包含来自INFOSEEK的视觉实体和来自Wikidia频率最高的实体
	* 在训练和验证过程中，With-KB protocol为每一个查询的视觉实体提供实体标签
	* 在测试过程中，模型仅基于{I, Q}对进行评估

### 4.1 Models without KB Information
* **Random & Prior.** 
	* 从训练集中随机抽样答案，大多数答案是基于问题先验。该先验是使用4-gram问题分组得到的训练问题集合计算得到的
* **PALM(Q-only) Model.** 
	* 为了验证INFOSEEK中视觉内容的重要性，使用PaLM(540B)建立了一个question-only baseline
	* 使用文本问题作为唯一的输入，并使用5次上下文学习（5-shot in-context-learning）
* **BLIP2 & InstructBLIP.** 
	* 使用了两个预先训练过的视觉语言模型，即BLIP2与InstructBLIP
	* 这两个模型共享相同的架构
		* 训练一个Q-former Transformer：将一个冻结的视觉编码器连接至一个冻结的instruct-tuned指令调优语言模型
		* 基于输入图像和文本输出文本
	* InstructBLIP在26个视觉语言数据集上对BLIP进行微调，并声称在unseen视觉语言任务上显示出更强的零迁移性能
	* 对于这两个模型，作者使用$INFOSEEK_{Wikidata}$微调其Q-former，来提高表现
* **PaLI-17B & PaLI-X.** 
	* 在PaLI系列模型中选择SOTA性能的两个额外预训练视觉语言模型来进行实验
		* 即使用PaLI-17B (ViT-e+mT5XXL)和PaLI-X (ViT-22B+ UL2-33B)
		* 其是在有10亿图像文本对的WebLI上进行预训练的
		* 这两个模型都使用了非指令调优语言模型，在INFOSEEK上显示出最小的零迁移性能【即在INFOSEEK上表现很差？】
		* 因此，在$INFOSEEK_{Wikidata}$上进行微调来提升这俩的性能

### 4.2 Models with KB Information
在这个protocol中，用两个解耦的子问题显式地建模了回答info-seeking问题的路径：
1. 识别grounded to the KB的视觉实体
2. 文本推理来回答这个问题
这种pipeline系统的隐藏好处是能够提高可解释性，因为通过诊断每个子组件能够更容易的定位问题源
* **Sub-task #1: Visual Entity Recognition.** 
	* 遵循OVEN中定义的实体识别任务，使用图像和文本查询（例如，“这个建筑是什么？”）作为模型输入，并预测100K个多模态维基百科条目中的实体
	* 使用预训练的CLIP（模型（ViT-L/14）作为本研究的视觉实体识别模型，因为它具有很强的泛化能力。
		* 具体来说，遵循CLIP2CLIP模型来微调CLIP，将本文数据集中的多模态表示（图像，问题）编码为query，将来自KB的（Wikipedia image,Wikipedia title）作为候选candidates
		* 然后基于query与candidates之间的加权余弦相似度分数，检索前k=5个最相似的实体
* **Sub-task #2: Language QA with LLM or KB Reader.** 
	* 通过视觉实体识别，已经可以将查询到的视觉信息表示为其文本描述。
	* 这使我们能够独立地研究语言推理组件，以理解一个强大的LLM或KB(基于知识的)阅读器能带来多少改进。
	* **PaLM: Large Language Model.**
		* 我们使用PaLM（540B）来研究从文本语料库的预训练到模型参数中可以记忆的知识量。
		* 给定一个问题和查询的实体名称（来自实体识别）
		* 使用5-shot in-context例子来提示PaLM，以此推理答案
		* prompt格式为“question: This is {entity} {question} answer:”
	* **Fusion-in Decoder (FiD): KB Reader.** 
		* 使用SOTA的检索增强模型，它从一个知识库中阅读信息，以理解维基百科文章在KB中的价值。
		* 具体来说，采用了FiD模型，该模型将N篇=100篇检索到的文章作为输入，并生成答案
		* 该模型使用$T5_{Large}$骨干（660M）对自然问题进行了预训练，并在INFOSEEK上进行了微调。
		* 在推理过程中，我们从Wikipedia中的前20个段落中检索k=5个视觉实体（来自实体识别），并将100段提供给FiD以生成答案。

## 五、Experiments
### 5.1 Results for No-KB Models
* **Main result.**
	* 表4给出了端到端模型的结果。
	* 在这种设置下，最好的预训练模型是PaLI-X，尽管该模型的整体性能的绝对数字仍然很低。
	* 这部分是由于信息搜索问题通常需要识别实体和检索与问题相关的特定信息，这使得端到端模型成为一项具有挑战性的任务。
	* 由于PaLI-X是在具有更多模型参数的大型语料库上进行预训练的，与PaLI-17B相比，它在UNSEEN ENTITY部分上表现出更好的泛化能力
	* 同时，在UNSEEN的问题和UNSEEN的实体部分上仍然存在明显的性能差距，这表明模型难以从训练集中泛化到新的视觉实体。
	* 我们还展示了模型在OKVQA和VQAv2上的研究结果以进行比较，并观察到了一个巨大的性能差距，这再次强调了视觉信息寻求问题的难度。
* **Fine-tuning elicits knowledge from the model.**
	* 为了演示INFOSEEK训练数据的价值，我们在图3中报告了模型的零迁移性能。
	* 具体来说，我们发现，在没有微调的情况下，两个PaLI模型产生的总体性能可以忽略不计，远远低于微调后的对应模型。
		* 这为假设：微调能够帮助引出预训练PaLI模型中的知识，提供了支撑证据
	* 另一方面，BLIP2和InstructBLIP在INFOSEEK上显示了引人注目的零迁移性能，因为它们采用了冻结指令微调的LLM（即Flan-T5），并且InstructBLIP在VQA基准测试上进行了进一步的指令微调
		* 在INFOSEEK上进行少量微调后，BLIP2模型的性能进一步提高，显示了在Human部分上强大的泛化结果
		* 在图10中，我们展示了使用BLIP2预测一个unseen实体（i.e Amberd）的“country location”的例子，经过微调后，准确率从18%提高到了92%
		* 尽管在训练集中这个实体是Unseen的
	* 最后，在互联网无法检索到的领域外的图像上进行了一个真实世界的评估
	* 特别的是，用作者制作的90个问题和30张图像，在INFOSEEK训练语料库外的视觉实体上，评估微调后的PaLI
		* 结果是，PaLI- 17B和PaLI-X分别正确回答了22.2%和38.9%的问题
		* 图4给出了PaLI和BLIP2对两个域外实体（艺术品和时尚产品）的预测示例。
* **Why does instruction-tuned BLIP2 obtain worse zero-shot INFOSEEK results?** 
	* ![[Pasted image 20240619210432.png]]
	* 图3中一个令人惊讶的发现引起了我们的注意，并揭示了对未来模型改进的一个重要的准则
	* 我们发现$InstructBLIP_{0-shot}$的表现明显低于其初始checkpoint，BLIP2（在$INFOSEEK_{Wikidata}$上7.4vs11.3），这与InstructBLIP优越的零迁移表现相矛盾
	* 我们进行人工分析，并发现了InstructBLIP的一个常见错误：与BLIP2相比，它倾向于生成粗粒度预测（例如，架构师vs一个人的名字）。这使得其在INFOSEEK上的性能下降
	* 我们假设这可以归因于InstructBLIP的指令调优数据集（例如，VQAv2和OK-VQA），它们共享一个细粒度较低的答案分布
	* 幸运的是，在$INFOSEEK_{Wikidata}$上微调有助于缩小差距。

###  5.2 Results for With-KB Models
* **Models with KB access perform better.**
	* 值得注意的是，在具有挑战性的$INFOSEEK_{Human}$部分，pipeline模型显著优于最好的No-KB模型。
	* 这强调了pipeline系统通过有效地利用视觉识别和语言推理来回答视觉信息检索问题的能力


## 六、Related Work


## 七、 Conclusion


## 八、 Limitation

