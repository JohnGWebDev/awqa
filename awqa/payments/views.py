import stripe
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, TemplateView
from django.conf import settings
from django.shortcuts import render
from django.urls import path
from . models import Product
secret_key = settings.STRIPE_SECRET_KEY

# Set your secret key: remember to switch to your live secret key in production!
stripe.api_key = secret_key

User = settings.AUTH_USER_MODEL

YOUR_DOMAIN = 'http://localhost:8000'

class CheckoutView(DetailView):
    model = Product
    template_name = 'payments/checkout.html'

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(pk=kwargs.get('pk'))
            price_id = product.price.price_id
            session = stripe.checkout.Session.create(
                ui_mode='embedded',
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                return_url=f"{YOUR_DOMAIN}/payments/session-status/?session_id={{CHECKOUT_SESSION_ID}}",
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'clientSecret': session.client_secret})

class SessionStatusView(View):
    template_name = "payments/return_page.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if not session_id:
            return JsonResponse({'error': 'Missing session_id'}, status=400)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)

        customer_email = session.get('customer_details', {}).get('email', 'N/A')
        payment_status = session.get('payment_status', 'unknown')
        amount_total = session.get('amount_total', 0) / 100  # Amount is in cents
        currency = session.get('currency', 'usd').upper()

        # Render the return page with session details
        return render(request, self.template_name, {
            'customer_email': customer_email,
            'payment_status': payment_status,
            'amount_total': amount_total,
            'currency': currency,
        })
    

class StripeWebhookView(View):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = 'whsec_...'  # Replace with your webhook secret

        try:
            # Verify the event by constructing it
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']  # Get the session object
            customer_email = session['customer_details']['email']  # Assuming you use email to identify users

            # Increment the user's max_aquariums
            try:
                user = User.objects.get(email=customer_email)
                user.max_aquariums += 1  # Increment the max_aquariums field
                user.save()
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        return JsonResponse({'status': 'success'})