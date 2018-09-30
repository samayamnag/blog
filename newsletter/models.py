from django.db import models
from django.conf import settings
from django.utils.timezone import now
from .utils import make_activation_code
# Create your models here.

User = settings.AUTH_USER_MODEL


class Newsletter(models.Model):
    title = models.CharField(
        max_length=200, verbose_name='Newsletter title'
    )
    slug = models.SlugField(
        db_index=True, unique=True
    )
    email = models.EmailField(
        verbose_name='E-mail',
        help_text='Sender e-mail'
    )
    sender = models.CharField(
        max_length=100, verbose_name='Sender', help_text='Sender name'
    )
    visible = models.BooleanField(
        default=True, verbose_name='Visible', db_index=True
    )
    send_html = models.BooleanField(
        default=True, verbose_name='Send html',
        help_text='Whether or not to send HTML versions of e-mails.'
    )

    class Meta:
        verbose_name = 'Newsletter'
        verbose_name_plural = 'Newsletters'

    def __str__(self):
        return self.title

    def get_sender(self):
        return get_address(self.name, self.email)

    def get_subscriptions(self):
        return Subscription.objects.fiter(newsletter=self, subscribed=True)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    newsletter = models.ForeignKey(
        Newsletter, verbose_name='Newsletter', on_delete=models.CASCADE
    )
    create_date = models.DateTimeField(editable=False, default=now)
    activation_code = models.CharField(
        max_length=40, default=make_activation_code
    )
    subscribed = models.BooleanField(default=False, db_index=True)
    subscribe_date = models.DateTimeField(null=True, blank=True)

    # This should be a pseudo-field, I reckon.
    unsubscribed = models.BooleanField(default=False, db_index=True)
    unsubscribe_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'subscription'
        verbose_name_plural = 'subscriptions'
        unique_together = ('user', 'email', 'newsletter')

    def __str__(self):
        if self.full_name:
            return f'{self.full_name} <{self.email}> to {self.newsletter}'
        return f'{self.email} to {self.newsletter}'

    def _subscribe(self):
        """
        Internal helper method for managing subscription state
        during subscription.
        """
        self.subscribed = True
        self.subscribe_date = now()
        self.unsubscribed = False

    def _unsubscribe(self):
        """
        Internal helper method for managing subscription state
        during unsubscription.
        """
        self.unsubscribe_date = now()
        self.unsubscribed = True
        self.subscribed = False

    def update(self, action):
        """
        Update subscription according to requested action:
        subscribe/unsubscribe/update/, then save the changes.
        """

        assert action in ('subscribe', 'unsubscribe', 'update')

        if action == 'subscribe' or action == 'update':
            self.subscribed = True
        else:
            self.unsubscribed = True

        # This triggers the subscribe() and/or unsubscribe() methods, taking
        # care of stuff like maintaining the (un)subscribe date.
        self.save()

    def save(self, *args, **kwargs):
        # This is a lame way to find out if we have changed but using Django
        # API internals is bad practice. This is necessary to discriminate
        # from a state where we have never been subscribed but is mostly for
        # backward compatibility. It might be very useful to make this just
        # one attribute 'subscribe' later. In this case unsubscribed can be
        # replaced by a method property.

        if self.pk:
            subscription = Subscription.objects.get(pk=self.pk)
            old_subscribed = subscription.subscribed
            old_unsubscribed = subscription.unsubscribed

            # If we are subscribed now and we used not to be so, subscribe.
            # If we user to be unsubscribed but are not so anymore, subscribe.
            if ((self.subscribed and not old_subscribed) or
               (old_unsubscribed and not self.unsubscribed)):
                self._subscribe()

                assert not self.unsubscribed
                assert self.subscribed
            # If we are unsubcribed now and we used not to be so, unsubscribe.
            # If we used to be subscribed but are not subscribed anymore,
            # unsubscribe.
            elif ((self.unsubscribed and not old_unsubscribed) or
                  (old_subscribed and not self.subscribed)):
                self._unsubscribe()

                assert not self.subscribed
                assert self.unsubscribed
        else:
            if self.subscribed:
                self._subscribe()
            elif self.unsubscribed:
                self._unsubscribe()
        super(Subscription, self).save(*args, **kwargs)


def get_address(name, email):
    if name:
        return f'{name} <{email}>'
    return f'{email}'
