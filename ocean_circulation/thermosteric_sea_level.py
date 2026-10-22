##########################计算热膨胀海平面代码
#####################################
import xarray as xr
import glob
####ESM1-2-LR
so_files= sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\so_Omon_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_*.nc"))
####CanESM5
# so_files= sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\so_Omon_CanESM5_historical_r1i1p1f1_gn_*.nc"))
#####UKESM1
# so_files= sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\so_Omon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc"))

s_all = xr.open_mfdataset(so_files, combine='by_coords')
so_A=s_all['so'].sel(time=slice("1958-01-16", "2014-12-16"))
print(s_all)
####ESM1-2-LR
th_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\thetao_Omon_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_*.nc"))
####CanESM5
# th_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\thetao_Omon_CanESM5_historical_r1i1p1f1_gn_*.nc"))
#####UKESM1
# th_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\thetao_Omon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc"))

th_all = xr.open_mfdataset(th_files, combine='by_coords')

####MPI-ESM1-2-LR
area=xr.open_dataset(r"D:\Class_data\Ocean_circulation_class\areacello_Ofx_MPI-ESM1-2-LR_historical_r1i1p1f1_gn.nc")
area_cell=area['areacello']

# ####CanESM5
# area1= xr.open_dataset(r"D:\Class_data\Ocean_circulation_class\areacello_Ofx_CanESM5_historical_r1i1p1f1_gn.nc")
# area_cell=area1['areacello']

####UKESM1
# ##计算面积网格
# v_files = sorted(glob.glob(r"D:\Class_data\Ocean_circulation_class\volcello_Omon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc"))
# v_all = xr.open_mfdataset(v_files, combine='by_coords')
# v_A=v_all['volcello'].sel(time=slice("1958-01-16", "2014-12-16"))
# v_A=v_A.groupby("time.year").mean(dim="time", skipna=True)
# dep_bnds=s_all['lev_bnds'].sel(time=slice("1958-01-16", "2014-12-16"))
# dep_bnds=dep_bnds.groupby("time.year").mean(dim="time", skipna=True)
# delta_dep=dep_bnds.isel(bnds=1)-dep_bnds.isel(bnds=0)
# area_cell=(v_A/delta_dep).mean(dim='lev').mean('year')   #sum(dim=['j','i'],skipna=True)


so_A=s_all['so'].sel(time=slice("1958-01-16", "2014-12-16"))
th_A=th_all['thetao'].sel(time=slice("1958-01-16", "2014-12-16"))
# v_A=v_all['volcello']
dep_bnds=s_all['lev_bnds'].sel(time=slice("1958-01-16", "2014-12-16"))

##求取年平均值
so_A=so_A.groupby("time.year").mean(dim="time", skipna=True)
th_A=th_A.groupby("time.year").mean(dim="time", skipna=True)
dep_bnds=dep_bnds.groupby("time.year").mean(dim="time", skipna=True)

# print(v_A.shape,so_A.shape,th_A.shape)
delta_th_A=th_A-th_A.sel(year=slice(1981,2010)).mean('year')

delta_dep=dep_bnds.isel(bnds=1)-dep_bnds.isel(bnds=0)
print(delta_dep.shape)

import gsw
##计算压力深度
z=-so_A['lev'].values
z=z[:,None,None]
lat=so_A['latitude'].values

p=gsw.p_from_z(z,lat[None,:,:])
alpha=gsw.alpha(so_A,th_A,p)

sh=(alpha*delta_th_A*delta_dep).sel(lev=slice(2000, 6000)).sum(dim='lev',skipna=True)
sh_global_mean=1000*(sh*area_cell).sum(dim=['j','i'],skipna=True).values/area_cell.sum(dim=['j','i'],skipna=True).values
print(sh_global_mean)

##########################
# import matplotlib.pyplot as plt
# import numpy as np
# time=np.arange(1958,2015)
# # 设置坐标轴
# xticks_position=np.arange(1958,2015,5)
# plt.plot(time, sh_global_mean, label='thermosteric sea level',color='crimson')
# plt.xlabel("year",fontsize=16,fontname='Times New Roman')
# plt.ylabel("thermosteric sea level [mm]",fontsize=16,fontname='Times New Roman')
# plt.xticks(xticks_position,fontsize=14, fontname='Times New Roman')
# plt.yticks(fontsize=14, fontname='Times New Roman')
# plt.show()


# import matplotlib.pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.feature as cfeature
# import cmocean
# import matplotlib.colors as mcolors
# import numpy as np
# ###############绘制α的深度-纬度断面图##############
# plt.figure(figsize=(10,6))
# ax=plt.axes(projection=ccrs.PlateCarree(central_longitude=180))
# cmap=cmocean.cm.balance
#
# levels=np.arange(-6,6.01,0.3)
# norm=mcolors.BoundaryNorm(levels,cmap.N)
# im=ax.pcolormesh(z,
#                         lat,
#                         alpha,  #将ORAS5的单位m换成cm
#                         cmap=cmap,
#                         norm=norm,  #有norm存在，就不能用最大最小值
#                         # vmin=-0.2,
#                         # vmax=0.2,
#                         ##transform=ccrs.PlateCarree()这一步，明确之处绘图数据以地理纬度坐标表示，使用cartopy能够将其正确地投影到指定地地图投影，如Robsin投影上
#                         transform=ccrs.PlateCarree(),
#                         # norm=norm,   #norm和vmax、vmin不能同时用
#                         shading='nearest'
#                          )
#
#
# #添加colorbar
# cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.06,extend='both',orientation='horizontal')
# cbar.ax.tick_params(labelsize=14)
# # #刻度位置
# # ticks=np.arange(-6,6.01,1.5)
# # cbar.set_ticks(ticks)
# # cbar.ax.minorticks_off()
# #
# #  #控制colorbar的字体格式
# # for label in cbar.ax.get_yticklabels():
# #     label.set_fontname('Times New Roman')
# #     # cbar.set_label('SSH [m]', fontsize=14, fontweight='bold', fontname='Times New Roman')
# #     #在colorbar右侧添加单位
# # cbar.ax.text(
# #         1.06, 0.5,
# #         'mm/yr',  # ← 这就是缺失的 s
# #         transform=cbar.ax.transAxes,
# #         va='center',
# #         ha='left',
# #         fontsize=16,
# #         fontname='Times New Roman',
# #         # fontweight='bold'
# #         )
# #
# #     # 添加海岸线、国界、陆地//这里使用cartopy
# # ax.coastlines(resolution='110m',linewidth=0.5)
# # ax.add_feature(cfeature.BORDERS,linewidth=0.5)
# # ax.add_feature(cfeature.LAND,facecolor='lightgray')
# #     #使用cartopy内置陆地遮罩，目的是去掉陆地上的异常值。使用pcolor时，如果数据中陆地处不是NaN，而是0或者其他值，陆地同样会被pcolor填色
# # ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=2)
# # ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=3)
# # ax.set_facecolor('white')
# #
# #     # ##添加经纬度坐标(下面这一小段代码，适用于PlateCarree坐标系，不适用于Robinson坐标系)
# #     # #设置经纬度范围
# # ax.set_extent([-180,180,-72,72],crs=ccrs.PlateCarree())
# #     #创建经纬度网格线，用gridlines;
# # gl=ax.gridlines(
# #         draw_labels=True, #让经纬度数值显示在边框
# #         linewidth=0.3,    #网格线的粗细（0.3 很细）
# #         color='none',     #网格线颜色,设置为none,就是隐藏网格线
# #         alpha=0.5,        #透明度
# #         linestyle='--'    #虚线样式
# #     )
# #     #隐藏上方与右边的刻度值
# # gl.top_labels=False
# # gl.right_labels=False
# #     #调整字体大小
# # gl.xlabel_style={'size':16,'fontname':'Times New Roman'}
# # gl.ylabel_style={'size':16,'fontname':'Times New Roman'}
# #
# # ax.set_title(
# #         "Reconstructed trend(1993-2024)",
# #         fontsize=18,
# #         fontname="Times New Roman",
# #         pad=8
# #     )
# # plt.xticks(fontsize=18,fontname='Times New Roman')
# # plt.yticks(fontsize=18, fontname='Times New Roman')
# #
# # plt.subplots_adjust(
# #         left=0.06,
# #         right=0.98,
# #         bottom=0.02,
# #         top=1.2
# #     )
# plt.show()
