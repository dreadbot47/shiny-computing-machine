import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

def contact():
    mess._show(title='Contact us', message="Please contact us on: 2255")

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        mess._show(title='Some file missing', message='Please contact us for help')
        window.destroy()

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    if op == key:
        if newp == nnewp:
            txf = open("TrainingImageLabel/psd.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()

def change_pass():
    global master
    master = tk.Toplevel(window)
    master.geometry("400x160")
    master.resizable(False, False)
    master.title("Change Password")
    master.configure(background="#f0f0f0")
    
    # Apply modern styling
    style = ttk.Style(master)
    style.configure('TEntry', font=('Roboto', 12))
    style.configure('TButton', font=('Roboto', 10, 'bold'))
    
    # Create a frame for content
    content_frame = tk.Frame(master, bg="#f0f0f0", padx=20, pady=10)
    content_frame.pack(fill="both", expand=True)
    
    lbl4 = tk.Label(content_frame, text='Enter Old Password', bg='#f0f0f0', font=('Roboto', 12))
    lbl4.grid(row=0, column=0, sticky='w', pady=5)
    
    global old
    old = ttk.Entry(content_frame, width=25, font=('Roboto', 12), show='*')
    old.grid(row=0, column=1, pady=5)
    
    lbl5 = tk.Label(content_frame, text='Enter New Password', bg='#f0f0f0', font=('Roboto', 12))
    lbl5.grid(row=1, column=0, sticky='w', pady=5)
    
    global new
    new = ttk.Entry(content_frame, width=25, font=('Roboto', 12), show='*')
    new.grid(row=1, column=1, pady=5)
    
    lbl6 = tk.Label(content_frame, text='Confirm New Password', bg='#f0f0f0', font=('Roboto', 12))
    lbl6.grid(row=2, column=0, sticky='w', pady=5)
    
    global nnew
    nnew = ttk.Entry(content_frame, width=25, font=('Roboto', 12), show='*')
    nnew.grid(row=2, column=1, pady=5)
    
    # Button frame
    btn_frame = tk.Frame(content_frame, bg="#f0f0f0")
    btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
    
    save1 = ttk.Button(btn_frame, text="Save", command=save_pass, width=15)
    save1.pack(side="left", padx=5)
    
    cancel = ttk.Button(btn_frame, text="Cancel", command=master.destroy, width=15)
    cancel.pack(side="left", padx=5)
    
    master.transient(window)
    master.grab_set()
    master.focus_set()

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        tf = open("TrainingImageLabel/psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas is None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("TrainingImageLabel/psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == key:
        TrainImages()
    elif password is None:
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')

def clear():
    txt.delete(0, 'end')
    res = "1) Take Images → 2) Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1) Take Images → 2) Save Profile"
    message1.configure(text=res)

def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists:
        with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial += 1
        serial = (serial // 2)
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
    Id = txt.get()
    name = txt2.get()
    if (name.isalpha() or ' ' in name):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                cv2.imwrite("TrainingImage/" + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID: " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        message1.configure(text=res)
    else:
        if not name.isalpha():
            res = "Enter Correct name"
            message.configure(text=res)

def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("TrainingImageLabel/Trainner.yml")
    res = "Profile Saved Successfully"
    message1.configure(text=res)
    message.configure(text='Total Registrations till now: ' + str(ID[0]))

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    exists3 = os.path.isfile("TrainingImageLabel/Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails/StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails/StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        return

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if conf < 50:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)[1:-1]
                bb = str(aa)[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance/Attendance_" + date + ".csv")
    if exists:
        with open("Attendance/Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
    else:
        with open("Attendance/Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)

    with open("Attendance/Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i += 1
            if i > 1 and i % 2 != 0:
                iidd = str(lines[0]) + '   '
                tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))

    cam.release()
    cv2.destroyAllWindows()

######################################## USED STUFFS ############################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.title("Facial Recognition Attendance System")
window.geometry("1280x720")
window.resizable(True, False)

# Set app theme with modern colors
main_bg = "#f5f5f5"  # Light gray background
accent_color = "#3498db"  # Blue accent color
secondary_accent = "#2ecc71"  # Green for positive actions
danger_color = "#e74c3c"  # Red for warnings/dangerous actions
text_color = "#2c3e50"  # Dark text for better contrast
header_bg = "#34495e"  # Dark header background
card_bg = "#ffffff"  # White background for cards

window.configure(background=main_bg)

# Configure ttk styles for a more modern look
style = ttk.Style(window)
style.theme_use('clam')  # Use clam theme as base

# Configure styles for various widgets
style.configure('TFrame', background=main_bg)
style.configure('Header.TLabel', font=('Roboto', 18, 'bold'), background=header_bg, foreground='white')
style.configure('Card.TFrame', background=card_bg, relief='flat')
style.configure('TButton', font=('Roboto', 12), background=accent_color, foreground='white')
style.configure('Accent.TButton', background=accent_color, foreground='white')
style.configure('Success.TButton', background=secondary_accent, foreground='white')
style.configure('Danger.TButton', background=danger_color, foreground='white')
style.configure('TLabel', font=('Roboto', 12), background=card_bg)
style.configure('Header.TLabel', font=('Roboto', 16, 'bold'), background=header_bg, foreground='white')
style.configure('Title.TLabel', font=('Roboto', 24, 'bold'), background=main_bg, foreground=text_color)
style.configure('Subtitle.TLabel', font=('Roboto', 14), background=main_bg, foreground=text_color)
style.configure('Info.TLabel', font=('Roboto', 12), background=card_bg, foreground=text_color)
style.configure('Treeview', font=('Roboto', 11))
style.map('TButton', background=[('active', accent_color)])

# Create a header frame
header_frame = ttk.Frame(window, style='TFrame')
header_frame.pack(fill='x', pady=10)

# App title and date-time display
app_title = ttk.Label(header_frame, text="FACIAL RECOGNITION ATTENDANCE SYSTEM", style='Title.TLabel')
app_title.pack(pady=5)

datetime_frame = ttk.Frame(header_frame, style='TFrame')
datetime_frame.pack(pady=5)

datef = ttk.Label(datetime_frame, text=f"{day}-{mont[month]}-{year}", style='Subtitle.TLabel')
datef.pack(side='left', padx=10)

separator = ttk.Label(datetime_frame, text="|", style='Subtitle.TLabel')
separator.pack(side='left')

clock = ttk.Label(datetime_frame, style='Subtitle.TLabel')
clock.pack(side='left', padx=10)
tick()

# Main content area with two panels
content_frame = ttk.Frame(window, style='TFrame')
content_frame.pack(fill='both', expand=True, padx=20, pady=10)

# Left panel for Attendance
left_panel = ttk.Frame(content_frame, style='Card.TFrame')
left_panel.pack(side='left', fill='both', expand=True, padx=10, pady=10)

left_header = ttk.Label(left_panel, text="Attendance Records", style='Header.TLabel')
left_header.pack(fill='x', ipady=8)

# Add a subframe for the treeview and scrollbar with some padding
tv_frame = ttk.Frame(left_panel, style='Card.TFrame')
tv_frame.pack(fill='both', expand=True, padx=15, pady=15)

# Configure the Treeview with better styling
tv = ttk.Treeview(tv_frame, height=15, columns=('name', 'date', 'time'), style='Treeview')
tv.pack(side='left', fill='both', expand=True)

tv.column('#0', width=80, anchor='center')
tv.column('name', width=150, anchor='center')
tv.column('date', width=100, anchor='center')
tv.column('time', width=100, anchor='center')

tv.heading('#0', text='ID')
tv.heading('name', text='NAME')
tv.heading('date', text='DATE')
tv.heading('time', text='TIME')

# Add scrollbar
scroll = ttk.Scrollbar(tv_frame, orient='vertical', command=tv.yview)
scroll.pack(side='right', fill='y')
tv.configure(yscrollcommand=scroll.set)

# Controls for left panel
control_frame_left = ttk.Frame(left_panel, style='Card.TFrame')
control_frame_left.pack(fill='x', padx=15, pady=15)

trackImg = ttk.Button(control_frame_left, text="Take Attendance", command=TrackImages, style='Success.TButton')
trackImg.pack(fill='x', pady=5)

quitWindow = ttk.Button(control_frame_left, text="Exit Application", command=window.destroy, style='Danger.TButton')
quitWindow.pack(fill='x', pady=5)

# Right panel for Registration
right_panel = ttk.Frame(content_frame, style='Card.TFrame')
right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)

right_header = ttk.Label(right_panel, text="New Registration", style='Header.TLabel')
right_header.pack(fill='x', ipady=8)

# Registration form
form_frame = ttk.Frame(right_panel, style='Card.TFrame')
form_frame.pack(fill='both', expand=True, padx=15, pady=15)

# ID field
id_frame = ttk.Frame(form_frame, style='Card.TFrame')
id_frame.pack(fill='x', pady=10)

id_label = ttk.Label(id_frame, text="Student ID:", style='Info.TLabel')
id_label.pack(anchor='w', pady=5)

id_entry_frame = ttk.Frame(id_frame, style='Card.TFrame')
id_entry_frame.pack(fill='x')

txt = ttk.Entry(id_entry_frame, font=('Roboto', 12), width=30)
txt.pack(side='left', fill='x', expand=True, ipady=5)

clearButton = ttk.Button(id_entry_frame, text="Clear", command=clear, style='Danger.TButton', width=10)
clearButton.pack(side='right', padx=5)

# Name field
name_frame = ttk.Frame(form_frame, style='Card.TFrame')
name_frame.pack(fill='x', pady=10)

name_label = ttk.Label(name_frame, text="Student Name:", style='Info.TLabel')
name_label.pack(anchor='w', pady=5)

name_entry_frame = ttk.Frame(name_frame, style='Card.TFrame')
name_entry_frame.pack(fill='x')

txt2 = ttk.Entry(name_entry_frame, font=('Roboto', 12), width=30)
txt2.pack(side='left', fill='x', expand=True, ipady=5)

clearButton2 = ttk.Button(name_entry_frame, text="Clear", command=clear2, style='Danger.TButton', width=10)
clearButton2.pack(side='right', padx=5)

# Instructions and status messages
message1 = ttk.Label(form_frame, text="1) Take Images → 2) Save Profile", style='Info.TLabel')
message1.pack(pady=15)

message = ttk.Label(form_frame, text="", style='Info.TLabel')
message.pack(pady=5)

# Registration buttons
buttons_frame = ttk.Frame(form_frame, style='Card.TFrame')
buttons_frame.pack(fill='x', pady=10)

takeImg = ttk.Button(buttons_frame, text="Take Images", command=TakeImages, style='Accent.TButton')
takeImg.pack(fill='x', pady=5)

trainImg = ttk.Button(buttons_frame, text="Save Profile", command=psw, style='Success.TButton')
trainImg.pack(fill='x', pady=5)

# Set up total registrations counter
res = 0
exists = os.path.isfile("StudentDetails/StudentDetails.csv")
if exists:
    with open("StudentDetails/StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res += 1
    res = (res // 2) - 1
else:
    res = 0
message.configure(text='Total Registrations: ' + str(res))

# Create menubar with modern styling
menubar = tk.Menu(window)
window.config(menu=menubar)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Change Password", command=change_pass)
help_menu.add_command(label="Contact Support", command=contact)
help_menu.add_separator()
help_menu.add_command(label="Exit", command=window.destroy)

window.mainloop()