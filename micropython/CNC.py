import math
from machine import Timer, Pin
import time
import machine

pulse = 0.02
max_f = 20
frequency = 1000
timer_counter = 0
x_counter = 0
y_counter = 0
timer0 = Timer(0)
x_dir = Pin(21, Pin.OUT)
y_dir = Pin(22, Pin.OUT)
x_pul = Pin(23, Pin.OUT)
y_pul = Pin(25, Pin.OUT)
x_pul.off()
y_pul.off()
finished = True


def linear_move(x, y, f):
    global pulse, timer_counter, x_counter, y_counter, timer0, x_pul, y_pul, finished
    length = math.sqrt((x * pulse) ** 2 + (y * pulse) ** 2)
    interrupts = int((length / f) * frequency)
    timer_counter = 0
    x_counter = 0
    y_counter = 0
    if x > 0:
        x_dir.on()
    else:
        x_dir.off()
    if y > 0:
        y_pul.on()
    else:
        y_pul.off()
    finished = False

    def callback(t):
        global timer_counter, x_counter, y_counter, x_pul, y_pul, finished
        timer_counter += 1
        if timer_counter >= interrupts:
            timer0.deinit()
            while x_counter < x:
                x_counter += 1
                x_pul.on()
                time.sleep_us(100)
                x_pul.off()
            while y_counter < y:
                y_counter += 1
                y_pul.on()
                time.sleep_us(100)
                y_pul.off()
            finished = True
            return
        x_move = (timer_counter / interrupts) * x >= x_counter
        y_move = (timer_counter / interrupts) * y >= y_counter
        if x_move:
            x_pul.on()
            x_counter += 1
        if y_move:
            y_pul.on()
            y_counter += 1
        time.sleep_us(100)
        if x_move:
            x_pul.off()
        if y_move:
            y_pul.off()

    timer0.init(period=1, mode=Timer.PERIODIC, callback=callback)
    while not finished:
        time.sleep_us(50)


def test():
    machine.freq(240000000)
    linear_move(10, 10**3, 10**2)
    machine.freq(160000000)


def test2():
    machine.freq(240000000)
    max_time = 0
    for _ in range(100):
        start_time = time.ticks_ms()
        for i in range(1000):
            linear_move(10, 10**3, 10**2)
        end_time = time.ticks_ms()
        diff_time = time.ticks_diff(end_time, start_time)
        if diff_time > max_time:
            max_time = diff_time
    machine.freq(160000000)
    return max_time
