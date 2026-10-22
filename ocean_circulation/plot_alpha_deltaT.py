import os
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# ============================================================
# 1. 文件路径和模式名称
# ============================================================

DATA_DIR = "/home2/cheny/Ocean_circulation_data"

models = [
    {
        "name": "CanESM5",
        "file": os.path.join(
            DATA_DIR,
            "CanESM5",
            "Can_alpha_deltaT_depth_lat_v2.nc"
        )
    },
    {
        "name": "MPI-ESM1-2-LR",
        "file": os.path.join(
            DATA_DIR,
            "MPI-ESM1-2-LR",
            "MPI_alpha_deltaT_depth_lat_v2.nc"
        )
    },
    {
        "name": "UKESM1-0-LL",
        "file": os.path.join(
            DATA_DIR,
            "UKESM1-0-LL",
            "UK_alpha_deltaT_depth_lat_v2.nc"
        )
    }
]

output_png = os.path.join(
    DATA_DIR,
    "alpha_deltaT_section_3models.png"
)

# ============================================================
# 2. 统一绘图参数
# ============================================================

vmax = 0.0004
levels = np.linspace(-vmax, vmax, 21)

cbar_ticks = np.array([
    -0.00040, -0.00032, -0.00024,
    -0.00016, -0.00008, 0,
     0.00008,  0.00016,  0.00024,
     0.00032,  0.00040
])

# ============================================================
# 3. 创建 GridSpec 布局
# ============================================================

fig = plt.figure(figsize=(10, 15))

gs = fig.add_gridspec(
    nrows=3,
    ncols=2,
    width_ratios=[1, 0.05],
    height_ratios=[1, 1, 1],
    hspace=0.12,
    wspace=0.12
)

# 三个纵向子图
axes = [
    fig.add_subplot(gs[i, 0])
    for i in range(3)
]

# 共用 colorbar，跨越三行
cax = fig.add_subplot(gs[:, 1])

# ============================================================
# 4. 逐个读取数据并绘图
# ============================================================

im = None

for i, model in enumerate(models):

    ax = axes[i]

    print(f"\n正在处理: {model['name']}")
    print("文件:", model["file"])

    if not os.path.exists(model["file"]):
        raise FileNotFoundError(
            f"找不到文件: {model['file']}"
        )

    with xr.open_dataset(model["file"]) as ds:

        print(ds)

        da = ds["alpha_deltaT"]

        # 检查维度
        assert set(da.dims) == {"lev", "latitude"}, (
            f"{model['name']} 维度异常: {da.dims}"
        )

        # 统一维度顺序
        da = da.transpose("lev", "latitude")

        # 深度、纬度排序
        da = da.sortby("lev")
        da = da.sortby("latitude")

        # 只保留 0–6000 m
        da = da.where(
            (da["lev"] >= 0) & (da["lev"] <= 6000),
            drop=True
        )

        # 提取绘图数据
        lat = da["latitude"].values
        depth = da["lev"].values
        section = da.values

        print("绘图数据形状:", section.shape)
        print("深度范围:", np.nanmin(depth), np.nanmax(depth))
        print("纬度范围:", np.nanmin(lat), np.nanmax(lat))
        print("有效数据比例:", np.isfinite(section).mean())

        if not np.isfinite(section).any():
            raise ValueError(
                f"{model['name']} 的剖面数据全部为 NaN"
            )

        print("最小值:", np.nanmin(section))
        print("最大值:", np.nanmax(section))

        # 绘制填色等值线
        im = ax.contourf(
            lat,
            depth,
            section,
            levels=levels,
            cmap="RdBu_r",
            extend="both"
        )

    # --------------------------------------------------------
    # 子图格式
    # --------------------------------------------------------

    ax.set_xlim(-90, 91)
    ax.set_ylim(6000, 0)
    ax.tick_params(axis="x", labelsize=14)
    ax.tick_params(axis="y", labelsize=14)

    ax.set_ylabel("Depth (m)", fontsize=15)
    ax.set_xticks(np.arange(-80, 81, 20))

    # 标题放在每个子图左上方
    ax.set_title(
        model["name"],
        loc="left",
        fontsize=15
        )

    # 只在最下方的子图显示横轴标签
    if i == len(models) - 1:
        ax.set_xlabel("Latitude (°)", fontsize=15)
    else:
        ax.tick_params(
            axis="x",
            labelbottom=False,
            bottom=True
        )

    # 深度方向网格线
    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )

# ============================================================
# 5. 共用 colorbar
# ============================================================

cbar = fig.colorbar(
    im,
    cax=cax,
    orientation="vertical",
    ticks=cbar_ticks
)

cbar.set_label(
    r"$\alpha\Delta T$",
    fontsize=15
)

cbar.ax.tick_params(labelsize=14)

# 科学计数法
formatter = ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((0, 0))

cbar.formatter = formatter
cbar.update_ticks()
cbar.ax.yaxis.get_offset_text().set_fontsize(14)

# ============================================================
# 6. 保存
# ============================================================

fig.savefig(
    output_png,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\n图片已保存:", output_png)
