#####################计算热膨胀海平面趋势的代码(时间范围为1958-2014)#########
#################该程序用来计算各分量的trend map######################
import font_manager
import pandas as pd
import numpy as np
df=pd.read_csv(r'D:\Class_data\Code\thetao_UKEMSL.csv',encoding='utf-8')
print(df.head())
time=df['year'].values

thetao1=df['thetao_r1ip1f2'].values
thetao2=df['thetao_r2ip1f2'].values
thetao3=df['thetao_r3ip1f2'].values
thetao4=df['thetao_r4ip1f2'].values

# ESM1_sh=df['MPI-ESM1-2-LR'].values
# CanESM5=df['CanESM5'].values
# UKESM1=df['UKESM1'].values
#
# CanESM5_700m=df['CanESM5 0_700m']
# CanESM5_700_2000m=df['CanESM5 700_2000m']
# CanESM5_2000m=df['CanESM5 2000m']
# CanESM5_0_2000m=df['CanESM5 0_2000m']
#
# ESM1_2_LR_700m=df['MPI-ESM1-2-LR 0_700m']
# ESM1_2_LR_700_2000m=df['MPI-ESM1-2-LR 700_2000m']
# ESM1_2_LR_2000m=df['MPI-ESM1-2-LR 2000m']
# ESM1_2_LR_0_2000m=df['MPI-ESM1-2-LR 0_2000m']
#
# UKESM1_0_LL_700m=df['UKESM1 0_700m']
# UKESM1_0_LL_700_2000m=df['UKESM1 700_2000m']
# UKESM1_0_LL_2000m=df['UKESM1 2000m']
# UKESM1_0_LL_0_2000m=df['UKESM1 0_2000m']

######模式平均ensemble mean######
# ####以下代码是将三个CMPI6模式叠成(time, 3)的二维数组
# sl_all=np.column_stack([ESM1_2_LR_700m, CanESM5_700m, UKESM1_0_LL_700m])
# sl_mean=sl_all.mean(axis=1)
# ##计算每年平均后的std
# std=sl_all.std(axis=1, ddof=0)
# ####90置信区间
# lower=sl_mean-1.65*std
# upper=sl_mean+1.65*std
# # print(lower,upper)

# #############计算热膨胀海平面的trend########################
# from scipy.stats import linregress
# results=linregress(time,sl_mean)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年sl_mean_700m trend:{k_recoun:.2f},std:{recoun_std:.2f},lower:{k_recoun-1.65*recoun_std:.2f},upper:{k_recoun+1.65*recoun_std:.2f},90%CI:{1.65*recoun_std:.2f}")

# from scipy.stats import linregress
# results=linregress(time,CanESM5_700_2000m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年CanESM5_700_2000m trend:{k_recoun:.2f},std:{recoun_std:.2f},lower:{k_recoun-1.65*recoun_std:.2f},upper:{k_recoun+1.65*recoun_std:.2f},90%CI:{1.65*recoun_std:.2f}")
#
# from scipy.stats import linregress
# results=linregress(time,CanESM5_2000m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年CanESM5_2000m trend:{k_recoun:.2f},std:{recoun_std:.2f},lower:{k_recoun-1.65*recoun_std:.2f},upper:{k_recoun+1.65*recoun_std:.2f},90%CI:{1.65*recoun_std:.2f}")
#
# from scipy.stats import linregress
# results=linregress(time,ESM1_2_LR_700m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年ESM1_2_LR_700m trend:{k_recoun:.2f},std:{recoun_std:.2f},lower:{k_recoun-1.65*recoun_std:.2f},upper:{k_recoun+1.65*recoun_std:.2f},90%CI:{1.65*recoun_std:.2f}")
#
# from scipy.stats import linregress
# results=linregress(time,ESM1_2_LR_700_2000m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年ESM1_2_LR_700_2000m trend:{k_recoun:.2f},std:{recoun_std:.2f},lower:{k_recoun-1.65*recoun_std:.2f},upper:{k_recoun+1.65*recoun_std:.2f},90%CI:{1.65*recoun_std:.2f}")
#
# from scipy.stats import linregress
# results=linregress(time,ESM1_2_LR_2000m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年ESM1_2_LR_2000m trend:{k_recoun:.2f},std:{recoun_std:.2f},lower:{k_recoun-1.65*recoun_std:.2f},upper:{k_recoun+1.65*recoun_std:.2f},90%CI:{1.65*recoun_std:.2f}")
#
# from scipy.stats import linregress
# results=linregress(time,UKESM1_0_LL_700m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年UKESM1_0_LL_700m trend:{k_recoun:.2f},std:{recoun_std:.2f},lower:{k_recoun-1.65*recoun_std:.2f},upper:{k_recoun+1.65*recoun_std:.2f},90%CI:{1.65*recoun_std:.2f}")
#
# from scipy.stats import linregress
# results=linregress(time,UKESM1_0_LL_700_2000m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年UKESM1_0_LL_700_2000m trend:{k_recoun:.5f},std:{recoun_std:.5f},lower:{k_recoun-1.65*recoun_std:.5f},upper:{k_recoun+1.65*recoun_std:.5f},90%CI:{1.65*recoun_std:.5f}")
#
# from scipy.stats import linregress
# results=linregress(time,UKESM1_0_LL_2000m)
# k_recoun=results.slope
# b_recoun=results.intercept
# recoun_std = results.stderr
# print(f"1993-2014年UKESM1_0_LL_2000m trend:{k_recoun:.5f},std:{recoun_std:.5f},lower:{k_recoun-1.65*recoun_std:.5f},upper:{k_recoun+1.65*recoun_std:.5f},90%CI:{1.65*recoun_std:.5f}")

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
xticks_position=np.arange(1958,2015,7)
# plt.fill_between(time, lower, upper, color='grey', alpha=0.3)
# plt.plot(time, CanESM5, label='CanESM5',color='crimson')
# plt.plot(time, ESM1_sh, label='MPI-ESM1-2-R', color='blue')
# plt.plot(time, UKESM1, label='UKESM1-0-LL',color='green')
# plt.xlabel("year",fontsize=16,fontname='Times New Roman')
# plt.ylabel("thermosteric sea level [mm]",fontsize=16,fontname='Times New Roman')

##############绘制thetao###############
plt.plot(time,thetao1, label='r1ip1f2',color='black')
plt.plot(time,thetao2, label='r2ip1f2',color='crimson')
plt.plot(time,thetao3, label='r3ip1f2',color='blue')
plt.plot(time,thetao4, label='r4ip1f2',color='green')
plt.ylabel("thetao [℃]",fontsize=16,fontname='Times New Roman')
plt.xlabel("year",fontsize=16,fontname='Times New Roman')
plt.xticks(xticks_position,fontsize=14, fontname='Times New Roman')
plt.yticks(fontsize=14, fontname='Times New Roman')
plt.legend(prop=font_manager.FontProperties(fname=None,family='Times New Roman',size=12),loc='upper left')
plt.tight_layout()
plt.show()






