import os
import glob
import numpy as np
import xarray as xr

# ============================================================
# 1. 文件路径与时间范围
# ============================================================

DATA_DIR = "/home2/cheny/Ocean_circulation_data/UKESM1-0-LL"

alpha_file = os.path.join(
    DATA_DIR, "UK_alpha_deltaT_1958_2014_3D_v2.nc"
)

output_file = os.path.join(
    DATA_DIR, "UK_alpha_deltaT_depth_lat_v2.nc"
)

start_date = "1958-01-16"
end_date = "2014-12-16"

# ============================================================
# 2. 读取已有的 alpha*deltaT 三维数据
# ============================================================

alpha_ds = xr.open_dataset(alpha_file)
alpha_deltaT = alpha_ds["alpha_deltaT"]

print("alpha_deltaT dims:", alpha_deltaT.dims)
print("alpha_deltaT shape:", alpha_deltaT.shape)

# ============================================================
# 3. 读取网格体积 volcello 和垂向层边界 lev_bnds
# ============================================================

vol_files = sorted(
    glob.glob(os.path.join(DATA_DIR, "volcello*.nc"))
)

so_files = sorted(
    glob.glob(os.path.join(DATA_DIR, "so*.nc"))
)

if not vol_files:
    raise FileNotFoundError("没有找到 volcello*.nc 文件")

if not so_files:
    raise FileNotFoundError("没有找到 so*.nc 文件")

print("volcello 文件数:", len(vol_files))
print("so 文件数:", len(so_files))

vol_ds = xr.open_mfdataset(
    vol_files,
    combine="by_coords"
)

s_ds = xr.open_mfdataset(
    so_files,
    combine="by_coords"
)

# 选取研究时段
volcello = vol_ds["volcello"].sel(
    time=slice(start_date, end_date)
)

dep_bnds = s_ds["lev_bnds"].sel(
    time=slice(start_date, end_date)
)

if volcello.sizes.get("time", 0) == 0:
    raise ValueError("研究时段内没有 volcello 数据")

if dep_bnds.sizes.get("time", 0) == 0:
    raise ValueError("研究时段内没有 lev_bnds 数据")

print("volcello dims:", volcello.dims)
print("lev_bnds dims:", dep_bnds.dims)

# ============================================================
# 4. 利用网格体积和垂向层厚估算水平网格面积
# ============================================================

# 每年的平均网格体积
v_annual = volcello.groupby(
    "time.year"
).mean(
    dim="time",
    skipna=True
)

# 每年的平均垂向层边界
dep_bnds_annual = dep_bnds.groupby(
    "time.year"
).mean(
    dim="time",
    skipna=True
)

# 垂向层厚
delta_dep = (
    dep_bnds_annual.isel(bnds=1)
    - dep_bnds_annual.isel(bnds=0)
)

# 网格体积 / 垂向层厚 ≈ 水平网格面积
area_annual = v_annual / delta_dep

# 对深度层和年份求平均
area_cell = area_annual.mean(
    dim="lev",
    skipna=True
).mean(
    dim="year",
    skipna=True
)

# 仅保留有效的正面积
area_cell = area_cell.where(
    np.isfinite(area_cell) & (area_cell > 0)
)

print("area_cell dims:", area_cell.dims)
print("area_cell shape:", area_cell.shape)

# ============================================================
# 5. 读取二维真实纬度，检查网格维度
# ============================================================

lat2d = alpha_ds["latitude"]

print("alpha_deltaT dims:", alpha_deltaT.dims)
print("area_cell dims:", area_cell.dims)
print("latitude dims:", lat2d.dims)

assert set(alpha_deltaT.dims) == {"lev", "j", "i"}, (
    f"alpha_deltaT 维度异常: {alpha_deltaT.dims}"
)

assert set(area_cell.dims) == {"j", "i"}, (
    f"area_cell 维度异常: {area_cell.dims}"
)

assert set(lat2d.dims) == {"j", "i"}, (
    f"latitude 维度异常: {lat2d.dims}"
)

# 统一维度顺序
alpha_deltaT = alpha_deltaT.transpose(
    "lev", "j", "i"
)

area_cell = area_cell.transpose(
    "j", "i"
)

lat2d = lat2d.transpose(
    "j", "i"
)

# 严格检查网格坐标
alpha_deltaT, area_cell, lat2d = xr.align(
    alpha_deltaT,
    area_cell,
    lat2d,
    join="exact"
)

print("面积网格形状:", area_cell.shape)
print("纬度网格形状:", lat2d.shape)

# ============================================================
# 6. 选择 0—6000 m
# ============================================================

alpha_deltaT = alpha_deltaT.where(
    (alpha_deltaT["lev"] >= 0)
    & (alpha_deltaT["lev"] <= 6000),
    drop=True
)

print(
    "选择后的深度范围:",
    float(alpha_deltaT["lev"].min()),
    float(alpha_deltaT["lev"].max())
)

# ============================================================
# 7. 按实际地理纬度分箱，每 5° 一个纬度带
# ============================================================

lat_edges = np.arange(-90, 95, 5)
lat_centers = (
    lat_edges[:-1] + lat_edges[1:]
) / 2

section_list = []

for k in range(len(lat_edges) - 1):

    lat_min = lat_edges[k]
    lat_max = lat_edges[k + 1]
    lat_center = lat_centers[k]

    # 普通纬度带左闭右开，最后一个纬度带包含 +90°
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

    # 当前纬度带内有效的网格
    valid = (
        lat_mask
        & area_cell.notnull()
        & alpha_deltaT.notnull()
    )

    # 面积权重：只使用有效网格
    weights = area_cell.where(valid)

    # 分子：alpha*deltaT × 网格面积
    numerator = (
        alpha_deltaT * weights
    ).sum(
        dim=("j", "i"),
        skipna=True
    )

    # 分母：有效网格面积总和
    denominator = weights.sum(
        dim=("j", "i"),
        skipna=True
    )

    # 每个深度、每个纬度带的面积加权平均
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
# 8. 合并所有纬度带，得到深度—纬度剖面
# ============================================================

alpha_deltaT_section = xr.concat(
    section_list,
    dim="latitude"
)

alpha_deltaT_section = alpha_deltaT_section.transpose(
    "lev", "latitude"
)

# ============================================================
# 9. 检查结果
# ============================================================

section = alpha_deltaT_section.values
depth = alpha_deltaT_section["lev"].values
lat = alpha_deltaT_section["latitude"].values

print("\n========== 计算结果 ==========")
print("剖面维度:", alpha_deltaT_section.dims)
print("剖面形状:", section.shape)
print("深度范围:", np.nanmin(depth), np.nanmax(depth))
print("纬度范围:", np.nanmin(lat), np.nanmax(lat))
print(
    "alpha*deltaT 范围:",
    np.nanmin(section),
    np.nanmax(section)
)
print(
    "有效数据比例:",
    np.isfinite(section).mean()
)

# ============================================================
# 10. 保存 NetCDF
# ============================================================

output_ds = alpha_deltaT_section.to_dataset(
    name="alpha_deltaT"
)

output_ds["alpha_deltaT"].attrs["description"] = (
    "Area-weighted mean of alpha*deltaT in 5-degree "
    "geographic latitude bands"
)

output_ds["latitude"].attrs["units"] = "degrees_north"
output_ds["lev"].attrs["units"] = "m"

output_ds.to_netcdf(output_file)

print("\n结果已保存:", output_file)

# ============================================================
# 11. 关闭文件
# ============================================================

output_ds.close()
alpha_ds.close()
vol_ds.close()
s_ds.close()
