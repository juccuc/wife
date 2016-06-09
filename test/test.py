
text=[]
fmt=""

sql="insert into risk_factor_summary values "
s=sql
f=open("vv.sql","w")


for i in xrange(1,len(text)):
    s = fmt % tuple(text[i])
    f.write(sql + s[:-1] + ";\n")


f.close()
