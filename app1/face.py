import threading
import cv2
from deepface import DeepFace
import time
import tkinter as tk

def display_alert():
    window = tk.Tk()
    window.title("Alert")
    txt="Welcome back"
    
    txt2=filename[39:len(filename)-4]
    txt3=txt+' '+txt2
    window.geometry("300x100")
    label = tk.Label(window, text=txt3, font=("Arial", 14))
    label.pack()
    window.after(3000, window.destroy)  
    window.mainloop()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0
filename = "C:\\Users\\Asus\\Desktop\\sample\\egov\\app1\\bright.jpg"
face_match = False
reference_img = cv2.imread(filename=filename)
def check_face(frame):
    global face_match
    try:
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except:
        face_match = False  

while True:
    ret, frame = cap.read()
    if ret:
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        if face_match:
            cv2.putText(frame, "MATCH!!!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "NO MATCH!!!", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("VIDEO", frame)

    key = cv2.waitKey(1)
    if key == ord("q") or face_match:
        break

if face_match:
    start_time = time.time() 
    display_alert()

    while True:
        elapsed_time = time.time() - start_time  
        if elapsed_time >= 3:
            cv2.destroyAllWindows() 
            break

cap.release()
