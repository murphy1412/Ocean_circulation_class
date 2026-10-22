#################################3该程序用于探讨模式数据UKESM1-0-LL1993年前出现异常的原因#########################
import xarray as xr
import glob
# so_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\New_UKESM1-0-LL\so_Omon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc"))
# s_all = xr.open_mfdataset(so_files, combine='by_coords')
# # print(s_all)
# so_A=s_all['so'].sel(time=slice("1958-01-16", "2014-12-16"))
# print(so_A.shape)
# print(s_all['lev_bnds'].sel(lev=slice(600,2000)).values)
# print(s_all['lev_bnds'].values)

th_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\New_UKESM1-0-LL\thetao_Omon_UKESM1-0-LL_historical_r5i1p1f3_gn_*.nc"))
th_all = xr.open_mfdataset(th_files, combine='by_coords')
v_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\New_UKESM1-0-LL\volcello_Omon_UKESM1-0-LL_historical_r5i1p1f3_gn_*.nc"))
v_all = xr.open_mfdataset(v_files, combine='by_coords')
# print(s_all,th_all,v_all)
so_A=th_all['so'].sel(time=slice("1958-01-16", "2014-12-16"))
th_A=th_all['thetao'].sel(time=slice("1958-01-16", "2014-12-16"))
v_A=v_all['volcello'].sel(time=slice("1958-01-16", "2014-12-16"))
##求取年平均值
so_A=so_A.groupby("time.year").mean(dim="time", skipna=True)
th_A=th_A.groupby("time.year").mean(dim="time", skipna=True)
v_A=v_A.groupby("time.year").mean(dim="time", skipna=True)
print(th_A.shape,v_A)

delta_th_A=th_A-th_A.sel(year=slice(1981,2010)).mean('year')

##计算面积网格
dep_bnds=th_all['lev_bnds'].sel(time=slice("1958-01-16", "2014-12-16"))
dep_bnds=dep_bnds.groupby("time.year").mean(dim="time", skipna=True)
delta_dep=dep_bnds.isel(bnds=1)-dep_bnds.isel(bnds=0)
area=(v_A/delta_dep).mean(dim='lev').mean('year')      #sum(dim=['j','i'],skipna=True)
print(area.dims)
print(th_A.dims)

delta_th_A=delta_th_A.mean(dim='lev',skipna=True)
thetao_mean=(delta_th_A*area).sum(dim=['j','i'],skipna=True)/area.sum(dim=['j','i'],skipna=True)
print(thetao_mean.values)


rou = 1025.0
cp = 3990.0

# ohc_cell_700=(rou*cp*delta_th_A*v_A).sel(lev=slice(0,700)).sum(dim=['lev','j','i'],skipna=True)
# ohc_cell_700_2000=(rou*cp*delta_th_A*v_A).sel(lev=slice(700,2000)).sum(dim=['lev','j','i'],skipna=True)
# ohc_cell_2000=(rou*cp*delta_th_A*v_A).sel(lev=slice(2000,6000)).sum(dim=['lev','j','i'],skipna=True)
# ohc_cell_0_2000=(rou*cp*delta_th_A*v_A).sel(lev=slice(0,2000)).sum(dim=['lev','j','i'],skipna=True)

# print("700:",ohc_cell_700.values)
# # print("700-2000:",ohc_cell_700_2000.values)
# # print("2000:",ohc_cell_2000.values)
# # print("0_2000:",ohc_cell_0_2000.values)


# import pandas as pd
# df=pd.read_csv(r'D:\Class_data\Ocean_circulation_class\New_UKESM1-0-LL\UKESM1-members.csv',encoding='utf-8')
# print(df.head())
# time=df['year'].values
# UKESM1_0_LL_700m2=df['OHC_700m_r2i1p1f2']
# UKESM1_0_LL_700m1=df['OHC_700m_r1i1p1f2']
# UKESM1_0_LL_700m3=df['OHC_700m_r3i1p1f2']
# UKESM1_0_LL_700m4=df['OHC_700m_r4i1p1f2']
#
# UKESM1_0_LL_700_2000m1=df['OHC_700_2000m_r1i1p1f2']
# UKESM1_0_LL_700_2000m2=df['OHC_700_2000m_r2i1p1f2']
# UKESM1_0_LL_700_2000m3=df['OHC_700_2000m_r3i1p1f2']
# UKESM1_0_LL_700_2000m4=df['OHC_700_2000m_r4i1p1f2']
#
#
# UKESM1_0_LL_0_2000m1=df['OHC_0_2000m_r1i1p1f2']
# UKESM1_0_LL_0_2000m2=df['OHC_0_2000m_r2i1p1f2']
# UKESM1_0_LL_0_2000m3=df['OHC_0_2000m_r3i1p1f2']
# UKESM1_0_LL_0_2000m4=df['OHC_0_2000m_r4i1p1f2']
#
# UKESM1_0_LL_2000m1=df['OHC_2000m_r1i1p1f2']
# UKESM1_0_LL_2000m2=df['OHC_2000m_r2i1p1f2']
# UKESM1_0_LL_2000m3=df['OHC_2000m_r3i1p1f2']
# UKESM1_0_LL_2000m4=df['OHC_2000m_r4i1p1f2']
#
# UKESM1_0_LL_2000m2=df['OHC_2000m_r2i1p1f2']
#
# import numpy as np
# time=np.arange(1958,2015)
# import matplotlib.pyplot as plt
# from matplotlib import font_manager
# fig, axs = plt.subplots(2, 2, figsize=(10,6), sharex=True)
#
# fontsize_axis = 14
# fontsize_tick = 12
# plt.rcParams['font.family'] = 'Times New Roman'
#
# print(2)
#
# axs[0,0].plot(time, UKESM1_0_LL_700m1,label='r1i1p1f2', color='black')
# axs[0,0].plot(time, UKESM1_0_LL_700m2,label='r2i1p1f2',color='crimson')
# axs[0,0].plot(time, UKESM1_0_LL_700m3, label='r3i1p1f2',color='blue')
# axs[0,0].plot(time, UKESM1_0_LL_700m4, label='r4i1p1f2',color='green')
#
# # axs[0,0].plot(time, pacific_Steric, label='Steric',color='orange')
# # axs[0,0].plot(ayear, sla_AL_pacific, label='Altimetry',color='black')
# axs[0,0].set_ylabel("OHC [J]", fontsize=16,fontname='Times New Roman')
# axs[0,0].set_xlabel('year', fontsize=16, fontname='Times New Roman')
# xticks_position=np.arange(1958,2015,7)
# axs[0,0].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# axs[0,0].tick_params(axis='y', labelsize=14)
# for label in axs[0, 0].get_yticklabels():
#     label.set_fontname('Times New Roman')
#
# axs[0,1].plot(time, UKESM1_0_LL_700_2000m1,label='r1i1p1f2', color='black')
# axs[0,1].plot(time, UKESM1_0_LL_700_2000m2,label='r2i1p1f2',color='crimson')
# axs[0,1].plot(time, UKESM1_0_LL_700_2000m3, label='r3i1p1f2',color='blue')
# axs[0,1].plot(time, UKESM1_0_LL_700_2000m4, label='r4i1p1f2',color='green')
# xticks_position=np.arange(1958,2015,7)
# axs[0,1].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# axs[0,1].tick_params(axis='y', labelsize=14)
# for label in axs[0, 1].get_yticklabels():
#     label.set_fontname('Times New Roman')
#
# axs[1,0].plot(time, UKESM1_0_LL_0_2000m1,label='r1i1p1f2', color='black')
# axs[1,0].plot(time, UKESM1_0_LL_0_2000m2,label='r2i1p1f2',color='crimson')
# axs[1,0].plot(time, UKESM1_0_LL_0_2000m3, label='r3i1p1f2',color='blue')
# axs[1,0].plot(time, UKESM1_0_LL_0_2000m4, label='r4i1p1f2',color='green')
# axs[1,0].set_ylabel("OHC [J]", fontsize=16,fontname='Times New Roman')
# xticks_position=np.arange(1958,2015,7)
# axs[1,0].set_xticks(xticks_position,labels=xticks_position,fontsize=14, fontname='Times New Roman')
# axs[1,0].tick_params(axis='y', labelsize=14)
# for label in axs[1, 0].get_yticklabels():
#     label.set_fontname('Times New Roman')
#
# axs[1,1].plot(time, UKESM1_0_LL_2000m1,label='r1i1p1f2', color='black')
# axs[1,1].plot(time, UKESM1_0_LL_2000m2,label='r2i1p1f2',color='crimson')
# axs[1,1].plot(time, UKESM1_0_LL_2000m3, label='r3i1p1f2',color='blue')
# axs[1,1].plot(time, UKESM1_0_LL_2000m4, label='r4i1p1f2',color='green')
# # 设置坐标轴
# xticks_position=np.arange(1958,2015,7)
# plt.xticks(xticks_position,fontsize=14, fontname='Times New Roman')
# plt.yticks(fontsize=14, fontname='Times New Roman')
# plt.legend(prop=font_manager.FontProperties(fname=None,family='Times New Roman',size=12),loc='lower right')
#
# print(3)
# plt.show()












