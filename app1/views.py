from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from django.http import HttpResponseBadRequest

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.http import HttpResponse
from django.shortcuts import render
import cv2
from deepface import DeepFace
import threading
import time
import tkinter as tk

def display_alert():
    window = tk.Tk()
    window.title("Alert")
    txt = "Welcome back"
    filename = "C:\\Users\\Asus\\Desktop\\Python\\ravanth.jpg"
    txt2 = filename[29:len(filename)-4]
    txt3 = txt + ' ' + txt2
    window.geometry("300x100")
    label = tk.Label(window, text=txt3, font=("Arial", 14))
    label.pack()
    window.after(3000, window.destroy)  
    window.mainloop()

def webcam_view(request):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    counter = 0
    filename = "C:\\Users\\Asus\\Desktop\\sample\\egov\\app1\\ravanth.jpg"
    face_match = False
    reference_img = cv2.imread(filename=filename)

    def check_face(frame):
        nonlocal face_match
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
    cv2.destroyAllWindows() 

    return render(request,'razor.html')


# Authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def main(request):
    return render(request,'home.html')


def homepage(request):
    currency = 'INR'
    amount = 1000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # Order ID of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # We need to pass these details to frontend.
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url
    }

    return render(request, 'razor.html', context=context)


@csrf_exempt
def paymenthandler(request):

    # Only accept POST request.
    if request.method == "POST":
        try:

            # Get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:

                    # Capture the payment
                    razorpay_client.payment.capture(payment_id, amount)

                    # Render success page on successful capture of payment
                    return render(request, 'home.html')
                except:

                    # If there is an error while capturing payment.
                    return render(request, 'home.html')
            else:

                # If signature verification fails.
                return render(request, 'home.html')
        except:

            # If we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # If other than POST request is made.
        return HttpResponseBadRequest()


def home(request):
    return render(request, 'login2.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'ravanth' and password == 'ravanth':   
            return render(request, 'video.html')
        else:
            error_message = 'Incorrect username or password. Please try again.'
            return render(request, 'login2.html', {'error_message': error_message})
    else:
        return render(request, 'login2.html')



def home1(request):
    if request.method == 'POST':
        otp = request.POST.get('OTP')
        if otp == '5599':
            return render(request, 'home.html')
        else:
            error_message = 'Incorrect username or password. Please try again.'
            return render(request, 'login2.html', {'error_message': error_message})


def register(request):

    if request.method == 'POST':

        username = request.POST.get('phone_number')
        print(username)
        url = "https://www.fast2sms.com/dev/bulkV2"

        querystring = {"authorization": "KNwzJuq1NCvQdCJ0DIoHAwDzJaY5htlvFFFcZZrXiIQb81n7cLsPrjnvM17T",
                       "variables_values": "5599", "route": "otp", "numbers": username}

        headers = {
            'cache-control': "no-cache"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        print(response.text)
        return render(request, 'register.html')
    elif request.method == 'GET':

        return render(request, 'register.html')


def about(request):
    return render(request, 'about.html')


def contacts(request):
    return render(request, 'contacts.html')


def documents(request):
    return render(request, 'documents.html')


def accounts(request):
    return render(request, 'accounts.html')


def payments(request):
    return render(request, 'payments.html')


def logout(request):
    return render(request, 'login2.html')

def notify(request):
    return render(request,'notifications.html')

def setting(request):
    return render(request,'settings.html')

