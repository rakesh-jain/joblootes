from rest_framework import serializers
from rest_framework import serializers

class EmailSender(serializers.Serializer):
    subject = serializers.CharField(max_length=300)
    body = serializers.CharField(required=False, allow_blank=True)
    emails = serializers.CharField()
    html_file = serializers.FileField(required=False, allow_null=True)
    attachments = serializers.ListField(
        child=serializers.FileField(), required=False, allow_empty=True
    )

    def validate_emails(self, value):
        emails = []
        if isinstance(value, str):
            emails = [e.strip() for e in value.split(",") if e.strip()]
        elif isinstance(value, list):
            for e in value:
                if isinstance(e, str):
                    emails.extend([x.strip() for x in e.split(",") if x.strip()])

        # Validate each email
        for e in emails:
            serializers.EmailField().run_validation(e)
        return emails
