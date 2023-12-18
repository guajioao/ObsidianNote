ASPP（Atrous Spatial Pyramid Pooling）,空洞空间卷积池化金字塔。简单理解就是个升级版池化层，其目的与普通的池化层一致，尽可能地去提取特征。结构如下：
![[Pasted image 20230925205247.png]]
* 1x1卷积（最左绿色块）
* 3个池化卷积，膨胀因子可以自定义（中间三个蓝色块）
* ASPP Pooling（）最右三层
### ASPP Conv
* 空洞卷积层与一般卷积间的差别在于膨胀率，膨胀率控制的是卷积时的 padding 以及 dilation。通过不同的填充以及与膨胀，可以获取不同尺度的感受野，提取多尺度的信息。
* 卷积核始终为3x3
```python
class ASPPConv(nn.Sequential):
    def __init__(self, in_channels, out_channels, dilation):
        modules = [
            nn.Conv2d(in_channels, out_channels, 3, padding=dilation, dilation=dilation, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU()
        ]
        super(ASPPConv, self).__init__(*modules)
```

### ASPP Pooling
ASPP Polling 首先是一个 `AdaptiveAvgPool2d` 层。所谓自适应均值池化，其自适应的地方在于**不需要**指定**kernel size 和 stride**，**只需**指定最后的**输出尺寸**（此处为 1×1）。
* 通过将各通道的特征图分别压缩至 1×1，从而提取各通道的特征，进而获取全局的特征
* 然后是一个 1×1 的卷积层，对上一步获取的特征进行进一步的提取，并降维
* 需要注意的是，在 ASPP Polliing 的网络结构部分，只是对特征进行了提取；而在 forward 方法中，除了顺序执行网络的各层外，最终还将特征图从1×1 上采样回原来的尺寸
```python
class ASPPPooling(nn.Sequential):
	def __init__(self, in_channels, out_channels):
	    super(ASPPPooling, self).__init__(
	        nn.AdaptiveAvgPool2d(1),
	        nn.Conv2d(in_channels, out_channels, 1, bias=False),
	        nn.BatchNorm2d(out_channels),
	        nn.ReLU())
	        
	def forward(self, x):
	   size = x.shape[-2:]
	   for mod in self:
	       x = mod(x)
	   return F.interpolate(x, size=size, mode='bilinear', align_corners=False)

```

### ASPP
1. 最开始是一个 1×1 的卷积层，进行降维；
2. 构建 “池化金字塔”。对于给定的膨胀因子 atrous_rates，叠加相应的空洞卷积层，提取不同尺度下的特征；
3. 添加空洞池化层；
4. 出层，用于对ASPP各层叠加后的输出，进行卷积操作，得到最终结果；
5. forward() 方法，其顺序执行ASPP的各层，将各层的输出按通道叠加，并通过输出层的 conv -> bn -> relu -> dropout 降维至给定通道数，获取最终结果。
```python
class ASPP(nn.Module):
    def __init__(self, in_channels, atrous_rates, out_channels=256):
        super(ASPP, self).__init__()
        modules = []
        # 注释 1
        modules.append(nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU()))

        # 注释 2
        rates = tuple(atrous_rates)
        for rate in rates:
            modules.append(ASPPConv(in_channels, out_channels, rate))

        # 注释 3
        modules.append(ASPPPooling(in_channels, out_channels))

        self.convs = nn.ModuleList(modules)
        
        # 注释 4
        self.project = nn.Sequential(
            nn.Conv2d(len(self.convs) * out_channels, out_channels, 1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Dropout(0.5))
    
    # 注释 5
    def forward(self, x):
        res = []
        for conv in self.convs:
            res.append(conv(x))
        res = torch.cat(res, dim=1)
        return self.project(res)

```
