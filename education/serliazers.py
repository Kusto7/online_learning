from rest_framework import serializers

from education.models import Course, Lesson, Payment, Subscription
from education.sercices import creates_payment_intent, retrieve_payment_intent
from education.validators import LinkValidator


class PaymentSerializer(serializers.ModelSerializer):
    payment_stripe = serializers.SerializerMethodField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.get('context').get('request')

    def get_payment_stripe(self, instance):
        if self.request.stream.method == 'POST':
            stripe_id = creates_payment_intent(int(instance.amount))
            obj_payments = Payment.objects.get(id=instance.id)
            obj_payments.stripe_id = stripe_id
            obj_payments.save()
            return retrieve_payment_intent(stripe_id)
        if self.request.stream.method == 'GET':
            if not instance.stripe_id:
                return None
            return retrieve_payment_intent(instance.stripe_id)

    class Meta:
        model = Payment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    validators = [LinkValidator(field='link')]

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    validators = [LinkValidator(field='link')]
    subscription = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = kwargs.get('context').get('request')

    @staticmethod
    def get_lesson_count(instanse):
        return instanse.lesson.all().count()

    def get_subscription(self, instance):
        user = self.request.user
        sub_all = instance.subscription.all()
        for sub in sub_all:
            if sub.subscriber == user:
                return True
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
