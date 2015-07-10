# ##############################################################################
# ICARENG path draw using matplotlib basemaps.
# Copyright (C) 2015-07 Joaquin Bogado <jbogado@linti.unlp.edu.ar>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#################################################################################

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from spacepy import pycdf
from math import sin, cos, sqrt, acos, asin, atan2, pi, atan, degrees


def xyz2xy(x, y, z, Rx=0, Ry=0, Rz=0):
    #rotate R degrees around axis
    x0  =  x
    y0  =  y*cos(Rx) + z*sin(Rx)
    z0  =  z*cos(Rx) - y*sin(Rx)
    x1  =  x0*cos(Ry) - z0*sin(Ry)
    y1  =  y0
    z1  =  z0*cos(Ry) + x0*sin(Ry)
    x2  =  x1*cos(Rz) + y1*sin(Rz)
    y2  =  y1*cos(Rz) - x1*sin(Rz)
    return x2, y2

def xyz2plh(x, y, z, A=6378137.0, FL=0):
#Converts XYZ geocentric coordinates to Phi (latitude),
# Lambda (longitude), H (height) referred to an
# ellipsoid of semi-major axis A and flattening FL.

    B = A * (1.0 - FL)
    #if z < 0.0:
    #    B = -B

    r = sqrt( x*x + y*y )
    e = ( B*z - (A*A - B*B) ) / ( A*r )
    f = ( B*z + (A*A - B*B) ) / ( A*r )

    p= (4.0 / 3.0) * (e * f + 1.0)
    q= 2.0 * (e * e - f * f)
    d= p * p * p + q * q
    if (d >= 0.0):
        v = pow((sqrt(d) - q), (1.0 / 3.0)) - pow((sqrt(d) + q), (1.0 / 3.0))
    else:
        v = 2.0 * sqrt(-p) * cos(acos(q / (p * sqrt(-p))) / 3.0)

    if(v*v < abs(p)):
        v= -(v * v * v + 2.0 * q) / (3.0 * p)
    g= (sqrt(e * e + v ) + e) / 2.0
    t = sqrt(g * g + (f - v * g) / (2.0 * g - e) ) - g

    P = atan((A*(1.0 - t * t)) / (2.0*B*t))
    H = (r - A * t) * cos(P) + (z - B) * sin(P)

    zlong = atan2(y, x)
    if (zlong < 0.0):
        zlong = zlong + 2 * pi
    L = zlong
    P = P*180/pi
    L = L*180/pi
    return P, L, H
#ecef.py
#https://code.google.com/p/pysatel/source/browse/trunk/coord.py?r=22

from math import pow, degrees, radians
from scipy import mat, cos, sin, arctan, sqrt, pi, arctan2, deg2rad, rad2deg

#TO-DO: UPDATE THESE NUMBERS USING THE earth_radius.py
#
# Constants defined by the World Geodetic System 1984 (WGS84)
a = 6378.137
b = 6356.7523142
esq = 6.69437999014 * 0.001
e1sq = 6.73949674228 * 0.001
f = 1 / 298.257223563

def geodetic2ecef(lat, lon, alt, degrees=True):
    """geodetic2ecef(lat, lon, alt)
                     [deg][deg][m]
    Convert geodetic coordinates to ECEF."""
    if degrees:
        lat=deg2rad(lat)
        lon=deg2rad(lon)
    #lat, lon = radians(lat), radians(lon)
    xi = sqrt(1 - esq * sin(lat))
    x = (a / xi + alt) * cos(lat) * cos(lon)
    y = (a / xi + alt) * cos(lat) * sin(lon)
    z = (a / xi * (1 - esq) + alt) * sin(lat)
    return x, y, z

def ecef2geodetic(x, y, z, degrees=True):
    """ecef2geodetic(x, y, z)
                     [m][m][m]
    Convert ECEF coordinates to geodetic.
    J. Zhu, "Conversion of Earth-centered Earth-fixed coordinates \
    to geodetic coordinates," IEEE Transactions on Aerospace and \
    Electronic Systems, vol. 30, pp. 957-961, 1994."""
    r = sqrt(x * x + y * y)
    Esq = a * a - b * b
    F = 54 * b * b * z * z
    G = r * r + (1 - esq) * z * z - esq * Esq
    C = (esq * esq * F * r * r) / (pow(G, 3))
    S = (1 + C + sqrt(C * C + 2 * C))**(1/3.0)
    P = F / (3 * pow((S + 1 / S + 1), 2) * G * G)
    Q = sqrt(1 + 2 * esq * esq * P)
    r_0 =  -(P * esq * r) / (1 + Q) + sqrt(0.5 * a * a*(1 + 1.0 / Q) - \
        P * (1 - esq) * z * z / (Q * (1 + Q)) - 0.5 * P * r * r)
    U = sqrt(pow((r - esq * r_0), 2) + z * z)
    V = sqrt(pow((r - esq * r_0), 2) + (1 - esq) * z * z)
    Z_0 = b * b * z / (a * V)
    h = U * (1 - b * b / (a * V))
    lat = arctan((z + e1sq * Z_0) / r)
    lon = arctan2(y, x)
    return rad2deg(lat), rad2deg(lon), z



# set up orthographic map projection with
# perspective of satellite looking down at 50N, 100W.
# use low resolution coastlines.
# map = Basemap(projection='geos',lon_0=0,resolution='l')
map = Basemap(projection='spaeqd',boundinglat=1,lon_0=0,resolution='h')
#map = Basemap(projection='cyl',llcrnrlat=-89.9999,urcrnrlat=89.9999,llcrnrlon=-180,urcrnrlon=180,lat_ts=0,resolution='l')
# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
map.fillcontinents(color='coral',lake_color='aqua')
# draw the edge of the map projection region (the projection limb)
map.drawmapboundary(fill_color='aqua')
# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))
# make up some data on a regular lat/lon grid.
#nlats = 73; nlons = 145; delta = 2.*np.pi/(nlons-1)
#lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
#lons = (delta*np.indices((nlats,nlons))[1,:,:])
#wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
#mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
# compute native map projection coordinates of lat/lon grid.
#x, y = map(lons*180./np.pi, lats*180./np.pi)
# contour data over the map.
#cs = map.contour(x,y,wave+mean,15,linewidths=1.5)

cdf = pycdf.CDF('~/cdfsall/SACD_H0_ICARENG_20150522_V01.cdf')

lat = []
lon = []
for p in cdf['Position'][...]:
    p,l,h = ecef2geodetic(p[0], p[1], p[2])
    lat.append(p)
    lon.append(l)

#p, l, h = xyz2plh(1000,1000, 6378137.0)
p = np.array(lat)
l = np.array(lon)
x, y = map(l,p)
cs = map.plot(x, y, 'r.')

cdf = pycdf.CDF('~/cdfsall/SACD_H0_ICARENG_20150523_V01.cdf')

lat = []
lon = []
for p in cdf['Position'][...]:
    p,l,h = ecef2geodetic(p[0], p[1], p[2])
    lat.append(p)
    lon.append(l)

#p, l, h = xyz2plh(1000,1000, 6378137.0)
p = np.array(lat)
l = np.array(lon)
x, y = map(l,p)
cs = map.plot(x, y, 'g.')

cdf = pycdf.CDF('~/cdfsall/SACD_H0_ICARENG_20150524_V01.cdf')

lat = []
lon = []
for p in cdf['Position'][...]:
    p,l,h = ecef2geodetic(p[0], p[1], p[2])
    lat.append(p)
    lon.append(l)

#p, l, h = xyz2plh(1000,1000, 6378137.0)
p = np.array(lat)
l = np.array(lon)
x, y = map(l,p)
cs = map.plot(x, y, 'b.')

plt.title('Satellite Path')
plt.show()
