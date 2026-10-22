import os
import glob
import numpy as np
import xarray as xr

# ============================================================
# 1. 文件路径
# ============================================================

DATA_DIR = "/home2/cheny/Ocean_circulation_data/MPI-ESM1-2-LR"

thetao_files = sorted(glob.glob(
    os.path.join(
        DATA_DIR,
        "thetao_Omon_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_*.nc"
    )
))

areacello_files = sorted(glob.glob(
    os.path.join(
        DATA_DIR,
        "areacello_Ofx_MPI-ESM1-2-LR_historical_r1i1p1f1_gn.nc"
    )
))

so_files = sorted(glob.glob(
    os.path.join(
        DATA_DIR,
        "so_Omon_MPI-ESM1-2-LR_historical_r1i1p1f1_gn_*.nc"
    )
))

print("thetao 文件数:", len(thetao_files))
print("areacello 文件数:", len(areacello_files))
print("so 文件数:", len(so_files))

# ============================================================
# 2. 读取数据
# ============================================================

th_ds = xr.open_mfdataset(thetao_files, combine="by_coords")
a_ds = xr.open_mfdataset(areacello_files, combine="by_coords")
s_ds = xr.open_mfdataset(so_files, combine="by_coords")

# 选取 1958—2014 年
start_date = "1958-01-01"
end_date = "2014-12-31"

thetao = th_ds["thetao"].sel(
    time=slice(start_date, end_date)
)

areacello = a_ds["areacello"]

print("thetao dims:", th_ds["thetao"].dims)
print("areacello dims:", areacello.dims)

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
# 5. 读取水平网格面积和二维地理纬度
# ============================================================

# 去除面积缺测或无效的网格
areacello = areacello.where(areacello > 0)

# 使用温度数据对应文件中的二维真实纬度
lat2d = th_ds["latitude"]

print("delta_T dims:", delta_T.dims)
print("areacello dims:", areacello.dims)
print("latitude dims:", lat2d.dims)

# ============================================================
# 6. 检查维度并统一维度顺序
# ============================================================

assert set(areacello.dims) == {"j", "i"}, (
    f"areacello 维度异常: {areacello.dims}"
)

assert set(lat2d.dims) == {"j", "i"}, (
    f"latitude 维度异常: {lat2d.dims}"
)

assert set(delta_T.dims) == {"lev", "j", "i"}, (
    f"delta_T 维度异常: {delta_T.dims}"
)

areacello = areacello.transpose("j", "i")
lat2d = lat2d.transpose("j", "i")
delta_T = delta_T.transpose("lev", "j", "i")

# 严格检查坐标是否能够对齐
delta_T, areacello, lat2d = xr.align(
    delta_T,
    areacello,
    lat2d,
    join="exact"
)

print("面积网格形状:", areacello.shape)
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
# 8. 按实际地理纬度分箱
#    每 5° 一个纬度带，使用 areacello 面积加权
# ============================================================

lat_edges = np.arange(-90, 95, 5)
lat_centers = (lat_edges[:-1] + lat_edges[1:]) / 2

# 只保留有效的正网格面积
area = areacello.where(
    np.isfinite(areacello) & (areacello > 0)
)

section_list = []

for k in range(len(lat_edges) - 1):

    lat_min = lat_edges[k]
    lat_max = lat_edges[k + 1]
    lat_center = lat_centers[k]

    # 纬度带采用左闭右开区间，最后一个纬度带包含 +90°
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

    # 当前纬度带内，同时满足面积有效、温度变化有效
    valid = (
        lat_mask
        & area.notnull()
        & delta_T.notnull()
    )

    # 无效网格不参与面积加权
    weights = area.where(valid)

    # 分子：温度变化 × 网格面积
    numerator = (
        delta_T * weights
    ).sum(
        dim=("j", "i"),
        skipna=True
    )

    # 分母：有效网格面积之和
    denominator = weights.sum(
        dim=("j", "i"),
        skipna=True
    )

    # 面积加权平均温度变化
    mean_value = (
        numerator / denominator
    ).where(denominator > 0)

    # 添加当前纬度带中心坐标
    mean_value = mean_value.expand_dims(
        latitude=[lat_center]
    )

    section_list.append(mean_value)

    print(
        f"完成纬度带 {lat_min:5.1f}° 至 "
        f"{lat_max:5.1f}°"
    )

# 合并所有纬度带
delta_T_section = xr.concat(
    section_list,
    dim="latitude"
)

# 调整为深度 × 纬度
delta_T_section = delta_T_section.transpose(
    "lev", "latitude"
)

# ============================================================
# 9. 提取绘图数据并检查结果
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
# 10. 保存结果
# ============================================================

output_file = os.path.join(
    DATA_DIR,
    "MPI_deltaT_dep_lat_v2.nc"
)

output_ds = delta_T_section.to_dataset(
    name="delta_T"
)

output_ds["delta_T"].attrs["description"] = (
    "Area-weighted mean of delta_T in 5-degree geographic "
    "latitude bands"
)

output_ds["latitude"].attrs["units"] = "degrees_north"
output_ds["lev"].attrs["units"] = "m"

output_ds.to_netcdf(output_file)

print("\n结果已保存:", output_file)

