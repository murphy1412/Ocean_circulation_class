# Ocean_circulation_class
此仓库用于存放海洋环流与生化效应课程报告的相关代码

代码说明

CanESM5.py用于计算CanESM5模式的OHC；

UKESM1-0-LL.py用于计算UKESM1-0-LL模式的OHC；

ESM1-2-LR.py用于计算MPI-ESM1-2-LR模式的OHC；

UKESM1-members.py是计算模式UKESM1-0-LL的四个实验成员的专门代码，成员包括r1i1p1f2、r2i1p1f2、r3i1p1f2、r4i1p1f2，并绘制下图：
<img width="1108" height="686" alt="image" src="https://github.com/user-attachments/assets/d2e44181-95bb-4aa3-bc30-8b172dba177a" />

all_CMIP6.py用于计算各个模式的OHC的趋势以及海洋净吸热率，包含三种模式的图像绘制：
<img width="1108" height="382" alt="image" src="https://github.com/user-attachments/assets/562e4b63-bb63-4254-a6dd-29f98bf20c7e" />




thermosteric_sea_level.py用于计算热膨胀海平面

sh_trend_calculation.py用于计算热膨胀海平面的趋势以及热膨胀海平面时序图的代码；同时也是绘制thetao时序变化图：

<img width="1108" height="438" alt="image" src="https://github.com/user-attachments/assets/75da99a0-e9aa-4170-a73e-da8d046a4145" />
<img width="599" height="450" alt="image" src="https://github.com/user-attachments/assets/aa3aabee-30bf-4f37-b0a5-7a5e49d4e78a" />

ssp585.py对应绘制下图：
<img width="1108" height="762" alt="image" src="https://github.com/user-attachments/assets/8ca0cf08-977f-4c4a-97bb-1482e76b5244" />



Can_deltaT_lat_dep.py用于计算CanESM5模式的位温变化及对应的纬度、深度；

MPI_deltaT_lat_dep_v2.py用于计算MPI-ESM1-2-LR模式的位温变化及对应的纬度、深度

UK_deltaT_lat_dep.py用于计算UKESM1-0-LL模式的位温变化及对应的纬度、深度；

plot_deltaT.py用于绘制三个模式的位温变化随纬度、深度分布，如下图：
<img width="2886" height="3759" alt="79e3fc3cc6070bd5d18c4c6e1b2a7b16" src="https://github.com/user-attachments/assets/0cdeaf31-e29e-4c18-a9c2-09af6d363a6c" />




Can_alpha_deltaT_lat_lon.py用于计算CanESM5模式的热膨胀系数乘位温变化αΔT的各格点值；

Can_alpha_deltaT_lat_dep.py基于上一步对CanESM5模式的αΔT进行经度平均及纬度处理；

MPI_alpha_deltaT_lat_lon.py、MPI_alpha_deltaT_lat_dep.py和alpha_deltaT_lat_lon.py、UK_alpha_deltaT_lat_dep_v2.py分别用于对MPI-ESM1-2-LR和UKESM1-0-LL模式进行上述类似处理；

plot_alpha_deltaT.py用于绘制三个模式的αΔT随纬度、深度的分布，如图：
<img width="2885" height="3759" alt="e1f14f4fbf67eb4ec7d3d22de30d3d26" src="https://github.com/user-attachments/assets/593789e2-32d5-487d-8d46-54206ee8015c" />


















