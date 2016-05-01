from django.contrib import admin
import BaseApp.models as BaseAppModels
# Register your models here.

admin.site.register(BaseAppModels.AppUser)
admin.site.register(BaseAppModels.Business)
admin.site.register(BaseAppModels.Catalog)
admin.site.register(BaseAppModels.Item)
admin.site.register(BaseAppModels.Service)
admin.site.register(BaseAppModels.Order)
admin.site.register(BaseAppModels.ItemOrder)
admin.site.register(BaseAppModels.OpeningHours)
admin.site.register(BaseAppModels.AppConversation)
admin.site.register(BaseAppModels.Appointment)
admin.site.register(BaseAppModels.Dispute)
admin.site.register(BaseAppModels.BasePost)
admin.site.register(BaseAppModels.Discount)
admin.site.register(BaseAppModels.BaseBenefit)
admin.site.register(BaseAppModels.TicketBenefit)
admin.site.register(BaseAppModels.FriendBenefit)
admin.site.register(BaseAppModels.DiscountBenefit)
admin.site.register(BaseAppModels.Comment)
admin.site.register(BaseAppModels.PostLike)
admin.site.register(BaseAppModels.BusinessLike)
admin.site.register(BaseAppModels.UserFriendBenefit)
admin.site.register(BaseAppModels.UserTicketBenefit)
admin.site.register(BaseAppModels.Phone)

