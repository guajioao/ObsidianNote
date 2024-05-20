InstructPix2Pix: Learning to Follow Image Editing Instructions

发表于：CVPR2023

## 结构
![[Pasted image 20240520095813.png]]
* 主要的设计在于训练数据生成
* InstructPix2Pix模型
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

### 3.2.1 Classifier-free Guidance for Two Conditionings
* Classifier-free diffusion guidance
	* 常用于类别条件和文本条件图像的生成，以提高生成图像的视觉质量，使采样图像更加符合条件
* 实现方式
	* 联合训练有条件和无条件去噪的扩散模型，在推理时结合两个score estimates
* 


## 四、实现细节


## 五、实验结果


## 六、结论

