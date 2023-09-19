from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from education.permissions import IsModerator, IsCustomPermission, IsOwner

from education.models import Course, Lesson, Payment, Subscription
from education.serliazers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from education.tasks import send_course_update


class PaymentViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели платежа
        education.models.Payment """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson')
    ordering_fields = ('date', 'method',)
    permission_classes = [IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели курса
        education.models.Course """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsCustomPermission]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_course_update.delay(new_lesson.course.id)


class LessonCreateAPIView(generics.CreateAPIView):
    """ Generic для создания модели урока
        education.models.Lesson """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """ Generic для отображения модели уроков
        education.models.Lesson """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Generic для детального просмотра модели урока
        education.models.Lesson """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Generic для обновления модели урока
        education.models.Lesson """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_update(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()
        if new_lesson:
            send_course_update.delay(new_lesson.course.id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Generic для удаления модели урока
        education.models.Lesson """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class SubscriptionViewSet(ModelViewSet):
    """ ViwSet для модели подписки
        education.models.Subscription """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
