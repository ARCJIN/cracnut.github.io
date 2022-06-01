from django.shortcuts import render , redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from app1.models import Chatbox,Followrequest,Story, Customer, Club ,Bagitem, Order , Product , Post, Seller , Comment , Ratings , Review , Lvl1tags, Lvl2tags, Lvl3tags, Lvl4tags, Lvl5tags
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from .filters import *
from django.contrib import messages
from .forms import *
from app1.userlogin import c_list
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.urls import reverse
import re

from django.db.models.functions import Now
# Create your views here.

s_list = []
list = []
import json
import hashlib

def stringify(data):
  return json.dumps(data)
def crypto_hash(*args):

  stringified_args = sorted(map(stringify, args))
  joined_data = "".join(stringified_args)
  """
  to convert any kind of data to stringed data
  """



  """
  return hashlib.sha256(data)
  will produce error because it requires data to be converted to binary, therefore we encode it with utf-8
  """

  return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

#https://dev.to/kunaal438/how-to-make-instagram-clone-using-html-css-fully-responsive-49co
if len(list)==0:
    try:
        if "c" in c_list:
            user = Customer.objects.get(id = str(c_list[0]))
            user.logoutit()
            user.save()
            c_list.clear()
        elif "s" in c_list:
            user = Seller.objects.get(id = str(c_list[0]))
            user.logoutit()
            user.save()
            c_list.clear

    except:
        pass




def count_posts_of(iuser):
    return Post.objects.filter(creator = iuser).count()

def count_products_of(iseller):
    return Product.objects.filter(seller = iseller).count()
def count_comments_of(ipost):
    return Comment.objects.filter(post = ipost).count()
def baseintro(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user}
        return render(request, 'app1/baseintro.html' , context )



def chatbox(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:

        clubs = Club.objects.all().order_by('-created_date')

        context = {'user':user, 'clubs':clubs}
        return render(request,'app1/clubs.html' , context)


def chatbox_detail(request,pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        club = Club.objects.get(id = pk)
        post_list = Post.objects.filter(club = club)
        if request.method == "POST":
            x = request.POST.get('id')
            posh = Post.objects.get(id = x)
            if user in posh.likers.all():
                posh.likers.remove(user)
                posh.save()
            elif user not in posh.likers.all():
                posh.likers.add(user)
                posh.save()
        context = {'user':user , 'club':club , 'post_list':post_list}
        return render(request,'app1/club_detail.html',context)


def commentbox(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    if user == None:
        return redirect('/')
    else:

        post = Post.objects.get(id = pk)
        comments = Comment.objects.filter(post=post).order_by('-date_created')
        if request.method == "POST":
            x = Comment()
            x.text =  request.POST.get('text')
            x.creator = user
            x.post = post
            post.add_comment()
            post.save()
            x.save()


        context = {'user':user , 'post':post , 'comments':comments}
        return render(request , 'app1/commentbox.html' , context)

def memberlist(request , pk):

    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    if user == None:
        return redirect('/')
    else:
        club = Club.objects.get(id = pk)
        if request.method == "POST" and "kickout" in request.POST:
            id = request.POST.get('member')
            member = Customer.objects.get(id = id)
            if member in club.members.all():
                club.members.remove(member)
                club.save()

        if request.method == "POST" and "makeelite" in request.POST:
            id = request.POST.get('member')
            member = Customer.objects.get(id = id)
            if member not in club.elites.all():
                club.elites.add(member)
                club.save()
        if request.method == "POST" and "undomakeelite" in request.POST:
            id = request.POST.get('member')
            member = Customer.objects.get(id = id)
            if member in club.elites.all():
                club.elites.remove(member)
                club.save()



        context = {"user":user , "club":club}
        return render(request , 'app1/memberlist.html' , context)


def home(request ):

    customer = Customer.objects.all().order_by('name')
    seller = Seller.objects.all().order_by('name')
    post = Post.objects.all().order_by('desc')
    order = Order.objects.all()
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])

        else:
            user = None
    except:
        user = None
    if user == None:
        return redirect('/')
    else:

        leaders = []
        for icustomer in customer:
            if len(leaders) == 0:
                leaders.append(icustomer)
            else:
                for c in range(0,len(leaders)):
                    if icustomer.num_of_followers() > leaders[c].num_of_followers():
                        leaders.insert(c , icustomer)
                        break
                    elif icustomer.num_of_followers() < leaders[c].num_of_followers():
                        if c == len(leaders) -1:
                            leaders.append(icustomer)
                            break
                        else:
                            continue
                    elif icustomer.num_of_followers() == leaders[c].num_of_followers():
                        if icustomer.num_of_following() > leaders[c].num_of_following():
                            if c == len(leaders) -1:
                                leaders.append(icustomer)
                                break
                            else:
                                continue
                        elif icustomer.num_of_following() < leaders[c].num_of_following():
                            leaders.insert(c , icustomer)
                            break
                        elif icustomer.num_of_following() == leaders[c].num_of_following():
                            leaders.insert(c , icustomer)
                            break
                        else:
                            return HttpResponse("What the hell error")

                    else:
                        return HttpResponse("What the hell error")


        postleaders = []
        for ipost in post:
            if len(postleaders) == 0:
                postleaders.append(ipost)
            else:
                for c in range(0,len(postleaders)):
                    if ipost.likers.count() > postleaders[c].likers.count():
                        postleaders.insert(c , ipost)
                        break
                    if ipost.likers.count() < postleaders[c].likers.count():
                        if c == len(postleaders) -1:
                            posleaders.append(ipost)
                            break
                        else:
                            continue
                    elif  ipost.likers.count() == postleaders[c].likers.count():
                        if ipost.likers.count() > postleaders[c].likers.count():
                            if c == len(postleaders) -1:
                                postleaders.append(ipost)
                                break
                            else:
                                continue
                        elif ipost.likers.count() < postleaders[c].likers.count():
                            postleaders.insert(c , ipost)
                            break
                        elif ipost.likers.count() == postleaders[c].likers.count():
                            postleaders.insert(c , ipost)
                            break
                        else:
                            return HttpResponse("What the hell error")

                    else:
                        return HttpResponse("What the hell error")
        uploaded_file_url = 0
        if request.method == "POST" and request.FILES['profile_image']:
            if request.POST.get('desc') :
                post = Post()
                post.creator = user
                post.desc = request.POST.get('desc')
                post.profile_image = request.FILES['profile_image']
                post.save()
                fs = FileSystemStorage()

                filename = fs.save(post.profile_image.name , post.profile_image)
                uploaded_file_url = fs.url(filename)
                print("success")
                return redirect(reverse('customer_detail', kwargs={'pk':user.id}))
            else:
                print("You need to write a text")
                return HttpResponse("Pls enter some description")

        no_of_users = customer.count()
        no_of_sellers = seller.count()
        order= Order.objects.all()
        no_of_orders = order.count()
        orders_delivered = order.filter(status = "Delivered")
        orders_pending = order.filter(status = "Pending")
        context = {'no_of_sellers':no_of_sellers,'postleaders':postleaders,'leaders':leaders, 'uploaded_file_url':uploaded_file_url,'user':user,'customer':customer,'order':order,'no_of_users': no_of_users, 'no_of_orders': no_of_orders,
                                                        'orders_pending':orders_pending,'orders_delivered':orders_delivered,
                                                        }
        return render(request, 'app1/home.html' , context )

def searchlist(request):



    posts = Post.objects.all()


    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {"user":user , "posts":posts }
    if request.method == "POST":
        searched = request.POST['searched']
        customers = Customer.objects.filter(Q(name__contains=searched)| Q(username__contains=searched))
        sellers = Seller.objects.filter(Q(name__contains=searched)| Q(username__contains=searched))
        products = Product.objects.filter(Q(name__contains=searched)|Q(category__contains=searched)| Q(colour__contains=searched)| Q(material__contains=searched)| Q(size__contains=searched)| Q(desc__contains=searched))

        return render(request, 'app1/searchlist.html' , {"searched":searched, "customers":customers , "user":user , "sellers":sellers, "products":products, "posts":posts } )
    else:
        return render(request, 'app1/searchlist.html' , context )

def clubsearchlist(request):
    clubs = Club.objects.all()
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    context = {"user":user , "clubs":clubs }

    if request.method == "POST":
        searched = request.POST['searched']
        clubs = Club.objects.filter(Q(name__contains=searched)| Q(text__contains=searched))

        return render(request, 'app1/clubsearchlist.html' , {"searched":searched, "clubs":clubs , "user":user} )
    else:
        return render(request, 'app1/searchlist.html' , context )



def site_data(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'user':user}
    return render(request, 'app1/site_data_page.html',context  )



def site_progress(request):

    customers= Customer.objects.all()
    no_of_users = customers.count()
    orders= Order.objects.all()
    no_of_orders = orders.count()

    orders_delivered = orders.filter(status = "Delivered")
    orders_pending = orders.filter(status = "Pending")
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    return render(request, 'app1/site_progress.html',{'user':user,'no_of_users': no_of_users, 'no_of_orders': no_of_orders,
                                                        'orders_pending':orders_pending,'orders_delivered':orders_delivered,
                                                        } )





def customer_login(request):

    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            customer = Customer.objects.get(username = username)
            id = customer.id
            list.clear()
            list.append(id)
            list.append("c")
            c_list.append(id)
            c_list.append("c")

            if customer.password == password or customer.password == crypto_hash(password):
                if customer.is_login == False:
                    if customer.is_block == True:
                        return HttpResponse("Your Account has been suspended due to violations of community guidelines")
                    else:
                        customer.loginit()
                        customer.save()
                        return redirect('product_list')
                else:
                    return redirect('product_list')

            else:
                msg = "you entered the wrong info, please try again"
                context = {'user':user, 'msg':msg}
                return render(request, 'app1/customer_login.html',context )
        except:
            msg = "No user exist with username {x}".format(x = username)
            context = {'user':user, 'msg':msg}
            return render(request, 'app1/customer_login.html',context )


    context = {'user':user}
    return render(request, 'app1/customer_login.html',context )









def seller_login(request):

    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            seller = Seller.objects.get(username = username)
        except:
            return HttpResponse("No user exists with this username")
        print("c")
        id = seller.id
        list.clear()
        list.append(id)
        list.append("s")
        c_list.append(id)
        c_list.append("s")


        if seller.password == password :
            if seller.is_login == False:
                seller.loginit()
                seller.save()

                return redirect('sellerintro')
            else:
                print("test")
                return redirect('sellerintro')

        else:
            print("you entered the wrong info, please try again")
            return redirect('seller_login')
    context = {'user':user}
    return render(request, 'app1/seller_login.html', context)





def customerintro(request ):
    try:
        user = Customer.objects.get(id = list[0])
    except:
        user = None
    orders = Order.objects.all()[::-1]
    posts = Post.objects.filter(creator = user)
    """
    a = {}
    a[0] = 0
    x = 1
    for ipost in posts:

        comments = Comment.objects.filter(post = ipost)
        i = len(comments)
        a[x] = i
        x = x+1
    print(a)
    """
    x = count_posts_of(user)

    context = {'user':user , 'orders':orders , 'posts':posts , 'x':x}
    return render(request, 'app1/customerintro.html',context )



def sellerintro(request ):
    try:
        user = Seller.objects.get(id = list[0])
    except:
        user = None
    orders = Order.objects.all()
    products = Product.objects.all().filter(seller = user)
    posts = Post.objects.all()
    x = count_products_of(user)
    context = {'x':x, 'user':user , 'orders':orders , 'posts':posts, 'products':products}
    return render(request, 'app1/sellerintro.html',context )

def customerlogout(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None


    if request.method == "POST":
        if user.is_login == True:
            user.logoutit()
            list.clear()
            user.save()
            return redirect('/')
        elif user == None:
            return redirect('/')
    context = {'user':user}

    return render(request, 'app1/customerlogout.html',context )





def sellerlogout(request):
    user = Seller.objects.get(id = str(list[0]))


    if request.method == "POST":
        if user.is_login == True:
            user.logoutit()
            list.clear()
            user.save()
            return redirect('/')
    context = {'user':user}

    return render(request, 'app1/sellerlogout.html',context )













def follower_list(request , pk):
    customers = Customer.objects.all()
    customer = Customer.objects.get(id = pk)
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'customer':customer,'user':user,'customers':customers}
    return render(request,'app1/follower_list.html',context)


def following_list(request , pk):
    customers = Customer.objects.all()
    customer = Customer.objects.get(id = pk)
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'customer':customer,'user':user,'customers':customers}
    return render(request,'app1/following_list.html',context)




def pendingorderslist(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    orders = Order.objects.filter(seller = user)
    context = {'user':user , 'orders':orders}
    return render(request, 'app1/pendingorderslist.html',context)


















def likelist(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    post = Post.objects.get(id = pk)
    likers = post.likers.all()
    context = {'user':user, 'post':post,'likers':likers}
    return render(request, 'app1/likelist.html' , context)



def productlikelist(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    product = Product.objects.get(id = pk)
    likers = product.likers.all()
    context = {'user':user, 'product':product,'likers':likers}
    return render(request, 'app1/productlikelist.html' , context)


def ratinglist(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    product = Product.objects.get(id = pk)
    likers = product.likers.all()
    ratings = Ratings.objects.filter(product = product)
    x = []
    for rat in ratings:
        if rat.author == user:
            x.append(user)

    if len(x) == 0:
        a=1
    else:
        a=0


    if request.method == "POST":
        form = Ratings()
        form.product = product
        form.author = user

        form.score = request.POST.get('score')
        if int(form.score)<1 or int(form.score)>5:
            return HttpResponse("Rating should be between 1 to 5")
        else:
            print("successful")
            form.save()
            return redirect('customerintro')
    context = {'a': a , 'user':user, 'product':product,'likers':likers , 'ratings':ratings}
    return render(request, 'app1/ratinglist.html' , context)

def reviewlist(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    product = Product.objects.get(id = pk)
    likers = product.likers.all()
    ratings = Ratings.objects.filter(product = product)
    reviews = Review.objects.filter(product=product)
    if request.method == "POST":
        form = Review()
        form.product = product
        form.author = user
        form.text = request.POST.get('text')
        print("successfull")
        form.save()
    context = {'user':user, 'product':product,'likers':likers ,'reviews':reviews,'ratings':ratings}
    return render(request, 'app1/reviewlist.html' , context)










def products(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'user',user}
    return render(request, 'app1/products.html' , context )

def customer(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'user',user}
    return render(request, 'app1/customers.html',context )

def order(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'user',user}
    return render(request, 'app1/order.html',context )

def tag(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'user',user}
    return render(request, 'app1/tag.html', context )









class ProductListView(ListView):
    model = Product
    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['posts'] = posts
        return context

def productdetail(request , pk):
        posts = Post.objects.all()

        product = Product.objects.get(id = pk)
        seller = product.seller
        orders_count = Order.objects.filter(product = product).count()
        ratings = Ratings.objects.filter(product = product)
        ratings_count = int(ratings.count())
        answer = 0
        reviews_count = Review.objects.filter(product=product).count()
        for rating in ratings:
            answer = answer+ int(rating.score)

        try:
            answer = answer/(int(ratings.count()))
        except ZeroDivisionError :
            answer = 0
        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None


        if user not in product.likers.all():
            if request.method == "POST"  and "submit" in request.POST:

                product.likers.add(user)
                product.save()
        else:
            if request.method == "POST"  and "submit" in request.POST:

                product.likers.remove(user)
                product.save()
        bag = 1
        try:
            bagid = Bagitem.objects.get(owner = user , content = product)
        except:
            bagid = False
        if request.method == 'POST' and "addtocart" in request.POST:
            id = request.POST.get('name')
            item = Product.objects.get(id = id)
            quantity = request.POST.get('quantity')
            print("quantity is :", quantity)
            if quantity != None:
                try:
                    if int(quantity) > int(product.quantity):
                        msg = "*Order quantity exceeds inventory. Please input quantity less than {x}".format(x = product.quantity)
                        context = {'msg':msg,'bagid':bagid,'bag':bag, 'seller':seller,'ratings_count':ratings_count, 'reviews_count':reviews_count , 'answer':answer, 'posts':posts, 'user':user , 'product':product,'orders_count':orders_count}
                        return render(request , 'app1/product_detail.html' , context)
                    else:
                        msg = ""
                        bag = Bagitem()
                        bag.name = user.name + item.name
                        bag.owner = user
                        bag.content = item
                        bag.quantity = 1
                        bag.item_in_bag = True
                        bag.quantity = quantity
                        bag.save()
                        context = {'msg':msg,'bagid':bagid,'bag':bag, 'seller':seller,'ratings_count':ratings_count, 'reviews_count':reviews_count , 'answer':answer, 'posts':posts, 'user':user , 'product':product,'orders_count':orders_count}
                        return redirect(reverse('ibag'))
                except:
                    quantity = 0
                    msg = "*Enter number of units to purchase this item"
                    context = {'msg':msg,'bagid':bagid,'bag':bag, 'seller':seller,'ratings_count':ratings_count, 'reviews_count':reviews_count , 'answer':answer, 'posts':posts, 'user':user , 'product':product,'orders_count':orders_count}
                    return render(request , 'app1/product_detail.html' , context)

            else:
                quantity = 0
                msg = "*Enter number of units to purchase this item"
                context = {'msg':msg,'bagid':bagid,'bag':bag, 'seller':seller,'ratings_count':ratings_count, 'reviews_count':reviews_count , 'answer':answer, 'posts':posts, 'user':user , 'product':product,'orders_count':orders_count}
                return render(request , 'app1/product_detail.html' , context)
        context = {'bagid':bagid,'bag':bag, 'seller':seller,'ratings_count':ratings_count, 'reviews_count':reviews_count , 'answer':answer, 'posts':posts, 'user':user , 'product':product,'orders_count':orders_count}
        return render(request , 'app1/product_detail.html' , context)

def men(request):
    x = []
    y = "men"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def women(request):
    x = []
    y = "women"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def electronics(request):
    x = []
    y = "electr"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def tshirts(request):
    x = []
    y = "tshirt"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def shirts(request):
    x = []
    y = "shirt"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)
def hoodies(request):
    x = []
    y = "hoodie"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def cups(request):
    x = []
    y = "cup"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def phonecovers(request):
    x = []
    y = "phone c"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def bands(request):
    x = []
    y = "band"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def gymvests(request):
    x = []
    y = "gym"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def keychains(request):
    x = []
    y = "keychain"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def posters(request):
    x = []
    y = "poster"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def stickers(request):
    x = []
    y = "sticker"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def notebooks(request):
    x = []
    y = "notebook"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)




def caps(request):
    x = []
    y = "cap"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def bags(request):
    x = []
    y = "bag"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def socks(request):
    x = []
    y = "sock"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def masks(request):
    x = []
    y = "mask"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)



def footwears(request):
    x = []
    y = "footwear"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def bottles(request):
    x = []
    y = "bottle"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def summer(request):
    x = []
    y = "summer"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def winter(request):
    x = []
    y = "winter"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)





def beach(request):
    x = []
    y = "beach"
    product = Product.objects.all()
    for iproduct in product:
        if re.search(y, str(iproduct.desc)) or re.search(y, str(iproduct.name)) or re.search(y, str(iproduct.category)) or re.search(y, str(iproduct.material)) or re.search(y, str(iproduct.colour)) or re.search(y, str(iproduct.size)) :
            x.append(iproduct)
    itemtotalcount = len(x)
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':x , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def fashionoftheweek(request):

    product = Product.objects.all().filter(fashion_of_the_week = True)
    itemtotalcount = product.count()
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':product , 'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)

def highdemand(request):

    product = Product.objects.all().filter(is_highdemand = True)
    itemtotalcount = product.count()
    count = 0
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':product ,'itemtotalcount':itemtotalcount , 'count':count}
        return render(request , 'app1/shop.html' , context)


def special(request):
    count = 0
    product = Product.objects.all().filter(is_special = True)
    itemtotalcount = product.count()
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':product,'itemtotalcount':itemtotalcount, 'count':count}
        return render(request , 'app1/shop.html' , context)

def promoted(request):
    count = 0
    product = Product.objects.all().filter(is_promoted = True)
    itemtotalcount = product.count()
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        context = {'user':user,'items':product,'itemtotalcount':itemtotalcount,'count':count}
        return render(request , 'app1/shop.html' , context)




class OrderListView(ListView):
    model = Order
    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['posts'] = posts
        return context

def orderdetailview(request, pk):
    order = Order.objects.get(id = pk)
    product = order.product
    posts = Post.objects.all()
    nowtime = date.today()
    dc = order.date_created.date()
    x = str(nowtime-dc)
    x = x[0:3]
    y = x
    if order.product.returnperiod == None:
        order.product.returnperiod = 0
        order.save()

    try:
        if int(y) > int(order.product.returnperiod):
            ordertime = False
        else:
            ordertime = True
    except:
        ordertime = True
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        bag = 1
        try:
            bagid = Bagitem.objects.get(owner = user , content = order.product)
        except:
            bagid = False
        if request.method == 'POST' and "addtocart" in request.POST:
            id = request.POST.get('name')
            item = Product.objects.get(id = id)
            quantity = request.POST.get('quantity')
            if quantity != None:
                try:
                    if int(quantity) > int(product.quantity):
                        msg = "Order quantity exceeds inventory. Please input quantity less than {x}".format(x = product.quantity)
                        context = {'ordertime':ordertime,'order': order,'msg':msg,'bagid':bagid, 'posts':posts, 'user':user , 'product':product}
                        return render(request , 'app1/order_detail.html' , context)
                    else:
                        msg = ""
                        bag = Bagitem()
                        bag.name = user.name + item.name
                        bag.owner = user
                        bag.content = item
                        bag.quantity = 1
                        bag.item_in_bag = True
                        bag.quantity = quantity
                        bag.save()
                        context = {'ordertime':ordertime,'order': order,'msg':msg,'bagid':bagid,'bag':bag, 'posts':posts, 'user':user , 'product':product}

                        return redirect(reverse('ibag'))
                except:
                    quantity = 0
                    msg = "Enter number of units to purchase this item"
                    context = {'ordertime':ordertime,'order': order,'msg':msg,'bagid':bagid, 'posts':posts, 'user':user , 'product':product}

                    return render(request , 'app1/order_detail.html' , context)
            else:
                quantity = 0
                msg = "Enter number of units to purchase this item"
                context = {'ordertime':ordertime,'order': order,'msg':msg,'bagid':bagid,'bag':bag, 'posts':posts, 'user':user , 'product':product}
                return render(request , 'app1/order_detail.html' , context)

        if request.method == 'POST' and "returnbutton" in request.POST:
            id = request.POST.get('name')
            order = Order.objects.get(id = id)
            order.status = "Refund Request Active"
            order.order_status = "Cancelled"
            order.save()
            return redirect(reverse('order_detail', kwargs={'pk':order.id}))

    context = {'ordertime':ordertime,'order': order,'bagid':bagid,'bag':bag, 'posts':posts, 'user':user , 'product':product}

    return render(request , 'app1/order_detail.html' , context)









class CustomerListView(ListView):

    model = Customer


    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None

        if user == None:
            return redirect('/')
        else:
            context = super().get_context_data(**kwargs)
            context['user'] = user
            context['posts'] = posts
            return context
    #extra_context = {'user':user, 'posts':posts}


    def get_queryset(self):
        return Customer.objects.all().order_by("username")

def customerdetailview(request , pk):
    customer = Customer.objects.get(id = pk)

    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None


    posts = Post.objects.filter(creator = customer)
    x = count_posts_of(customer)
    context = {'user':user , 'customer':customer , 'posts':posts, 'x':x}
    try:
        if user == None:
            return redirect('/')
        elif user.is_seller == True:
            return render(request, 'app1/customer_detail.html' , context)
        else:
            if customer in user.followings.all() :
                #UnFollow
                if request.method == "POST" and "unfollow" in request.POST :
                    user.followings.remove(customer)
                    customer.followers.remove(user)
                    user.save()
                    customer.save()
            else:
                #follow
                if request.method == "POST" and "follow" in request.POST :
                    user.followings.add(customer)
                    customer.followers.add(user)
                    user.save()
                    customer.save()

            if request.method == "POST" and "crushed" in request.POST:
                customer.crushed.add(user)
                customer.save()
            if request.method == "POST" and "uncrushed" in request.POST:
                customer.crushed.remove(user)
                customer.save()
            if request.method == "POST" and "req" in request.POST:
                a_req = Followrequest()
                a_req.experiencer = customer
                a_req.provider = user
                a_req.identity = str(customer.name) + str(user.name)
                a_req.save()

            if request.method == "POST" and "delreq" in request.POST:
                a_req = Followrequest.objects.filter(experiencer = customer , provider = user)
                a_req[0].delete()





    except:
        print("error occured")
        return redirect('/')

    try:
        a = Followrequest.objects.filter(provider = user, experiencer = customer)
        b = len(a)
        if b>0:
            req_sent = True
        else:
            req_sent = False
    except:
        req_sent = False
    context = {'req_sent': req_sent,'user':user , 'customer':customer , 'posts':posts, 'x':x}
    return render(request, 'app1/customer_detail.html' , context)
    #extra_context = {'user':user,'orders' : Order.objects.all(), 'posts':posts}




class SellerListView(ListView):

    model = Customer


    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['posts'] = posts
        return context
    #extra_context = {'user':user, 'posts':posts}


    def get_queryset(self):
        return Seller.objects.all().order_by("username")

class SellerDetailView(DetailView):
    model = Seller



    def get_context_data(self, **kwargs):
        posts = Post.objects.all()

        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        orders = Order.objects.all()
        context['user'] = user
        context['posts'] = posts
        context['products'] = products
        context['orders'] = orders
        return context
    #extra_context = {'user':user,'orders' : Order.objects.all(), 'posts':posts}









def createorder(request , pk ):
    customer = Customer.objects.all()
    product = Product.objects.get(id = pk)
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    orderform = OrderForm()

    if request.method == "POST":
        orderform = OrderForm(request.POST)

        a = request.POST.get('house')
        b = request.POST.get('colony')
        c = request.POST.get('city')
        d = request.POST.get('state')
        e = request.POST.get('pincode')
        if product.quantity<=0:
            return(HttpResponse("CURRENT ORDER UNAVAILABLE"))
        else:
            if (orderform.is_valid()):
                print("valid")

                obj = orderform.save(commit=False)
                obj.customer = user
                obj.seller = product.seller
                obj.product = product
                obj.address = "House: {}, Colony: {}, City: {}, state: {}, Pincode: {}".format(a,b,c,d,e)
                product.quantity = product.quantity -1
                product.save()
                print("should execute")
                if obj.is_block == True:
                    obj.is_block = True
                else:
                    obj.is_block = False

                    if obj.mode_of_payment == "CASH" :
                        obj.order_status = "Order Confirmed"
                        obj.status = "Pending"
                        obj.save()
                        print("Order saved")


                        return redirect('customerintro')

                    elif obj.mode_of_payment == "Gpay Confirmation Call" :
                        obj.order_status = "Order Confirmed"
                        obj.status = "Pending"
                        obj.save()
                        print("Order saved")


                        return redirect('customerintro')

                    elif obj.mode_of_payment == "VNITS":
                        if user.crypto_owned < product.price :
                            return HttpResponse("Insufficient Balance, Pls Add Funds by going to -> Profile -> Add Funds. * Do not refresh the page")
                        else:
                            user.crypto_owned -= product.price
                            product.seller.crypto_owned += product.price
                            obj.status = "Transaction Successful"
                            obj.order_status = "Pending"

                            user.save()
                            product.seller.save()
                            obj.save()


                    else:
                        if obj.is_transaction_successfull == True:
                            obj.status = "Transaction Successful"
                            obj.order_status = "Pending"
                            obj.save()

                            return redirect('customerintro')
                        elif obj.is_transaction_successfull == False:
                            obj.status = "Transaction Failed"
                            obj.order_status = "Cancelled"
                            obj.save()

                        else:
                            obj.status = "Transaction to be verfied"
                            obj.order_status = "Pending"
                            obj.save()

                            return redirect('/')

            else:
                orderform = OrderForm()
                print("Not Valid")

    context = {'orderform':orderform , 'user':user , 'product': product}
    return  render(request , 'app1/order_form.html' , context)



def createcustomer(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    form = CustomerForm
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form , 'user':user}
    return  render(request , 'app1/customer_form.html' , context)


def createproduct(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    form = ProductForm
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form , 'user':user}
    return  render(request , 'app1/product_form.html' , context)




def productupload(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None


    if request.method == "POST":
        product = Product()
        product.seller = user
        product.save()
        try:
            if request.POST.get('name'):
                product.name = request.POST.get('name')
                product.save()
        except:
            return HttpResponse("Some Error")
        try:
            if request.POST.get('itemid'):
                product.itemid = request.POST.get('itemid')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('category'):
                product.category = request.POST.get('category')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('colour'):
                product.colour = request.POST.get('colour')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('material'):
                product.material = request.POST.get('material')
                product.save()
        except:
            return HttpResponse("Some Error")


        try:
            if request.POST.get('size'):
                product.size = request.POST.get('size')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('desc'):
                product.desc = request.POST.get('desc')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('price'):
                product.price = request.POST.get('price')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('quantity'):
                product.quantity = request.POST.get('quantity')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.FILES['profile_image1'] :
                product.profile_image1 = request.FILES['profile_image1']
                product.save()
        except:
            return redirect(reverse('seller_detail', kwargs={'pk':user.id}))

        try:
            if request.FILES['profile_image2'] :
                product.profile_image2 = request.FILES['profile_image2']
                product.save()
        except:
            return redirect(reverse('seller_detail', kwargs={'pk':user.id}))

        try:
            if request.FILES['profile_image3'] :
                product.profile_image3 = request.FILES['profile_image3']
                product.save()
        except:
            return redirect(reverse('seller_detail', kwargs={'pk':user.id}))

        try:
            if request.FILES['profile_image4'] :
                product.profile_image4 = request.FILES['profile_image4']
                product.save()
        except:
            return redirect(reverse('seller_detail', kwargs={'pk':user.id}))

        try:
            if request.FILES['profile_image5'] :
                product.profile_image5 = request.FILES['profile_image5']
                product.save()
        except:
            return redirect(reverse('seller_detail', kwargs={'pk':user.id}))

        return redirect('/')


    context = {'user':user}
    return  render(request , 'app1/productupload.html' , context)





def addcustomer(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    uploaded_file_url = 0
    try:
        if request.method == "POST":
            print("not going in")
            if request.POST.get('name') and request.POST.get('username') and  request.POST.get('email') and  request.POST.get('password'):
                customer = Customer()
                customer.name =  request.POST.get('name')
                customer.username = request.POST.get('username')
                customer.email = request.POST.get('email')

                x = request.POST.get('password')
                customer.password = crypto_hash(x)

                #customer.profile_image = request.FILES['profile_image']



                #fs = FileSystemStorage()

                ##uploaded_file_url = fs.url(filename)

                customer.save()
                bag = Bag()
                bag.owner = customer
                bag.name = crypto_hash(customer.name)
                bag.save()
                print("user and bag saved")
                context = {'user':user }#, 'uploaded_file_url':uploaded_file_url}
                return redirect('customer_login')
            else:
                print("user not saved")
                context = {'user':user, "msg":"Creation of seller account Failed"}
                return render(request , 'app1/add_customer.html', context)
        context = {'user':user, "msg":""}
        return render(request , 'app1/add_customer.html', context)


    except:
        context = {'user':user , "msg":"Account with this username already exists"}
        return render(request , 'app1/add_customer.html', context)


def ibag(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    bag = Bagitem.objects.filter(owner = user)
    x = len(bag)
    if request.method == 'POST':


        if "delbutton" in request.POST:
            id = request.POST.get('id')
            item = Product.objects.get(id = id)
            bagitem = Bagitem.objects.filter(Q(content = item) & Q(owner = user))
            for x in bagitem:
                print(len(bagitem))
                x.delete()
                v = Bagitem.objects.filter(owner = user)
                if len(v) == 0:
                    return redirect('product_list')
                else:
                    return redirect(reverse('ibag'))

        elif "placeorder" in request.POST:
            bag = Bagitem.objects.filter(owner = user)
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            pincode = request.POST.get('zip')


            for item in bag:
                order = Order()
                order.customer = user
                order.product = item.content
                order.seller = item.content.seller
                order.order_status = "Order Confirmed"
                order.status = "Cash"
                order.mode_of_payment = "CASH"
                order.is_transaction_successfull = False
                order.quantity = item.quantity
                order.address = str(address) + str(city) + str(state) + str(pincode)
                order.save()
                item.content.quantity -= order.quantity
                item.content.save()
                item.delete()

            return redirect('product_list')


    sum = 0
    for item in bag:
        sum = sum+ (item.quantity* item.content.price)

    itemcount = len(bag)
    context = {'x':x,'sum':sum,'user':user, 'bag':bag, 'itemcount':itemcount}
    return render(request , 'app1/ibag.html', context)

def addseller(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'user':user}
    try:
        if request.method == "POST":
            if request.POST.get('name') and request.POST.get('username') and  request.POST.get('email') and  request.POST.get('password'):
                seller = Seller()
                seller.name =  request.POST.get('name')
                seller.username = request.POST.get('username')
                seller.email = request.POST.get('email')

                seller.password = request.POST.get('password')


                seller.save()

                return redirect('seller_login')
            else:
                context = {'user':user, "msg":"Creation of seller account Failed"}
                return render(request , 'app1/add_seller.html', context)

        context = {'user':user , "msg":""}
        return render(request , 'app1/add_seller.html', context)

    except :
        context = {'user':user , "msg":"Account with this username already exists"}
        return render(request , 'app1/add_seller.html', context)


def addclub(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    context = {'user':user}
    try:
        if request.method == "POST":
            if request.POST.get('name') and request.POST.get('password') and  request.POST.get('text') and  request.POST.get('fees_to_enter') and request.FILES['profile_image']:
                seller = Club()
                owner = Customer.objects.get(username = "jinx")
                seller.name =  request.POST.get('name')
                seller.admin = user
                seller.password = request.POST.get('password')
                seller.text = request.POST.get('text')
                seller.profile_image = request.FILES['profile_image']
                seller.fees_to_enter = request.POST.get('fees_to_enter')
                seller.creation_fees = request.POST.get('creation_fees')

                print("clearing if")
                if user == owner:
                    seller.save()
                    seller.members.add(user)
                    print("yes im the owner")
                    return redirect(reverse('chatbox_detail', kwargs={'pk':seller.id}))

                if user.crypto_owned < seller.creation_fees:
                    print("Insufficientfunds")
                    return HttpResponse("Insufficient Balance to create a club")
                else:
                    user.crypto_owned -= seller.creation_fees
                    owner.crypto_owned += seller.creation_fees
                    print("complete funds")
                    seller.save()
                    seller.members.add(user)
                    return redirect(reverse('chatbox_detail', kwargs={'pk':seller.id}))


                return redirect('chatbox')
            else:
                print("Not posted yet")
                context = {'user':user, "msg":"Creation of Club account Failed"}
                return render(request , 'app1/addclub.html', context)

        context = {'user':user , "msg":""}
        return render(request , 'app1/addclub.html', context)

    except Exception as e:
        print(type(e) , e.args , e)
        print("some error occured")
        context = {'user':user , "msg":"Account with this username already exists"}
        return render(request , 'app1/addclub.html', context)





class UpdateOrder(UpdateView):
    model = Order
    fields = "__all__"
    success_url = '/'
    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['posts'] = posts
        return context

def updatecustomer(request,pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    customer = Customer.objects.get(id=pk)
    x = count_posts_of(user)
    context = {'x':x,'user':user, 'customer':customer}

    if request.method == "POST":

        try:
            if request.POST.get('name'):
                customer.name = request.POST.get('name')
        except:
            pass



        try:
            if request.POST.get('contactnumber'):
                customer.phone = request.POST.get('contactnumber')
        except:
            pass

        try:
            if request.POST.get('password'):
                customer.name = request.POST.get('password')
        except:
            pass

        try:
            if request.POST.get('address'):
                customer.address = request.POST.get('address')
        except:
            pass

        try:
            if request.POST.get('desc'):
                customer.desc = request.POST.get('desc')
        except:
            pass

        try:
            if request.FILES['profile_image']:
                print("happening")
                customer.profile_image = request.FILES['profile_image']
        except:
            pass

        try:
            if request.POST.get('crypto_owned'):
                customer.crypto_owned = request.POST.get('crypto_owned')
        except:
            pass

        try:
            if request.POST.get('money_owned'):
                customer.money_owned = request.POST.get('money_owned')
        except:
            pass

        try:
            if request.POST.get('is_admin'):
                customer.is_admin = request.POST.get('is_admin')
        except:
            pass

        try:
            if request.POST.get('is_certified'):
                customer.is_certified = request.POST.get('is_certified')
        except:
            pass
        try:
            if request.POST.get('gender'):
                customer.gender = request.POST.get('gender')
        except:
            pass

        try:
            if request.POST.get('interested'):
                customer.interested = request.POST.get('interested')
        except:
            print("ERror in interested")
            pass

        customer.save()
        print("Success")
        return redirect('customerintro')


    return render(request,'app1/customerupdate.html',context)


def updateseller(request,pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    seller = Seller.objects.get(id=pk)
    context = {'user':user, 'seller':seller}

    if request.method == "POST":

        try:
            if request.POST.get('name'):
                seller.name = request.POST.get('name')
        except:
            pass



        try:
            if request.POST.get('contactnumber'):
                seller.phone = request.POST.get('contactnumber')
        except:
            pass

        try:
            if request.POST.get('password'):
                seller.name = request.POST.get('password')
        except:
            pass

        try:
            if request.POST.get('shop_address'):
                seller.shop_address = request.POST.get('shop_address')
        except:
            pass

        try:
            if request.POST.get('home_address'):
                seller.home_address = request.POST.get('home_address')
        except:
            pass

        try:
            if request.FILES['profile_image']:
                seller.profile_image = request.FILES['profile_image']
                seller.save()
        except:
            pass

        try:
            if request.POST.get('crypto_owned'):
                seller.crypto_owned = request.POST.get('crypto_owned')
        except:
            pass

        try:
            if request.POST.get('money_owned'):
                seller.money_owned = request.POST.get('money_owned')
        except:
            pass

        try:
            if request.POST.get('is_admin'):
                seller.is_admin = request.POST.get('is_admin')
        except:
            pass

        try:
            if request.POST.get('is_certified'):
                seller.is_certified = request.POST.get('is_certified')
        except:
            pass

        seller.save()
        print("Success")
        return redirect('/')


    return render(request,'app1/sellerupdate.html',context)















def customerupdate(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    customer = Customer.objects.get(id=pk)
    uploaded_file_url = 0
    if request.method == "POST":

        try:
            if request.POST.get('name'):
                customer.name = request.POST.get('name')
        except:
            pass

        try:
            if request.POST.get('username'):
                customer.username = request.POST.get('username')
        except:
            pass

        try:
            if request.POST.get('contactnumber'):
                customer.phone = request.POST.get('contactnumber')
        except:
            pass

        try:
            if request.POST.get('password'):
                customer.name = request.POST.get('password')
        except:
            pass

        try:
            if request.POST.get('address'):
                customer.address = request.POST.get('address')
        except:
            pass

        try:
            if request.POST.get('desc'):
                customer.desc = request.POST.get('desc')
        except:
            pass

        try:
            if request.POST.get('gender'):
                customer.gender = request.POST.get('gender')
        except:
            pass
        try:
            if request.POST.get('interested'):
                customer.interested = request.POST.get('interested')
        except:
            pass

        try:

            if request.POST.get('profile_image') :
                print("m")
                customer.profile_image.delete()
                customer.profile_image = request.FILES['profile_image']
                customer.save()
                #customer.profile_image.delete()

                #customer.profile_image = request.FILES['profile_image']

                fs = FileSystemStorage()

                customer.save()

                filename = fs.save(customer.profile_image.name , customer.profile_image)

                uploaded_file_url = fs.url(filename)

            else:
                print("if is not executing")

        except:
            pass

        customer.save()
        print("Success")
        return redirect(reverse('customerintro'))
    x = count_posts_of(user)
    context = {'x':x,'user':user, 'customer':customer , 'uploaded_file_url': uploaded_file_url}

    return render(request,'app1/customerupdate.html',context)





def sellerupdate(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    seller = Seller.objects.get(id=pk)

    uploaded_file_url = 0
    if request.method == "POST":

        try:
            if request.POST.get('name'):
                seller.name = request.POST.get('name')
        except:
            pass

        try:
            if request.POST.get('username'):
                seller.username = request.POST.get('username')
        except:
            pass

        try:
            if request.POST.get('contactnumber'):
                seller.phone = request.POST.get('contactnumber')
        except:
            pass

        try:
            if request.POST.get('password'):
                seller.password = request.POST.get('password')
        except:
            pass

        try:
            if request.POST.get('email'):
                seller.email = request.POST.get('email')
        except:
            pass


        try:
            if request.POST.get('address'):
                seller.home_address = request.POST.get('home_address')
        except:
            pass

        try:
            if request.POST.get('shop_address'):
                seller.shop_address = request.POST.get('shop_address')
        except:
            pass

        try:
            if request.FILES['profile_image']:
                seller.profile_image.delete()
                seller.profile_image = request.FILES['profile_image']
                fs = FileSystemStorage()
                seller.save()
                filename = fs.save(seller.profile_image.name , seller.profile_image)
                uploaded_file_url = fs.url(filename)
        except:
            pass

        seller.save()
        print("Success")
        return redirect(reverse('sellerintro'))
    context = {'user':user, 'seller':seller, 'uploaded_file_url':uploaded_file_url}
    return render(request,'app1/sellerupdate.html',context)












def postupdate(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    post = Post.objects.get(id=pk)
    customer = post.creator
    if request.method == "POST":

        try:
            if request.POST.get('desc'):
                post.desc = request.POST.get('desc')
                post.save()
        except:
            return HttpResponse("Some Error")

        return redirect(reverse('post_detail', kwargs={'pk':post.id}))
    context = {'user':user , 'post':post,'customer':customer}
    return render(request,'app1/postupdate.html',context)







def orderupdate(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    order = Order.objects.get(id=pk)
    seller = order.seller
    if request.method == "POST":

        try:
            if request.POST.get('status'):
                order.status = request.POST.get('status')
                order.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('address'):
                order.address = request.POST.get('address')
                order.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('mode_of_payment'):
                order.mode_of_payment = request.POST.get('mode_of_payment')
                order.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('is_transaction_successfull'):
                order.is_transaction_successfull = request.POST.get('is_transaction_successfull')
                order.save()
        except:
            return HttpResponse("Some Error")

        if user.is_customer:
            return redirect('customerintro')
        elif user.is_seller:
            return redirect('sellerintro')
    x = count_products_of(seller)
    context = {'x':x, 'user':user , 'order':order , 'seller':seller}
    return render(request,'app1/orderupdate.html',context)

def productupdate(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    product = Product.objects.get(id=pk)
    context = {'user':user, 'product':product}
    return render(request,'app1/productupdate.html',context)

def commentupdate(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    comment = Comment.objects.get(id=pk)


    context = {'user':user, 'comment':comment}
    if request.method == "POST":

        try:
            if request.POST.get('text'):
                comment.text = request.POST.get('text')
                comment.save()
        except:
            return HttpResponse("Some Error")

        return redirect(reverse('commentbox', kwargs={'pk':comment.post.id}))
    return render(request,'app1/commentupdate.html',context)



def updateproduct(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    product = Product.objects.get(id=pk)
    seller = product.seller

    context = {'user':user, 'product':product, 'seller':seller}
    if request.method == "POST":

        try:
            if request.POST.get('itemid'):
                product.itemid = request.POST.get('itemid')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('category'):
                product.category = request.POST.get('category')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('colour'):
                product.colour = request.POST.get('colour')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('material'):
                product.material = request.POST.get('material')
                product.save()
        except:
            return HttpResponse("Some Error")


        try:
            if request.POST.get('size'):
                product.size = request.POST.get('size')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('desc'):
                product.desc = request.POST.get('desc')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('price'):
                product.price = request.POST.get('price')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.POST.get('quantity'):
                product.quantity = request.POST.get('quantity')
                product.save()
        except:
            return HttpResponse("Some Error")

        try:
            if request.FILES['profile_image1'] :
                product.profile_image1 = request.FILES['profile_image1']

                product.save()
        except:
            return redirect(reverse('product_detail', kwargs={'pk':product.id}))

        try:
            if request.FILES['profile_image2'] :
                product.profile_image2 = request.FILES['profile_image2']

                product.save()
        except:
            return redirect(reverse('product_detail', kwargs={'pk':product.id}))

        try:
            if request.FILES['profile_image3'] :
                product.profile_image3 = request.FILES['profile_image3']

                product.save()
        except:
            return redirect(reverse('product_detail', kwargs={'pk':product.id}))

        try:
            if request.FILES['profile_image4'] :
                product.profile_image4 = request.FILES['profile_image4']

                product.save()
        except:
            return redirect(reverse('product_detail', kwargs={'pk':product.id}))

        try:
            if request.FILES['profile_image5'] :
                product.profile_image5 = request.FILES['profile_image5']

                product.save()
        except:
            return redirect(reverse('product_detail', kwargs={'pk':product.id}))

        return redirect(reverse('product_detail', kwargs={'pk':product.id}))
    return render(request,'app1/product_form.html',context)



class UpdateProduct(UpdateView):
    model = Product
    fields = "__all__"
    success_url = '/'
    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        try:
            if "c" in list:
                user = Customer.objects.get(id = list[0])
            elif "s" in list:
                user = Seller.objects.get(id = list[0])
            else:
                user=None
        except:
            user = None
        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['posts'] = posts
        return context















def deleteorder(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    order = Order.objects.get(id = pk)
    delcus = False
    delorder=True
    delprod = False
    delpost= False
    delsel = False
    delcom=False
    context = {'delcom':delcom, 'user':user,'item':order , 'delpost':delpost ,'delsel':delsel, 'delcus':delcus , 'delprod':delprod , 'delorder':delorder}
    if request.method == "POST":
        order.delete()
        return redirect('home')
    return render(request , 'app1/delete.html' , context)


def deletecustomer(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    delcus = True
    delorder=False
    delprod = False
    delpost= False
    delcom = False
    delsel = False
    customer = Customer.objects.get(id = pk)
    post = Post.objects.filter(creator = customer)
    order = Order.objects.filter(customer = customer)

    context = {'user':user,'delcom':delcom, 'item':customer ,'delsel':delsel, 'delpost':delpost , 'delcus':delcus , 'delprod':delprod , 'delorder':delorder}
    if request.method == "POST":

        for ipost in post:
            comment = Comment.objects.filter(post = ipost)
            for icomment in comment:
                icomment.delete()
            ipost.delete()
        for iorder in order:
            iorder.delete()

        customer.delete()
        return redirect('home')
    return render(request , 'app1/delete.html' , context)




def deleteseller(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
        user = None
    delcus = False
    delorder=False
    delprod = False
    delpost= False
    delcom = False
    delsel = True
    seller = Seller.objects.get(id = pk)
    product = Product.objects.filter(seller = seller)

    context = {'user':user,'delcom':delcom,'delsel':delsel, 'item':seller , 'delpost':delpost , 'delcus':delcus , 'delprod':delprod , 'delorder':delorder}
    if request.method == "POST":
        for iproduct in product:
            reviews = Review.objects.filter(product = iproduct)
            ratings = Ratings.objects.filter(product = iproduct)
            for review in reviews:
                review.delete()
            for rating in ratings:
                rating.delete()
            iproduct.delete()

        seller.delete()
        return redirect('home')
    return render(request , 'app1/delete.html' , context)





def deleteproduct(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    delcus = False
    delorder=False
    delsel = False
    delprod = True
    delpost= False
    delcom = False
    product = Product.objects.get(id = pk)
    reviews = Review.objects.filter(product = product)
    ratings = Ratings.objects.filter(product = product)
    context = {'user':user,'item':product ,'delcom':delcom,'delsel':delsel, 'delpost':delpost , 'delcus':delcus , 'delprod':delprod , 'delorder':delorder}
    if request.method == "POST":
        for review in reviews:
            review.delete()
        for rating in ratings:
            rating.delete()
        product.delete()
        return redirect('home')
    return render(request , 'app1/delete.html' , context)


def deletepost(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    delcus = False
    delorder=False
    delprod = False
    delpost= True
    delcom = False
    delsel = False
    post = Post.objects.get(id = pk)
    comments = Comment.objects.filter(post=post)
    context = {'user':user,'item':post ,'delsel':delsel, 'delpost':delpost ,'delcom':delcom, 'delcus':delcus , 'delprod':delprod , 'delorder':delorder}
    if request.method == "POST":
        for comment in comments:
            comment.delete()
        post.delete()
        return redirect(reverse('customerintro'))
    return render(request , 'app1/delete.html' , context)


def deletecomment(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    delcus = False
    delsel = False
    delorder=False
    delprod = False
    delpost= False
    delcom = True
    comment = Comment.objects.get(id = pk)
    context = {'delsel':delsel, 'user':user, 'item':comment , 'delpost':delpost , 'delcus':delcus ,'delcom':delcom, 'delprod':delprod , 'delorder':delorder}
    if request.method == "POST":
        comment.delete()
        return redirect(reverse('commentbox', kwargs={'pk':comment.post.id}))
    return render(request , 'app1/delete.html' , context)





















def blockproduct(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    blockpost = False
    blockcomment = False
    blockproduct = True
    blockcustomer = False
    blockorder = False
    blockseller = False
    product = Product.objects.get(id = pk)
    context = {'blockseller':blockseller , 'user':user, 'item':product ,  'blockpost':blockpost, 'blockcomment':blockcomment, 'blockproduct':blockproduct, 'blockcustomer':blockcustomer , 'blockorder':blockorder}

    if request.method == "POST":
        product.blockit()
        product.save()
        return redirect(reverse('product_detail', kwargs={'pk':product.id}))
    return render(request , 'app1/block.html' , context)

def blockcustomer(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    blockpost = False
    blockcomment = False
    blockproduct = False
    blockcustomer = True
    blockorder = False
    blockseller = False
    customer = Customer.objects.get(id = pk)
    context = {'blockseller':blockseller , 'user':user, 'item':customer ,  'blockpost':blockpost, 'blockcomment':blockcomment, 'blockproduct':blockproduct, 'blockcustomer':blockcustomer , 'blockorder':blockorder}

    if request.method == "POST":
        customer.blockit()
        customer.save()
        return redirect(reverse('customer_detail', kwargs={'pk':customer.id}))
    return render(request , 'app1/block.html' , context)



def blockorder(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    blockpost = False
    blockcomment = False
    blockproduct = False
    blockcustomer = False
    blockorder = True
    blockseller = False
    order = Order.objects.get(id = pk)
    context = {'blockseller':blockseller , 'user':user, 'item':order ,  'blockpost':blockpost, 'blockcomment':blockcomment, 'blockproduct':blockproduct, 'blockcustomer':blockcustomer , 'blockorder':blockorder}

    if request.method == "POST":
        order.blockit()
        order.save()
        print("Instead block is called")
        return redirect(reverse('order_detail', kwargs={'pk':order.id}))
    return render(request , 'app1/block.html' , context)



def blockpost(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    blockpost = True
    blockcomment = False
    blockproduct = False
    blockcustomer = False
    blockorder = False
    blockseller = False
    post = Post.objects.get(id = pk)
    context = {'blockseller':blockseller , 'user':user, 'item':post ,  'blockpost':blockpost, 'blockcomment':blockcomment, 'blockproduct':blockproduct, 'blockcustomer':blockcustomer , 'blockorder':blockorder}

    if request.method == "POST":
        post.blockit()
        post.save()
        return redirect(reverse('post_detail', kwargs={'pk':post.id}))
    return render(request , 'app1/block.html' , context)


def blockcomment(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None


    blockpost = False
    blockcomment = True
    blockproduct = False
    blockcustomer = False
    blockorder = False
    blockseller = False

    comment = Comment.objects.get(id = pk)
    context = {'blockseller':blockseller , 'user':user, 'item':comment ,  'blockpost':blockpost, 'blockcomment':blockcomment, 'blockproduct':blockproduct, 'blockcustomer':blockcustomer , 'blockorder':blockorder}

    if request.method == "POST":
        comment.blockit()
        comment.save()
        return redirect(reverse('commentbox', kwargs={'pk':comment.post.id}))
    return render(request , 'app1/block.html' , context)


def blockseller(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    blockpost = False
    blockcomment = False
    blockproduct = False
    blockcustomer = False
    blockorder = False
    blockseller = True
    seller = Seller.objects.get(id = pk)

    if request.method == "POST":
        seller.blockit()
        seller.save()
        return redirect(reverse('seller_detail', kwargs={'pk':seller.id}))

    context = {'item':seller, 'blockseller':blockseller , 'user':user ,  'blockpost':blockpost, 'blockcomment':blockcomment, 'blockproduct':blockproduct, 'blockcustomer':blockcustomer , 'blockorder':blockorder}

    return render(request , 'app1/block.html',context)








def unblockproduct(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    unblockpost = False
    unblockcomment = False
    unblockproduct = True
    unblockcustomer = False
    unblockorder = False
    unblockseller = False
    product = Product.objects.get(id = pk)
    context = { 'unblockseller':unblockseller ,  'user':user,'item':product, 'unblockpost':unblockpost, 'unblockcomment':unblockcomment, 'unblockproduct':unblockproduct, 'unblockcustomer':unblockcustomer , 'unblockorder':unblockorder}

    if request.method == "POST":
        product.unblockit()
        product.save()
        return redirect(reverse('product_detail', kwargs={'pk':product.id}))
    return render(request , 'app1/unblock.html' , context)

def unblockcustomer(request, pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    unblockpost = False
    unblockcomment = False
    unblockproduct = False
    unblockcustomer = True
    unblockorder = False
    unblockseller = False
    customer = Customer.objects.get(id = pk)
    if request.method == "POST":
        if customer.is_block == True:
            customer.unblockit()
            customer.save()
            return redirect(reverse('customer_detail', kwargs={'pk':customer.id}))
    context = { 'unblockseller':unblockseller ,  'user':user,'item':customer, 'unblockpost':unblockpost, 'unblockcomment':unblockcomment, 'unblockproduct':unblockproduct, 'unblockcustomer':unblockcustomer , 'unblockorder':unblockorder}

    return render(request , 'app1/unblock.html' , context)


def unblockorder(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    unblockpost = False
    unblockcomment = False
    unblockproduct = False
    unblockcustomer = False
    unblockorder = True
    unblockseller = False
    order = Order.objects.get(id = pk)
    context = { 'unblockseller':unblockseller ,  'user':user,'item':order, 'unblockpost':unblockpost, 'unblockcomment':unblockcomment, 'unblockproduct':unblockproduct, 'unblockcustomer':unblockcustomer , 'unblockorder':unblockorder}
    if request.method == "POST":
        if order.is_block == True:
            order.unblockit()
            order.save()
            return redirect(reverse('order_detail', kwargs={'pk':order.id}))

    return render(request , 'app1/unblock.html' , context)






def unblockpost(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    unblockpost = True
    unblockcomment = False
    unblockproduct = False
    unblockcustomer = False
    unblockorder = False
    unblockseller = False
    post = Post.objects.get(id = pk)
    context = { 'unblockseller':unblockseller ,  'user':user,'item':post, 'unblockpost':unblockpost, 'unblockcomment':unblockcomment, 'unblockproduct':unblockproduct, 'unblockcustomer':unblockcustomer , 'unblockorder':unblockorder}
    if request.method == "POST":
        if post.is_block == True:
            post.unblockit()
            post.save()
            return redirect(reverse('post_detail', kwargs={'pk':post.id}))

    return render(request , 'app1/unblock.html' , context)





def unblockcomment(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    unblockpost = False
    unblockcomment = True
    unblockproduct = False
    unblockcustomer = False
    unblockorder = False
    unblockseller = False
    comment = Comment.objects.get(id = pk)
    context = { 'unblockseller':unblockseller ,  'user':user, 'item':comment, 'unblockpost':unblockpost, 'unblockcomment':unblockcomment, 'unblockproduct':unblockproduct, 'unblockcustomer':unblockcustomer , 'unblockorder':unblockorder}
    if request.method == "POST":
        if comment.is_block == True:
            comment.unblockit()
            comment.save()

            return redirect(reverse('commentbox', kwargs={'pk':comment.post.id}))

    return render(request , 'app1/unblock.html' , context)


def unblockseller(request,pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    unblockpost = False
    unblockcomment = False
    unblockproduct = False
    unblockcustomer = False
    unblockorder = False
    unblockseller = True
    seller = Seller.objects.get(id = pk)
    context = { 'unblockseller':unblockseller ,  'user':user, 'item':seller, 'unblockpost':unblockpost, 'unblockcomment':unblockcomment, 'unblockproduct':unblockproduct, 'unblockcustomer':unblockcustomer , 'unblockorder':unblockorder}
    if request.method == "POST":
        if seller.is_block == True:
            seller.unblockit()
            seller.save()

            return redirect(reverse('seller_detail', kwargs={'pk':seller.id}))
    return render(request,'app1/unblock.html',context)
























def postlist(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    posts = Post.objects.all().order_by( '-date_created')
    context = {'user':user , 'posts':posts}
    return render(request , "app1/postlist.html" ,context )


def postdetail(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    post = Post.objects.get(id = pk)
    tag1 = Lvl1tags.objects.filter(post1 = post)
    tag2 = Lvl2tags.objects.filter(post2 = post)
    tag3 = Lvl3tags.objects.filter(post3 = post)
    tag4 = Lvl4tags.objects.filter(post4 = post)
    tag5 = Lvl5tags.objects.filter(post5 = post)
    lvl1button = False
    lvl2button = False
    lvl3button = False
    lvl4button = False
    lvl5button = False
    showall = False
    if post.creator == user:
        if len(tag1)>=1:
            showall = True
        else:
            lvl1button = True
    else:
        for object in tag1:
            if user in object.connections1.all():
                l = []
                for item in tag2:
                    if item.parent2 == user:
                        l.append(user)
                    else:
                        continue

                if len(l)==0:
                    lvl2button = True
                else:
                    showall = True
                break

            else:
                continue


        for object in tag2:
            if user in object.connections2.all():
                l = []
                for item in tag3:
                    if item.parent3 == user:
                        l.append(user)
                    else:
                        continue

                if len(l)==0:
                    lvl3button = True
                else:
                    showall = True
                break

            else:
                continue


        for object in tag3:
            if user in object.connections3.all():
                l = []
                for item in tag4:
                    if item.parent4 == user:
                        l.append(user)
                    else:
                        continue

                if len(l)==0:
                    lvl4button = True
                else:
                    showall = True
                break

            else:
                continue


        for object in tag4:
            if user in object.connections4.all():
                l = []
                for item in tag5:
                    if item.parent5 == user:
                        l.append(user)
                    else:
                        continue

                if len(l)==0:
                    lvl5button = True
                else:
                    showall = True
                break

            else:
                continue


    reach = 1

    for object in tag1:
        reach = reach+ object.connections1.count()

    for object in tag2:
        reach = reach+ object.connections2.count()

    for object in tag3:
        reach = reach+ object.connections3.count()

    for object in tag4:
        reach = reach+ object.connections4.count()

    for object in tag5:
        reach = reach+ object.connections5.count()

    if user not in post.likers.all():
        if request.method == "POST":

            post.likers.add(user)
            post.save()
    else:
        if request.method == "POST":

            post.likers.remove(user)
            post.save()
    comments =  Comment.objects.filter(post=post)
    number_of_comments = len(comments)
    context = {'reach':reach, 'lvl1button':lvl1button,'lvl2button':lvl2button,'lvl3button':lvl3button,'lvl4button':lvl4button,'lvl5button':lvl5button,'showall':showall,'user':user , 'post':post , 'number_of_comments':number_of_comments,'tag1':tag1,'tag2':tag2,'tag3':tag3,'tag4':tag4,'tag5':tag5,}
    return render(request , "app1/postdetail.html" ,context )





def tag1(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    post = Post.objects.get(id = pk)
    bank = Customer.objects.get(username = 'vincorpbank')
    fees = 0

    customer_list = Customer.objects.all().order_by("username")

    if request.method == "POST":
        print("kdmsck" , request.POST.get('p1'))
        r = False

        try:
            p1 = Customer.objects.get(username = request.POST.get('p1'))

        except:
            return HttpResponse("Input Correct  username for First Field")

        try:
            p2 = Customer.objects.get(username = request.POST.get('p2'))

        except:
            return HttpResponse("Input Correct  username for Second Field")

        try:
            p3 = Customer.objects.get(username = request.POST.get('p3'))

        except:
            return HttpResponse("Input Correct  username for Third Field")

        try:
            p4 = Customer.objects.get(username = request.POST.get('p4'))

        except:
            return HttpResponse("Input Correct  username for Fourth Field")

        try:
            p5 = Customer.objects.get(username = request.POST.get('p5'))

        except:
            return HttpResponse("Input Correct  username for Fifth Field")
        l = [p1,p2,p3,p4,p5]
        tag1 = Lvl1tags.objects.filter(post1 = post)
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                else:
                    if l[i] == l[j]:
                        r = True
                        break
        s = False
        a = 0
        for tag in tag1:
            for person in l:
                a = a+1
                if person in tag.connections1.all():
                    s = True
                    break


        if r == True :
            return HttpResponse("You cannot tag 2 accounts with same username")

        elif s == True:
            return HttpResponse("Account at position {} is already tagged".format(a))
        else:

            if user.crypto_owned < fees:
                return HttpResponse("Insufficient Balance to add tags, Pls add more VNITS ")
            else:
                t = Lvl1tags()
                t.post1 = post
                t.parent1 = post.creator
                t.text = "{}{}{}".format(post.desc , user.username , user.crypto_owned)
                t.save()
                t.connections1.add(p1)
                t.connections1.add(p2)
                t.connections1.add(p3)
                t.connections1.add(p4)
                t.connections1.add(p5)

                user.crypto_owned -= fees
                bank.crypto_owned += fees
                t.save()
                user.save()
                post.save()
                bank.save()
                return redirect('customerintro')
    context = {'user':user,'bank':bank,'customer_list':customer_list}
    return render(request , 'app1/tag1.html' , context)








def tag2(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    post = Post.objects.get(id = pk)
    bank = Customer.objects.get(username = 'vincorpbank')

    fees = 0
    customer_list = Customer.objects.all()
    if request.method == "POST":



        try:
            p1 = Customer.objects.get(username = request.POST.get('p1'))

        except:
            return HttpResponse("Input Correct  username for First Field")

        try:
            p2 = Customer.objects.get(username = request.POST.get('p2'))

        except:
            return HttpResponse("Input Correct  username for Second Field")

        try:
            p3 = Customer.objects.get(username = request.POST.get('p3'))

        except:
            return HttpResponse("Input Correct  username for Third Field")

        try:
            p4 = Customer.objects.get(username = request.POST.get('p4'))

        except:
            return HttpResponse("Input Correct  username for Fourth Field")

        try:
            p5 = Customer.objects.get(username = request.POST.get('p5'))

        except:
            return HttpResponse("Input Correct  username for Fifth Field")
        l = [p1,p2,p3,p4,p5]
        tag1 = Lvl1tags.objects.filter(post1 = post)
        tag2 = Lvl2tags.objects.filter(post2 = post)
        r = False
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                else:
                    if l[i] == l[j]:
                        r = True
                        break
        a = 0
        s = False
        for tag in tag1:
            for person in l:
                a +=1
                try:
                    if person in tag.connections1.all():
                        s = True
                        break
                except Exception as e :
                    print("2 ",e)
                    continue
        a = 0
        v = False
        for tag in tag2:

            for person in l:
                a+=1
                try:
                    if person in tag.connections2.all():
                        v = True
                        break
                except Exception as e:

                    print("1 ",e)
                    continue

        print("r,s,v" , r,s,v)

        if r == True :
            return HttpResponse("You cannot tag 2 accounts with same username")

        elif s or v:
            return HttpResponse("Account at position {} is already tagged".format(a))
        else:
            if user.crypto_owned == None:
                user.crypto_owned = 0
                user.save()
            if user.crypto_owned < fees:
                return HttpResponse("Insufficient Balance to add tags, Pls add more VNITS ")
            else:
                t = Lvl2tags()
                t.post2 = post
                t.parent2 = user
                t.text = "{}{}{}".format(post.desc , user.username , user.crypto_owned)
                t.save()
                t.connections2.add(p1)
                t.connections2.add(p2)
                t.connections2.add(p3)
                t.connections2.add(p4)
                t.connections2.add(p5)

                user.crypto_owned += 0.1 * fees
                bank.crypto_owned -= 0.1 * fees
                t.save()
                user.save()
                post.save()
                bank.save()
                return redirect('customerintro')
    context = {'user':user,'bank':bank,'customer_list':customer_list}
    return render(request , 'app1/tag1.html' , context)














def tag3(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    post = Post.objects.get(id = pk)
    bank = Customer.objects.get(username = 'vincorpbank')

    fees = 0
    customer_list = Customer.objects.all()
    if request.method == "POST":



        try:
            p1 = Customer.objects.get(username = request.POST.get('p1'))

        except:
            return HttpResponse("Input Correct  username for First Field")

        try:
            p2 = Customer.objects.get(username = request.POST.get('p2'))

        except:
            return HttpResponse("Input Correct  username for Second Field")

        try:
            p3 = Customer.objects.get(username = request.POST.get('p3'))

        except:
            return HttpResponse("Input Correct  username for Third Field")

        try:
            p4 = Customer.objects.get(username = request.POST.get('p4'))

        except:
            return HttpResponse("Input Correct  username for Fourth Field")

        try:
            p5 = Customer.objects.get(username = request.POST.get('p5'))

        except:
            return HttpResponse("Input Correct  username for Fifth Field")
        l = [p1,p2,p3,p4,p5]
        tag1 = Lvl1tags.objects.filter(post1 = post)
        tag2 = Lvl2tags.objects.filter(post2 = post)
        tag3 = Lvl3tags.objects.filter(post3 = post)
        r = False
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                else:
                    if l[i] == l[j]:
                        r = True
                        break
        a = 0
        s = False
        for tag in tag1:
            for person in l:
                a+=1
                try:
                    if person in tag.connections1.all():
                        s = True
                        break
                except Exception as e :
                    print("2 ",e)
                    continue
        a = 0
        v = False
        for tag in tag2:
            for person in l:
                a+=1
                try:
                    if person in tag.connections2.all():
                        v = True
                        break
                except Exception as e:

                    print("1 ",e)
                    continue
        a=0
        w = False
        for tag in tag3:
            for person in l:
                a+=1
                try:
                    if person in tag.connections3.all():
                        w = True
                        break
                except Exception as e:

                    print("3 ",e)
                    continue


        print("r,s,v,w" , r,s,v,w)

        if r == True :
            return HttpResponse("You cannot tag 2 accounts with same username")

        elif s or v or w:
            return HttpResponse("Account at position {} is already tagged".format(a))
        else:
            if user.crypto_owned == None:
                user.crypto_owned = 0

            if user.crypto_owned < fees:
                return HttpResponse("Insufficient Balance to add tags, Pls add more VNITS ")
            else:
                t = Lvl3tags()
                t.post3 = post
                t.parent3 = user
                t.text = "{}{}{}".format(post.desc , user.username , user.crypto_owned)
                t.save()
                t.connections3.add(p1)
                t.connections3.add(p2)
                t.connections3.add(p3)
                t.connections3.add(p4)
                t.connections3.add(p5)

                user.crypto_owned += 0.01 * fees
                bank.crypto_owned -= 0.01 * fees
                t.save()
                user.save()
                post.save()
                bank.save()
                return redirect('customerintro')
    context = {'user':user,'bank':bank,'customer_list':customer_list}
    return render(request , 'app1/tag1.html' , context)






def tag4(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    post = Post.objects.get(id = pk)
    bank = Customer.objects.get(username = 'vincorpbank')

    fees = 0
    customer_list = Customer.objects.all()
    if request.method == "POST":



        try:
            p1 = Customer.objects.get(username = request.POST.get('p1'))

        except:
            return HttpResponse("Input Correct  username for First Field")

        try:
            p2 = Customer.objects.get(username = request.POST.get('p2'))

        except:
            return HttpResponse("Input Correct  username for Second Field")

        try:
            p3 = Customer.objects.get(username = request.POST.get('p3'))

        except:
            return HttpResponse("Input Correct  username for Third Field")

        try:
            p4 = Customer.objects.get(username = request.POST.get('p4'))

        except:
            return HttpResponse("Input Correct  username for Fourth Field")

        try:
            p5 = Customer.objects.get(username = request.POST.get('p5'))

        except:
            return HttpResponse("Input Correct  username for Fifth Field")
        l = [p1,p2,p3,p4,p5]
        tag1 = Lvl1tags.objects.filter(post1 = post)
        tag2 = Lvl2tags.objects.filter(post2 = post)
        tag3 = Lvl3tags.objects.filter(post3 = post)
        tag4 = Lvl4tags.objects.filter(post4= post)
        r = False
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                else:
                    if l[i] == l[j]:
                        r = True
                        break
        a = 0
        s = False
        for tag in tag1:
            for person in l:
                a+=1
                try:
                    if person in tag.connections1.all():
                        s = True
                        break
                except Exception as e :
                    print("2 ",e)
                    continue
        a = 0
        v = False
        for tag in tag2:
            for person in l:
                a+=1
                try:
                    if person in tag.connections2.all():
                        v = True
                        break
                except Exception as e:

                    print("1 ",e)
                    continue
        a = 0
        w = False
        for tag in tag3:
            for person in l:
                a+=1
                try:
                    if person in tag.connections3.all():
                        w = True
                        break
                except Exception as e:

                    print("3 ",e)
                    continue


        a = 0

        f = False
        for tag in tag4:
            for person in l:
                a+=1
                try:
                    if person in tag.connections4.all():
                        s = True
                        break
                except Exception as e :
                    print("4 ",e)
                    continue



        print("r,s,v,w,f" , r,s,v,w,f)

        if r == True :
            return HttpResponse("You cannot tag 2 accounts with same username")

        elif s or v or w or f :
            return HttpResponse("Account at position {} is already tagged".format(a))
        else:
            if user.crypto_owned == None :
                user.crypto_owned = 0
            if user.crypto_owned < fees:
                return HttpResponse("Insufficient Balance to add tags, Pls add more VNITS ")
            else:
                t = Lvl4tags()
                t.post4 = post
                t.parent4 = user
                t.text = "{}{}{}".format(post.desc , user.username , user.crypto_owned)
                t.save()
                t.connections4.add(p1)
                t.connections4.add(p2)
                t.connections4.add(p3)
                t.connections4.add(p4)
                t.connections4.add(p5)

                user.crypto_owned += 0.001 * fees
                bank.crypto_owned -= 0.001 * fees
                t.save()
                user.save()
                post.save()
                bank.save()
                return redirect('customerintro')
    context = {'user':user,'bank':bank,'customer_list':customer_list}
    return render(request , 'app1/tag1.html' , context)



def tag5(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    post = Post.objects.get(id = pk)
    bank = Customer.objects.get(username = 'vincorpbank')

    fees = 0
    customer_list = Customer.objects.all()
    if request.method == "POST":



        try:
            p1 = Customer.objects.get(username = request.POST.get('p1'))

        except:
            return HttpResponse("Input Correct  username for First Field")

        try:
            p2 = Customer.objects.get(username = request.POST.get('p2'))

        except:
            return HttpResponse("Input Correct  username for Second Field")

        try:
            p3 = Customer.objects.get(username = request.POST.get('p3'))

        except:
            return HttpResponse("Input Correct  username for Third Field")

        try:
            p4 = Customer.objects.get(username = request.POST.get('p4'))

        except:
            return HttpResponse("Input Correct  username for Fourth Field")

        try:
            p5 = Customer.objects.get(username = request.POST.get('p5'))

        except:
            return HttpResponse("Input Correct  username for Fifth Field")
        l = [p1,p2,p3,p4,p5]
        tag1 = Lvl1tags.objects.filter(post1 = post)
        tag2 = Lvl2tags.objects.filter(post2 = post)
        tag3 = Lvl3tags.objects.filter(post3 = post)
        tag4 = Lvl4tags.objects.filter(post4= post)
        tag5 = Lvl5tags.objects.filter(post5= post)

        r = False
        for i in range(5):
            for j in range(5):
                if i == j:
                    continue
                else:
                    if l[i] == l[j]:
                        r = True
                        break
        a = 0
        s = False
        for tag in tag1:
            for person in l:
                a+=1
                try:
                    if person in tag.connections1.all():
                        s = True
                        break
                except Exception as e :
                    print("2 ",e)
                    continue
        a = 0
        v = False
        for tag in tag2:
            for person in l:
                a+=1
                try:
                    if person in tag.connections2.all():
                        v = True
                        break
                except Exception as e:

                    print("1 ",e)
                    continue
        a=0
        w = False
        for tag in tag3:
            for person in l:
                a+=1
                try:
                    if person in tag.connections3.all():
                        w = True
                        break
                except Exception as e:

                    print("3 ",e)
                    continue


        a=0
        f = False
        for tag in tag4:
            for person in l:
                a+=1
                try:
                    if person in tag.connections4.all():
                        s = True
                        break
                except Exception as e :
                    print("4 ",e)
                    continue

        a = 0
        g = False
        for tag in tag5:
            for person in l:
                a+=1
                try:
                    if person in tag.connections5.all():
                        g = True
                        break
                except Exception as e :
                    print("5 ",e)
                    continue



        print("r,s,v,w,f,g" , r,s,v,w,f,g)

        if r == True :
            return HttpResponse("You cannot tag 2 accounts with same username")

        elif s or v or w or f or g :
            return HttpResponse("Account at position {} is already tagged".format(a))
        else:
            if user.crypto_owned == None:
                user.crypto_owned = 0
            if user.crypto_owned < fees:
                return HttpResponse("Insufficient Balance to add tags, Pls add more VNITS ")
            else:
                t = Lvl5tags()
                t.post5 = post
                t.parent5 = user
                t.text = "{}{}{}".format(post.desc , user.username , user.crypto_owned)
                t.save()
                t.connections5.add(p1)
                t.connections5.add(p2)
                t.connections5.add(p3)
                t.connections5.add(p4)
                t.connections5.add(p5)

                user.crypto_owned += 0.0001 * fees
                bank.crypto_owned -= 0.0001 * fees
                t.save()
                user.save()
                post.save()
                bank.save()
                return redirect('customerintro')
    context = {'user':user,'bank':bank,'customer_list':customer_list}
    return render(request , 'app1/tag1.html' , context)



def tagrequests(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    requests = Followrequest.objects.filter(experiencer = user , acceptance_status = False)
    posts = Post.objects.all()
    t1 = []
    tag1 = Lvl1tags.objects.all()
    tag2 = Lvl2tags.objects.all()
    tag3 = Lvl3tags.objects.all()
    tag4 = Lvl4tags.objects.all()
    tag5 = Lvl5tags.objects.all()

    i = []
    for tag in tag1:
        if user in tag.connections1.all():
            show1 = True
            for atag in tag2:
                if user == atag.parent2 and atag.post2 == tag.post1:
                    show1 = False
                    break

            if show1 == True:
                i.append(tag)

    j = []
    for tag in tag2:
        if user in tag.connections2.all():
            show1 = True
            for atag in tag3:
                if user == atag.parent3 and atag.post3 == tag.post2:
                    show1 = False
                    break

            if show1 == True:
                j.append(tag)

    k = []
    for tag in tag3:
        if user in tag.connections3.all():
            show1 = True
            for atag in tag4:
                if user == atag.parent4 and atag.post4 == tag.post3:
                    show1 = False
                    break

            if show1 == True:
                k.append(tag)

    l = []
    for tag in tag4:
        if user in tag.connections4.all():
            show1 = True
            for atag in tag5:
                if user == atag.parent5 and atag.post5 == tag.post4:
                    show1 = False
                    break

            if show1 == True:
                l.append(tag)

    if request.method == "POST" and "decline" in request.POST:
        a = request.POST.get('identity')
        req = Followrequest.objects.get(identity = a)
        req.delete()

    if request.method == "POST" and "accept" in request.POST:
        a = request.POST.get('identity')
        req = Followrequest.objects.get(identity = a)

        user.followers.add(req.provider)
        req.provider.followings.add(user)
        user.save()
        req.provider.save()
        req.delete()
    context = {'requests': requests, 'l': l,'i':i , 'j' :j , 'k' : k ,'user':user , 'tag1':tag1, 'tag2':tag2, 'tag3':tag3, 'tag4':tag4, 'tag5':tag5}
    return render(request , 'app1/tagrequests.html' , context)



def listfeed(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    y = []
    if user == None:
        return redirect('/')
    else:

        #Story.objects.filter(created_date__lt=Now()-timespan(days=1)).delete()
        story_list = []
        for following in user.followings.all():
            story_items_per_user = Story.objects.filter(composer = following)
            if len(story_items_per_user) != 0:
                story_list.append(story_items_per_user)
        print("storylist" , story_list)
        posts = Post.objects.all().order_by('-date_created')
        #y.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))
        comments = Comment.objects.all()
        if request.method == "POST":
            x = request.POST.get('id')
            posh = Post.objects.get(id = x)
            if user in posh.likers.all():
                posh.likers.remove(user)
                posh.save()
            elif user not in posh.likers.all():
                posh.likers.add(user)
                posh.save()
        tag1 = Lvl1tags.objects.all()
        tag2 = Lvl2tags.objects.all()
        tag3 = Lvl3tags.objects.all()
        tag4 = Lvl4tags.objects.all()
        tag5 = Lvl5tags.objects.all()
        c = set()
        b = []
        a = []
        d = set()
        e = set()

        for post in posts:
            if post.creator in user.followings.all() or post.creator == user or user.is_admin and post.is_block == False and post not in c:
                c.add(post)

        for tag in tag1:
            if tag.post1 not in b:
                a.append(tag)
                b.append(tag.post1)

        for tag in tag2:
            if tag.post2 not in b:
                b.append(tag.post2)
                a.append(tag)
        for tag in tag3:
            if tag.post3 not in b:
                b.append(tag.post3)
                a.append(tag)
        for tag in tag4:
            if tag.post4 not in b:
                b.append(tag.post4)
                a.append(tag)
        for tag in tag5:
            if tag.post5 not in b:
                b.append(tag.post5)
                a.append(tag)

        for tag in a:
            try:
                for connection in tag.connections1.all():
                    if user in connection.followers.all():
                        d.add(tag.post1)
            except:
                continue

            try:
                for connection in tag.connections2.all():
                    if user in connection.followers.all():
                        d.add(tag.post2)
            except:
                continue

            try:
                for connection in tag.connections3.all():
                    if user in connection.followers.all():
                        d.add(tag.post3)
            except:
                continue

            try:
                for connection in tag.connections4.all():
                    if user in connection.followers.all():
                        d.add(tag.post4)
            except:
                continue

            try:
                for connection in tag.connections5.all():
                    if user in connection.followers.all():
                        d.add(tag.post5)
            except:
                continue

        c.update(d)
        for item in c:
            if item != None:
                e.add(item)

        f = []
        for item in e:
            f.append(item)


        f = f[::-1]


    print("c is:" ,c)
    print(" element in cis" , len(c))
    customer_list = Customer.objects.all()
    context = {'customer_list':customer_list,'story_list':story_list,'f':f,'user':user, 'posts':posts,'comments':comments }
    return render(request , 'app1/listfeed.html', context)


def feedlist(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    y = []
    if user == None:
        return redirect('/')
    else:
        posts = Post.objects.all().order_by('-date_created')
        #y.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))
        comments = Comment.objects.all()
        if request.method == "POST":
            x = request.POST.get('id')
            posh = Post.objects.get(id = x)
            if user in posh.likers.all():
                posh.likers.remove(user)
                posh.save()
            elif user not in posh.likers.all():
                posh.likers.add(user)
                posh.save()
        tag1 = Lvl1tags.objects.all()
        tag2 = Lvl2tags.objects.all()
        tag3 = Lvl3tags.objects.all()
        tag4 = Lvl4tags.objects.all()
        tag5 = Lvl5tags.objects.all()
    context = {'tag1':tag1,'tag2':tag2,'tag3':tag3,'tag4':tag4,'tag5':tag5,'user':user, 'posts':posts,'comments':comments }
    return render(request , 'app1/feedlist.html', context)






def transfer(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    msg = ""
    if user == None:
        return redirect('/')
    else:
        customer = Customer.objects.get(id = pk)
        if request.method == "POST":
            x = request.POST.get('units')
            if x == None:
                x = 0
            y = request.POST.get('security')
            if user.security == None:
                user.security = "abczxy"
                user.save()

            if user.crypto_owned >= int(x) and int(x)>0  and ( y == user.security or user.security == None) :
                transfer = Transfer()
                transfer.giver = user
                transfer.taker = customer
                transfer.units = float(request.POST.get('units'))
                transfer.save()
                user.crypto_owned = user.crypto_owned - transfer.units
                customer.crypto_owned = customer.crypto_owned + transfer.units
                user.save()
                customer.save()

                msg = "Transfer Successful. Please do not refresh/reloador go back."
                context = {'user':user , 'customer':customer, 'msg':msg }
                return render(request , 'app1/transfer.html' , context)
            else:
                if int(x)<0 :
                    msg = "Please Enter a valid number of units to transfer. *Only Positive Integer values are acceptable"
                    context = {'user':user , 'customer':customer, 'msg':msg }
                    return render(request , 'app1/transfer.html' , context)

                elif y!= user.security:
                    msg = "Enter correct security password"
                    context = {'user':user , 'customer':customer, 'msg':msg }
                    return render(request , 'app1/transfer.html' , context)
                else:
                    msg = "Insufficient Balance. * Go to your profile > Add Funds."
                    context = {'user':user , 'customer':customer, 'msg':msg }
                    return render(request , 'app1/transfer.html' , context)
    context = {'user':user , 'customer':customer , 'msg':msg}
    return render(request , 'app1/transfer.html' , context)



def pay(request , pk):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None
    msg=""
    if user == None:
        return redirect('/')
    else:
        seller = Seller.objects.get(id = pk)
        if request.method == "POST":
            x= request.POST.get('units')
            if x == None:
                x = 0
            y = request.POST.get('security')
            if user.security == None:
                user.security = "abczxy"
                user.save()
            if user.crypto_owned >= int(x) and int(x)>0  and ( y == user.security or user.security == None) :
                pay = Pay()
                pay.payer = user
                pay.keeper = seller
                pay.units = float(request.POST.get('units'))
                pay.save()
                user.crypto_owned = user.crypto_owned - pay.units
                seller.crypto_owned = seller.crypto_owned + pay.units
                user.save()
                seller.save()

                msg = "Transfer Successful. Please do not refresh/reloador go back."
                context = {'user':user , 'seller':seller, 'msg':msg }
                return render(request , 'app1/pay.html' , context)

            else:
                if int(x)<0 :
                    msg = "Please Enter a valid number of units to transfer. *Only Positive Integer values are acceptable"
                    context = {'user':user , 'seller':seller, 'msg':msg }
                    return render(request , 'app1/pay.html' , context)

                elif y!= user.security:
                    msg = "Enter correct security password"
                    context = {'user':user , 'seller':seller, 'msg':msg }
                    return render(request , 'app1/pay.html' , context)
                else:
                    msg = "Insufficient Balance. * Go to your profile > Add Funds."
                    context = {'user':user , 'seller':seller, 'msg':msg }
                    return render(request , 'app1/pay.html' , context)
    context = {'user':user , 'seller':seller, 'msg':msg}
    return render(request , 'app1/pay.html' , context)





def message(request):
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:

        context = {'message':"Transfer completed" , 'user':user}
        return render(request,'app1/message.html' , context)




def crushlist(request):
    msg = ""
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:

        context = {'msg':msg , 'user':user}
        return render(request,'app1/crushlist.html' , context)






def private(request):
    msg = ""
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:

        context = {'msg':msg , 'user':user}
        if request.method == "POST":
            user.makeprivate()
            user.save()
            return redirect(reverse('customerintro'))
        context = {'msg':msg , 'user':user}
        return render(request,'app1/private.html' , context)



def public(request):
    msg = ""
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:

        if request.method == "POST":
            if user.is_private:
                user.makepublic()
                user.save()
                return redirect(reverse('customerintro'))

        context = {'msg':msg , 'user':user}
        return render(request,'app1/public.html' , context)



def clubupdate(request , pk):
    msg = ""
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        customer = Club.objects.get(id=pk)
        uploaded_file_url = 0
        if request.method == "POST":

            try:
                if request.POST.get('password'):
                    customer.password = request.POST.get('password')
            except:
                pass



            try:
                if request.POST.get('text'):
                    customer.text = request.POST.get('text')
            except:
                pass

            try:
                if request.POST.get('fees_to_enter'):
                    customer.fees_to_enter = request.POST.get('fees_to_enter')
            except:
                pass
            try:
                if request.POST.get('is_private'):
                    customer.is_private = request.POST.get('is_private')
            except:
                pass

            try:

                if request.FILES['cover_image'] :
                    print("m")
                    customer.cover_image.delete()
                    customer.cover_image = request.FILES['cover_image']
                    customer.save()
                    #customer.profile_image.delete()

                    #customer.profile_image = request.FILES['profile_image']

                    fs = FileSystemStorage()

                    customer.save()

                    filename = fs.save(customer.cover_image.name , customer.cover_image)

                    uploaded_file_url = fs.url(filename)

                else:
                    print("if is not executing")

            except:
                pass

            try:

                if request.FILES['profile_image'] :
                    print("m")
                    customer.profile_image.delete()
                    customer.profile_image = request.FILES['profile_image']
                    customer.save()
                    #customer.profile_image.delete()

                    #customer.profile_image = request.FILES['profile_image']

                    fs = FileSystemStorage()

                    customer.save()

                    filename = fs.save(customer.profile_image.name , customer.profile_image)

                    uploaded_file_url = fs.url(filename)

                else:
                    print("if is not executing")

            except:
                pass

            customer.save()
            if customer.is_private == False:
                customer.fees_to_enter = 0
                customer.save()

            print("Success")
            return redirect(reverse('chatbox_detail', kwargs={'pk':customer.id}))
        x = count_posts_of(user)
        context = {'x':x,'user':user, 'customer':customer, 'club':customer , 'uploaded_file_url': uploaded_file_url}

        return render(request,'app1/clubupdate.html',context)


def clubeditmember(request , pk):
    msg = ""
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        customer = Club.objects.get(id=pk)
        uploaded_file_url = 0
        if request.method == "POST":

            try:
                if request.POST.get('password'):
                    customer.password = request.POST.get('password')
            except:
                pass



            try:
                if request.POST.get('text'):
                    customer.text = request.POST.get('text')
            except:
                pass

            try:
                if request.POST.get('fees_to_enter'):
                    customer.fees_to_enter = request.POST.get('fees_to_enter')
            except:
                pass
            try:
                if request.POST.get('is_private'):
                    customer.is_private = request.POST.get('is_private')
            except:
                pass

            try:

                if request.FILES['cover_image'] :
                    print("m")
                    customer.cover_image.delete()
                    customer.cover_image = request.FILES['cover_image']
                    customer.save()
                    #customer.profile_image.delete()

                    #customer.profile_image = request.FILES['profile_image']

                    fs = FileSystemStorage()

                    customer.save()

                    filename = fs.save(customer.cover_image.name , customer.cover_image)

                    uploaded_file_url = fs.url(filename)

                else:
                    print("if is not executing")

            except:
                pass

            try:

                if request.FILES['profile_image'] :
                    print("m")
                    customer.profile_image.delete()
                    customer.profile_image = request.FILES['profile_image']
                    customer.save()
                    #customer.profile_image.delete()

                    #customer.profile_image = request.FILES['profile_image']

                    fs = FileSystemStorage()

                    customer.save()

                    filename = fs.save(customer.profile_image.name , customer.profile_image)

                    uploaded_file_url = fs.url(filename)

                else:
                    print("if is not executing")

            except:
                pass

            customer.save()
            print("Success")
            return redirect(reverse('chatbox_detail', kwargs={'pk':customer.id}))
        x = count_posts_of(user)
        context = {'x':x,'user':user, 'customer':customer, 'club':customer , 'uploaded_file_url': uploaded_file_url}

        return render(request,'app1/clubupdate.html',context)


def clubpassword(request,pk):
    msg = ""
    try:
        if "c" in list:
            user = Customer.objects.get(id = list[0])
        elif "s" in list:
            user = Seller.objects.get(id = list[0])
        else:
            user=None
    except:
        user = None

    if user == None:
        return redirect('/')
    else:
        club = Club.objects.get(id = pk)
        if request.method == "POST":
            x = request.POST.get("input")
            if x == club.password or crypto_hash(x) == club.password:
                return redirect(reverse('chatbox_detail', kwargs={'pk':club.id}))
            else:
                msg = "Password to Club '{x}' was incorrect ".format(x = club.name)
                context = {"msg":msg,"user":user}
                return render(request,'app1/clubpassword.html',context)
        context = {"msg":msg, "user":user}
        return render(request , 'app1/clubpassword.html' ,context)
