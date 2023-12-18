所谓TTA，思想非常简单，就是在评测阶段，给每个输入进行多种数据增广变换，将一个输入变成多个输入，然后再merge起来一起输出，形成一种**ensemble**的效果，一方面可以提点，另一方面可以提升model calibration （ECE来评价）的效果，实现起来也是非常简单，可以直接用Pretrained model来做，相当环保。
问题来了，是否可以找出一个最优的组合策略？
文献2发表在UAI 2020，提出了一种贪心算法，固定增广步数，每一步都从整个增广空间里选一个使得Calibrated LL提升最大的增广方式。这种方法也是非常naive的，一定不是最优的，如paper title所言，是一种简单的baseline。如下图：![[Pasted image 20231029203651.png]]

文献3是文献2的一种改进，发表在NIPS 2020，提出了一种所谓Learning Loss的方法，如下图右图（左图是经典TTA）：![[Pasted image 20231029203813.png]]
本文的insight也非常简单，提出了一种基于loss prediction来select数据增广的方法，这里会多一步，需要训练一个DNN来做loss predictor，具体如下图：
![[Pasted image 20231029203834.png]]