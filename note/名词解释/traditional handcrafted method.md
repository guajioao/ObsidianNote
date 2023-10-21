Zhu, C., Li, G., Wang, W., Wang, R.: An Innovative Salient Object Detection using Center-Dark Channel Prior. In: Proceedings of the IEEE International Conference on Computer Vision Workshops, pp. 1509–1515 (**2017**)

摘要：Saliency detection aims to detect the most attractive objects in images, which has been widely used as a foundation for various multimedia applications. In this paper, we propose a novel salient object detection algorithm for RGB-D images using center-dark channel prior. First, we generate an initial saliency map based on a color saliency map and a depth saliency map of a given RGB-D image. Then, we generate a center-dark channel map based on a center saliency prior and a dark channel prior. Finally, we fuse the initial saliency map with the center dark channel map to generate the final saliency map. The proposed algorithm is evaluated on two public RGB-D datasets, and the experimental results show that our method outperforms the state-of-the-art methods.
1. 基于给定RGB-D图像的color saliency map和depth saliency map生成初始initial saliency map
2. 基于一个中心显著先验center saliency prior和dark channel prior生成一个center-dark channel map
3. 融合initial saliency map与center-dark channel map，产生最终的显著图

这个？传统架构：
![[Pasted image 20231015104301.png]]