##############################数据ACCESS-ESM1-5计算OHC####################################

import xarray as xr
import glob
so_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\so_Omon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_*.nc"))
s_all = xr.open_mfdataset(so_files, combine='by_coords')
so_A=s_all['so'].sel(time=slice("1958-01-01", "2014-12-31"))
# print(s_all['lev_bnds'].sel(lev=slice(600,2000)).values)
# print(s_all['lev_bnds'].values)
# print(s_all)
th_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\thetao_Omon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_*.nc"))
th_all = xr.open_mfdataset(th_files, combine='by_coords')
v_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\volcello_Omon_ACCESS-ESM1-5_historical_r1i1p1f1_gn_*.nc"))
v_all = xr.open_mfdataset(v_files, combine='by_coords')
# print(s_all,th_all,v_all)
so_A=s_all['so'].sel(time=slice("1958-01-01", "2014-12-31"))
th_A=th_all['thetao'].sel(time=slice("1958-01-01", "2014-12-31"))
v_A=v_all['volcello'].sel(time=slice("1958-01-01", "2014-12-31"))
##求取年平均值
so_A=so_A.groupby("time.year").mean(dim="time", skipna=True)
th_A=th_A.groupby("time.year").mean(dim="time", skipna=True)
v_A=v_A.groupby("time.year").mean(dim="time", skipna=True)
print(v_A.shape,v_A)

delta_th_A=th_A-th_A.sel(year=slice(1981,2010)).mean('year')

rou = 1025.0
cp = 3990.0

ohc_cell_700=(rou*cp*delta_th_A*v_A).sel(lev=slice(0,700)).sum(dim=['lev','j','i'],skipna=True)
ohc_cell_700_2000=(rou*cp*delta_th_A*v_A).sel(lev=slice(700,2000)).sum(dim=['lev','j','i'],skipna=True)
ohc_cell_2000=(rou*cp*delta_th_A*v_A).sel(lev=slice(2000,6000)).sum(dim=['lev','j','i'],skipna=True)

print("700:",ohc_cell_700.values)
print("700-2000:",ohc_cell_700_2000.values)
print("2000:",ohc_cell_2000.values)

ohc_cell_700 = ohc_cell_700.compute()
ohc_cell_700_2000 = ohc_cell_700_2000.compute()
ohc_cell_2000 = ohc_cell_2000.compute()

import numpy as np
time=np.arange(1958,2015)
import matplotlib.pyplot as plt
from matplotlib import font_manager
fig, axs = plt.subplots(2, 2, figsize=(10,6), sharex=True)

fontsize_axis = 14
fontsize_tick = 12
plt.rcParams['font.family'] = 'Times New Roman'

print(2)
axs[0,0].plot(time, ohc_cell_700, label='0-700m',color='crimson')
axs[0,0].plot(time, ohc_cell_700_2000, label='700-2000m',color='blue')
axs[0,0].plot(time, ohc_cell_2000, label='>2000m',color='green')
# axs[0,0].plot(time, pacific_Steric, label='Steric',color='orange')
# axs[0,0].plot(ayear, sla_AL_pacific, label='Altimetry',color='black')
axs[0,0].set_ylabel("OHC [J]", fontsize=16,fontname='Times New Roman')
axs[0,0].set_xlabel('year', fontsize=16, fontname='Times New Roman')
# plt.ylabel('OHC [J]', fontsize=16, fontname='Times New Roman')
# 设置坐标轴
xticks_position=np.arange(1958,2015,5)
plt.xticks(xticks_position,fontsize=14, fontname='Times New Roman')
plt.yticks(fontsize=14, fontname='Times New Roman')
plt.legend(prop=font_manager.FontProperties(fname=None,family='Times New Roman',size=12),loc='upper left')

plt.show()




