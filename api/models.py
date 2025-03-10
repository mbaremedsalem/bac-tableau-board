from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50, default="", blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)

    # Nouveau champ pour l'image
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Nouveau champ pour les posts (si vous voulez stocker une liste de posts, par exemple)
    post = models.TextField(blank=True, null=True)

    def __str__(self):
        return self. str(reset_passwopostrd_token)

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):

    user = instance

    if created:
        profile = Profile(user=user)
        profile.save() 

class DemChqDtl(models.Model):
    CHECKBK_NOOPER = models.CharField(max_length=255)
    CHECKBKNB = models.CharField(max_length=255)
    REFER1 = models.CharField(max_length=255)
    REFER2 = models.CharField(max_length=255)
    STATUS = models.CharField(max_length=255)
    STATUSDATE = models.DateField()
    ID = models.AutoField(primary_key=True)
    SYS_VERSION_NUMBER = models.IntegerField()
    SYS_CREATED_DATE = models.DateField()
    SYS_CREATED_BY = models.CharField(max_length=255)
    SYS_UPDATED_DATE = models.DateField()
    SYS_UPDATED_BY = models.CharField(max_length=255)
    STATE = models.CharField(max_length=255)
    VALIDE = models.CharField(max_length=255)
    CIRMAN = models.CharField(max_length=255)

    class Meta:
        db_table = 'DEMCHQDTL'             


# models.py
class Virest(models.Model):
    OPER = models.CharField(max_length=20,primary_key=True)
    comptec = models.CharField(max_length=20)
    NOMBE = models.CharField(max_length=255)
    DATOPER = models.DateField()
    DEV1 = models.CharField(max_length=3)
    MNTDEVC = models.DecimalField(max_digits=15, decimal_places=2)
    COMPTED = models.CharField(max_length=20)
    DORDRED = models.CharField(max_length=255)
    NOOPER = models.CharField(max_length=50)
    COURS12 = models.DecimalField(max_digits=10, decimal_places=6)
    devised = models.CharField(max_length=3)
    devisec = models.CharField(max_length=3)
    mntdevd = models.DecimalField(max_digits=15, decimal_places=2)
    mntdevc = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        db_table = 'VIREST'  # This tells Django that this model represents the AUB.VIREST table in Oracle DB

    def __str__(self):
        return f"{self.oper} - {self.beneficiaire}"

class Cpt(models.Model):
    COMPTE = models.CharField(max_length=20, primary_key=True)
    CLIENT = models.CharField(max_length=50)
    NOM = models.CharField(max_length=200)
    NCG  = models.CharField(max_length=40)
    TYP = models.CharField(max_length=30)
    DATOUV = models.CharField(max_length=50)
    DATFRM = models.CharField(max_length=60)
    CODFRM = models.CharField(max_length=100)
    EXPL = models.CharField(max_length=20)
    AGENCE = models.CharField(max_length=20)
    POSDEV = models.CharField(max_length=20000)
    DATVAL = models.CharField(max_length=60)


    class Meta:
        db_table = 'CPT'  # This tells Django that this model represents the AUB.CPT table in Oracle DB

    def __str__(self):
        return self.COMPTE

class Guichet(models.Model):
    datoper = models.CharField(max_length=50)
    COMPTED = models.CharField(max_length=20, primary_key=True)
    COMPTEC = models.CharField(max_length=20)
    devised = models.CharField(max_length=50)
    devisec = models.CharField(max_length=50)
    nomlib = models.CharField(max_length=200)
    mntnetd  = models.CharField(max_length=40)
    mntnetc = models.CharField(max_length=30)
    libav1 = models.CharField(max_length=50)
    devised = models.CharField(max_length=60)
    devisec = models.CharField(max_length=100)

    class Meta:
        db_table = 'GUICHET'  # This tells Django that this model represents the AUB.CPT table in Oracle DB

    def __str__(self):
        return self.COMPTE
        
