from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_otp_email(email, otp):
    """
    Send OTP email
    """

    message = f"""
Hello,

Your One-Time Password (OTP) for verification is:

{otp}

This code will expire in 5 minutes.

If you did not request this code, ignore this email.
Do not share this OTP with anyone.

Thanks,
ParkShare Team
"""

    send_mail(
        subject="Your OTP Verification Code",
        message=message,
        from_email="abdullah.4110r.work@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )

    print("Email sent successfully")
