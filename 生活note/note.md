git remote add origin https://github.com/guajioao/ObsidianNote.git


	* 今天回顾了一下CESL，作者提到因为是用pm来监督cm的生成，而cm对pm的作用主要是抑制非显著区域。导致如果pm的生成效果不好，显著区域出现缺失的情况，cm是无法补回来的。我就想，那这样就不能用pm来监督cm的生成了，因为只会越训练mask越少。能不能直接用cm mask的图像类别识别结果来自监督？就是cm的mask效果越好分类结果越正确这样。然后sm参与了cm的生成过程，相当于sm对cm也有一个提升作用。但是又感觉CLIP分类准确度的提高与细节不一定有关系？这样又会出现细节不足的情况，作者设置了pm就是因为比cm细节信息更多


看了这些22年的论文之后回顾之前看的SAN和ZegCLIP，发现这两篇论文里，SAN通过attention bias计算sls,再跟文本特征计算相似度获得掩码的分类，而不用mask或crop图像之后再识别图像分类，直接绕过了masked图像的识别误差问题。ZegCLIP使用Scale层的输出作为掩码的来源这个是不是一个创新点？感觉也相当于一个相似度的计算结果，就是用Decoder来获得T和H的相关度这样，这个算新么？跟DenseCLIP的分数图有点像又感觉不太一样

我后面比较了一下这些论文给出的结果，在这两个有共同测试的数据集上ZegCLIP的表现没有SAN效果好。但是SAN是完全监督的，ZegCLIP只用了seen类的掩码训练。就感觉没办法比较SAN对unseen类的效果。SAN里面统计了VOC和PC-59的label相似度分别为0.91和0.86，在这两个数据集上两个论文都做了实验，SAN是比ZegCLIP高的，在VOC上高了大约8%，在PC上就只高了3.3了。感觉是不是还是可以说明ZegCLIP在unseen类上的识别效果比SAN更好，SAN的综合效果比ZegCLIP好一点？

Transformer对Seq2Seq问题的效果很好，然后我就想，图像分割是不是也可以看成一个对于输入图像转成mask序列的问题？比如语音翻译是一段音频转成文本序列，而语义分割是图像像素->一组0~N的mask序列

































