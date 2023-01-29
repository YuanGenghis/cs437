import picar_4wd as fc
import time

speed = 10

def main():
    while True:
        # 37 is the baseline distance; which seems to be 37cm
        scan_list = fc.scan_step(37)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)

        # 3 intervals of ultrasonic sensor here
        # Case 1: dist < 10cm           -> 0
        # Case 2: 10cm < dist < 37cm    -> 1
        # Case 3: 37cm < dist           -> 2

        # The check for len(tmp) handles initializations
        if tmp != [2,2,2,2] and len(tmp) == 4:
            # When runs into an obstacle, the car will back up for 0.3s
            fc.backward(speed)
            time.sleep(0.3)

            # Then turn right for 0.1s
            fc.turn_right(speed)
            time.sleep(0.1)
        else:
            fc.forward(speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
