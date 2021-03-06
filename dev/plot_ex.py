#debuging with BBox:
                    #fig.canvas.draw()
                    par.draw(renderer = fig.canvas.get_renderer())
                    # Get Displaycoordinate in Pixel, translate to Axes coord
                    #box = par.yaxis.get_tightbbox(renderer = fig.canvas.get_renderer())
                    #print("box", box)
                    #pad = par.yaxis.majorTicks[0].get_pad_pixels()
                    labelpos = par.yaxis.label.get_window_extent()
                    #pxy = par.yaxis.label.get_position()
                    
                    #tick = par.yaxis.get_ticklabel_extents(renderer = fig.canvas.get_renderer())
                    oleft,oright = par.yaxis.get_text_widths(renderer = fig.canvas.get_renderer())
                    #pt.x1 = pt.x1 + oright
                    #spinebbox = par.spines['right'].get_transform().transform_path(par.spines['right'].get_path()).get_extents()
                    extents1, extents2 = par.yaxis.get_ticklabel_extents(renderer = fig.canvas.get_renderer())
                    #extents1 = par.yaxis._get_tick_boxes_siblings(renderer = fig.canvas.get_renderer())
                    #print("tick",pad)

                    ticks_to_draw = par.yaxis._update_ticks()
                    ticklabelBoxes, ticklabelBoxes2 = par.yaxis._get_tick_bboxes(ticks_to_draw,renderer = fig.canvas.get_renderer())
                    print("extents",extents1)
                    print("oright",oright)
                    print("tickbox ", ticklabelBoxes2)    

                    box = labelpos.transformed(par.transAxes.inverted())
                    #box = extents2.transformed(par.transAxes.inverted())
                    ticklabelBoxes2 = ticklabelBoxes2[1].transformed(par.transAxes.inverted())
                    #box = extents1[1][1].transformed(par.transAxes.inverted())
                    rect = Rectangle((box.xmin,box.ymin),box.width,box.height,clip_on=False, fill=False, transform= par.transAxes,ec='r', zorder=1000)
                    par.add_patch(rect)
                    rect1 = Rectangle((ticklabelBoxes2.xmin,ticklabelBoxes2.ymin),ticklabelBoxes2.width,ticklabelBoxes2.height,clip_on=False, fill=False, transform= par.transAxes,ec='r', zorder=1000)
                    par.add_patch(rect1)




import matplotlib.pyplot as plt


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


fig, host = plt.subplots()
fig.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

# Offset the right spine of par2.  The ticks and label have already been
# placed on the right by twinx above.
par2.spines["right"].set_position(("axes", 1.2))
# Having been created by twinx, par2 has its frame off, so the line of its
# detached spine is invisible.  First, activate the frame but make the patch
# and spines invisible.
make_patch_spines_invisible(par2)
# Second, show the right spine.
par2.spines["right"].set_visible(True)

#create plot, label for legende
p1, = host.plot([0, 1, 2], [0, 1, 2],ls="-",color="b", marker="o", label="Density")
p2, = par1.plot([0, 1, 2], [0, 3, 2], ls="-",color="r", label="Temperature")
p3, = par2.plot([0, 1, 2], [50, 30, 15], ls="-",color="g", label="Velocity")

#set Limits, ohne = hig-min
host.set_xlim(0, 2)
host.set_ylim(0, 2)
par1.set_ylim(0, 4)
par2.set_ylim(1, 65)

host.set_xlabel("Distance")
host.set_ylabel("Density")
par1.set_ylabel("Temperature")
par2.set_ylabel("Velocity")

#setzt farbe der labels
host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
par2.yaxis.label.set_color(p3.get_color())


plt.gcf().canvas.draw()
#position in pixel of Label-Bbox as object; var.x0 = value of x0
var = host.yaxis.label.get_window_extent()

#erzeugt einen zusätzlichen punkt, clip_on false für ausserhalb 
plt.scatter(-1,-1,marker="o",clip_on=False)




#fuer farbige punkte auf den  achsen
tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1.get_color(), **tkw)
par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
par2.tick_params(axis='y', colors=p3.get_color(), **tkw)

#legende in graph
lines = [p1, p2, p3]
host.legend(lines, [l.get_label() for l in lines])

plt.show()





#VARIANTE 2: 


from mpl_toolkits.axisartist.parasite_axes import HostAxes, ParasiteAxes
fig = plt.figure()
        host = HostAxes(fig, [0.15, 0.1, 0.65, 0.8])
        par1 = ParasiteAxes(host, sharex=host)
        par2 = ParasiteAxes(host, sharex=host)
        host.parasites.append(par1)
        host.parasites.append(par2)
        host.set_ylabel("Density")
        host.set_xlabel("Distance")
        host.axis["right"].set_visible(False)
        par1.axis["right"].set_visible(True)
        par1.set_ylabel("Temperature")
        par1.axis["right"].major_ticklabels.set_visible(True)
        par1.axis["right"].label.set_visible(True)
        par2.set_ylabel("Velocity")
        offset = (60, 0)
        new_axisline = par2.get_grid_helper().new_fixed_axis
        par2.axis["right2"] = new_axisline(loc="right", axes=par2, offset=offset)
        fig.add_axes(host)
        host.set_xlim(0, 2)
        host.set_ylim(0, 2)
        host.set_xlabel("Distance")
        host.set_ylabel("Density")
        par1.set_ylabel("Temperature")
        plt.scatter(-0,1,marker="o")
        p1, = host.plot([0, 1, 2], [0, 1, 2], label="Density")
        p2, = par1.plot([0, 1, 2], [0, 3, 2], label="Temperature")
        p3, = par2.plot([0, 1, 2], [50, 30, 15], label="Velocity")
        par1.set_ylim(0, 4)
        par2.set_ylim(1, 65)
        host.legend()
        host.axis["left"].label.set_color(p1.get_color())
        par1.axis["right"].label.set_color(p2.get_color())
        par2.axis["right2"].label.set_color(p3.get_color())


#Variante 3:


from mpl_toolkits.axes_grid.parasite_axes import SubplotHost
import matplotlib.pyplot as plt
import numpy as np
#data
x = (1, 3, 4, 6, 8, 9, 12)
y1 = (0, 1, 2, 2, 4, 3, 2)
y2 = (0, 3, 2, 3, 6, 4, 5)
y3 = (50, 40, 40, 30, 20, 22, 10)
y4 = (0.2, 0.5, 0.6, 0.9, 2, 5, 2)
y5 = (2, 0.5, 0.9, 9, 12, 15, 12)
y6 = (200, 500, 900, 900, 120, 150, 120)
#credits: http://matplotlib.sourceforge.net/examples/pylab_examples/multiple_yaxis_with_spines.html
class multiY():
    def __init__(self, height, width, X, LY, Xlabel, LYlabel, linecolor,
    set_marker, set_linestyle, fontsize, set_markersize,
    set_linewidth, set_mfc, set_mew, set_mec):
       
        self.X = X
       
        fig = plt.figure(figsize=(height, width))
       
        self.host = SubplotHost(fig, 111)
       
        plt.rc("font", size=fontsize)
       
        self.host.set_xlabel(Xlabel)
        self.host.set_ylabel(LYlabel)
        p1, = self.host.plot(X, LY, color=linecolor, marker=set_marker, ls=set_linestyle, ms=set_markersize, lw=set_linewidth, mfc=set_mfc, mew=set_mew, mec=set_mec)
       
        fig.add_axes(self.host)
       
        self.host.axis["left"].label.set_color(p1.get_color())
        self.host.tick_params(axis='y', color=p1.get_color())
       
    def parasites(self, set_offset, PY, PYlabel, side, Plinecolor,
    Pset_marker, Pset_linestyle, Pset_markersize, Pset_linewidth, Pset_mfc, Pset_mew, Pset_mec):           
        par = self.host.twinx()
        par.axis["right"].set_visible(False)
        offset = (set_offset, 0)
        new_axisline = par.get_grid_helper().new_fixed_axis
       
        par.axis["side"] = new_axisline(loc=side, axes=par, offset=offset)
       
        par.axis["side"].label.set_visible(True)
        par.axis["side"].set_label(PYlabel)
       
        p2, = par.plot(self.X, PY,color=Plinecolor, marker=Pset_marker, ls=Pset_linestyle, ms=Pset_markersize, lw=Pset_linewidth, mfc=Pset_mfc, mew=Pset_mew, mec=Pset_mec)
       
        par.axis["side"].label.set_color(p2.get_color())
        par.tick_params(axis='y', colors=p2.get_color())
#height, width, x-data, y-datam, X-label, Y-label, line color, markerstyle, linestyle,
# fontsize, markersize, linewidth, marker face color, marker edge with, marker edgecolor      
aa = multiY(10, 4, x, y1, "X-label", "Y-label", "r", "o", "None", 16, 8, 2, "none", "1", "r")
#offset, y-data, Y-label, side, color, marker edge with, marker edgecolor
aa.parasites(0, y2, "Parasite2", "right", "g", ">", "--", 10, 1, "none", "1", "g")
aa.parasites(-50, y3, "Parasite3", "left", "b", "<", "-", 10, 1, "none", "1", "b")
aa.parasites(50, y4, "Parasite4", "right", "m", "s", "-.", 10, 1, "none", "1", "m")
aa.parasites(-100, y5, "Parasite5", "left", "y", "d", "none", 10, 1, "none", "1", "y")
aa.parasites(100, y6, "Parasite6", "right", "k", "*", "--", 10, 1, "none", "1", "k")
#adjust the plot
plt.subplots_adjust(left=0.20, bottom=0.15, right=0.78, top=0.92, wspace=0.05, hspace=0)
plt.show()
#variante 4: FUNC!
import matplotlib.pyplot as plt
import numpy as np
def plotting_several_axis(variables, positions, colors, ylabels, xlabel, yaxislabels, 
                          fontsize=12, y_axis_dist = 0.2, figsize=(7,5)):

    plotting_several_axis(variables, positions, colors, ylabels, xlabel, yaxislabels, 
                          fontsize=12, y_axis_dist = 0.2, figsize=(7,5))

    Example:

    a1 = np.arange(1, 100, 1)
    a2 = np.arange(1, 100, 1)
    a = [a1, a2]
    b = [i**2 for i in a]
    c = [i/5 for i in b]
    d = [i*8 for i in c]
    e = [i+5 for i in d]
    variables = [a, b, c, d, e]

    positions = ['right', 'left', 'right', 'left', 'right']
    colors = ['green', 'blue', 'red', 'magenta', 'brown']
    ylabels = ['potatoes', 'rice', 'tomatoes', 'juice', 'cotton']
    xlabel = 'price'
    yaxislabels = ['item', 'kg', 'bunch', 'Liters', 'cm3']


    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig, host = plt.subplots(figsize=figsize)
    fig.subplots_adjust(right=0.75)
    ###### HOST PLOTTING
    tkw = dict(size=4, width=1.5, labelsize=fontsize)
    p1, = host.plot(variables[0][0], variables[0][1], colors[0], label=ylabels[0])
    host.set_xlabel(xlabel, fontsize=fontsize)
    host.set_ylabel(yaxislabels[0], fontsize=fontsize)
    host.yaxis.label.set_color(p1.get_color())
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)
    # host.set_xlim(0, 2)
    lines = [p1]
#     y_axis_dist = 0.2
    inc_r = 1
    inc_l = -y_axis_dist
    for ix, i in enumerate(variables):
        if ix != 0:
            par = host.twinx()
            if positions[ix] == 'right':
                par.spines[positions[ix]].set_position(("axes", inc_r))
                inc_r += y_axis_dist
            elif positions[ix] == 'left':
                par.spines[positions[ix]].set_position(("axes", inc_l))
                inc_l -= y_axis_dist
            make_patch_spines_invisible(par)
            par.spines[positions[ix]].set_visible(True)
            par.yaxis.set_label_position(positions[ix])
            par.yaxis.set_ticks_position(positions[ix])
            p, = par.plot(variables[ix][0], variables[ix][1], colors[ix], label=ylabels[ix])
            par.set_ylabel(yaxislabels[ix], fontsize=fontsize)
            par.yaxis.label.set_color(p.get_color())
            par.tick_params(axis='y', colors=p.get_color(), **tkw)
            lines.append(p)
    host.legend(lines, [l.get_label() for l in lines], fontsize=fontsize, loc='lower right')
    plt.savefig("example.png", dpi=300, bbox_inches="tight")
    plt.show()
a1 = np.arange(1, 100, 1)
a2 = np.arange(1, 100, 1)
a = [a1, a2]
b = [i**2 for i in a]
c = [i/5 for i in b]
d = [i*8 for i in c]
e = [i+5 for i in d]
variables = [a, b, c, d, e]
positions = ['right', 'left', 'right', 'left', 'right']
colors = ['green', 'blue', 'red', 'magenta', 'brown']
ylabels = ['potatoes', 'rice', 'tomatoes', 'juice', 'cotton']
xlabel = 'price'
yaxislabels = ['item', 'kg', 'bunch', 'Liters', 'cm3']
plotting_several_axis(variables, positions, colors, ylabels, xlabel, yaxislabels, y_axis_dist=0.2)
