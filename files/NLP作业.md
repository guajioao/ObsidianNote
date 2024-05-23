# 1、分词



# 2、TriGram

要使用Python构建TriGram模型并统计数量最多的和最少的TriGram，我们需要执行以下步骤：

1. 读取语料数据。
2. 分词并构建TriGram模型。
3. 使用平滑技术处理TriGram模型。
4. 统计并展示TriGram的出现次数。
5. 编写函数计算句子的概率。
6. 设计测试句子并比较平滑前后的效果。

由于您提供的语料是中文文本，我们还需要进行中文分词。这里我们可以使用`jieba`库来进行分词。以下是一个简单的示例代码，展示了如何实现上述步骤：

```python
import numpy as np
import matplotlib.pyplot as plt
import jieba

# 假设语料如下，实际应用中应读取文件
corpus = "这里是您的语料文本。"

# 分词
words = list(jieba.cut(corpus))

# 构建TriGram模型
def build_trigram_model(words):
    trigram = {}
    for i in range(len(words) - 2):
        trigram[tuple(words[i:i+3])] = trigram.get(tuple(words[i:i+3]), 0) + 1
    return trigram

# 应用平滑
def apply_smoothing(trigram, alpha=0.1):
    vocab = len(trigram.keys())
    for trigram_tuple in trigram:
        trigram[trigram_tuple] += alpha / vocab
    return trigram

# 统计TriGram出现次数
trigram_model = build_trigram_model(words)
trigram_model = apply_smoothing(trigram_model)

# 统计最多的100个和最少的100个TriGram
most_common = sorted(trigram_model.items(), key=lambda x: x[1], reverse=True)[:100]
least_common = sorted(trigram_model.items(), key=lambda x: x[1])[:100]

# 绘制折线图
most_common_counts = [count for _, count in most_common]
least_common_counts = [count for _, count in least_common]

plt.figure(figsize=(10, 5))
plt.plot(most_common_counts, label='Most Common')
plt.plot(least_common_counts, label='Least Common')
plt.xlabel('TriGram Index')
plt.ylabel('Frequency')
plt.title('TriGram Frequency Distribution')
plt.legend()
plt.show()

# 计算句子概率
def calculate_sentence_probability(sentence, trigram_model, word_to_index, index_to_word, smoothing=1e-3):
    words = list(jieba.cut(sentence))
    log_prob = 0.0
    for i in range(len(words) - 2):
        trigram_tuple = tuple(words[i:i+3])
        if trigram_tuple in trigram_model:
            log_prob += np.log(trigram_model[trigram_tuple] / (1.0 * smoothing))
        else:
            log_prob += np.log(smoothing)
    return log_prob

# 设计测试句子
test_sentence = "这是一个测试句子。"

# 构建单词索引映射
word_to_index = {word: i for i, word in enumerate(set(words))}
index_to_word = {i: word for word, i in word_to_index.items()}

# 计算原始概率
original_prob = calculate_sentence_probability(test_sentence, trigram_model, word_to_index, index_to_word, smoothing=0)
print(f"Original Probability: {original_prob}")

# 使用平滑后的概率
smoothed_prob = calculate_sentence_probability(test_sentence, trigram_model, word_to_index, index_to_word, smoothing=1e-3)
print(f"Smoothed Probability: {smoothed_prob}")
```

请注意，这个代码只是一个简单的示例，实际应用中需要根据具体的语料和需求进行调整。特别是，您需要将`corpus`变量替换为您的实际语料文本。此外，`jieba`分词可能不适用于所有中文文本，您可能需要调整分词策略以适应您的数据。

在绘制折线图时，由于TriGram的数量可能非常多，这里只展示了如何绘制最常见的和最不常见的100个TriGram的频率分布。如果您想要绘制所有TriGram的分布，可能需要考虑使用更高级的可视化技术，如直方图或对数尺度的图表。

最后，计算句子概率的部分使用了对数概率来避免数值下溢，并应用了平滑技术来处理未见过的TriGram。平滑值`alpha`是一个超参数，您可能需要根据您的数据进行调整。在实际应用中，您还需要构建一个从单词到索引的映射，以便在计算概率时使用。

# 3、利用语料库建立HMM模型

### **构建HMM模型**

利用给定语料，构建HMM模型。编写能够满足下面要求的程序：程序运行之后，能够输出三个模型参数文件：

**初始概率分布矩阵 π，由句子表示所构成的转移矩阵 A，由词性到词所构成的发射矩阵 B。**

根据上面的介绍，我们可以得到：

**1、初始状态：**初始分布就是一个隐藏状态的初始概率分布。就词性标注来说，初始分布表示的是一句话中第一个词是什么词性的概率分布，在本次实践中需要统计每句话中第一个词的词性所占的概率分布情况。

**2、转移矩阵：**首先需要统计隐藏状态的频数，如果有N个隐藏了的状态（词性），那么转移矩阵就是一个N*N的矩阵，它的元素表示的是一种状态转化到另一种状态的概率。

**3、发射矩阵：**其元素表示在给定一个词性（n）的情况下，它是某个词的概率表示。  

#### 准备工作

导入相关库，并定义相关的变量以及存取路径。

```python
import re
from collections import defaultdict

corpus_path = "199801-UTF8.txt"
pi_path = "./data/pi.txt"
A_path = "./data/A.txt"
B_path = "./data/B.txt"

# 句首词性频率 --- 用于计算初始状态的概率pi
postag_begin_freq = defaultdict(int)
# 句首词性总数 --- 用于计算初始状态概率pi
postag_begin_num = 0
# 词性序列 --- 用于计算状态转移矩阵A
postag_seq = []
# 词性发射频率，即某词性映射为了某词语多少次 --- 用于计算发射矩阵B
postag_to_word_freq = {}
```

#### 数据读取与预处理

a) 首先观察语料特点，删掉不需要的空行

b) 通过正则表达式，删掉句首的时间标记，以方便后续对句首词性进行读取

c) 对语料中的复合词组进行清洗

```python
with open(corpus_path, encoding="utf8") as f:
    sentences = f.readlines()
    for sentence in sentences:
        # 忽略空行
        if sentence == "\n":
            continue
        # 删除句首无用的时间标记
        sentence = re.sub("199.*?/m", "", sentence)
        # 将句子分为多个元素，形如"古琴/n"
        sentence = sentence.split()

        for i, item in enumerate(sentence):
            # 将句子元素分为词语和词性，其中item[0]为词语，item[1]为词性
            item = item.split("/")
            word = item[0]
            postag = item[1]

            # 去除复合词组中的"["标记
            if word[0] == "[":
                word = re.sub("^\[", "", word)
            # 去除复合词组中的"]"标记以及紧跟其后的标签
            if "]" in postag:
                postag = re.sub("].*", "", postag)

            # 记录句首词性频率 --- 用于计算初始状态概率pi
            if i == 0:
                postag_begin_freq[postag] += 1
                postag_begin_num += 1

            # 如果词性发射频率字典中无此词性，则新增关于此词性的映射 --- 用于计算发射矩阵B
            if postag not in postag_to_word_freq:
                postag_to_word_freq[postag] = defaultdict(int)
            # 记录此词词性转化为了哪个词，将对应词的词频加1
            postag_to_word_freq[postag][word] += 1

            # 将词性加入到词性序列中
            postag_seq.append(postag)
```

#### 数据计算

**计算初始状态 pi**

```python
# 将 句首词性频率 转换为概率 --- 此概率即为初始状态的概率pi
for key, val in postag_begin_freq.items():
    postag_begin_freq[key] = val / postag_begin_num
```

**计算矩阵状态转移矩阵 A**

```python
# 遍历词性序列，计算词性转换为下一个词性的频率 --- 用于计算状态转移矩阵A
postag_to_next_freq = {}
for i, postag in enumerate(postag_seq):
    # 最后一个词性不会转换为下一个词性，不进行计算
    if i == len(postag_seq) - 1:
        break
    if postag not in postag_to_next_freq:
        postag_to_next_freq[postag] = defaultdict(int)
    postag_to_next_freq[postag][postag_seq[i + 1]] += 1

# 将 下一个词性频率 转换为概率 --- 此概率即为状态转移矩阵A
for key, val in postag_to_next_freq.items():
    num = 0
    for freq in val.values():
        num += freq
    for postag, freq in val.items():
        postag_to_next_freq[key][postag] = freq / num
```

**计算发射矩阵B**

```python
# <----------------------------仿照计算A的方法，计算B------------------->
# 将 词性发射频率 转换为概率 --- 此概率即为发射矩阵B
for key, val in postag_to_word_freq.items():
    num = 0
    for freq in val.values():
        num += freq
    for word, freq in val.items():
        postag_to_word_freq[key][word] = freq / num
```

#### 数据存储

```python
with open(pi_path, "w") as f:
    # 将pi中键值对按概率值降序排列，返回结果是一个由元组构成的列表
    sorted_tup = sorted(postag_begin_freq.items(), key=lambda x: x[1], reverse=True)
    for postag, prob in sorted_tup:
        f.write("%s %s\n" % (postag, prob))
# <----------------------------仿照上述的存储方法，存储A和B ------------------->
with open(A_path, "w") as f:
    for postag_source, val in postag_to_next_freq.items():
        # 将A的一行结果按概率值降序排列，返回结果是一个由元组构成的列表
        sorted_tup = sorted(val.items(), key=lambda x: x[1], reverse=True)
        for postag_target, prob in sorted_tup:
            f.write("%s %s %s\n" % (postag_source, postag_target, prob))
        f.write("\n")

with open(B_path, "w") as f:
    for postag, val in postag_to_word_freq.items():
        # 将B的一行结果按概率值降序排列，返回结果是一个由元组构成的列表
        sorted_tup = sorted(val.items(), key=lambda x: x[1], reverse=True)
        for word, prob in sorted_tup:
            f.write("%s %s %s\n" % (postag, word, prob))
        f.write("\n")
```

### 模型应用

输入一个词，使用前向算法来计算输入的这个词的概率。

#### 读取矩阵文件

**读取A，B**

```python
def load_matrix(file_path):
    matrix = {}
    with open(file_path, 'r') as file:
        for line in file:
            # 以空格为分隔，将每一行划分
            parts = line.strip().split(' ')
            if len(line) == 1:  # 如果是空行，跳过
                continue
            state = parts[0]
            observation = parts[1]
            probability = float(parts[2])
            if state not in matrix:
                matrix[state] = {}
            matrix[state][observation] = probability
    return matrix
```

**读取pi**

```python
# <----------------------------仿照读取A,B，读取pi并构造成一个我们想要的字典数据------------------->
def load_pi_matrix(file_path):
    matrix = {}
    with open(file_path, 'r') as file:
        for line in file:
            # 以空格为分隔，将每一行划分
            parts = line.strip().split(' ')
            if len(line) == 1:  # 如果是空行，跳过
                continue
            # 因为pi矩阵只有两列，所以只需要取两列数据
            state = parts[0]
            probability = float(parts[1])
            if state not in matrix:
                matrix[state] = {}
            matrix[state] = probability
    return matrix
```

#### 2.2 前向算法

```python
# <----------------------------根据公式，计算前向概率------------------->
def forward_algorithm(A, B, pi, observations):
    num_observations = len(observations)
    # 初始化前向概率
    forward_probabilities = {state: 0.0 for state in pi}
    for state in pi:
        if observations[0] in B[state]:
            forward_probabilities[state] = pi[state] * B[state][observations[0]]

    # 递推计算前向概率
    for t in range(1, num_observations):
        new_forward_probabilities = {state: 0 for state in pi}
        for j in pi:
            prob = 0
            for i in pi:
                if j in A[i]:
                    prob += forward_probabilities[i] * A[i][j]
            # 如果输入的句子中的词不在文档中出现过，则概率为0
            if observations[t] not in B[j]:
                new_forward_probabilities[j] = 0
            else:
                new_forward_probabilities[j] = prob * B[j][observations[t]]
        forward_probabilities = new_forward_probabilities

    # 终止条件：将前向概率相加
    sentence_probability = sum(forward_probabilities.values())

    return sentence_probability
```

#### 2.3 运行

```python
import jieba
# 从文本文件加载 A 矩阵
A = load_matrix("data/A.txt")
# 从文本文件加载 B 矩阵
B = load_matrix("data/B.txt")
# 从文本文件加载 π 矩阵
pi = load_pi_matrix("data/pi.txt")

# 输入句子
while True:
    x = input("输入预测的句子:")
    if x == '退出':
        break
    else:
        observations = jieba.lcut(x)  # 用合适的状态符号替代
        # 计算句子概率
        sentence_probability = forward_algorithm(A, B, pi, observations)
        print("句子概率:", sentence_probability)
```

