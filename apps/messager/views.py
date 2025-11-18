from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailSender
from .services.email_service import send_mail


class EmailAPIView(APIView):
    def post(self, request):
        # Combine data & files properly
        data = request.data.copy()

        # Add all files properly (handles multiple attachments)
        for key in request.FILES:
            if len(request.FILES.getlist(key)) > 1:
                data.setlist(key, request.FILES.getlist(key))
            else:
                data[key] = request.FILES[key]

        serializer = EmailSender(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subject = serializer.validated_data["subject"]
        body = serializer.validated_data.get("body", "")
        emails = serializer.validated_data["emails"]
        html_file = serializer.validated_data.get("html_file")
        attachments = serializer.validated_data.get("attachments", [])

        html_content = None
        if html_file and not body:
            html_content = html_file.read().decode("utf-8")

        send_mail(
            subject=subject,
            recipient_list=emails,
            body_content=body,
            html_content=html_content,
            attachments=attachments,
        )

        return Response(
            {"message": "Emails are being sent asynchronously."},
            status=status.HTTP_200_OK,
        )
