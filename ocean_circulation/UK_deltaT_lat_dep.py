import os
import glob
import numpy as np
import xarray as xr

# ============================================================
# 1. 文件路径
# ============================================================

DATA_DIR = "/home2/cheny/Ocean_circulation_data/UKESM1-0-LL"

thetao_files = sorted(glob.glob(
    os.path.join(
        DATA_DIR,
        "thetao_Omon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc"
    )
))

volcello_files = sorted(glob.glob(
    os.path.join(
        DATA_DIR,
        "volcello_Omon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc"
    )
))

so_files = sorted(glob.glob(
    os.path.join(
        DATA_DIR,
        "so_Omon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc"
    )
))

print("thetao 文件数:", len(thetao_files))
print("volcello 文件数:", len(volcello_files))

# ============================================================
# 2. 读取数据
# ============================================================

th_ds = xr.open_mfdataset(thetao_files, combine="by_coords")
v_ds = xr.open_mfdataset(volcello_files, combine="by_coords")
s_ds = xr.open_mfdataset(so_files, combine="by_coords")

# 选取 1958—2014 年
start_date = "1958-01-16"
end_date = "2014-12-16"

thetao = th_ds["thetao"].sel(
    time=slice(start_date, end_date)
)

volcello = v_ds["volcello"].sel(
    time=slice(start_date, end_date)
)

# ============================================================
# 3. 计算逐年平均温度
# ============================================================

# 每年 12 个月的平均值，得到 1958—2014 年共 57 个年平均场
T_annual = thetao.groupby("time.year").mean(
    dim="time", skipna=True
)

# 确保时间范围完整
T_annual = T_annual.sel(year=slice(1958, 2014))

print("年平均温度数据维度:", T_annual.dims)
print("年份数量:", T_annual.sizes["year"])

# ============================================================
# 4. 对每个格点做线性回归，计算温度趋势
# ============================================================

# polyfit 的一次项系数为温度趋势，单位通常是 K/年或 °C/年
fit = T_annual.polyfit(
    dim="year",
    deg=1,
    skipna=True
)

T_trend = fit["polyfit_coefficients"].sel(degree=1)

# 1958 到 2014 的时间间隔是 56 年
# 趋势 × 56 年，得到线性趋势估算的累计温度变化
delta_years = 2014 - 1958
delta_T = T_trend * delta_years

delta_T.name = "delta_T"
delta_T.attrs["long_name"] = (
    "Temperature change estimated from linear trend, 1958-2014"
)
delta_T.attrs["units"] = "degree_Celsius"

print("趋势计算完成")
print("delta_T 维度:", delta_T.dims)

# ============================================================
# 5. 根据 volcello 和 lev_bnds 估算水平网格面积
# ============================================================

# 研究时段内，先计算每年的平均网格体积
v_annual = volcello.sel(
    time=slice(start_date, end_date)
).groupby("time.year").mean(
    dim="time",
    skipna=True
)

print("年度平均体积维度:", v_annual.dims)

# 读取研究时段内的垂向层边界
dep_bnds = s_ds["lev_bnds"].sel(
    time=slice(start_date, end_date)
)

# 计算每年平均的垂向层边界
dep_bnds = dep_bnds.groupby(
    "time.year"
).mean(
    dim="time",
    skipna=True
)

# 垂向层厚 = 下边界 - 上边界
delta_dep = (
    dep_bnds.isel(bnds=1)
    - dep_bnds.isel(bnds=0)
)

print("delta_dep 最小值:",
      float(delta_dep.min(skipna=True).compute()))

print("delta_dep 最大值:",
      float(delta_dep.max(skipna=True).compute()))

print("层厚小于等于 0 的数量:",
      int((delta_dep <= 0).sum().compute()))

print("无效层厚数量:",
      int((~np.isfinite(delta_dep)).sum().compute()))

print("无效体积数量:",
      int((~np.isfinite(v_annual)).sum().compute()))

# 体积 / 层厚 ≈ 水平网格面积
area_annual = (
    v_annual / delta_dep
)

# 对深度层和年份求平均，得到二维水平面积估计
area_cell = area_annual.mean(
    dim="lev",
    skipna=True
).mean(
    dim="year",
    skipna=True
)

# 排除无效面积
area_cell = area_cell.where(
    np.isfinite(area_cell) & (area_cell > 0)
)

print("估算面积维度:", area_cell.dims)
print("估算面积形状:", area_cell.shape)


# ============================================================
# 6. 读取二维地理纬度，统一网格维度
# ============================================================

lat2d = th_ds["latitude"]

print("delta_T dims:", delta_T.dims)
print("area_cell dims:", area_cell.dims)
print("latitude dims:", lat2d.dims)

# 检查维度
assert set(delta_T.dims) == {"lev", "j", "i"}, (
    f"delta_T 维度异常: {delta_T.dims}"
)

assert set(area_cell.dims) == {"j", "i"}, (
    f"area_cell 维度异常: {area_cell.dims}"
)

assert set(lat2d.dims) == {"j", "i"}, (
    f"latitude 维度异常: {lat2d.dims}"
)

# 统一维度顺序
delta_T = delta_T.transpose("lev", "j", "i")
area_cell = area_cell.transpose("j", "i")
lat2d = lat2d.transpose("j", "i")

# 严格对齐，防止网格错位
delta_T, area_cell, lat2d = xr.align(
    delta_T,
    area_cell,
    lat2d,
    join="exact"
)

print("面积网格形状:", area_cell.shape)
print("纬度网格形状:", lat2d.shape)


# ============================================================
# 7. 选择 0—6000 m
# ============================================================

delta_T = delta_T.where(
    (delta_T["lev"] >= 0)
    & (delta_T["lev"] <= 6000),
    drop=True
)

print(
    "选择后的深度范围:",
    float(delta_T["lev"].min()),
    float(delta_T["lev"].max())
)


# ============================================================
# 8. 按真实地理纬度分箱，每 5° 一个纬度带
# ============================================================

lat_edges = np.arange(-90, 95, 5)
lat_centers = (
    lat_edges[:-1] + lat_edges[1:]
) / 2

# 只使用有效的正面积
area = area_cell.where(
    np.isfinite(area_cell) & (area_cell > 0)
)

section_list = []

for k in range(len(lat_edges) - 1):

    lat_min = lat_edges[k]
    lat_max = lat_edges[k + 1]
    lat_center = lat_centers[k]

    # 普通纬度带：左闭右开
    # 最后一个纬度带：包含 +90°
    if k == len(lat_edges) - 2:
        lat_mask = (
            (lat2d >= lat_min)
            & (lat2d <= lat_max)
        )
    else:
        lat_mask = (
            (lat2d >= lat_min)
            & (lat2d < lat_max)
        )

    # 当前纬度带内的有效网格
    valid = (
        lat_mask
        & area.notnull()
        & delta_T.notnull()
    )

    # 无效网格不参与加权
    weights = area.where(valid)

    # 分子：温度变化 × 水平网格面积
    numerator = (
        delta_T * weights
    ).sum(
        dim=("j", "i"),
        skipna=True
    )

    # 分母：有效网格面积总和
    denominator = weights.sum(
        dim=("j", "i"),
        skipna=True
    )

    # 当前纬度带、每个深度的面积加权平均
    mean_value = (
        numerator / denominator
    ).where(denominator > 0)

    # 添加纬度带中心坐标
    mean_value = mean_value.expand_dims(
        latitude=[lat_center]
    )

    section_list.append(mean_value)

    print(
        f"完成纬度带 {lat_min:5.1f}° 至 "
        f"{lat_max:5.1f}°"
    )


# ============================================================
# 9. 合并纬度带，得到深度—纬度剖面
# ============================================================

delta_T_section = xr.concat(
    section_list,
    dim="latitude"
)

delta_T_section = delta_T_section.transpose(
    "lev", "latitude"
)


# ============================================================
# 10. 提取并检查绘图数据
# ============================================================

depth = delta_T_section["lev"].values
lat = delta_T_section["latitude"].values
section = delta_T_section.values

print("\n========== 计算结果 ==========")
print("剖面维度:", delta_T_section.dims)
print("剖面形状:", section.shape)
print("深度范围:", np.nanmin(depth), np.nanmax(depth))
print("纬度范围:", np.nanmin(lat), np.nanmax(lat))
print(
    "温度变化范围:",
    np.nanmin(section),
    np.nanmax(section)
)
print(
    "有效数据比例:",
    np.isfinite(section).mean()
)


# ============================================================
# 11. 保存结果
# ============================================================

output_file = os.path.join(
    DATA_DIR,
    "UK_deltaT_dep_lat.nc"
)

output_ds = delta_T_section.to_dataset(
    name="delta_T"
)

output_ds["delta_T"].attrs["description"] = (
    "Area-weighted mean of delta_T in 5-degree geographic "
    "latitude bands; horizontal area estimated from volcello "
    "divided by vertical layer thickness"
)

output_ds["latitude"].attrs["units"] = "degrees_north"
output_ds["lev"].attrs["units"] = "m"

output_ds.to_netcdf(output_file)

print("\n结果已保存:", output_file)
