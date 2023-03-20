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

    is_activated = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=64)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

class UserSession(AbstractBaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_user')
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

    full_name = models.CharField(max_length=250)
    picture_url = models.CharField(max_length=200, null=True, blank=True)
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

    def to_json(self):
        return {
            '_id': self.pk,
            'name': self.full_name,
            'image': self.picture_url,
            'cpf': self.cpf,
            'alias': self.alias,
            'phone': self.whatsapp,
            'birthday': self.birthday,
            'gender': self.gender,
            'cep': self.cep,
            'street': self.street,
            'street_number': self.street_number,
            'complement': self.complement,
            'neighborhood': self.neighborhood,
            'city': self.city,
            'card': self.card
        }


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

    def to_json(self):
        return {
            'name': self.consumer_name,
            'card_number': self.card_number,
            'cod': self.cod_card,
            'expiration_date': self.expiration_date,
            'flag': self.flag_card
        }

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
    
    email_company = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    state = models.ForeignKey('register.State', on_delete=models.CASCADE, related_name='state_company')
    city = models.ForeignKey('register.City', on_delete=models.CASCADE, related_name='city_company')
    neighborhood = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    complement = models.CharField(max_length=200, blank=True, null=True)
    cpf_owner = models.CharField(max_length=15, blank=True, null=True)

    cnpj = models.CharField(max_length=20)
    business_name = models.CharField(max_length=200)
    public_name = models.CharField(max_length=200)
    picture_url = models.CharField(max_length=200, null=True, blank=True)
    business_phone = models.CharField(max_length=12)
    business_specialty = models.ForeignKey('register.CompanySpecialty', on_delete=models.CASCADE, related_name='type_company', null=True)
    plan = models.CharField(max_length=10,
                            choices=PLAN_CHOICES)

    def to_json(self):
        return {
            'company_id': self.pk,
            'user_id': self.user,
            'email': self.email_company,
            'cep': self.cep,
            'state': self.state,
            'city': self.city,
            'neighborhood': self.neighborhood,
            'street': self.street,
            'number': self.number,
            'complement': self.complement,
            'cpf_owner': self.cpf_owner,
            'cnpj': self.cnpj,
            'company_name': self.business_name,
            'name': self.public_name,
            'image': self.picture_url,
            'company_phone': self.business_phone,
            'company_category': self.business_specialty,
            'plan': self.plan
        }

class City(AbstractBaseModel):
    name = models.CharField(max_length=100)
    state = models.ForeignKey('register.State', on_delete=models.CASCADE, related_name='state_city')

    def to_json(self):
        return {
            'city': self.name,
            'state': self.state_city.name,
            'uf': self.state_city.name
        }

class State(AbstractBaseModel):
    uf = models.CharField(max_length=2)
    name = models.CharField(max_length=100)

class CompanySpecialty(AbstractBaseModel):
    specialty = models.CharField(max_length=50)
    sub_specialty = models.CharField(max_length=50, blank=True, null=True)

class BusinessTransfer(AbstractBaseModel):
    business = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='payment_company')
    savings_account = models.BooleanField()
    pix_key = models.CharField(max_length=200)
    company_bank = models.CharField(max_length=100)
    agency_bank = models.CharField(max_length=8)
    bank_account = models.CharField(max_length=8)
    account_digit = models.CharField(max_length=2)

class Products(AbstractBaseModel):
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='product_company')
    product_name = models.CharField(max_length=200)
    product_description = models.CharField(max_length=300)
    product_category = models.ForeignKey('register.ProductCategory', on_delete=models.CASCADE, related_name='category_product')
    product_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_avalable = models.BooleanField(default=False)

    def to_product_json(self):
        return {
            'id': self.pk,
            'company': self.company.pk,
            'product': self.product_name,
            'description': self.product_description,
            'category': self.product_category.pk,
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

class Sales(AbstractBaseModel):
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='company_sales')
    product = models.ForeignKey('register.Products', on_delete=models.PROTECT, related_name='product_sale')
class Log(AbstractBaseModel):
    user = models.ForeignKey('register.User', on_delete=models.CASCADE)
    url = models.CharField(max_length=250, blank=True)
    authorized = models.BooleanField(default=False)

class Permission(AbstractBaseModel):
    permission_name = models.CharField(max_length=80)
    description = models.CharField(max_length=80)

class CompanyPermission(AbstractBaseModel):
    MASTER = "Master"
    REPORTS = "reports"
    PAYMENTS = "payments"
    DELIVERIES = "deliveries"
    BASIC = "basic"
    
    PERMISSIONS_CHOICES = (
        (MASTER, 'Completo'),
        (REPORTS, 'Relatorios'),
        (PAYMENTS, 'Pagamentos'),
        (DELIVERIES, 'Entregas'),
        (BASIC, 'Basico')
    )
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='company_permissions')
    permicted = models.ForeignKey('register.Permission', on_delete=models.PROTECT, related_name='permissions_company')
    description = models.CharField(max_length=80)
    level_permissions = models.CharField(max_length=6, choices=PERMISSIONS_CHOICES)

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

class Purchase(AbstractBaseModel):
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE, related_name='purchase_company')
    consumer = models.ForeignKey('register.Consumers', on_delete=models.CASCADE, related_name='purchase_consumers')
    total = models.CharField(max_length=8)

class Shopping_Cart(AbstractBaseModel):
    @property
    def total(self):
        if self.selected:
            new_amount = self.amount * self.product.product_price
            return new_amount
        else:
            return 0

    @property
    def remove_item(self):
        amount_item = self.amount - 1
        return amount_item

    consumer = models.ForeignKey('register.Consumers', null=True, on_delete=models.CASCADE, related_name='shopping_consumers')
    product = models.ForeignKey('register.Products', null=True, on_delete=models.SET_NULL, related_name='shopping_products')
    amount = models.IntegerField()
    selected = models.BooleanField()

    def to_json(self):
        return {
            'consumer': self.shopping_consumers.full_name,
            'product': self.product,
            'amount': self.amount,
            'selected': self.selected
        }

class Whishes(AbstractBaseModel):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGTH = 'higth'

    PRIORITY_CHOICES = (
        (LOW, 'Baixa'),
        (MEDIUM, 'Média'),
        (HIGTH, 'Alta'),
    )

    name_whishes_list = models.CharField(max_length=50)
    consumer = models.ForeignKey('register.Consumers', null=True, on_delete=models.SET_NULL, related_name='whishes_consumers')
    product = models.ForeignKey('register.Products', null=True, on_delete=models.SET_NULL, related_name='whishes_products')
    annotation = models.CharField(max_length=200)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default=MEDIUM)
    amount = models.CharField(max_length=4)

    def to_json(self):
        return {
            'name_list': self.name_whishes_list,
            'conumer': self.consumer,
            'product': self.product,
            'annotation': self.annotation,
            'priority': self.priority,
            'amount': self.amount
        }
    
class ProductsRating(AbstractBaseModel):
    VERY_LOW = '1'
    LOW = '2'
    NEUTRAL = '3'
    GOOD = '4'
    VERY_GOOD = '5'

    RATING_CHOICES = (
        (VERY_LOW, '1'),
        (LOW, '2'),
        (NEUTRAL, '3'),
        (GOOD, '4'),
        (VERY_GOOD, '5'),
    )

    user = models.ForeignKey('register.User', on_delete=models.SET_NULL, null=True, related_name='rating_user')
    product = models.ForeignKey('register.Products', on_delete=models.SET_NULL, null=True, related_name='rating_product')
    rating = models.CharField(max_length= 5, choices=RATING_CHOICES)

    def to_json(self):
        return {
            'user': self.user,
            'product': self.product,
            'rating': self.rating
        }
        
class pix(AbstractBaseModel):
    recive = models.ForeignKey('register.Company', on_delete=models.CASCADE)
    payer = models.ForeignKey('register.Consumers', on_delete=models.CASCADE)
    txid = models.CharField(max_length=32)
    value = models.CharField(max_length=8)
    time = models.CharField(max_length=25)
    payer_pix_key = models.CharField(max_length=45)
    return_pix = models.ForeignKey('register.return_pix', on_delete=models.CASCADE)
    
class return_pix(AbstractBaseModel):
    recive = models.ForeignKey('register.Company', on_delete=models.CASCADE)
    payer = models.ForeignKey('register.Consumers', on_delete=models.CASCADE)
    _id = models.CharField(max_length=40)
    rtrid = models.CharField(max_length=40)
    values = models.CharField(max_length=8)
    status = models.BooleanField()