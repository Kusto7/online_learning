from django.contrib import admin


from education.models import Course, Lesson, Payment, Subscription

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Subscription)
admin.site.register(Payment)
