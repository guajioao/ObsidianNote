import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

B, C, H, W = 1, 2, 2, 2

# Create a sample tensor with random values
x_1 = [[[[-0.7472,  0.8429],
          [ 0.9171, -0.4057]],

         [[ 0.8640,  1.4267],
          [ 0.6618,  0.8815]]]]
# x_2 = [[[[1.,2.],
#          [1.,2.]],
#         [[3.,4.],
#          [3.,4.]]],
#         ]
# x_2 = [[[[1.,2.],
#          [1.,2.],
#          [1.,2.]],
#         [[1.,2.],
#          [3.,4.],
#          [3.,4.]]],
#         ]
x_2 = torch.randn(B, C, H, W)
x = torch.FloatTensor(x_1)
global_pooling = nn.AdaptiveAvgPool3d(output_size=(B,1,C))
x_avg = global_pooling(x).squeeze(1)

def multi_sim(x,sim):
    B, C, H, W = x.shape
    x_flat = x.reshape(B,C,1,H * W)  #B*C*(HW) -> B*C*1*(HW)
    sim = sim.unsqueeze(1) #B*1*HW*HW
    
    x_expand = x_flat.expand(B,C,sim.shape[2],sim.shape[3])

    sim_brod,x_brod = torch.broadcast_tensors(sim,x_expand)
    s_sum = torch.sum(sim, dim=2)
    sim_brod = torch.div(sim_brod , s_sum)

    # 计算x*sim
    f = sim_brod@x_brod # B,C,HW,HW
    # f = torch.diagonal(f,dim1=-2,dim2=-1) # 主对角线元素为xi与对应Wi的乘积之和
    
    # f = torch.div(f , s_sum)
    f = torch.diagonal(f,dim1=-2,dim2=-1) # 主对角线元素为xi与对应Wi的乘积之和
    # print(f)
    f = f.reshape(B,C,H,W)
    
    return f

def cal_selfSim(x):
    # B,C,H,W = x.shape   # B,C*H*W
    x_orisin = x
    x = x.reshape(x.shape[0],x.shape[1],x.shape[2] * x.shape[3]) #B*C*(HW) -> B*(HW)*C

    # 归一化x后相乘，计算相似度
    x_norm = F.normalize(x, p=2, dim=1) # 在C这一维度归一化?
    # x_norm = x
    x_t = x_norm.permute(0, 2, 1) 
    x_sim = torch.einsum('bcl,bnc->bnl',x_norm,x_t)

    # x_sim = torch.mm(x_norm, x_norm.t())
    # print(x_sim.shape)


    return x_sim

def cal_simMap(f,x_avg):
    B,C,H,W = f.shape   # B,C,H,W
    # B,C = x_avg
    # print(x_avg.shape)

    # 计算x与x_avg的相似度
    f_norm = F.normalize(f, p=2, dim=1)
    x_avg_norm = F.normalize(x_avg, p=2, dim=2)

    sim_map = torch.einsum('bchw,bkc->bkhw',f_norm,x_avg_norm)

    return sim_map


x_sim = cal_selfSim(x)
f = multi_sim(x,x_sim)
sim_map = cal_simMap(f,x_avg)


print("x:")
print(x)
print("x_avg:")
print(x_avg)
print("sim_map between x's patch:")
print(x_sim)
print("f:")
print(f)
print("sim_map between f and x_avg:")
print(sim_map)