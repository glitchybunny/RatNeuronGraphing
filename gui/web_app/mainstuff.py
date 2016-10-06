import os
import parsematlab_rats
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
from plotly.offline import download_plotlyjs, plot, iplot, init_notebook_mode
from math import floor, hypot

from random import randint

init_notebook_mode(connected=True)

# Color scales
cs_default = ['#EB3821', '#DDE22A', '#67BB47', '#6FCBD5', '#354D9D', '#D2D0E9']
cs_magma = ['#FBFABD', '#FD9A69', '#E85461', '#842681', '#360F6B', '#000000']
cs_heatmap = ['rgb(165,0,38)', 'rgb(215,48,39)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(254,224,144)', 'rgb(224,243,248)', 'rgb(171,217,233)', 'rgb(116,173,209)', 'rgb(69,117,180)', 'rgb(49,54,149)']
cs_greyscale = ['rgb(0,0,0)', 'rgb(255,255,255)']
cs_hm_default = [[0,'#EB3821'], [10,'#DDE22A'], [20,'#67BB47'], [30,'#6FCBD5'], [40,'#354D9D'], [50,'#D2D0E9']]


# Create new folder if one doesn't already exist
def ensure_dir(f):
    d = os.path.dirname(os.getcwd() + f)
    if not os.path.exists(d):
        os.makedirs(d)
        return True
    return False

# Sorts the values in separate sections to list of plot-able coordinates
def vals_to_coords(vals):
    sortedvals = []
    coords = []
    n = []

    for i in vals:
        if i == 62: # end row
            sortedvals += [n]
            n = []
        else:
            n += [i]

    for i in range(len(sortedvals)):
        for j in sortedvals[i]:
            for k in j[2]:
                coords += [(k, j[1]+(i/len(sortedvals)))]

    return coords

# Main plotting function (call this from other code)
def plot_with_plotly(filename, colorscale=cs_default, quality=16, size=(512,512)):
    trace = {}

    for file in [filename]:
        extractedfile = parsematlab_rats.extractmatlab(file)
        coordinates = vals_to_coords(extractedfile)
        trace[file] = FF.create_2D_density (
            x = [i[0] for i in coordinates],
            y = [i[1] for i in coordinates],
            width = size[0],
            height = size[1],
            colorscale = colorscale,
            point_color = (0,0,0,0),
            point_size = 1,
            ncontours = quality
        )
        print(file + " graphed successfully")

    for i in trace:
        plot(trace[i], filename=i+'.html')#, auto_open=False)



### --- TEMPORARY TESTING CODE; REMOVE IN FINAL BUILD --- ###
if __name__ == '__main__':
    '''
    files = ['659601_rec03_all.mat']
    for i in files:
        plot_with_plotly(i, cs_greyscale, size=(1000,1000))
    '''
    extractedfile = parsematlab_rats.extractmatlab('659601_rec03_all.mat')

    width = 1200
    height = len(extractedfile)
    radius = int(60*(width/2500))

    heatmap = [[0 for i in range(width)] for j in range(height)]
    for k in vals_to_coords(extractedfile):
        _x = floor(k[0] * width // 50)
        _y = floor(k[1]*height//11)
        x1, x2 = max(0, min(width, _x-radius)), max(0, min(width, _x+radius))
        y1, y2 = max(0, min(height, _y-radius)), max(0, min(height, _y+radius))
        for i in range(x1, x2):
            for j in range(y1, y2):
                pythag = hypot(_x-i, _y-j)
                if pythag <= radius:
                    heatmap[j][i] += 1#-(pythag/radius)**1/2

    plot([{
        'z': heatmap,
        'type': 'heatmap',
        'hoverinfo': 'z',
        'colorscale': -1,
        'colorbar': {
            'tick0': 0,
            'dtick': 0
        }
    }], filename='waht.html')