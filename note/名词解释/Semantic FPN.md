Alexander Kirillov, Ross Girshick, Kaiming He, and Piotr Doll´ar. Panoptic feature pyramid networks. In CVPR, pages 6399–6408, 2019. 2, 5, 6, 7, 8
[Panoptic Feature Pyramid Networks.pdf](obsidian://open?vault=notes&file=papers%2Ftools%2FPanoptic%20Feature%20Pyramid%20Networks.pdf)
[code](https://github.com/facebookresearch/detectron2)
## Panoptic Feature Pyramid Networks
Panoptic Segmentation（全景分割）,全景分割的本意就是将Instanse segmentation和semantic segmention进行一种联合，下面是效果的比较图:![[Pasted image 20231012212621.png]]
### 概念
* stuff（填充物）：画面中的背景如Sky、Road、Building在Panoptic Segmentation的方法下这一类事物实例ID将会忽略
* things：画面中识别的物体，物体不仅进行了语义分割还进行了实例检测
* panotic quality（PQ）：用于识别与分割以及东西与东西性能的详细分类，下面会详细介绍
* TP（true positives）：正确的标签与错误标签组成一组
* FN（false negatives）：漏报率
* FP（false positives）：错误的标签

###
Panoptic Segmentation：
* 这种方法对于图像中的每个像素打上两个标签，一个是分类标签一个是实例ID
* 将像素分为两类，stuff和things，stuff的实例ID会被忽略，具有相同标签和id的像素都属于同一个对象，对于无法确定的像素，比如不在分类范围内模糊的像素则会给一个void标签
* 