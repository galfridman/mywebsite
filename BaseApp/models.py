from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from address import models as adress_model
import os
from conversation.models import Conversation as Conversation


def get_image_path(instance, filename):
    return os.path.join('img/', instance.__class__.__name__, str(instance.id), filename)


class AppUser(models.Model):
    birthdate = models.DateTimeField(null=True, blank=True)
    address = adress_model.AddressField(null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    gender = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u"%s %s" % (self.user.first_name, self.user.last_name)

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class Business(models.Model):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = adress_model.AddressField(null=True, blank=True)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    managers = models.ManyToManyField(AppUser)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return "%s" % self.name


class Phone(models.Model):
    business = models.ForeignKey(Business, related_name='phones')
    description = models.TextField(max_length='20')
    number = models.CharField(max_length=10, unique=True, validators=[RegexValidator(regex='^\d{10}$', message='Length has to be 10', code='Invalid number')])


class Catalog(models.Model):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    changed_at = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    business = models.ForeignKey(Business, related_name='business_catalogs')

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return "%s" % self.name


class Item(models.Model):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    catalog = models.ForeignKey(Catalog, related_name='catalog_items')
    created_at = models.DateTimeField(null=True, blank=True)
    changed_at = models.DateTimeField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    purchased_times = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return "%s" % self.name


class Service(models.Model):
    name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    catalog = models.ForeignKey(Catalog, 'catalog_services')
    created_at = models.DateTimeField(null=True, blank=True)
    changed_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    purchased_times = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return u"%s" % self.name

    def __str__(self):
        return "%s" % self.name


class Order(models.Model):
    user = models.ForeignKey(AppUser, related_name='user_orders')
    business = models.ForeignKey(Business, related_name='business_orders')
    type = models.TextField(null=True, blank=True)  # takeaway / delivery
    picking_time = models.DateField(null=True, blank=True)
    address = adress_model.AddressField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return u"Order %s" % self.id

    def __str__(self):
        return "Order %s" % self.id


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, related_name='item_orders')
    item = models.ForeignKey(Item, related_name='order_items')
    quantity = models.IntegerField(null=True, blank=True)


# business time

WEEKDAYS = [
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
]


class OpeningHours(models.Model):
    business = models.ForeignKey(Business, related_name='opening_hours')
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField(null=True, blank=True)
    to_hour = models.TimeField(null=True, blank=True)

    class Meta:
        ordering = ('weekday', 'from_hour')
        unique_together = ('weekday', 'from_hour', 'to_hour')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(null=True, blank=True),
                                 self.from_hour, self.to_hour)

    def __str__(self):
        return '%s: %s - %s' % (self.get_weekday_display(null=True, blank=True),
                                 self.from_hour, self.to_hour)


# end business time


class AppConversation(models.Model):
    appuser = models.ForeignKey(AppUser)
    business = models.ForeignKey(Business)
    conversation = models.OneToOneField(
        Conversation,
        verbose_name='Conversation',
        related_name='appconversation',
        null=True,
        blank=True
    )


class Appointment(models.Model):
    service = models.ForeignKey(Service, related_name='service_appointments')
    starting_time = models.TimeField(null=True, blank=True)
    user = models.ForeignKey(AppUser, related_name='user_appointments')
    conversation = models.ForeignKey(Conversation, related_name='conversation_appointments')


class Dispute(models.Model):
    service = models.ForeignKey(Service, related_name='service_disputes')
    type = models.TextField(null=True, blank=True)  # item / service / appointment / order
    item = models.ForeignKey(Item, related_name='item_disputes')
    Appointment = models.ForeignKey(Appointment)
    order = models.ForeignKey(Order, related_name='order_disputes')
    topic = models.TextField(null=True, blank=True)
    conversation = models.ForeignKey(Conversation, related_name='conversation_disputes')


class BasePost(models.Model):
    text = models.TextField(null=True, blank=True)
    business = models.ForeignKey(Business, related_name='business_base_posts')
    is_important = models.BooleanField(default=False)
    audience = models.TextField(null=True, blank=True)  # all / members
    created_at = models.DateTimeField(null=True, blank=True)
    changed_at = models.DateTimeField(null=True, blank=True)


class Discount(models.Model):
    amount_type = models.TextField(null=True, blank=True)  # percents / price
    amount = models.FloatField(null=True, blank=True)
    condition_type = models.TextField(null=True, blank=True)  # percents / price
    item = models.ForeignKey(Item, related_name='item_discounts')
    service = models.ForeignKey(Service, related_name='service_discounts')
    order = models.ForeignKey(Order, related_name='order_discounts')
    reward_type = models.TextField(null=True, blank=True)
    item_reward = models.ForeignKey(Item, related_name='item_reward_discounts')
    discount_reward = models.FloatField(null=True, blank=True)


class BaseBenefit(models.Model):
    title = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    business = models.ForeignKey(Business, related_name='business_base_benefits')
    starting_date = models.DateTimeField(null=True, blank=True)
    ending_date = models.DateTimeField(null=True, blank=True)


class TicketBenefit(models.Model):
    benefit = models.ForeignKey(BaseBenefit, related_name='ticket_base_benefits')
    amount = models.IntegerField(null=True, blank=True)  # required punchings


class FriendBenefit(models.Model):
    benefit = models.ForeignKey(BaseBenefit, related_name='friend_base_benefits')
    amount = models.IntegerField(null=True, blank=True)  # required friends


class DiscountBenefit(models.Model):
    benefit = models.ForeignKey(BaseBenefit, related_name='discount_base_benefits')


class Comment(models.Model):
    user = models.ForeignKey(AppUser, related_name='user_comments')
    text = models.TextField(null=True, blank=True)
    post = models.ForeignKey(BasePost, related_name='post_comments')
    created_at = models.DateTimeField(blank=True, auto_now_add=True)


class PostLike(models.Model):
    class Meta:
        unique_together = (('user', 'post'),)
    user = models.ForeignKey(AppUser, related_name='user_post_likes')
    post = models.ForeignKey(BasePost, related_name='base_post_likes')


class BusinessLike(models.Model):
    class Meta:
        unique_together = (('user', 'business'),)

    user = models.ForeignKey(AppUser, related_name='user_business_likes')
    business = models.ForeignKey(Business, related_name='business_likes')


class UserFriendBenefit(models.Model):
    user = models.ForeignKey(AppUser, related_name='user_friend_benefits')
    friend = models.ForeignKey(AppUser)
    benefit = models.ForeignKey(FriendBenefit, related_name='friend_base_benefits')


class UserTicketBenefit(models.Model):
    user = models.ForeignKey(AppUser, related_name='user_ticket_benefits')
    counter = models.IntegerField(null=True, blank=True)
    benefit = models.ForeignKey(TicketBenefit, related_name='ticket_base_benefits')
