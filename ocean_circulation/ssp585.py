####################################此代码是针对进阶题目######################
import xarray as xr
import glob
so_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\ssp585\so_Omon_CanESM5_ssp585_r5i1p1f3_gn_*.nc"))
s_all = xr.open_mfdataset(so_files, combine='by_coords')

th_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\ssp585\thetao_Omon_CanESM5_ssp585_r1i1p1f1_gn_*.nc"))
th_all = xr.open_mfdataset(th_files, combine='by_coords')
print(th_all)

so_A=s_all['so'].sel(time=slice("2015-01-01", "2100-12-31"))
th_A=th_all['thetao'].sel(time=slice("2015-01-01", "2100-12-31"))
area_all= xr.open_dataset(r"D:\Class_data\Ocean_circulation_class\ssp585\areacello_Ofx_CanESM5_ssp585_r1i1p1f1_gn.nc")

##求取年平均值
so_A=so_A.groupby("time.year").mean(dim="time", skipna=True)
th_A=th_A.groupby("time.year").mean(dim="time", skipna=True)
# area_A=area_all['areacello']
# dep_bnds=s_all['lev_bnds'].sel(time=slice("2015-01-01", "2100-12-31"))
# dep_bnds=dep_bnds.groupby("time.year").mean(dim="time", skipna=True)
# delta_dep=dep_bnds.isel(bnds=1)-dep_bnds.isel(bnds=0)
# v_A=delta_dep*area_A
# rou = 1025.0
# cp = 3990.0


z=-th_all['lev']
print(z.shape)

import numpy as np
delta_th_A=th_A-th_A.sel(year=slice(2015,2026)).mean('year',skipna=True)
delta_th_A_mean=delta_th_A.mean(dim=['j','i'],skipna=True)
#
# # ###计算OHC####
# ohc_cell=(rou*cp*delta_th_A*v_A).sum(dim=['j','i'],skipna=True)
# print(ohc_cell.shape)
time=np.arange(2015,2101)


import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean
import matplotlib.colors as mcolors
import numpy as np
###############绘制α的深度-纬度断面图##############
fig, ax = plt.subplots(figsize=(10, 6))
cmap=cmocean.cm.balance

levels=np.arange(-4,4.01,0.5)
norm=mcolors.BoundaryNorm(levels,cmap.N)
im=ax.pcolormesh(time,
                        z,
                        delta_th_A_mean.T,  #将ORAS5的单位m换成cm
                        cmap=cmap,
                        norm=norm,  #有norm存在，就不能用最大最小值
                        # vmin=-0.2,
                        # vmax=0.2,
                        # norm=norm,   #norm和vmax、vmin不能同时用
                        shading='auto'
                         )

##########针对thetao的标签
cs = ax.contour(time,
    z,
    delta_th_A_mean.T,
    levels=np.arange(-4, 4.01, 0.5),
    colors='black',
    linewidths=0.8)

labels =ax.clabel(cs,
    inline=True,
    fontsize=12,
    fmt='%.2f')

#################thetao colorbar############
cbar = plt.colorbar(im,
                    ax=ax,
                    pad=0.01,
                    extend='both',
                    orientation='vertical')
ticks = np.arange(-4, 4.1, 1)
cbar.set_ticks(ticks)
cbar.ax.set_title('thetao [℃]',
    fontsize=12,
    fontname='Times New Roman',
    pad=10)
cbar.ax.tick_params(labelsize=14)
cbar.ax.minorticks_off()

 #控制colorbar的字体格式
for label in cbar.ax.get_yticklabels():
    label.set_fontname('Times New Roman')
    # cbar.set_label('SSH [m]', fontsize=14, fontweight='bold', fontname='Times New Roman')



# 等值线
# cs=ax.contour(time,z,ohc_cell.T,
#     levels=np.arange(-10e22,10.01e22,1e22),
#     colors='k',
#     linewidths=0.8)
#
# labels = ax.clabel(cs,
#     inline=True,
#     fontsize=10,
#     fmt=lambda x: f'{x/1e22:.1f}',
#     )
#
# for txt in labels:
#     txt.set_fontname('Times New Roman')
#
# cbar = plt.colorbar(im,
#                     ax=ax,
#                     pad=0.01,
#                     extend='both',
#                     orientation='vertical')
# ticks = np.arange(-10, 10.1, 2) * 1e22
# cbar.set_ticks(ticks)
# cbar.set_ticklabels([f'{v/1e22:.0f}' for v in ticks])
# cbar.ax.set_title(r'OHC ($10^{22}$ J)',
#     fontsize=10,
#     fontname='Times New Roman',
#     pad=10)
# cbar.ax.tick_params(labelsize=14)
# cbar.ax.minorticks_off()
#
#  #控制colorbar的字体格式
# for label in cbar.ax.get_yticklabels():
#     label.set_fontname('Times New Roman')
#     # cbar.set_label('SSH [m]', fontsize=14, fontweight='bold', fontname='Times New Roman')
#

# ####贴在colorbar上方
# cbar.ax.set_title('OHC [J]', fontsize=14, fontname='Times New Roman', pad=10)
# #在colorbar右侧添加单位
# cbar.ax.text(
#         0.6, 10,
#         '℃',  # ← 这就是缺失的 s
#         transform=cbar.ax.transAxes,
#         va='center',
#         ha='left',
#         fontsize=16,
#         fontname='Times New Roman',
#         # fontweight='bold'
#         )
#
#
# ax.set_title(
#         "Reconstructed trend(1993-2024)",
#         fontsize=18,
#         fontname="Times New Roman",
#         pad=8
#     )


plt.xticks(fontsize=14,fontname='Times New Roman')
plt.yticks(fontsize=14, fontname='Times New Roman')
plt.xlabel('Year',fontsize=15, fontname='Times New Roman')
plt.ylabel('Depth [m]',fontsize=14, fontname='Times New Roman')

# dpi=300 是期刊常用标准，dpi=600 是高清印刷标准
fig.savefig('thetao_depth_time_CanESM5.png', dpi=300, bbox_inches='tight')

plt.show()












