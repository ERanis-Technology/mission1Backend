from django.core.mail import send_mail

def send_confirmation_email(email, user_type):
    send_mail(
        subject='Confirmation d\'inscription',
        message='Votre compte YNNOVAS a été créé avec succès.', #Veuillez activer votre compte via le lien fourni.,
        from_email='nana.heil@facsciences-uy1.cm',  # Replace with your email
        recipient_list=[email],
        fail_silently=False,
    )

def send_rejection_email(email, user_type):
    send_mail(
        subject='Rejet de votre inscription',
        message='Votre dossier n\'a pas été retenu. Merci de vérifier vos informations ou de contacter l\'administrateur.',
        from_email='nana.heil@facsciences-uy1.cm',
        recipient_list=[email],
        fail_silently=False,
    )