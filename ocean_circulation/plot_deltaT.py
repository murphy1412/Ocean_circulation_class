import xarray as xr
import numpy as np
import os
import matplotlib.pyplot as plt

# =========================
# 1. 文件路径和模式名称
# =========================
DATA_DIR = "/home2/cheny/Ocean_circulation_data"

models = [
    {
        "name": "CanESM5",
        "file": os.path.join(
            DATA_DIR, "CanESM5", "Can_deltaT_dep_lat.nc"
        )
    },
    {
        "name": "MPI-ESM1-2-LR",
        "file": os.path.join(
            DATA_DIR, "MPI-ESM1-2-LR", "MPI_deltaT_dep_lat_v2.nc"
        )
    },
    {
        "name": "UKESM1-0-LL",
        "file": os.path.join(
            DATA_DIR, "UKESM1-0-LL", "UK_deltaT_dep_lat.nc"
        )
    }
]

out_png = os.path.join(
    DATA_DIR, "deltaT_section_3models_v2.png"
)

# =========================
# 2. 统一绘图参数
# =========================
levels = np.arange(-2.4, 2.41, 0.3)
cbar_ticks = np.arange(-2.4, 2.41, 0.6)

# =========================
# 3. 创建三个纵向子图
# =========================
#fig, axes = plt.subplots(
#    nrows=3,
#    ncols=1,
#    figsize=(10, 15),
#    sharex=True,
#    sharey=True
#)

# 保存最后一个 contourf 对象，用于共用 colorbar
im = None

fig = plt.figure(figsize=(10, 15))

gs = fig.add_gridspec(
    nrows=3,
    ncols=2,
    width_ratios=[1, 0.05],
    height_ratios=[1, 1, 1],
    hspace=0.12,
    wspace=0.12
)

axes = [
    fig.add_subplot(gs[i, 0])
    for i in range(3)
]

# 色标轴：跨越三行
cax = fig.add_subplot(gs[:, 1])

# =========================
# 4. 逐个读取并绘图
# =========================
for i, model in enumerate(models):

    ax = axes[i]
    print(f"\n正在处理: {model['name']}")

    ds = xr.open_dataset(model["file"])

    print(ds)

    da = ds["delta_T"]

    # 选择 0–6000 m
    da = da.sel(lev=slice(0, 6000))

    lat = da["latitude"].values
    depth = da["lev"].values
    section = da.transpose("lev", "latitude").values

    print("数据维度:", da.dims)
    print("绘图数据形状:", section.shape)
    print("有效点数:", np.isfinite(section).sum())
    print(
        "温度变化范围:",
        float(da.min(skipna=True)),
        float(da.max(skipna=True))
    )

    if np.isfinite(section).sum() == 0:
        ds.close()
        raise ValueError(
            f"{model['name']} 的绘图数据全部为 NaN"
        )

    # 绘制填色等值线
    im = ax.contourf(
        lat,
        depth,
        section,
        levels=levels,
        cmap="RdBu_r",
        extend="both"
    )

    # 子图标题
    ax.set_title(
        model["name"],
        loc="left",
        fontsize=15
    )

    # 坐标范围
    ax.set_xlim(-90, 91)
    ax.set_ylim(6000, 0)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)

    # 纵轴标签：每个子图都显示
    ax.set_ylabel("Depth (m)", fontsize=15)

    # 横轴刻度：三个子图共用
    ax.set_xticks(np.arange(-80, 81, 20))

    # 只在最下方的子图显示横轴标签
    if i == len(models) - 1:
        ax.set_xlabel("Latitude (°)", fontsize=15)
    else:
        ax.tick_params(
            axis="x",
            labelbottom=False,
            bottom=True
        )

    # 深度方向的网格线
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

    ds.close()

# =========================
# 5. 添加共用 colorbar
# =========================
cbar = fig.colorbar(
    im,
    cax=cax,
    orientation="vertical",
    ticks=cbar_ticks
)
#    pad=0.08,
#    fraction=0.05,


cbar.set_label(r"$\Delta T$ (°C)", fontsize=15)
cbar.ax.tick_params(labelsize=14)

# =========================
# 6. 保存
# =========================

fig.savefig(
    out_png,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\n新图片:", out_png)
