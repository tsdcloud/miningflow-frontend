from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(max_length=150)
    password = forms.CharField(max_length=100)


class EntityForm(forms.Form):
    business_name = forms.CharField(max_length=100)
    acronym = forms.CharField(max_length=50)
    unique_identifier_number = forms.CharField(max_length=14)
    principal_activity = forms.CharField(max_length=150)
    regime = forms.IntegerField()
    tax_reporting_center = forms.CharField(max_length=150)
    trade_register = forms.CharField(max_length=18)
    logo = forms.CharField(max_length=1000000)
    type_person = forms.IntegerField()


class BranchForm(forms.Form):
    label = forms.CharField(max_length=100)
    origin_id = forms.CharField(max_length=1000)
    firm_id = forms.CharField(max_length=1000)


class ServiceForm(forms.Form):
    name = forms.CharField(max_length=100)
    branch_id = forms.CharField(max_length=1000)


class FunctionForm(forms.Form):
    name = forms.CharField(max_length=100)
    service_id = forms.CharField(max_length=1000)
    power = forms.IntegerField(min_value=1)


class CategorieForm(forms.Form):
    name = forms.CharField(max_length=100)


class ArticleForm(forms.Form):
    name = forms.CharField(max_length=100)
    category_id = forms.CharField(max_length=1000)


class StockageAeraForm(forms.Form):
    name = forms.CharField(max_length=100)
    village_id = forms.CharField(max_length=1000)


class CareerForm(forms.Form):
    name = forms.CharField(max_length=100)
    uin = forms.CharField(max_length=13)
    village_id = forms.CharField(max_length=1000)


class StockageAeraLvForm(forms.Form):
    stockageaera_id = forms.CharField(max_length=1000)
    last_demand_quantity = forms.IntegerField()
    last_demand_volume = forms.FloatField()


class CareerLvForm(forms.Form):
    career_id = forms.CharField(max_length=1000)
    last_demand_quantity = forms.IntegerField()
    last_demand_volume = forms.FloatField()


class CareerArticleForm(forms.Form):
    career_id = forms.CharField(max_length=1000)
    stockage_id = forms.CharField(max_length=1000)
    article_id = forms.CharField(max_length=1000)
    price_sale = forms.IntegerField()
    price_car = forms.IntegerField()


class ApiForm(forms.Form):
    end = forms.CharField(max_length=1000)
    detail = forms.BooleanField(required=False)
    terminaison = forms.CharField(max_length=1000)
    id = forms.CharField(max_length=1000, required=False)
    action = forms.CharField(max_length=1000, required=False)
