# ============================================================
# alpha*DeltaT latitude-longitude section
# MPI historical
# 1958-2014
# ============================================================


import os
import glob
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import gsw


# ============================================================
# 1. 数据路径
# ============================================================

DATA_DIR = "/home2/cheny/Ocean_circulation_data/MPI-ESM1-2-LR"


thetao_files = sorted(
    glob.glob(
        os.path.join(
            DATA_DIR,
            "thetao*.nc"
        )
    )
)

so_files = sorted(
    glob.glob(
        os.path.join(
            DATA_DIR,
            "so*.nc"
        )
    )
)


print("thetao:", len(thetao_files))
print("so:", len(so_files))


# ============================================================
# 2. 读取数据
# ============================================================

theta_ds = xr.open_mfdataset(
    thetao_files,
    combine="by_coords"
)


so_ds = xr.open_mfdataset(
    so_files,
    combine="by_coords"
)


theta = theta_ds["thetao"]

salt = so_ds["so"]


# ============================================================
# 3. 选取1958-2014
# ============================================================

theta = theta.sel(
    time=slice(
        "1958-01-01",
        "2014-12-31"
    )
)


salt = salt.sel(
    time=slice(
        "1958-01-01",
        "2014-12-31"
    )
)


# ============================================================
# 4. 年平均
# ============================================================


T_year = theta.groupby(
    "time.year"
).mean(
    "time",
    skipna=True
)


S_year = salt.groupby(
    "time.year"
).mean(
    "time",
    skipna=True
)

print(T_year)


# ============================================================
# 5. 温度趋势计算
# ============================================================

# °C/year

fit = T_year.polyfit(
    dim="year",
    deg=1,
    skipna=True
)


T_trend = fit[
    "polyfit_coefficients"
].sel(
    degree=1
)


# 1958-2014
years = 2014-1958


delta_T = T_trend * years


delta_T.name="delta_T"



print(
    "Delta T:",
    delta_T.min().values,
    delta_T.max().values
)


# ============================================================
# 6. 计算平均温度和盐度
# ============================================================


T_mean = T_year.mean(
    "year",
    skipna=True
)


S_mean = S_year.mean(
    "year",
    skipna=True
)


# ============================================================
# 7. 计算 alpha(S,T,P)
# ============================================================


depth = theta_ds["lev"]


# 深度(m)转换压力(dbar)
pressure = xr.DataArray(
    depth.values,
    dims=["lev"],
    coords={"lev":depth.values}
)

P = pressure.broadcast_like(
    T_mean
)


# 转 Absolute Salinity

SA = xr.apply_ufunc(
    gsw.SA_from_SP,
    S_mean,
    P,
    theta_ds["longitude"],
    theta_ds["latitude"],
    dask="parallelized",
    output_dtypes=[float]
)


# Conservative Temperature

CT = xr.apply_ufunc(
    gsw.CT_from_pt,
    SA,
    T_mean,
    dask="parallelized",
    output_dtypes=[float]
)

# Thermal expansion coefficient

alpha = xr.apply_ufunc(
    gsw.alpha,
    SA,
    CT,
    P,
    dask="parallelized",
    output_dtypes=[float]
)

alpha.name="alpha"

print(
    "alpha:",
    alpha.min().values,
    alpha.max().values
)

# ============================================================
# 8. 计算 alpha*DeltaT
# ============================================================


alpha_deltaT = alpha * delta_T


alpha_deltaT.name="alpha_deltaT"


print(
    "alphaDeltaT:",
    alpha_deltaT.min().values,
    alpha_deltaT.max().values
)

# ============================================================
# 9. 保存三维结果
# ============================================================


alpha_deltaT.to_netcdf(
    os.path.join(
        DATA_DIR,
        "MPI_alpha_deltaT_1958_2014_3D_v2.nc"
    )
)

