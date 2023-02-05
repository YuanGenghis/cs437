import picar_4wd as fc
import time

speed = 20

def main():
    fc.turn_right(speed)
    time.sleep(1.325)
    fc.stop()


main()

