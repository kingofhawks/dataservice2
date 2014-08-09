# coding=utf-8
import time
import thread

def timer(no, interval):
    print 'timer'
    cnt = 0
    while cnt < 10:
        print 'Thread:(%d) Time:%s\n' % (no, time.ctime())
        time.sleep(interval)
        cnt += 1
#    thread.exit_thread()

def test():
    print 'start first'
    thread.start_new_thread(timer, (1, 1))
    print 'start second'
    thread.start_new_thread(timer, (2, 2))
    time.sleep(60)

if __name__ == '__main__':  
    test()