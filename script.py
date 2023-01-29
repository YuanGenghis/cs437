import picar_4wd as fc
import time

speed = 10

def main():
    while True:
        scan_list = fc.scan_step(37)
        if not scan_list:
            continue

        tmp = scan_list[3:7]
        print(tmp)
        if tmp != [2,2,2,2] and tmp != [0,0]:
            fc.backward(speed)
            time.sleep(0.3)
            fc.turn_right(speed)
            time.sleep(0.1)
        else:
            fc.forward(speed)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
