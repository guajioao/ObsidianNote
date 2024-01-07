
收录于：


## 摘要：


## 目录：

* [[#结构]]
* [[#一、引言 Introduction]]
* [[#二、相关工作 Related Work]]
* [[#三、方法 Method]]
* [[#四、实现细节]]
* [[#五、实验结果]]
* [[#六、结论]]

## 结构
* 结构：
	* ![[Pasted image 20231224155842.png|475]]
* teacher与student网络的架构相同，但参数不同。
	* teacher网络的输出以batch的均值为中心
	* 每个网络都输出一个K维特征，使用一个温度softmax在特征维度进行归一化，然后计算交叉熵损失
	* teacher网络stop gradient，参数更新通过学生参数的an exponential moving average (ema)指数移动平均来更新
		* gt.params = *l* \* gt.params + (1- *l* )\* gs.params\ 
		* *l* 是动量参数

## 一、引言 Introduction


## 二、相关工作 Related Work


## 三、方法 Method


## 四、实现细节


## 五、实验结果


## 六、结论

