import numpy
import matplotlib
import matplotlib.pyplot as plt

def on_motion(event):
    if event.inaxes:
        print "------"
    #     print "before setting position : "
    #     print this_annotation.get_position()
        global  this_annotation
        this_annotation.remove()
        this_annotation = ax.annotate("Mouseover point %s" % str(event.x) + ' ' + str(event.y),
        xy=(event.xdata, event.ydata), xycoords='data',
        xytext=(event.x + 30, event.y), textcoords='figure pixels',
        horizontalalignment="left",
        arrowprops=dict(arrowstyle="simple",
                        connectionstyle="arc3,rad=-0.2"),
        bbox=dict(boxstyle="round", facecolor="w",
                  edgecolor="0.5", alpha=0.9)
        )

        # this_annotation.set_text('coordinate : ' + str(event.x) + ' ' + str(event.y))
        # this_annotation.center=(event.x, event.y)
    #     print "after setting position : "
    #     print this_annotation.get_position()
    #     ax.draw_artist(this_annotation)
        fig.canvas.draw()

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(range(10), range(10))


this_annotation = ax.annotate("coordinate : ",
xy = (100,100),
xycoords = 'figure pixels',
horizontalalignment = 'left',
verticalalignment = 'top',
fontsize = 20,
fontweight = 'bold',# animated=True,
bbox = dict(boxstyle="round", fc='black', ec="0.5", alpha=0.5)
)

fig.canvas.mpl_connect('button_press_event', on_motion)
plt.show()