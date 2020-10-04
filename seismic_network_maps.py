# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:12:09 2020

@author: Kevin Davidson
"""

import pygmt
import numpy as np
from obspy.clients.fdsn import Client

def plot_stations(network):
    """
    Draws a map of stations in an IRIS network.
    """
    client = Client('IRIS')
    network = network
    inventory = client.get_stations(network=network)
    net = inventory[0]
    lons = []
    lats = []
    names = []
    
    # extract the values we want from the inventory
    for sta in net:
        lons.append(sta.longitude)
        lats.append(sta.latitude)
        names.append(sta.code)
    
    #pad out the region we're going to draw
    region = [np.min(lons), np.max(lons), np.min(lats), np.max(lats)]
    x_pad = (region[1] - region[0]) * 0.1
    y_pad = (region[3] - region[2]) * 0.1
    region = [region[0] - x_pad, region[1] + x_pad, region[2] - y_pad, region[3] + y_pad]

    # Set up the stereographic projection
    lon_0 = np.mean(region[:2])
    lat_0 = np.mean(region[2:])
    if lat_0 > 0:
            ref_lat = 90
    else:
            ref_lat = -90

    # GMT strings
    projection = f'S{lon_0}/{ref_lat}/6i'
    map_scale= f'JTL+c{lon_0}+w100k+f'
    rose = 'JML+w1i+f3+l'

    # Create figure
    fig = pygmt.Figure()
    fig.grdimage(grid='@earth_relief_15s',
             region = region,
             projection = projection,
             frame = ['a', f'+t"{network} Seismograph Network"'],
             shading=True,
            )
    fig.coast(shorelines=True)
    fig.basemap(map_scale=map_scale, rose=rose)
    fig.plot(lons, lats, style='i0.2i', color='red', pen=True)
    fig.text(x=lons, y=lats, text=names, justify='CT', offset='j0/0.5')
    
    return fig