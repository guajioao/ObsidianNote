
收录于：ECCV2020
End-to-End Object Detection with Transformers
Detection Transformer (DETR)
Transformer在目标检测领域的成功应用
[code](https://github.com/encounter1997/SFA)

## 结构
* Overview
	* ![[Pasted image 20231122220228.png]]
	* 直接平行的预测多个目标候选框，与类别不匹配的会被归类到no object
* DETR结构图
	* ![[Pasted image 20231124202516.png]]
	* Backbone(CNN)提取特征图
	* 特征图被拉直+位置编码作为Transformer encoder的输入
	* Transformer decoder的输入为一组固定数量的可学习位置编码，即object queries
	* encoder的输出作为cross attention层的输入


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

