* UNet
* Deeplab
	* 提高感受野
	* v1版本利用空洞卷积'atrous'(with holes)而不是maxpooling
		* ![[Pasted image 20250914150556.png]]
		* (左) 传统卷积 (右) 空洞卷积
		* ![[Pasted image 20250914150915.png]]
		* 设置空洞卷积参数dilated (3x3, 7x7, 15x15)
	* v2提出ASPP(atrous convolution SPP)层
		* 在SPP中引入空洞卷积
			* ![[Pasted image 20250914154025.png]]
	* v3改进了ASPP模块
		* ![[Pasted image 20250914152636.png]]
		* 1个1x1卷积，3个3x3不同dilated的空洞卷积，全局平均池化
	* deeplabv3+
		* 
* 【SPPNet中提出】SPP层 - 不限制输入大小，均生成固定尺寸的输出
		* ![[Pasted image 20250914152116.png]]
		* 前面正常提取特征，进入该层时：（1）划分为16/4/1个区域，每个区域做maxpooling （2）得到固定的（16+4+1）x 256大小的输出