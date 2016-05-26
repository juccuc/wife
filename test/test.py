from pylab import *
from datetime import datetime,timedelta

frm='%Y-%m-%d %H:%M:%S.%f'

X=drange(datetime.strptime("2014-02-09 21:12:10.000000",frm),
              datetime.strptime("2014-02-22 10:57:04.000000",frm),timedelta(seconds=1));
print X.size

def aa(t):
    print type(t),t
    return 1
Y=np.fromfunction(aa,)

plot(X,Y,color="blue")
show()