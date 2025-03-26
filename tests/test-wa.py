import pywhatkit as pwk

try:
    pwk.sendwhatmsg_instantly("+492823904832948", "Hi, how are you?")
    print("Message Sent!")
except Exception as e:
    print(f"Error in sending the message: {e}")
