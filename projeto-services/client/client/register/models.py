from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

from .managers import UserManager


class AbstractBaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    company = models.ForeignKey('register.Company',
                                related_name='users',
                                on_delete=models.SET_NULL,
                                null=True)
    email = models.EmailField(name="email", unique=True)
    date_joined = models.DateField(name="date joined", auto_now_add=True)
    is_company = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(name="superuser", default=False)
    is_staff = models.BooleanField(name= "staff", default=False)

    session_token = models.CharField(max_length=64)
    activation_key = models.CharField(max_length=64)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"

class UserSession(AbstractBaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=64)

class Consumers(AbstractBaseModel):

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Masculino"),
        (GENDER_FEMALE, "Feminino"),
        (GENDER_OTHER, "Outro"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True)

    full_name = models.CharField(max_length=250, null=False, blank=False)
    cpf = models.CharField(max_length=15)
    alias = models.CharField(max_length=200, blank=True)
    whatsapp = models.CharField(max_length=15)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6,
                                choices=GENDER_CHOICES,
                                default=GENDER_OTHER)

    cep = models.CharField(max_length=9, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    street_number = models.CharField(max_length=10, null=True, blank=True)
    complement = models.CharField(max_length=300, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    card = models.ForeignKey('register.ConsumersCards', on_delete=models.CASCADE, blank=True, null=True, related_name='card_consumer')


class ConsumersCards(AbstractBaseModel):

    MASTER_CARD = "mastercard"
    VISA_CARD = "visa"
    HIPER_CARD = "hipercard"
    BANRI_CARD = "banricompras"
    ELO_CARD = "elo"
    ALELO_CARD = "alelo"
    AMERICAN_CARD = "america_express"

    CARDS_CHOICES = (
        (MASTER_CARD, "Mastercard"),
        (VISA_CARD, "Visa"),
        (HIPER_CARD, "Hipercarde"),
        (BANRI_CARD, "Banricompras"),
        (ELO_CARD, "Elo"),
        (ALELO_CARD, "Alelo"),
        (AMERICAN_CARD, "American express")
    )

    consumer_name = models.CharField(max_length=200, null=False, blank=False)
    card_number = models.CharField(max_length=50, null=False, blank=False)
    cod_card = models.CharField(max_length=5, null=False, blank=False)
    expiration_date = models.DateField(null=False, blank=False)
    flag_card = models.CharField(max_length=20,
                                choices=CARDS_CHOICES,
                                null=False, blank=False)

class Company(AbstractBaseUser):

    PLAN_BASIC = "plan_basic"
    PLAN_PREMIUM = "plan_premium"

    PLAN_CHOICES = (
        (PLAN_BASIC, 'Plano Basico'),
        (PLAN_PREMIUM, 'Plano Completo')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='company_name')
    
    name_owner = models.CharField(max_length=150)
    email_owner = models.CharField(max_length=100, blank=True, null=True)
    phone_owner = models.CharField(max_length=12)
    cep = models.CharField(max_length=10)
    state = models.ForeignKey('register.State', on_delete=models.CASCADE, related_name='state_company')
    city = models.ForeignKey('register.City', on_delete=models.CASCADE, related_name='city_company')
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=200, blank=True, null=True)
    cpf_owner = models.CharField(max_length=15)

    cnpj = models.CharField(max_length=20)
    business_name = models.CharField(max_length=200)
    public_name = models.CharField(max_length=200)
    business_phone = models.CharField(max_length=12)
    business_specialty = models.ForeignKey('register.CompanySpecialty', on_delete=models.CASCADE, related_name='type_company', null=True)
    plan = models.CharField(max_length=10,
                            choices=PLAN_CHOICES)

class City(AbstractBaseModel):
    name = models.CharField(max_length=100)
    state = models.ForeignKey('register.State', on_delete=models.CASCADE, related_name='state_city')

class State(AbstractBaseModel):
    uf = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

class CompanySpecialty(AbstractBaseModel):
    specialty = models.CharField(max_length=50)
    sub_specialty = models.CharField(max_length=50, blank=True, null=True)

class BusinessTransfer(AbstractBaseModel):
    business = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='business_company')
    savings_account = models.BooleanField()
    company_bank = models.CharField(max_length=100)
    agency_bank = models.CharField(max_length=8)
    bank_account = models.CharField(max_length=8)
    account_digit = models.CharField(max_length=2)

class Products(AbstractBaseModel):
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='product_company')
    product_name = models.CharField(max_length=200)
    product_categori = models.CharField(max_length=100, null=True, blank=True)
    product_price = models.CharField(max_length=10)
    is_avalable = models.BooleanField()
