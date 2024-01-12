Graph Cut（图形切割）应用于计算机视觉领域，用来有效的解决各种低级计算机视觉问题，例如图像平滑（image smoothing）、立体应对问题（stereo correspondence problem）、图像分割（image segmentation）等等
GraphCut利用最小割最大流算法进行图像的分割，可以将图像分割为前景和背景。使用该算法时需要在前景和背景处各画几笔作为输入，算法将建立各个像素点与前景背景相似度的赋权图，并通过求解最小切割区分前景和背景。算法效果图如下：
原图：![[Pasted image 20240112100621.png]]
标注：![[Pasted image 20240112100636.png]]
分割：![[Pasted image 20240112100656.png]]
