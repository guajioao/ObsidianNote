denseclip代码中初始化decode_head时用到了这个参数
![[Pasted image 20231014102614.png]]
解释：
* from: https://zhuanlan.zhihu.com/p/87572724?from_voters_page=true
* 上采样层 (upsample layer)，是语义分割等密集输出 (dense prediction) 任务的必备组件。
* 一般默认选择双线性插值 (bilinear) 或者最近邻 (nearest) 的方式。这两种方式在 pytorch 的 interpolate 函数中均有实现。
* bilinear 情况下，会伴随一个选项 align_corners，默认为 False
* false和true的对比：
	* align_corners=True：每个**像素的**在矩阵里的**下标i,j**被**直接视作**坐标系里的一个个的**坐标点**进行计算。
	* align_corners=False：每个**像素被视为**一个个**1×1大小的小方块**，此时**像素的坐标**并不是图像矩阵所对应的下标，而是**需要将下标i,j各加上0.5**才是此时每个像素在坐标系里的坐标。
	* ![[Pasted image 20231014142746.png]]
	* 左边为false的情况下，对边角不友好。在目标检测时，因为**少有物体中心出现在边角，所以影响不大**，且**False 带来的整数倍上下采样，又方便了坐标值的计算**
	* 但是对于语义分割，边角像素也要纳入mIoU的计算，会对最终的精度造成影响，因此**语义分割时一般采用align_corners=True**的设置
