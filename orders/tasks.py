from celery import shared_task
from time import sleep

@shared_task
def send_order_confirmation(order_id):
    """
    Simulates sending an email.
    In real life, this would connect to Gmail/AWS SES.
    """
    print(f"📧 Sending confirmation email for Order #{order_id}...")
    
    # Simulate the 5-second delay of talking to an email server
    sleep(5)
    
    print(f"✅ Email sent for Order #{order_id}!")
    return "Done"