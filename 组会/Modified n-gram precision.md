1. 首先计算一个单词在任何单个candidate翻译中出现的最大次数
![[605bb53047634be3cb6964cd5cefce6.png]]
例子中，Reference1中"the"出现了2次，Reference中"the"出现了1次，因此"the"这个单词的最大出现次数为2，记为 $max_{ref}$

2. 接下来，将每个candidate的词的总计数除以其最大inference计数，将这些截断的计数相加，然后除以候选词的总数
例子中，Candidate出现了7个"the"，但是单词"the"的 $max_{ref}$只有2，因此算Candidate的翻译正确单词个数只有2，最终它的Modified n-gram precision计算为 $p_n = \frac{2}{7}$ 












modified precision score: $$p_n = \frac{\sum}{} $$



1. $$Count_{w_i,j}^{clip} = min(Count_{w_i},Ref_j\_Count_{w_i})$$
	1. $Count_{w_i,j}^{clip}$为对第j个reference的单词 $w_i$的1
2. $$Count^{clip} = max(Count_{w_i,j}^{clip}),i=1,2,3\cdots$$
