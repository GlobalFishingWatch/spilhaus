# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import numpy as np
import sys
sys.path.append('..')
from spilhaus.plot_spilhaus import plot_spilhaus

presence_raster = np.load('../untracked/presence.npz')['presence']
fishing_raster = np.load('../untracked/fishing.npz')['fishing']
ocean_raster = np.load('../untracked/ocean.npz')['ocean']

plot_spilhaus(presence_raster, ocean_raster)


