# Importing modules
import math
import tkinter as tk
from tkinter import ttk,messagebox
from datetime import datetime,timezone
import calendar
import pytz
import sounddevice as sd
import soundfile as sf

class Clock:
    def __init__(self,root,timezone):
        self.root=root
        self.root.title('Analog Clock')
        self.root.geometry('800x400')
        self.canvas=tk.Canvas(self.root,width=400,height=400,bg='white')
        self.canvas.place(x=0,y=0)
        self.frame=ttk.Frame(self.root)
        self.frame.place(x=400,y=0,width=400,height=400)
        self.timezone=timezone
        self.alarm_hour=None
        self.alarm_min=None
        self.ring_alarm=False

# Creating Elements of frame
    def create_dropdown_theme(self,frame):
        def on_select_theme(event):
            self.selected_value1.set(dropdown_theme.get())
                
        
        label=ttk.Label(frame,text='Select Theme')
        label.place(x=40,y=60)
        options=['Pleasant Brown','Aesthetic Black','Creative Pink','Stylish Green','Orange Sunset',
                     'Jolly Cream','Metal Grey','Cherry Blossom']
        self.selected_value1 = tk.StringVar(frame)
        self.selected_value1.set(options[0])
        dropdown_theme=ttk.Combobox(frame,values=options, textvariable=self.selected_value1)
        dropdown_theme.place(x=200,y=60)
        dropdown_theme.bind('<<ComboboxSelected>>',on_select_theme)

    def create_dropdown_timezone(self,frame):
        def on_select_timezone(event):
            self.selected_value2.set(dropdown_timezone.get())
                

        label=ttk.Label(frame,text='Select Timezone')
        label.place(x=40,y=140)
        options=['Asia/Kolkata','Europe/london','America/New_York','Europe/Moscow','Asia/Tokyo',
            'Australia/Sydney','Asia/Riyadh','Africa/Johannesburg','America/Argentina/Buenos_Aires']
        self.selected_value2 = tk.StringVar(frame)
        self.selected_value2.set(options[0])
        dropdown_timezone=ttk.Combobox(frame,values=options, textvariable=self.selected_value2)
        dropdown_timezone.place(x=200,y=140)
        dropdown_timezone.bind('<<ComboboxSelected>>',on_select_timezone)

    def create_button_timer(self,frame):
        button_timer = ttk.Button(frame,text='Timer',command=self.select_button_timer)
        button_timer.place(x=160,y=220)

    def create_button_alarm(self,frame):
        self.button_alarm = ttk.Button(frame,text='Set Alarm',command=self.select_button_alarm)
        self.button_alarm.place(x=160,y=290)

    def create_button_clear(self,frame):
        self.button_clear= ttk.Button(frame,text='Clear',command=self.select_button_clear)
        self.button_clear.place(x=160,y=350)

# Drawing on Canvas
    def draw_clock_face(self,color):
        for i in range(1,13):
            angle=math.radians(i*30 - 90)
                
            # Point one
            x1 = 170 + math.cos(angle)*110
            y1 = 170 + math.sin(angle)*110

            # Point two
            x2 = 170 + math.cos(angle)*150
            y2 = 170 + math.sin(angle)*150

            # create line
            self.canvas.create_line(x1,y1,x2,y2,width=2,fill=color)

    def draw_hands(self,hour_color,min_color,sec_color,tz):
        country_tz = pytz.timezone(tz)
        utc_now = datetime.now(timezone.utc)
        country_now = utc_now.astimezone(country_tz)

        self.hour = country_now.hour
        self.min = country_now.minute
        self.sec = country_now.second

        # angles
        hour_angle = math.radians((self.hour + self.min/60)*30 - 90)
        min_angle = math.radians((self.min + self.sec/60)*6 - 90)
        sec_angle = math.radians(self.sec*6 - 90)

        # draw hands
        self.draw_lines(hour_angle,50,hour_color,3)
        self.draw_lines(min_angle,80,min_color,3)
        self.draw_lines(sec_angle,80,sec_color,2)

    def draw_lines(self,angle,length,color,width):
        x = 170 + math.cos(angle)*length
        y = 170 + math.sin(angle)*length

        self.canvas.create_line(170,170,x,y,fill=color,width=width,tag='hands')

    def show_time_day(self):
        meridian = 'A.M' if self.hour<12 else 'P.M'
        hour=self.hour if self.hour<12 else self.hour-12
        font=('Gotham',14,'bold')
        color = self.change_theme(self.selected_value1.get())
        self.canvas.create_text(170,350,text=f'{hour:02}:{self.min:02}:{self.sec:02} {meridian}',font=font,fill=color[1],tag='digital')

        now = datetime.now()
        weekdays={0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
        month_num = now.month
        month_name=calendar.month_name[month_num]
        self.canvas.create_text(170,370,font=font,text=f'{weekdays[now.weekday()]}, {now.day} {month_name}, {now.year}',fill=color[1],tag='digital')
        self.root.after(1000,self.show_time_day)




# Functions for buttons
    # Functions for Timer
    def select_button_timer(self):
        self.entry1=ttk.Entry(self.frame,width=3)
        self.entry1.place(x=140,y=260)
        self.entry1.insert(0,'00')
        self.label1=ttk.Label(self.frame,text=':')
        self.label1.place(x=166,y=260)

        self.entry2=ttk.Entry(self.frame,width=3)
        self.entry2.place(x=175,y=260)
        self.entry2.insert(0,'00')
        self.label2=ttk.Label(self.frame,text=':')
        self.label2.place(x=201,y=260)

        self.entry3=ttk.Entry(self.frame,width=3)
        self.entry3.place(x=210,y=260)
        self.entry3.insert(0,'00')

        self.button_start=ttk.Button(self.frame,text='Start',command=self.start_timer)
        self.button_start.place(x=300,y=260)

    def start_timer(self):
        flag=True
        try:
            hour = int(self.entry1.get()) if self.entry1.get() else 0
            minute = int(self.entry2.get()) if self.entry2.get() else 0
            second = int(self.entry3.get()) if self.entry3.get() else 0

            if not(0<=hour<=23 and 0<=minute<=59 and 0<=second<=59):
                raise ValueError
            
        except ValueError:
            messagebox.showinfo('Error','Please enter valid values (HH:MM:SS)')
            self.entry1.delete(0,tk.END)
            self.entry2.delete(0,tk.END)
            self.entry3.delete(0,tk.END)
            self.entry1.insert(0,'00')
            self.entry2.insert(0,'00')
            self.entry3.insert(0,'00')
            flag = False

        else:
            self.total_seconds = hour*3600 + minute*60 + second

        if flag:
            self.button_start.config(text='Stop',command=self.stop_timer,state=tk.NORMAL)
            self.update_timer()

        
    def stop_timer(self):
        self.button_start.config(text='Start',state=tk.NORMAL)

    def update_timer(self):
         
        hour = self.total_seconds //3600
        minute = (self.total_seconds % 3600) // 60
        second = self.total_seconds % 60
        self.entry1.delete(0,tk.END)
        self.entry2.delete(0,tk.END)
        self.entry3.delete(0,tk.END)
        self.entry1.insert(0,f'{hour:02}')
        self.entry2.insert(0,f'{minute:02}')
        self.entry3.insert(0,f'{second:02}')
        flag = self.button_start.cget('text')
        if self.total_seconds == 0 or flag == 'Start' :
            self.button_start.config(command=self.start_timer)
            self.button_clear.config(command=self.select_button_clear)  ####

            if self.total_seconds == 0:
                self.button_start.config(text='Start')
                self.play_sound_timer()
                self.button_clear.config(command=self.select_button_clear)  ####
            return
        self.total_seconds-=1
        
        self.root.after(1000,self.update_timer)

    # Functions for Alarm
    def select_button_alarm(self):
        self.entry4=ttk.Entry(self.frame,width=3)
        self.entry4.place(x=140,y=320)
        self.entry4.insert(0,'00')
        self.label3=ttk.Label(self.frame,text=':')
        self.label3.place(x=166,y=320)

        self.entry5=ttk.Entry(self.frame,width=3)
        self.entry5.place(x=175,y=320)
        self.entry5.insert(0,'00')
        options=['A.M','P.M']
        self.selected_value3 = tk.StringVar()
        self.selected_value3.set(options[0])
        self.dropdown_am_pm=ttk.Combobox(self.frame,values=options,width=4, textvariable=self.selected_value3)
        self.dropdown_am_pm.place(x=210,y=320)
                

        self.button_set=ttk.Button(self.frame,text='Set',command=self.set_alarm)
        self.button_set.place(x=300,y=320)

    def set_alarm(self):
        flag = True
        while True:
            try:
                hour=int(self.entry4.get())
                min=int(self.entry5.get())
            except ValueError:
                messagebox.showinfo('Error','Please enter valid values [HH:MM]')
                self.entry4.delete(0,tk.END)
                self.entry4.insert(0,'00')
                self.entry5.delete(0,tk.END)
                self.entry5.insert(0,'00')
                flag = False
            else:
                break
        
        if flag:
            meridian = self.dropdown_am_pm.get()
            self.entry4.destroy()
            self.entry5.destroy()
            self.dropdown_am_pm.destroy()
            self.label3.destroy()
            self.label_alarm = tk.Label(self.frame,text=f'Alarm set for {hour:02}:{min:02} {meridian}')
            self.label_alarm.place(x=140,y=320)
            self.button_set.config(text='Remove',command=self.remove_alarm)
                        
            if meridian == 'P.M':
                hour+=12
                        
            self.alarm_hour=hour
            self.alarm_min=min
            self.ring_alarm=True

    def remove_alarm(self):
        self.label_alarm.destroy()
        self.button_set.destroy()
        self.ring_alarm=False

    # Function for Clear
    def select_button_clear(self):
        try:
            self.entry1.destroy()
            self.entry2.destroy()
            self.entry3.destroy()
            self.label1.destroy()
            self.label2.destroy()
            self.button_start.destroy()
            self.entry4.destroy()
            self.entry5.destroy()
            self.label3.destroy()
            self.dropdown_am_pm.destroy()
            self.button_set.destroy()
        except:
            pass

# Funtion to change theme
    def change_theme(self,theme):

        themes={'Pleasant Brown':['#b6977d','#353634','#353634','#353634','#F8F4E1'],
                'Aesthetic Black':['#000000','#F4DFC8','#F4DFC8','#F4DFC8','#F4EAE0'],
                'Creative Pink':['#D2649A','#F6FAB9','#F6FAB9','#F6FAB9','#CAE6B2'],
                'Stylish Green':['#6B8A7A','#B7B597','#B7B597','#B7B597','#DAD3BE'],
                'Orange Sunset':['#FEFFD2','#FFBF78','#FFBF78','#FFBF78','#FF7D29'],
                'Jolly Cream':['#F1E5D1','#DBB5B5','#DBB5B5','#DBB5B5','#C39898'],
                'Metal Grey':['#686D76','#373A40','#373A40','#373A40','#DC5F00'],
                'Cherry Blossom':['#FFD0D0','#FF9EAA','#FF9EAA','#FF9EAA','#F9F9E0'],}

        return themes[theme]
    
# Functions to play sound
    def play_sound_timer(self):
        data, fs = sf.read('assets/timer.wav', dtype='float32')
        sd.play(data, fs)
        sd.wait()

    def play_sound_alarm(self): 
        Time=datetime.now()
        
        if (self.alarm_hour==Time.hour and self.alarm_min==Time.minute) and self.ring_alarm:

            data, fs = sf.read('assets/alarm.mp3',dtype='float32')
            sd.play(data,fs)
            sd.wait()
            self.ring_alarm=False

# Funtion to Update Clock
    def update_clock(self):
        self.canvas.delete('hands')
        self.canvas.delete('digital')
        theme=self.selected_value1.get()
        colors=self.change_theme(theme)
        self.canvas.config(bg=colors[0])
        tz=self.selected_value2.get()
        self.play_sound_alarm()
        self.draw_clock_face(colors[1])
        self.draw_hands(colors[2],colors[3],colors[4],tz=tz)
        self.show_time_day()
            

        self.root.after(1000,self.update_clock)


# Main Method
    def main(self):
        # adding elements to frame
        self.create_dropdown_theme(self.frame)
        self.create_dropdown_timezone(self.frame)
        self.create_button_timer(self.frame)
        self.create_button_alarm(self.frame)
        self.create_button_clear(self.frame)

        # drawing clock
        self.draw_clock_face('black')
        self.draw_hands('black','black','black','Asia/Kolkata')
        self.show_time_day()
        self.update_clock()

        self.root.mainloop()




if __name__=='__main__':
    root=tk.Tk()
    ob=Clock(root,'Asia/Kolkata')
    ob.main()

    

                