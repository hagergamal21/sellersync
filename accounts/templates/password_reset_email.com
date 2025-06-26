Someone asked for password reset for email {{email}}. Follow the link below:
{{ protocol}}://{{ domain }}{% url 'password_reset_sent' uidb64=uid token=token %}