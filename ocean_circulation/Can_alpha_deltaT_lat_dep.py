import os
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# ============================================================
# 1. 文件路径与时间范围
# ============================================================

DATA_DIR = "/home2/cheny/Ocean_circulation_data/CanESM5"

alpha_file = os.path.join(
    DATA_DIR, "Can_alpha_deltaT_1958_2014_3D_v2.nc"
)

#output_file = os.path.join(
#    DATA_DIR, "Can_alpha_deltaT_section.nc"
#)

start_date = "1958-01-01"
end_date = "2014-12-31"

# ============================================================
# 2. 读取 alpha*deltaT 数据
# ============================================================

alpha_ds = xr.open_dataset(alpha_file)
alpha_deltaT = alpha_ds["alpha_deltaT"]

# ============================================================
# 3. 读取已有的 areacello 和二维纬度
# ============================================================

area_files = sorted(
    glob.glob(os.path.join(DATA_DIR, "areacello*.nc"))
)

if not area_files:
    raise FileNotFoundError("没有找到 areacello*.nc 文件")

print("areacello 文件数:", len(area_files))

area_ds = xr.open_dataset(area_files[0])

areacello = area_ds["areacello"]
lat2d = alpha_ds["latitude"]

print("alpha_deltaT dims:", alpha_deltaT.dims)
print("areacello dims:", areacello.dims)
print("latitude dims:", lat2d.dims)

# 检查维度
assert set(areacello.dims) == {"j", "i"}, (
    f"areacello 维度异常: {areacello.dims}"
)
assert set(lat2d.dims) == {"j", "i"}, (
    f"latitude 维度异常: {lat2d.dims}"
)
assert set(alpha_deltaT.dims) == {"lev", "j", "i"}, (
    f"alpha_deltaT 维度异常: {alpha_deltaT.dims}"
)

# 统一维度顺序
areacello = areacello.transpose("j", "i")
lat2d = lat2d.transpose("j", "i")
alpha_deltaT = alpha_deltaT.transpose("lev", "j", "i")

# 确保坐标能够严格对齐，避免错误匹配网格
alpha_deltaT, areacello, lat2d = xr.align(
    alpha_deltaT,
    areacello,
    lat2d,
    join="exact"
)

print("面积网格形状:", areacello.shape)
print("纬度网格形状:", lat2d.shape)

# ============================================================
# 4. 选择 0—6000 m
# ============================================================

alpha_deltaT = alpha_deltaT.where(
    (alpha_deltaT["lev"] >= 0)
    & (alpha_deltaT["lev"] <= 6000),
    drop=True
)

print("选择后的深度范围:",
      float(alpha_deltaT.lev.min()),
      float(alpha_deltaT.lev.max()))

# ============================================================
# 5. 按实际地理纬度分箱
#    每 5° 一个纬度带，使用 areacello 面积加权
# ============================================================

lat_edges = np.arange(-90, 95, 5)
lat_centers = (lat_edges[:-1] + lat_edges[1:]) / 2

# 面积必须为正且有效
area = areacello.where(
    np.isfinite(areacello) & (areacello > 0)
)

section_list = []

for k in range(len(lat_edges) - 1):

    lat_min = lat_edges[k]
    lat_max = lat_edges[k + 1]
    lat_center = lat_centers[k]

    # 最后一个纬度带包含 +90°
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

    # 仅使用当前纬度带、面积有效、alpha*deltaT 有效的网格
    valid = (
        lat_mask
        & area.notnull()
        & alpha_deltaT.notnull()
    )

    # 对无效网格屏蔽面积权重
    weights = area.where(valid)

    # 分子：alpha*deltaT × 网格面积
    numerator = (
        alpha_deltaT * weights
    ).sum(dim=("j", "i"), skipna=True)

    # 分母：有效网格面积之和
    denominator = weights.sum(
        dim=("j", "i"),
        skipna=True
    )

    # 每个深度、每个纬度带的面积加权平均
    mean_value = (
        numerator / denominator
    ).where(denominator > 0)

    # 将纬度带中心作为横坐标
    mean_value = mean_value.expand_dims(
        latitude=[lat_center]
    )

    section_list.append(mean_value)

    print(
        f"完成纬度带 {lat_min:5.1f}° 至 "
        f"{lat_max:5.1f}°"
    )

# 合并为二维剖面，维度为 (latitude, lev)
alpha_deltaT_section = xr.concat(
    section_list,
    dim="latitude"
)

# 调整为 (lev, latitude)，方便绘制深度—纬度图
alpha_deltaT_section = alpha_deltaT_section.transpose(
    "lev", "latitude"
)

# ============================================================
# 6. 检查结果
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

# ============================================================
# 7. 保存 NetCDF
# ============================================================

output_file = os.path.join(
    DATA_DIR,
    "Can_alpha_deltaT_depth_lat_v2.nc"
)

output_ds = alpha_deltaT_section.to_dataset(
    name="alpha_deltaT"
)

output_ds["alpha_deltaT"].attrs["description"] = (
    "Area-weighted mean of alpha*deltaT in 5-degree geographic latitude bands"
)
output_ds["latitude"].attrs["units"] = "degrees_north"
output_ds["lev"].attrs["units"] = "m"

output_ds.to_netcdf(output_file)

print("\n结果已保存:", output_file)

# 关闭文件
area_ds.close()
