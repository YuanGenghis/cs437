def move25():
    speed4 = Speed(25)
    speed4.start()
    #time.sleep(2)
    fc.backward(100)
    x = 0
    for i in range(1):
        time.sleep(0.1)
        speed = speed4()
        x += speed * 0.1
        print("%smm/s"%speed)
    print("%smm"%speed)
    speed4.deinit()
    fc.stop()