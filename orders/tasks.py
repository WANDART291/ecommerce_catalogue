from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from .models import Order

@shared_task
def send_order_confirmation(order_id):
    """
    Simulates sending an order confirmation email immediately after checkout.
    """
    print(f"📧 Sending order confirmation email for Order #{order_id}...")
    
    # Simulate the 5-second delay of talking to an email server
    sleep(5)
    
    print(f"✅ Order confirmation email sent for Order #{order_id}!")
    return "Done"

@shared_task
def send_payment_success_email(order_id):
    """
    Sends an actual email (printed to console in dev) when Payment is verified.
    """
    try:
        # Get the order and the associated payment
        order = Order.objects.get(id=order_id)
        
        # Construct the email
        subject = f"Payment Successful: Order #{str(order.id)[:8]}"
        message = (
            f"Hi {order.user.username or 'Customer'},\n\n"
            f"We have successfully received your payment of {order.payment.amount} ETB.\n"
            f"Transaction Reference: {order.payment.transaction_id}\n\n"
            f"Your order is now being processed.\n\n"
            f"Thank you for shopping with us!"
        )
        
        # Send the email
        # Since we set EMAIL_BACKEND to 'console' in settings, this will print to your terminal.
        send_mail(
            subject, 
            message, 
            'noreply@ecommerce.com',  # From email
            [order.user.email],       # To email
            fail_silently=False
        )
        return f"Payment confirmation email sent for Order {order.id}"

    except Order.DoesNotExist:
        return f"Order {order_id} not found"
    except Exception as e:
        return f"Failed to send email: {str(e)}"