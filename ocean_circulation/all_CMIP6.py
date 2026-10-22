##############################读取所有计算所得的OHC数据，并按分层绘制图像###################
import pandas as pd
import xarray as xr
area1= xr.open_dataset(r"D:\Class_data\Ocean_circulation_class\areacello_Ofx_CanESM5_historical_r1i1p1f1_gn.nc")
area_CanESM5=area1['areacello'].sum().values

area2= xr.open_dataset(r"D:\Class_data\Ocean_circulation_class\areacello_Ofx_MPI-ESM1-2-LR_historical_r1i1p1f1_gn.nc")
area_ESM1_2_LR=area1['areacello'].sum().values

area_UKESM1=360978505166143.56
df=pd.read_csv(r'D:\Class_data\Code\OHC_global_time_series.csv',sep=',',encoding='utf-8')


# print(df)
time=df['year'][49:]
CanESM5_700m=df['CanESM5 700m'][49:]
CanESM5_700_2000m=df['CanESM5 700-2000m'][49:]
CanESM5_2000m=df['CanESM5 2000m'][49:]
CanESM5_0_2000m=df['CanESM5 0_2000m'][49:]

ESM1_2_LR_700m=df['MPI-ESM1-2-LR 700m'][49:]
ESM1_2_LR_700_2000m=df['MPI-ESM1-2-LR 700-2000m'][49:]
ESM1_2_LR_2000m=df['MPI-ESM1-2-LR 2000m'][49:]
ESM1_2_LR_0_2000m=df['MPI-ESM1-2-LR 0_2000m'][49:]

UKESM1_0_LL_700m=df['UKESM1-0-LL 700m'][49:]
UKESM1_0_LL_700_2000m=df['UKESM1-0-LL 700-2000m'][49:]
UKESM1_0_LL_2000m=df['UKESM1-0-LL 2000m'][49:]
UKESM1_0_LL_0_2000m=df['UKESM1-0-LL 0_2000m'][49:]

# ensemble_700m=df['ensemble_700m'].values
# ensemble_700_2000m=df['ensemble_700_2000m'].values
# ensemble_0_2000m=df['ensemble_0_2000m'].values
# ensemble_2000m=df['ensemble_2000m'].values

# import numpy as np
# OHC_700_all=np.column_stack([CanESM5_700m, ESM1_2_LR_700m, UKESM1_0_LL_700m])
# OHC_700_mean=OHC_700_all.mean(axis=1)
# ##计算每年平均后的std
# std=OHC_700_all.std(axis=1, ddof=0)
# ####90置信区间
# lower_700=OHC_700_mean-1.65*std
# upper_700=OHC_700_mean+1.65*std
#
#
# OHC_700_2000_all=np.column_stack([CanESM5_700_2000m, ESM1_2_LR_700_2000m, UKESM1_0_LL_700_2000m])
# OHC_700_2000_mean=OHC_700_2000_all.mean(axis=1)
# ##计算每年平均后的std
# std=OHC_700_2000_all.std(axis=1, ddof=0)
# ####90置信区间
# lower_700_2000=OHC_700_2000_mean-1.65*std
# upper_700_2000=OHC_700_2000_mean+1.65*std
#
#
# OHC_0_2000_all=np.column_stack([CanESM5_0_2000m, ESM1_2_LR_0_2000m, UKESM1_0_LL_0_2000m])
# OHC_0_2000_mean=OHC_0_2000_all.mean(axis=1)
# ##计算每年平均后的std
# std=OHC_0_2000_all.std(axis=1, ddof=0)
# ####90置信区间
# lower_0_2000=OHC_0_2000_mean-1.65*std
# upper_0_2000=OHC_0_2000_mean+1.65*std
#
#
# OHC_2000_all=np.column_stack([CanESM5_2000m, ESM1_2_LR_2000m, UKESM1_0_LL_2000m])
# OHC_2000_mean=OHC_2000_all.mean(axis=1)
# ##计算每年平均后的std
# std=OHC_2000_all.std(axis=1, ddof=0)
# ####90置信区间
# lower_2000=OHC_2000_mean-1.65*std
# upper_2000=OHC_2000_mean+1.65*std

# #1年划算为s
sec=1*365*24*3600
#海洋表面积为
A=3.6*(10**14)
print(A)
from scipy.stats import linregress
results=linregress(time,CanESM5_2000m)
k_recoun=results.slope
b_recoun=results.intercept
recoun_std = results.stderr
print(f"2005-2014年CanESM5_2000m OHC trend:{k_recoun},std:{recoun_std},lower:{k_recoun-1.65*recoun_std},upper:{k_recoun+1.65*recoun_std},90%CI:{1.65*recoun_std}")
CI90=recoun_std*1.65
###换算为W
k=k_recoun/(sec*area_CanESM5)
CI90=CI90/(sec*area_CanESM5)
print(f"k={k:.2f},CI90={CI90:.2f}")

results=linregress(time,ESM1_2_LR_2000m)
k_recoun=results.slope
b_recoun=results.intercept
recoun_std = results.stderr
print(f"2005-2014年ESM1_2_LR_2000m OHC trend:{k_recoun},std:{recoun_std},lower:{k_recoun-1.65*recoun_std},upper:{k_recoun+1.65*recoun_std},90%CI:{1.65*recoun_std}")
CI90=recoun_std*1.65
k=k_recoun/(sec*area_ESM1_2_LR)
CI90=CI90/(sec*area_ESM1_2_LR)
print(f"k={k:.2f},CI90={CI90:.2f}")

results=linregress(time,UKESM1_0_LL_2000m)
k_recoun=results.slope
b_recoun=results.intercept
recoun_std = results.stderr
print(f"2005-2014年UKESM1_0_LL_2000m OHC trend:{k_recoun},std:{recoun_std},lower:{k_recoun-1.65*recoun_std},upper:{k_recoun+1.65*recoun_std},90%CI:{1.65*recoun_std}")
CI90=recoun_std*1.65
k=k_recoun/(sec*area_UKESM1)
CI90=CI90/(sec*area_UKESM1)
print(f"k={k:.2f},CI90={CI90:.5f}")

#
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import font_manager
# # fig, axs = plt.subplots(2, 2, figsize=(10,6), sharex=True)
# # fontsize_axis = 14
# # fontsize_tick = 12
# # plt.rcParams['font.family'] = 'Times New Roman'
# # #
# # axs[0,0].plot(time, CanESM5_700m, color='crimson',label='CanESM5')
# # axs[0,0].plot(time, ESM1_2_LR_700m, color='blue', label='MPI-ESM1-2-LR')
# # axs[0,0].plot(time, UKESM1_0_LL_700m, color='green',label='UKESM1-0-LL')
# # axs[0,0].set_ylabel("OHC [J]", fontsize=16,fontname='Times New Roman')
# # xticks_position=np.arange(1958,2015,10)
# # axs[0,0].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# # # axs[0].set_yticklabels(axs[0].get_yticks(),fontsize=14, fontname='Times New Roman')
# #
# # axs[0,1].plot(time, CanESM5_700_2000m, color='crimson',label='CanESM5')
# # axs[0,1].plot(time, ESM1_2_LR_700_2000m, color='blue', label='MPI-ESM1-2-LR')
# # axs[0,1].plot(time, UKESM1_0_LL_700_2000m, color='green',label='UKESM1-0-LL')
# # xticks_position=np.arange(1958,2015,10)
# # axs[0,1].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# # # axs[1].set_yticklabels(axs[1].get_yticks(),fontsize=14, fontname='Times New Roman')
# #
# # axs[1,0].plot(time, CanESM5_0_2000m, color='crimson',label='CanESM5')
# # axs[1,0].plot(time, ESM1_2_LR_0_2000m, color='blue', label='MPI-ESM1-2-LR')
# # axs[1,0].plot(time, UKESM1_0_LL_0_2000m, color='green',label='UKESM1-0-LL')
# # axs[1,0].set_ylabel("OHC [J]", fontsize=16,fontname='Times New Roman')
# # xticks_position=np.arange(1958,2015,7)
# # axs[1,0].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# #
# # axs[1,1].plot(time, CanESM5_2000m, color='crimson',label='CanESM5')
# # axs[1,1].plot(time, ESM1_2_LR_2000m, color='blue', label='MPI-ESM1-2-LR')
# # axs[1,1].plot(time, UKESM1_0_LL_2000m, color='green',label='UKESM1-0-LL')
# # xticks_position=np.arange(1958,2015,7)
# # axs[1,1].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
#
#
#
# ##############################绘制ensemble mean的时序图##############################
# fig, ax = plt.subplots()
# import matplotlib.ticker as ticker
# formatter = ticker.ScalarFormatter(useMathText=True)
# formatter.set_powerlimits((22, 22)) # 强制科学计数法为 10^22
# ax.yaxis.set_major_formatter(formatter)
# ax.yaxis.get_offset_text().set_text(r'$10^{22}$') # 强制覆盖偏移文本为 10^22
# offset_text = ax.yaxis.get_offset_text()
# offset_text.set_fontfamily('Times New Roman')
#
# plt.plot(time, OHC_700_mean, color='crimson',label='0_700m')
# plt.plot(time, OHC_700_2000_mean, color='blue',label='700_2000m')
# plt.plot(time, OHC_0_2000_mean, color='purple',label='0_2000m')
# plt.plot(time, OHC_2000_mean, color='yellow',label='>2000m')
# plt.ylabel("OHC [J]", fontsize=16,fontname='Times New Roman')
# xticks_position=np.arange(1958,2015,7)
# plt.xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# plt.yticks(fontsize=14, fontname='Times New Roman')
# plt.fill_between(time, lower_700, upper_700, color='crimson', alpha=0.1)
# plt.fill_between(time, lower_700_2000, upper_700_2000, color='blue', alpha=0.1)
# plt.fill_between(time, lower_0_2000, upper_0_2000, color='purple', alpha=0.1)
# plt.fill_between(time, lower_2000, upper_2000, color='yellow', alpha=0.2)
#
# plt.legend(prop=font_manager.FontProperties(fname=None,family='Times New Roman',size=12),loc='upper left')
# # axs[0,1].plot(time, OHC_700_2000_mean, color='crimson',label='700_2000m')
# # xticks_position=np.arange(1958,2015,10)
# # axs[0,1].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# # # axs[1].set_yticklabels(axs[1].get_yticks(),fontsize=14, fontname='Times New Roman')
# # axs[0,1].fill_between(time, lower_700_2000, upper_700_2000, color='grey', alpha=0.3)
# #
# # axs[1,0].plot(time, OHC_0_2000_mean, color='crimson',label='0_2000m')
# # xticks_position=np.arange(1958,2015,7)
# # axs[1,0].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# # axs[1,0].fill_between(time, lower_0_2000, upper_0_2000, color='grey', alpha=0.3)
# #
# # axs[1,1].plot(time, OHC_2000_mean, color='crimson',label='>2000m')
# # xticks_position=np.arange(1958,2015,7)
# # axs[1,1].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# # axs[1,1].fill_between(time, lower_2000, upper_2000, color='grey', alpha=0.3)
# # # plt.fill_between(time, lower, upper, color='grey', alpha=0.3)
# # # plt.plot(time, sl_mean, label='MPI-ESM1-2-LR',color='grey')
# #
#
# plt.show()





















