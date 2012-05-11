import os, re
import subprocess as sub

DEBUG_EXE = "debug.exe"
TARGET_EXE = "patched.exe"
SAMPLES_DIR = "samples"
TOTAL = 100

def run(sample_fn, dt, c, timeout):
    dt, c, timeout = str(dt), str(c), str(timeout)
    p = sub.Popen([DEBUG_EXE, TARGET_EXE, sample_fn, dt, c, timeout], stdout=sub.PIPE, stderr=sub.PIPE)

    o, errors = p.communicate()

    txt = o+errors
    return txt

def crashed(txt):
    return txt.find("watchdog end")<0

def extract(txt):
    l = re.findall("elapsed: (.*), total bbs: (.*)", txt)
    t = l[0][0]
    n = l[0][1]
    return int(t),int(n)

def one(fn, dt,c,timeout):
    o = run(fn, dt, c, timeout)
    if crashed(o):
        print o
        assert False
    t,n = extract(o)
    return float(t),float(n)

fns = os.listdir(SAMPLES_DIR)
fns = map(lambda fn: os.path.join(SAMPLES_DIR, fn), fns)

dt1,c1,timeout1 = 1000,0.0,2000
dt2,c2,timeout2 = 200,1.01,2000
speed = accuracy = 0.0

TOTAL = min(len(fns), TOTAL)
fns = fns[:TOTAL]
print "TOTAL:", TOTAL

for i,fn in enumerate(fns):
    print i
    t1,n1 = one(fn,dt1,c1,timeout1)
    t2,n2 = one(fn,dt2,c2,timeout2)
    
    print t1, n1
    print t2, n2

    speed += t2/t1
    accuracy += n2/n1

speed = speed/TOTAL
accuracy = accuracy/TOTAL

print "speed:", speed
print "accuracy:", accuracy
