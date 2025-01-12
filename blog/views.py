from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import BlogPost, Subscriber
from .serializers import BlogPostSerializers
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BlogPostListView(ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializers

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostDetailsView(RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializers
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)



def perform_create(self, serializer):
    post = serializer.save(author=self.request.user)
    subscribers = Subscriber.objects.all().values_list('email', flat=True)

    try:
        send_mail(
            'Test Subject',
            'This is a test email.',
            settings.EMAIL_HOST_USER,
            list(subscribers),
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")
        return Response({"error": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubscribeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            return Response({'error': 'Email already subscribed'}, status=status.HTTP_400_BAD_REQUEST)

        Subscriber.objects.create(email=email)

        try:
            send_mail(
                'New Subscriber',
                f'New subscriber added: {email}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            return Response({"error": "Failed to send email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'message': 'Subscribed successfully'}, status=status.HTTP_201_CREATED)
