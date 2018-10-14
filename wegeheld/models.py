from django.db import models
from django.utils import timezone
from cpsecrets import token_bytes

class Action(models.Model):
    name_map=models.CharField(max_length=60)
    name_app=models.CharField(max_length=60)
    tmstmp=models.DateTimeField('last edit', auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return " {} {} ({}) [{:%d.%m.%Y}]".format(self.name_map, self.name_app, self.list_position, self.crdate.date() )
    def getFilename():
        return "Action.csv"
    def getHead():
        return ["id", "name"]
    def getRow(self):
        return [self.id, self.name_app]
    def getJsonName(): 
        return 'actions'
    def getJsonMapping():
        return lambda o : {'id': o.id, 'name': o.name_app}

class Town(models.Model):
    name=models.CharField(max_length=60)
    tmstmp=models.DateTimeField('last edit', auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    postalcode = models.CharField(max_length=255)
    def __str__(self):
        return " {} ({})[{:%d.%m.%Y}]".format(self.name, self.id, self.crdate )
    def getFilename():
        return "Town.csv"
    def getHead():
        return ["id", "name", "postalcode"]
    def getRow(self):
        return [self.id, self.name, self.postalcode]

class Street(models.Model):
    name=models.CharField(max_length=60)
    town = models.ForeignKey(Town, on_delete=models.DO_NOTHING)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def getFilename():
        return "Street.csv"
    def getHead():
        return ["id", "name", "town"]
    def getRow(self):
        return [self.id, self.name, self.town.name]
    def __str__(self):
        return "{} / {} ({})[{:%d.%m.%Y}]".format(self.town.name, self.name, self.id, self.crdate )
    class Meta: 
        ordering = ['town','name']


class Address(models.Model):
    streetnumber=models.CharField(max_length=40)
    town=models.ForeignKey(Town, on_delete=models.DO_NOTHING)
    street=models.ForeignKey(Street, on_delete=models.DO_NOTHING)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return " {} ({})[{} {} {:%d.%m.%Y}]".format(self.town, self.id, self.street, self.streetnumber, self.crdate)
    class Meta: 
        ordering = ['town','street']

class CarBrand(models.Model):
    name=models.CharField(max_length=60)
    tmstmp=models.DateTimeField('last edit',default=timezone.now)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    class Meta:
        ordering = ['list_position','crdate']
    def __str__(self):
        return " {} ({}) [{}]".format(self.name, self.list_position, self.tmstmp )
    def getFilename():
        return "Brand.csv"
    def getHead():
        return ["id", "name"]
    def getRow(self):
        return [self.id, self.name]
    def getJsonName(): 
        return 'brands'
    def getJsonMapping():
        return lambda o : {'id': o.id, 'name': o.name}

class CarColor(models.Model):
    name=models.CharField(max_length=60)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    hexValue=models.CharField(max_length=7)
    class Meta:
        ordering = ['list_position','crdate']

    def __str__(self):
        return " {} ({}) [{}]".format(self.name, self.list_position, self.tmstmp )

    def getFilename():
        return "Colors.csv"
    def getHead():
        return ["id", "name", "hex"]
    def getRow(self):
        return [self.id, self.name, '#'+self.hexValue]
    def getJsonName(): 
        return 'colors'
    def getJsonMapping():
        return lambda o : {'id': o.id, 'name': o.name}

class Car(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.DO_NOTHING)
    color = models.ForeignKey(CarColor, on_delete=models.DO_NOTHING)
    licenseplate=models.CharField(max_length=70)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    class Meta:
        ordering = ['brand','crdate']
    def __str__(self):
        return " {} ({}) [{}]".format(self.brand, self.color, self.tmstmp )

class Obstruction(models.Model):
    name=models.CharField(max_length=190)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    remark=models.CharField(max_length=190, blank=True, null=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return " {} ({}) [{}]".format(self.name, self.list_position, self.tmstmp )
    class Meta:
        ordering = ['list_position']
    def getFilename():
        return "Obstruction.csv"
    def getHead():
        return ["id", "name"]
    def getRow(self):
        return [self.id, self.name]
    def getJsonName(): 
        return 'obstructions'
    def getJsonMapping():
        return lambda o : {'id': o.id, 'name': o.name, 'remark': o.remark}

class Offense(models.Model):
    name=models.CharField(max_length=90)
    fee=models.DecimalField(max_digits=7,decimal_places=2)
    icon=models.CharField(max_length=120)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return " {} ({}) [{}]".format(self.name, self.list_position, self.tmstmp )
    class Meta:
        ordering = ['list_position']
    def getFilename():
        return "OffenseType.csv"
    def getHead():
        return ["id", "name"]
    def getRow(self):
        return [self.id, self.name]
    def getJsonName(): 
        return 'offenses'
    def getJsonMapping():
        return lambda o : {'id': o.id, 'name': o.name}

class Reporter(models.Model):
    email = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    tmstmp = models.DateTimeField('last edit',auto_now=True)
    crdate = models.DateTimeField('create',auto_now_add=True)
    list_position = models.IntegerField(default=90)
    authkey=models.CharField(max_length=64)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def createAuthKey(self):
        self.authkey=token_bytes(32)
        self.hidden=true # until verification
        return self.authkey
    def __str__(self):
        return " {} ({}) [{}]".format(self.nickname, self.email, self.tmstmp.date() )

class Funnysaying(models.Model):
    text=models.CharField(max_length=180)
    valid_offenses=models.ForeignKey(Offense, on_delete=models.DO_NOTHING, blank=True, null=True )
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return " {} [{}]".format(self.text, self.tmstmp )
    def getFilename():
        return "Funnysaying.csv"
    def getHead():
        return ["id", "offenseId", "text"]
    def getRow(self):
        return [self.id, self.valid_offenses_id, self.text]
    def getJsonName(): 
        return 'sayings'
    def getJsonMapping():
        return lambda o : {'id': o.id, 'text': o.text, 'valid_offenses': o.valid_offenses_id}

class Report(models.Model):
    longitude= models.DecimalField(max_digits=11,decimal_places=6)
    latitude= models.DecimalField(max_digits=11,decimal_places=6)
    date= models.DateTimeField('meldung')
    photos = models.IntegerField(default=0)
    free_text= models.CharField(max_length=155)
    address= models.ForeignKey(Address, on_delete=models.DO_NOTHING)
    offense= models.ForeignKey(Offense, on_delete=models.DO_NOTHING)
    obstruction= models.ForeignKey(Obstruction, on_delete=models.DO_NOTHING, blank=True, null=True)
    car= models.ForeignKey(Car, on_delete=models.DO_NOTHING, blank=True,null=True)
    action= models.ForeignKey(Action, on_delete=models.DO_NOTHING)
    reporter= models.ForeignKey(Reporter, on_delete=models.DO_NOTHING)
    funny_saying= models.ForeignKey(Funnysaying, on_delete=models.DO_NOTHING, blank=True, null=True)
    tweet=models.CharField(max_length=115, blank=True)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return " {} {} {} [{}]".format(self.car.brand.name, self.car.color.name, self.address.town, self.crdate )

class Photo(models.Model):
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    filename=models.CharField(max_length=90)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    class Meta:
        ordering = ['list_position']

class PublicAffairsOffice(models.Model):
    postalcode= models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    tmstmp=models.DateTimeField('last edit',auto_now=True)
    crdate =models.DateTimeField('create',auto_now_add=True)
    list_position=models.IntegerField(default=90)
    deleted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    def getFilename():
        return "Office.csv"
    def getHead():
        return ["plz", "name", "email"]
    def getRow(self):
        return [self.postalcode ,self.name , self.email ]
    def __str__(self):
        return "{}: {} {} [{}]".format(self.name, self.postalcode, self.email, self.crdate )


def last_touched():
    last = "id,timestamp\n"
    last +="Color,{}".format(round(CarColor.objects.latest('tmstmp').tmstmp.timestamp()))+"\n"
    last +="Action,{}".format(round(Action.objects.latest('tmstmp').tmstmp.timestamp()))+"\n"
    last +="OffenseType,{}".format(round(Offense.objects.latest('tmstmp').tmstmp.timestamp()))+"\n"
    last +="Brand,{}".format(round(CarBrand.objects.latest('tmstmp').tmstmp.timestamp()))+"\n"
    last +="Office,{}".format(round(PublicAffairsOffice.objects.latest('tmstmp').tmstmp.timestamp()))+"\n"
    last +="Saying,{}".format(round(Funnysaying.objects.latest('tmstmp').tmstmp.timestamp()))+"\n"
    return last
    
class EmailText(models.Model):
    postalcode=models.CharField(max_length=255, blank=True,null=True)
    offense= models.ForeignKey(Offense, on_delete=models.DO_NOTHING, blank=True, null=True)
    hidden=models.BooleanField(default=False)
    template=models.TextField(max_length=16500)
    def getJsonName(): 
        return 'emailtexts'
    def getJsonMapping():
        return lambda o : {'id': o.id, 'template': o.template, 'offense_id': o.offense_id}
