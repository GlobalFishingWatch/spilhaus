import matplotlib.colors as mpcolors
import matplotlib.cm as mpcm
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import RegularGridInterpolator

from .spilhaus import (
    make_spilhaus_xy_gridpoints,
    from_spilhaus_xy_to_lonlat,
    prettify_spilhaus_df,
)


def hex_to_rgb(value):
    value = value.lstrip("#")
    lv = len(value)
    return tuple(int(value[i : i + lv // 3], 16) / 255.0 for i in range(0, lv, lv // 3))


def create_filled(mask, source_raster, fill=np.nan):
    empty = np.zeros(mask.shape)
    empty.fill(fill)
    empty[mask] = source_raster
    return empty


def interpolate_onto(lon, lat, source_raster):
    n_lat, n_lon = source_raster.shape
    source_lon = -180 + (0.5 + np.arange(n_lon) * 360) / n_lon
    source_lat = -90 + (0.5 + np.arange(n_lat) * 180) / n_lat

    interpolator = RegularGridInterpolator(
        (source_lat, source_lon),
        source_raster,
        bounds_error=False,  # ???
    )

    targets = np.stack((lat, (lon + 180) % 360 - 180), axis=-1)

    return interpolator(targets)


def plot_spilhaus(
    foreground_raster,
    ocean_raster,
    cmap=mpcm.plasma,
    background_color="#000000",
    resolution=2000,
    vmin=1,
    vmax=10000,
    dpi=300,
):
    # This is not a great way to plot a raster since it falls apart at low resolution,
    # but it's quick and fairly easy to set up.

    presence_df = make_spilhaus_xy_gridpoints(spilhaus_res=resolution)
    old_settings = np.seterr(all='ignore')
    lon, lat = from_spilhaus_xy_to_lonlat(presence_df["x"], presence_df["y"])
    np.seterr(**old_settings)

    mask = ~(np.isnan(lon) | np.isnan(lat))

    valid_lon = lon[mask]
    valid_lat = lat[mask]


    presence_df["z"] = create_filled(
        mask, interpolate_onto(valid_lon, valid_lat, foreground_raster)
    )

    splilhaus_ocean = presence_df.copy()
    splilhaus_ocean["z"] = create_filled(
        mask, interpolate_onto(valid_lon, valid_lat, ocean_raster > 0), fill=0.0
    )

    pretty_presence_df = prettify_spilhaus_df(presence_df)
    pretty_ocean_df = prettify_spilhaus_df(splilhaus_ocean)

    if isinstance(background_color, str):
        background_color = hex_to_rgb(background_color)

    z = np.minimum(pretty_presence_df["z"], 0.99 * vmax)

    norm = mpcolors.LogNorm(vmin=vmin, vmax=vmax, clip=True)

    fig, ax = plt.subplots(1, 1, figsize=(16, 16), dpi=dpi)

    foreground_mask = (pretty_ocean_df['z'] > 0)

    plt.scatter(
        x=pretty_presence_df["x"][foreground_mask],
        y=pretty_presence_df["y"][foreground_mask],
        c=z[foreground_mask],
        edgecolors="none",
        s=36.0 / dpi,
        cmap=cmap,
        norm=norm,
        zorder=1,
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])

    if background_color is not None:
        ax.patch.set_facecolor(background_color)
    plt.show()
