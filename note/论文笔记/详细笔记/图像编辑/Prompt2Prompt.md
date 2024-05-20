PROMPT-TO-PROMPT IMAGE EDITING WITH CROSS-ATTENTION CONTROL

发表于：ICLR2023

## 结构
* Overview
	* ![[Pasted image 20240519161743.png]]
	* 图像特征作为Q，文本tokens作为K，相乘得到注意力图$M_t$
	* 注意力注入
		* 将原本句子中的某个词替换，得到新的注意力图$M_t^{*}$
		* 将原注意力图$M_t$注入新注意力图$M_t^{*}$中，替换与语义修改无关的部分
			* 【问题】如何判断的语义是否改变？修改前后的单词对应部分tokens就是改变了的语义
			* 【问题】为什么不是将$M_t^*$语义相关的部分注入$M_t$中？
	* 重新加权注意力图，控制修改的强弱程度
	* 一小部分(20%)自注意力的注入有助于保留原内容 
## 摘要：


## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]


## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

