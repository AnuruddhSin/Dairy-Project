import random


# Generates Random OTP
def GenerateRandomOTP():
    otp = random.randint(1000,9999)
    return otp