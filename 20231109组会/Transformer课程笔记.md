论文原名：Attention Is All You Need 
[[Transformer_Attention is all you need.pdf]]

# 一、Encoder
结构：![[Pasted image 20231020212356.png|176]]
## 1. Multi-Head Attention

## 2. 归一化[Layer Normalization]


# 二、Decoder


## 1. Masked Multi-Head Attention
训练的时候输入为正确答案【叫Teacher Forcing】
推理的时候一个一个的生成文字序列


## 2. Cross Attention（1与3之间的Multi-Head Attention）【2016就有Cross Attention了】
**连接Encoder与Decoder**的部分
1. Mask的self-attention的输出x经过一个与权值矩阵相乘的transform得到q
2. encoder的输出$a_i, i \in [1,n]$分别经过两个transform，得到$k_i$和$v_i$
3. q与encoder**所有的**ki相乘，再经过归一化得到$\alpha_i'$
4. $\alpha_i'$再与**对应的** $v_i$相乘，得到Decoder中Cross attention的 $v_i$
![[Pasted image 20231020194702.png|450]]
Decoder和Encoder中都有很多的层，原始论文都用了Encoder最后一层的输出来与Decoder中每一层做Cross attention




## 3. Feed Forward



# 拓展
1. Seq2Seq的model如何做copy？
比如做摘要的时候直接复制原文的专业名词等
2. Beam Search
	1. 适用于语音识别这种结果比较明显的任务
	2. 不适合需要发挥创造力的任务（TTS，Sentence complement）
3. 评估标准
	1. 训练的时候：minimize CE不一定好
	2. 验证的时候应该用[BLEU score]
	3. 测试的时候两个句子作比较
4. Scheduled Sampling
	1. 训练的时候用GT的句子，但是inference的时候看到的是机器自己产生的，不一定正确。因此如果训练的时候完全用正确的样本，在测试的时候可能会出现一个一步错、步步错的结果
	2. 解决方法：Scheduled Sampling
		* 是在用LSTM时提出的方法，不一定适配Transformer
	3. 一些适配Transformer的方法![[Pasted image 20231020214759.png]]

# 作业
* **1.任务：将一段文本从英文翻译为中文**
	* Cats are so cute. -> 貓咪真可愛。
* 2.训练数据集
	* Paired data 已经标注好的(英文，中文)对
		* TED2020: TED talks with transcripts translated by a global community of volunteers to more than 100 language
		* We will use (en, zh-tw) aligned pairs
	* Monolingual data
		* 只有中文的数据
* 3.评估方式
	* BLEU 
		* 比较生成句子与GT之间一样的字有多少个，越符合就认为生成的越好
		* 1. [[Modified n-gram precision]] (n=1~4)
			* [[N-gram]]：文本中连续出现的N个词
		* Brevity penalty: penalizes short hypotheses： $$BP = \begin{Bmatrix}1 & if\quad c > r
				\\e^{(1-r/c)} &if\quad c\le r
			\end{Bmatrix}		$$
			* c是candidate，指机器译文
			* r是reference，指参考译文
		* The BLEU score is the geometric mean of n-gram precision, multiplied by brevity penalty
		* $BLEU = BP\times exp(\sum_{n=1}^{N} w_nlogp_n)$
			* BP:长度过短句子的惩罚
			* N最大语法的阶数，实际取4
			* $w_n = 1/N$
			* $p_n$：出现在答案中的n元词语占候选译文中n元词语总数的比例【就是Modified n-gram precision啦】
* 

