import serial
import time
import tkinter as tk

# Change COM port to correct num
ser = serial.Serial("COM6", baudrate=9600, timeout=10)
time.sleep(5) # Account for arduiono serial setup

# Create window
root = tk.Tk()
root.title('Guitar GUI')
root.geometry('1000x400') # Mutable aspect ratio

top_frame = tk.Frame(root, height=100)
top_frame.pack(fill="x")

title = tk.Label(top_frame, text="Guitar strings and frets", font=("Arial", 16))
title.pack(pady=10)

grid_frame = tk.Frame(root)
grid_frame.pack(fill="both", expand=True)

STRINGS = 5
FRETS = 13
cells = []

def grid_setup():
    for i in range(STRINGS):
        grid_frame.rowconfigure(i, weight=1)
        row = []
        for j in range(FRETS):
            grid_frame.columnconfigure(j, weight=1)

            cell = tk.Label(
                grid_frame,
                bg="white",
                relief="solid",
                borderwidth=1
            )
            cell.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
            row.append(cell)

        cells.append(row)

def get_line(line):
    try:
        info = line.split()
        string = int(info[0])
        frets = [int(i) for i in info[1].split(",")]
    except Exception as e:
        print(e)

    return string, frets

# make rolling avgs for first 10 seconds calibration, add fret avgs for each reading for eaach string, increment count for each string read
# divide by count at end of calibration
# when reading is +/- x from avg, change fret color on GUI
template_dict = {
    "fret_avgs": [0 for _ in range(13)],
    "count": 0
}

rolling_avg_dict = {string_num: template_dict for string_num in range(STRINGS)}

def calibrate():
    t_end = time.time() + 20
    while time.time() < t_end:
        try:
            line = ser.readline().decode('utf-8').strip()
            string, frets = get_line(line)

            for fret in range(FRETS):
                rolling_avg_dict[string]["fret_avgs"][fret] += frets[fret]
            rolling_avg_dict[string]["count"] += 1 
        except Exception as e:
            print(e)

    try:
        for cur_string in range(STRINGS):
            for cur_fret in range(FRETS):
                rolling_avg_dict[cur_string]["fret_avgs"][cur_fret] /= rolling_avg_dict[cur_string]["count"]
    except Exception as e:
        print(e)

def clear_cur_string(string_num):
    for fret in range(FRETS):
        cells[string_num][fret].config(bg="white")

def update_screen():
    try:
        line = ser.readline().decode('utf-8').strip()
        string, frets = get_line(line)
        print(string, frets)
        clear_cur_string(string)

        for fret_num, fret in enumerate(frets):
            if fret + 100 > rolling_avg_dict[string]["fret_avgs"][fret_num] or fret - 100 < rolling_avg_dict[string]["fret_avgs"][fret_num] or fret > 1000:
                cells[string][fret_num].config(bg="green")
    except Exception as e:
        print(e)
    root.after(5, update_screen)

calibrate()
grid_setup()
update_screen()
root.mainloop()