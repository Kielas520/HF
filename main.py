import time
import modules.now_recv as now
from modules.stepper import Stepper
from modules.serial_recv import read_uart

time.sleep(1)

mode = 0
con_frame = 0

def ang_solve(data):
    ang = (data / 110) * 90
    return ang


motor_y = Stepper(25,27,steps_per_rev=200*16,speed_sps=2000, timer_id=1)
motor_x = Stepper(26,16,steps_per_rev=200*16,speed_sps=2000, timer_id=2)
    
while True:
    data_esp = now.read_espnow()
    data_esp = now.process_data(data_esp)

    if data_esp:
        
        if data_esp[6] == 64:
            con_frame += 1
        if con_frame > 3 and data_esp[6] == 0:
            mode += 1
            mode = mode % 2
            con_frame = 0
 
        if mode == 0:
            print(data_esp)
            if data_esp[4] > 10 or data_esp[4] < -10:
                #print(-ang_solve(data_esp[4]) * 0.05)
                motor_y.target_deg_relative(ang_solve(data_esp[4]) * 0.05)
            if data_esp[1] > 10 or data_esp[1] < -10 :
                #print(-ang_solve(data_esp[1]) * 0.05)
                motor_x.target_deg_relative(-ang_solve(data_esp[1]) * 0.05)
        
        elif mode == 1:
            data = read_uart()
            if data:
                print(data)
                if data[0] == 1:
                    motor_x.target_deg_relative(-data[1] * 0.1)
                    motor_y.target_deg_relative(-data[2] * 0.1)
            else:
                continue
    else:
        continue


    #print(data_esp)
    time.sleep(0.01)