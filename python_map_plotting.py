import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import geopandas as gpd
import datetime
import json
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Choose month 
month = 'July'

# Initialise background and data
uk = gpd.read_file(gpd.datasets.get_path('uk_highres')) # Custom map for background 
maxv, minv = max(gdf_2000_means[month]), min(gdf_2000_means[month])

# Initialise plot 
#fig = plt.subplots(figsize=(6,7),dpi=300)
ax = uk.plot(figsize=(6,7),kind='geo',
color='green', edgecolor='black', linewidth=0.5)
divider = make_axes_locatable(ax)

# ax plot
ax.set_facecolor('dodgerblue')
ax.set_title(f"{month} average temperature pre-2000")
ax.set_xlim(-9,3)
ax.set_xticks([])
ax.set_yticks([])

# Create cax
cax = divider.append_axes("right",size="5%",pad=0.1)

# Plot
gdf_2000_means.plot(column=month,cmap='magma',legend=True, \
                    vmin=minv, vmax=maxv, ax=ax, cax=cax, marker='s')

# Colorbar
cax.set_ylabel("Temperature ${C}^{\circ}$",rotation=90)


# Show
plt.savefig('../../Downloads/test_map.png',dpi=300) # Can set dpi to 300 when saving for high-res images