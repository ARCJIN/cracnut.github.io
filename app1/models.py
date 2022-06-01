from django.db import models
from app1.userlogin import c_list
from django.core.validators import MaxValueValidator , MinValueValidator
# Create your models here.

def get_customer_profile_image_filepath(self,pk):
    return f'customer_profile_images/{self.pk}/{"profile_image.png"}'

def get_seller_profile_image_filepath(self,pk):
    return f'seller_profile_images/{self.pk}/{"profile_image.png"}'

def get_product_profile_image_filepath(self,pk):
    return f'product_profile_images/{self.pk}/{"profile_image.png"}'

def get_post_profile_image_filepath(self,pk):
    return f'post_profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return "static/companyphoto/borushki.jpg"

class Customer(models.Model):
    name = models.CharField(max_length = 50 , null = True , blank = True)
    username = models.CharField(max_length = 50 , blank = False , unique = True)
    password = models.CharField(max_length = 100 , blank = False , null = True )
    security = models.CharField(max_length = 100 , blank = False , null = True )
    email = models.EmailField(max_length = 50)
    followers = models.ManyToManyField('self', related_name='follower' , null=True , symmetrical=False)
    followings = models.ManyToManyField('self', related_name='following' , null=True, symmetrical=False)

    phone = models.CharField(max_length = 50 , null =True)
    created_date = models.DateTimeField(auto_now_add=True, null = True)
    last_login =        models.DateTimeField(verbose_name="created_date" , auto_now = True )
    address = models.CharField(max_length = 200 , null = True)
    crypto_owned = models.FloatField(null = True)
    profile_image = models.ImageField(null = True, max_length = 255, blank = True  ,upload_to="customerprofileimages/", default = "customerprofileimages/13ry.jpg" )
    money_owned = models.FloatField(null = True)
    is_certified = models.BooleanField(default = False , null = True)
    is_block = models.BooleanField(default = False , null = True)
    is_login = models.BooleanField(default = False , null = True)
    is_admin = models.BooleanField(default = False , null = True)
    desc = models.CharField(null=True , max_length=200)
    GENDER = (('MALE','MALE'),('FEMALE','FEMALE'))
    gender = models.CharField(max_length = 20 , choices = GENDER, blank = True)
    INTERESTED = (('MALE','MALE'),('FEMALE','FEMALE'))
    interested = models.CharField(max_length = 20 , choices = INTERESTED, blank = True)
    crushed = models.ManyToManyField('self', related_name='crushed_list' , null=True , symmetrical=False)
    is_private = models.BooleanField(default = False , null = True)
    is_customer = True
    is_seller = False
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


    def certifyit(self):
        self.is_certified = True
    def uncertifyit(self):
        self.is_certified = False
    def get_absolute_url(self):
        return reverse("customer_list",kwargs={'pk':self.pk})
    def makeprivate(self):
        self.is_private = True
    def makepublic(self):
        self.is_private = False
    def blockit(self):
        self.is_block = True

    def loginit(self):
        self.is_login = True

    def logoutit(self):
        self.is_login = False

    def unblockit(self):
        self.is_block = False
    def num_of_followers(self):
        return self.followers.count()
    def num_of_following(self):
        return self.followings.count()


    def __str__(self):
        return f" name={self.name}, followers = {self.followers}, following = {self.followings}"

class Seller(models.Model):
    name = models.CharField(max_length = 50 , null = True , blank = True)
    username = models.CharField(max_length = 50 , blank = False , unique = True)
    password = models.CharField(max_length = 100 , blank = False , null = True )
    email = models.EmailField(max_length = 50)
    phone = models.CharField(max_length = 50 , null =True)
    created_date = models.DateTimeField(auto_now_add=True, null = True)
    last_login =        models.DateTimeField(verbose_name="created_date" , auto_now = True )
    home_address = models.CharField(max_length = 200 , null = True)
    shop_address = models.CharField(max_length = 200 , null = True)
    crypto_owned = models.FloatField(null = True)
    profile_image = models.ImageField(null = True, max_length = 255, blank = True ,upload_to="sellerprofileimages/" )
    money_owned = models.FloatField(null = True)
    is_certified = models.BooleanField(default = False , null = True)
    is_block = models.BooleanField(default = False , null = True)
    is_login = models.BooleanField(default = False , null = True)
    is_admin = models.BooleanField(default = False , null = True)
    is_seller = True
    is_customer = False
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]


    def certifyit(self):
        self.is_certified = True
    def uncertifyit(self):
        self.is_certified = False
    def get_absolute_url(self):
        return reverse("customer_list",kwargs={'pk':self.pk})
    def blockit(self):
        self.is_block = True

    def loginit(self):
        self.is_login = True

    def logoutit(self):
        self.is_login = False

    def unblockit(self):
        self.is_block = False

    def __str__(self):
        return self.name



class Followrequest(models.Model):
    provider = models.ForeignKey(Customer,null = True ,related_name="provider", on_delete= models.SET_NULL)
    experiencer = models.ForeignKey(Customer,null = True , related_name="experiencer",on_delete= models.SET_NULL)
    acceptance_status = models.BooleanField(default = False , null=True)
    identity = models.CharField(max_length = 100, null=True)

    def accept(self):
        self.acceptance_status = True
    def decline(self):
        self.acceptance_status = False




class Tag(models.Model):
    name = models.CharField(max_length = 200 , null = True)

    def get_absolute_url(self):
        return reverse("tag",kwargs={'pk':self.pk})
    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False


    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length = 50)
    seller = models.ForeignKey(Seller , null = True , on_delete= models.SET_NULL)
    itemid = models.CharField(max_length = 50, default = 0)
    CATEGORY = (('tshirt','tshirt'),('shirt','shirt'),('hoodie','hoodie'),('cup','cup'),('phone covers','phone covers'),('bands','bands'),('gym vests','gym vests'),('keychain','keychain'),('posters','posters'),('stickers','stickers'),('notebooks','notebooks'),('caps','caps'),('bags','bags'),('socks','socks'),('footwear','footwear'),('masks','masks'))
    category = models.CharField(max_length = 20 , choices = CATEGORY , blank = True)
    COLOUR = (('red','red'),('blue','blue'),('green','green'),('orange','orange'),('purple','purple'),('yellow','yellow'),('black','black'),('white','white'))
    colour = models.CharField(max_length = 20 , choices = COLOUR, blank = True)
    material = models.CharField(max_length = 20 , blank = True)
    SIZE = (('S','S'),('M','M'),('L','L'),('XL','XL'),('XXL','XXL'),('XXXL','XXXL'))
    size = models.CharField(max_length = 5 , choices = SIZE , blank = True)
    returnperiod = models.PositiveIntegerField(null = True, default = 0)
    #product_image = models.ImageField(blank = False ,upload_to = 'product_images/')
    desc = models.CharField(max_length = 500, null =True , blank = True)
    likers = models.ManyToManyField(Customer, related_name="products_liked")
    number_of_likes = models.IntegerField(default=0)
    number_of_views = models.IntegerField(default = 0)
    number_of_purchases = models.IntegerField(default = 0)
    price = models.IntegerField(default = 0)
    quantity = models.IntegerField(default = 0)
    created_date = models.DateTimeField(auto_now_add=True , null = True)
    tags = models.ManyToManyField(Tag)
    is_block = models.BooleanField(default = False , null = True)
    fashion_of_the_week = models.BooleanField(default = False , null = True)
    is_special = models.BooleanField(default = False , null = True)
    is_promoted = models.BooleanField(default = False , null = True)
    is_highdemand = models.BooleanField(default = False , null = True)

    profile_image1 = models.ImageField(null = True, max_length = 255, blank = True , upload_to="productprofileimages/", default = get_default_profile_image )
    profile_image2 = models.ImageField(null = True, max_length = 255, blank = True , upload_to="productprofileimages/" , default = get_default_profile_image )
    profile_image3 = models.ImageField(null = True, max_length = 255, blank = True , upload_to="productprofileimages/" , default = get_default_profile_image )
    profile_image4 = models.ImageField(null = True, max_length = 255, blank = True , upload_to="productprofileimages/" , default = get_default_profile_image )
    profile_image5 = models.ImageField(null = True, max_length = 255, blank = True , upload_to="productprofileimages/" , default = get_default_profile_image )

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]











    def fashion_of_the_weekit(self):
        self.fashion_of_the_week = True
    def unfashion_of_the_weekit(self):
        self.fashion_of_the_week = False

    def specialit(self):
        self.is_special = True
    def unspecialit(self):
        self.is_special = False


    def promoteit(self):
        self.is_promoted = True
    def unpromoteit(self):
        self.is_promoted = False

    def highdemandit(self):
        self.is_highdemand = True
    def unhighdemandit(self):
        self.is_highdemand = False




    def get_absolute_url(self):
        return reverse("product",kwargs={'pk':self.pk})
    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False


    def __str__(self):
        return f" desc={self.desc}, likers = {self.likers}, name={self.name}"





class Bagitem(models.Model):
    name = models.CharField(max_length = 50)
    owner = models.ForeignKey(Customer , null = True , on_delete= models.SET_NULL)
    content = models.ForeignKey(Product, null = True , on_delete= models.SET_NULL)
    quantity = models.PositiveIntegerField(null = True, default = 1)
    item_in_bag = models.BooleanField(null = True , default = False)
    def __str__(self):
        return f"name = {self.name}{self.owner}{self.content}{self.quantity}"



class Order(models.Model):
    STATUS = (('Cash','Cash'),('Transaction Failed','Transaction Failed'), ('Transaction Successful','Transaction Successful') ,('Transaction to be verfied','Transaction to be verified'), ('Refund Request Active','Refund Request Active'), ('Refund Successful','Refund Successful'))
    ORDER_STATUS = (('Order Confirmed','Order Confirmed'),('Pending','Pending'),('Out for delivery','Out for delivery'),('Delivered','Delivered') , ('Cancelled','Cancelled'))
    customer = models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    product = models.ForeignKey(Product,null = True , on_delete= models.SET_NULL)
    seller = models.ForeignKey(Seller , null = True , on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True , null = True)
    address = models.CharField(max_length = 100 , null = True )
    order_status = models.CharField(max_length = 30 , null = True , choices = ORDER_STATUS)
    status = models.CharField(max_length = 30 , null = True , choices = STATUS)
    is_block = models.BooleanField(default = False , null = True)
    MODE_OF_PAYMENT = (('CASH','CASH'),('Gpay Confirmation Call','Gpay Confirmation Call'))
    mode_of_payment = models.CharField(max_length = 30 , null = True , choices = MODE_OF_PAYMENT)
    is_transaction_successfull = models.BooleanField(default = False,null = True)
    quantity = models.PositiveIntegerField(null = True)
    def __str__(self):
        return f"address = {self.address}"

    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False



class Club(models.Model):
    name = models.CharField(max_length = 100, unique=True)
    admin = models.ForeignKey(Customer, related_name="admin",on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=200 , null=True,blank=True,default="0000")
    trustee = models.ForeignKey(Customer, related_name="trustee",on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null = True)
    text = models.CharField(max_length = 1000)
    profile_image = models.ImageField(null = True,blank = True, default = get_default_profile_image , upload_to="clubprofileimages/",)
    cover_image = models.ImageField(null = True,blank = True, default = get_default_profile_image , upload_to="clubprofileimages/",)
    creation_fees = models.PositiveIntegerField(null = True, blank=True , default = 0)
    fees_to_enter = models.PositiveIntegerField(null = True , blank = True , default = 0)
    members = models.ManyToManyField(Customer, related_name="members")
    elites = models.ManyToManyField(Customer , related_name="elites")
    is_private = models.BooleanField(null = True , default = False)
    def __str__(self):
        return f" admin={self.admin}, trustee = {self.trustee} , created_date = {self.created_date} "
    def get_absolute_url(self):
        return reverse("club_list",kwargs={'pk':self.pk})


class Post(models.Model):
    creator = models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    desc = models.CharField(max_length = 500)
    profile_image = models.ImageField(null = True,blank = True, default = get_default_profile_image , upload_to="postprofileimages/",)
    is_block = models.BooleanField(default = False , null = True)
    is_special = models.BooleanField(default = False , null = True)
    is_promoted = models.BooleanField(default = False , null = True)
    is_highdemand = models.BooleanField(default = False , null = True)
    likers = models.ManyToManyField(Customer, related_name="posts_liked")
    num_of_comments = models.PositiveIntegerField(default=0, null = True)
    club = models.ForeignKey(Club, null=True, on_delete=models.SET_NULL)
    is_private = models.BooleanField(null = True , default = False)






    date_created = models.DateTimeField(auto_now_add=True , null = True)

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def specialit(self):
        self.is_special = True
    def unspecialit(self):
        self.is_special = False

        #self.likers.add(Customer.objects.get(id=list[0]))

    def promoteit(self):
        self.is_promoted = True
    def unpromoteit(self):
        self.is_promoted = False

    def highdemandit(self):
        self.is_highdemand = True
    def unhighdemandit(self):
        self.is_highdemand = False

    def add_comment(self):
        self.num_of_comments += 1

    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False


    ##def __str__(self):
        #return self.desc

    def __str__(self):
        return f" desc={self.desc}, likers = {self.likers}"









class Story(models.Model):
    composer = models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    desc = models.CharField(max_length = 500)
    profile_image = models.ImageField(null = True,blank = True, default = get_default_profile_image , upload_to="postprofileimages/",)
    is_block = models.BooleanField(default = False , null = True)
    is_special = models.BooleanField(default = False , null = True)
    is_promoted = models.BooleanField(default = False , null = True)
    is_highdemand = models.BooleanField(default = False , null = True)
    likers = models.ManyToManyField(Customer, related_name="storys_liked")
    is_closed_friend = models.BooleanField(null = True , default = False)
    viewers = models.ManyToManyField(Customer, related_name='viewers' , null=True)

    created_date = models.DateTimeField(auto_now_add=True , null = True)

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def specialit(self):
        self.is_special = True
    def unspecialit(self):
        self.is_special = False

        #self.likers.add(Customer.objects.get(id=list[0]))

    def promoteit(self):
        self.is_promoted = True
    def unpromoteit(self):
        self.is_promoted = False

    def highdemandit(self):
        self.is_highdemand = True
    def unhighdemandit(self):
        self.is_highdemand = False

    def add_comment(self):
        self.num_of_comments += 1

    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False


    ##def __str__(self):
        #return self.desc

    def __str__(self):
        return f" desc={self.desc}, likers = {self.likers}"











class Comment(models.Model):
    creator =  models.ForeignKey(Customer,null = True , on_delete= models.SET_NULL)
    post =  models.ForeignKey(Post,null = True , on_delete= models.SET_NULL)
    text = models.CharField(max_length=200,null=True)
    is_block = models.BooleanField(default = False, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null = True)




    def __str__(self):
        return f" creator={self.creator}, text = {self.text} , post = {self.post} "
    def blockit(self):
        self.is_block = True

    def unblockit(self):
        self.is_block = False



















class Chatbox(models.Model):
    sender = models.ForeignKey(Customer, related_name="sender",on_delete=models.SET_NULL, null=True)
    reciever = models.ForeignKey(Customer, related_name="reciever",on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length = 1000)
    created_date = models.DateTimeField(auto_now_add=True, null = True)
    def __str__(self):
        return self.text


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="product1",on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Customer, related_name="author1",on_delete=models.SET_NULL, null=True)
    text = models.CharField(null=True,blank = True , max_length=400)
    def __str__(self):
        return f" product={self.product}, author = {self.author}, text = {self.text}"
class Ratings(models.Model):
    product = models.ForeignKey(Product, related_name="product2",on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Customer, related_name="author2",on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=5 , validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return f" product={self.product}, author = {self.author}, score = {self.score}"




class Transfer(models.Model):
    giver = models.ForeignKey(Customer, related_name="giver",on_delete=models.SET_NULL, null=True)
    taker = models.ForeignKey(Customer, related_name="taker",on_delete=models.SET_NULL, null=True)
    units = models.PositiveIntegerField(default = 0 , null = True)
    def __str__(self):
        return f" giver={self.giver}, taker = {self.taker}, units = {self.units}"


class Pay(models.Model):
    payer = models.ForeignKey(Customer, related_name="payer",on_delete=models.SET_NULL, null=True)
    keeper = models.ForeignKey(Seller, related_name="keeper",on_delete=models.SET_NULL, null=True)
    units = models.PositiveIntegerField(default = 0 , null = True)
    def __str__(self):
        return f" payer={self.payer}, keeper = {self.keeper}, units = {self.units}"


class Lvl1tags(models.Model):
    post1 = models.ForeignKey(Post, related_name="post1",on_delete=models.SET_NULL, null=True)
    parent1 = models.ForeignKey(Customer, related_name="parent1",on_delete=models.SET_NULL, null=True)
    connections1 = models.ManyToManyField(Customer, related_name='connections1' , null=True, symmetrical=False)
    text= models.CharField(max_length = 50,null=True)
    def __str__(self):
        return f"text = {self.text}"

class Lvl2tags(models.Model):
    post2 = models.ForeignKey(Post, related_name="post2",on_delete=models.SET_NULL, null=True)
    parent2 = models.ForeignKey(Customer, related_name="parent2",on_delete=models.SET_NULL, null=True)
    connections2 = models.ManyToManyField(Customer, related_name='connections2' , null=True, symmetrical=False)
    text= models.CharField(max_length = 50,null=True)
    def __str__(self):
        return f"text = {self.text}"

class Lvl3tags(models.Model):
    post3 = models.ForeignKey(Post, related_name="post3",on_delete=models.SET_NULL, null=True)
    parent3 = models.ForeignKey(Customer, related_name="parent3",on_delete=models.SET_NULL, null=True)
    connections3 = models.ManyToManyField(Customer, related_name='connections3' , null=True, symmetrical=False)
    def __str__(self):
        return f" post3={self.post3}, parent3 = {self.parent3}, connections3 = {self.connections3}"

class Lvl4tags(models.Model):
    post4 = models.ForeignKey(Post, related_name="post4",on_delete=models.SET_NULL, null=True)
    parent4 = models.ForeignKey(Customer, related_name="parent4",on_delete=models.SET_NULL, null=True)
    connections4 = models.ManyToManyField(Customer, related_name='connections4' , null=True, symmetrical=False)
    def __str__(self):
        return f" post4={self.post4}, parent4 = {self.parent4}, connections4 = {self.connections4}"

class Lvl5tags(models.Model):
    post5 = models.ForeignKey(Post, related_name="post5",on_delete=models.SET_NULL, null=True)
    parent5 = models.ForeignKey(Customer, related_name="parent5",on_delete=models.SET_NULL, null=True)
    connections5 = models.ManyToManyField(Customer, related_name='connections5' , null=True, symmetrical=False)
    def __str__(self):
        return f" post5={self.post5}, parent5 = {self.parent5}, connections5 = {self.connections5}"
