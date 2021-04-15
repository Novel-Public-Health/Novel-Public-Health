from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings


@receiver(valid_ipn_received)
def ipn_receiver(sender, **kwargs):
    ipn_obj = sender

    # check for subscription signup IPN
    if ipn_obj.txn_type == "subscr_signup":

        # get user id and activate the account
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        user.active = True
        user.save()

        subject = 'Sign Up Complete'

        message = 'Thanks for signing up!'

        email = EmailMessage(subject,
                             message,
                             settings.EMAIL_HOST_USER,
                             [user.email])

        email.send()

    # check for subscription payment IPN
    elif ipn_obj.txn_type == "subscr_payment":

        # get user id and extend the subscription
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        # user.extend()  # extend the subscription

        subject = 'Your Invoice for {} is available'.format(
            datetime.strftime(datetime.now(), "%b %Y"))

        message = 'Thanks for using our service. The balance was automatically ' \
                  'charged to your credit card.'

        email = EmailMessage(subject,
                             message,
                             settings.EMAIL_HOST_USER,
                             [user.email])

        email.send()

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        pass

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        profile.user_type = 1
        profile.save()