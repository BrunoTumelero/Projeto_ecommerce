from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

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
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateField(_("date joined"), auto_now_add=True)
    is_company = models.BooleanField(default=False)
    is_consumer = models.BooleanField(default=False)
    is_superuser = models.BooleanField(_("superuser"), default=False)
    is_staff = models.BooleanField(_("staff"), default=False)

    session_token = models.CharField(max_length=64, blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=64)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

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
                                primary_key=True,
                                related_name='consumer_name')

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

class Company(AbstractBaseModel):

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
    product_description = models.CharField(max_length=300)
    product_category = models.ForeignKey('register.ProductCategory', on_delete=models.CASCADE, related_name='category_product')
    product_price = models.CharField(max_length=10)
    is_avalable = models.BooleanField(default=False)

    def to_product_json(self):
        return {
            'id': self.pk,
            'company': self.company.pk,
            'product': self.product_name,
            'price': self.product_price,
            'is_avaliable': self.is_avalable
        }

class ProductCategory(AbstractBaseModel):
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    #sub_category = models.ForeignKey('register.SubCategory', on_delete=models.CASCADE, blank=True, null=True, related_name='ptoductcategory_subcategory')

    def to_json(self):
        return {
            'id': self.pk,
            'name': self.category,
            'description': self.description
        }

class SubCategory(AbstractBaseModel):
    sub_category = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    category = models.ForeignKey('register.ProductCategory', on_delete=models.CASCADE, related_name='subcategory_productcategory')

class Log(AbstractBaseModel):
    user = models.ForeignKey('register.User', on_delete=models.CASCADE)
    url = models.CharField(max_length=250, blank=True)
    authorized = models.BooleanField(default=False)

class Permission(AbstractBaseModel):
    permission_name = models.CharField(max_length=80)
    description = models.CharField(max_length=80)

class UserPermission(AbstractBaseModel):
    user = models.ForeignKey('register.User', on_delete=models.PROTECT, related_name='permissions')
    permission = models.ForeignKey('register.Permission', on_delete=models.PROTECT, related_name='user_permissions')

class CompanyPermission(AbstractBaseModel):
    permicted = models.CharField(max_length=80)
    description = models.CharField(max_length=80)

class UserCompanyPermission(AbstractBaseModel):
    LEVEL_ADM = 'administrator'
    LEVEL_CLERK = 'clerk'

    LEVEL_CHOICES = (
        (LEVEL_ADM, 'Administrativo'),
        (LEVEL_CLERK, 'Atendimento')
    )

    user = models.ForeignKey('register.User',
                            on_delete=models.PROTECT)
    company = models.ForeignKey('register.Company',
                                on_delete=models.PROTECT)
    permission = models.ForeignKey('register.CompanyPermission',
                                    on_delete=models.PROTECT)
    level = models.CharField(max_length=6,
                            choices=LEVEL_CHOICES,
                            default=LEVEL_CLERK)

class purchase(AbstractBaseModel):
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='purchase_company')
    consumer = models.ForeignKey('register.consumer', on_delete=models.CASCADE, related_name='purchase_consumer')
    total = models.FloatField()
    