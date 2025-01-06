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

# # Plot Vessel Presence
#
# Plot vessel presence using the Spilhaus projection. This is nices in that it shows how the oceans connect better than
# more convential projections, but it suffers from some pretty serious size distortions. Most dramatically, the Chinese
# coast appears much larger in this projection than it should.

import numpy as np
import sys
sys.path.append('..')
from spilhaus.plot_spilhaus import plot_spilhaus

presence_raster = np.load('./presence_example.npz')['presence']
ocean_raster = np.load('./ocean.npz')['ocean']

plot_spilhaus(presence_raster, ocean_raster, resolution=6000, dpi=72)


