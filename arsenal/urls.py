from django.contrib import admin
from django.urls import path #, include
from app1 import views
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from django.conf.urls.static import static

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$', views.customer_login , name = "customer_login") ,
    url(r'^baseintro/$', views.baseintro , name = "baseintro") ,
    url(r'^customerlogin/$', views.customer_login , name = 'customer_login') ,
    url(r'^home/$', views.home , name = 'home') ,
    url(r'^sellerlogin/$', views.seller_login , name = 'seller_login') ,
    url(r'^customerintro/$', views.customerintro , name = 'customerintro') ,
    url(r'^sellerintro/$', views.sellerintro , name = 'sellerintro') ,
    url(r'^customerlogout/$', views.customerlogout , name = 'customerlogout') ,
    url(r'^sellerlogout/$', views.sellerlogout , name = 'sellerlogout') ,

    url(r'^chatbox/$', views.chatbox , name = "chatbox") ,
    url(r'^chatbox/(?P<pk>\d+)$', views.chatbox_detail, name='chatbox_detail'),

    url(r'^commentbox/(?P<pk>\d+)$', views.commentbox, name='commentbox'),

    url(r'^searchlist/$' , views.searchlist , name = 'searchlist'),
    url(r'^clubsearchlist/$' , views.clubsearchlist , name = 'clubsearchlist'),
    url(r'^site_data_page/$', views.site_data , name = 'site_data') ,
    url(r'^site_progress/$', views.site_progress , name = 'site_progress') ,

    url(r'^follower_list(?P<pk>\d+)$', views.follower_list, name='follower_list'),
    url(r'^following_list/(?P<pk>\d+)$', views.following_list, name='following_list'),
    url(r'^likelist/(?P<pk>\d+)$', views.likelist, name='likelist'),
    url(r'^crushlist/$', views.crushlist, name='crushlist'),
    url(r'^productlikelist/(?P<pk>\d+)$', views.productlikelist, name='productlikelist'),
    url(r'^ratinglist/(?P<pk>\d+)$', views.ratinglist, name='ratinglist'),
    url(r'^reviewlist/(?P<pk>\d+)$', views.reviewlist, name='reviewlist'),
    url(r'^pendingorderslist/(?P<pk>\d+)$', views.pendingorderslist, name='pendingorderslist'),
    url(r'^feedlist/$', views.feedlist, name='feedlist'),
    url(r'^listfeed/$', views.listfeed, name='listfeed'),
    url(r'^tag/$', views.tag , name = 'tag'),


    url(r'^product_list/$',views.ProductListView.as_view(),name='product_list'),
    url(r'^product/(?P<pk>\d+)$', views.productdetail, name='product_detail'),

    url(r'^clubpassword/(?P<pk>\d+)$', views.clubpassword, name='clubpassword'),





    url(r'^winter/$',views.winter,name='winter'),
    url(r'^summer/$',views.summer,name='summer'),
    url(r'^beach/$',views.beach,name='beach'),
    url(r'^fashionoftheweek/$',views.fashionoftheweek,name='fashionoftheweek'),
    url(r'^highdemand/$',views.highdemand,name='highdemand'),
    url(r'^special/$',views.special,name='special'),
    url(r'^promoted/$',views.promoted,name='promoted'),
    url(r'^transfer/(?P<pk>\d+)$',views.transfer,name='transfer'),
    url(r'^pay/(?P<pk>\d+)$',views.pay,name='pay'),
    url(r'^men/$',views.men,name='men'),
    url(r'^women/$',views.women,name='women'),
    url(r'^electronics/$',views.electronics,name='electronics'),
    url(r'^tshirts/$',views.tshirts,name='tshirts'),
    url(r'^shirts/$',views.shirts,name='shirts'),
    url(r'^hoodies/$',views.hoodies,name='hoodies'),
    url(r'^cups/$',views.cups,name='cups'),
    url(r'^phonecovers/$',views.phonecovers,name='phonecovers'),
    url(r'^stickers/$',views.stickers,name='stickers'),
    url(r'^notebooks/$',views.notebooks,name='notebooks'),
    url(r'^bandsn/$',views.bands,name='bands'),
    url(r'^gymvests/$',views.gymvests,name='gymvests'),
    url(r'^keychains/$',views.keychains,name='keychains'),
    url(r'^posters/$',views.posters,name='posters'),
    url(r'^caps/$',views.caps,name='caps'),
    url(r'^bags/$',views.bags,name='bags'),
    url(r'^socks/$',views.socks,name='socks'),
    url(r'^masks/$',views.masks,name='masks'),
    url(r'^footwears/$',views.footwears,name='footwears'),
    url(r'^bottles/$',views.bottles,name='bottles'),

    url(r'^ibag/$',views.ibag,name='ibag'),
    url(r'^customer_list/$',views.CustomerListView.as_view(),name='customer_list'),
    url(r'^customer/(?P<pk>\d+)$', views.customerdetailview, name='customer_detail'),
    url(r'^seller_list/$',views.SellerListView.as_view(),name='seller_list'),
    url(r'^seller/(?P<pk>\d+)$', views.SellerDetailView.as_view(), name='seller_detail'),
    url(r'^message/$',views.message,name='message'),
    url(r'^memberlist/(?P<pk>\d+)$', views.memberlist, name='memberlist'),
    url(r'^order_list/$',views.OrderListView.as_view(),name='order_list'),
    url(r'^order/(?P<pk>\d+)$', views.orderdetailview, name='order_detail'),


    url(r'^post_list/$',views.postlist,name='post_list'),
    url(r'^post/(?P<pk>\d+)$', views.postdetail, name='post_detail'),
    url(r'^tag1/(?P<pk>\d+)$', views.tag1, name='tag1'),
    url(r'^tag2/(?P<pk>\d+)$', views.tag2, name='tag2'),
    url(r'^tag3/(?P<pk>\d+)$', views.tag3, name='tag3'),
    url(r'^tag4/(?P<pk>\d+)$', views.tag4, name='tag4'),
    url(r'^tag5/(?P<pk>\d+)$', views.tag5, name='tag5'),
    url(r'^tagrequests/(?P<pk>\d+)$', views.tagrequests, name='tagrequests'),

    url(r'^create_order/(?P<pk>\d+)$' , views.createorder , name = 'create_order'),
    url(r'^create_customer/$' , views.createcustomer , name = 'create_customer'),
    url(r'^create_product/$' , views.createproduct , name = 'create_product'),
    url(r'^productupload/$' , views.productupload , name = 'productupload'),

    url(r'^add_customer/$' , views.addcustomer , name = 'add_customer'),
    url(r'^add_seller/$' , views.addseller , name = 'add_seller'),
    url(r'^addclub/$' , views.addclub , name = 'addclub'),


    url(r'update_order/(?P<pk>\d+)' , views.UpdateOrder.as_view() , name = 'update_order'),
    url(r'update_customer/(?P<pk>\d+)' , views.updatecustomer , name = 'update_customer'),
    url(r'update_product/(?P<pk>\d+)' , views.updateproduct , name = 'update_product'),
    url(r'update_seller/(?P<pk>\d+)' , views.updateseller , name = 'update_seller'),
    url(r'clubupdate/(?P<pk>\d+)' , views.clubupdate , name = 'clubupdate'),
    url(r'clubeditmember/(?P<pk>\d+)' , views.clubeditmember , name = 'clubeditmember'),

    url(r'customer_update/(?P<pk>\d+)' , views.customerupdate , name = 'customer_update'),
    url(r'post_update/(?P<pk>\d+)' , views.postupdate , name = 'post_update'),
    url(r'product_update/(?P<pk>\d+)' , views.productupdate , name = 'product_update'),
    url(r'order_update/(?P<pk>\d+)' , views.orderupdate , name = 'order_update'),
    url(r'comment_update/(?P<pk>\d+)' , views.commentupdate , name = 'comment_update'),
    url(r'seller_update/(?P<pk>\d+)' , views.sellerupdate , name = 'seller_update'),



    url(r'delete_order/(?P<pk>\d+)' , views.deleteorder , name = 'delete_order'),
    url(r'delete_customer/(?P<pk>\d+)' , views.deletecustomer , name = 'delete_customer'),
    url(r'delete_product/(?P<pk>\d+)' , views.deleteproduct , name = 'delete_product'),
    url(r'delete_post/(?P<pk>\d+)' , views.deletepost , name = 'delete_post'),
    url(r'delete_comment/(?P<pk>\d+)' , views.deletecomment , name = 'delete_comment'),
    url(r'delete_seller/(?P<pk>\d+)' , views.deleteseller , name = 'delete_seller'),



    url(r'block_order/(?P<pk>\d+)' , views.blockorder , name = 'block_order'),
    url(r'block_customer/(?P<pk>\d+)' , views.blockcustomer , name = 'block_customer'),
    url(r'block_product/(?P<pk>\d+)' , views.blockproduct , name = 'block_product'),
    url(r'block_post/(?P<pk>\d+)' , views.blockpost , name = 'block_post'),
    url(r'block_comment/(?P<pk>\d+)' , views.blockcomment , name = 'block_comment'),
    url(r'block_seller/(?P<pk>\d+)' , views.blockseller , name = 'block_seller'),
    url(r'^private/$' , views.private , name = 'private'),
    url(r'^public/$' , views.public , name = 'public'),

    url(r'unblockorder/(?P<pk>\d+)' , views.unblockorder , name = 'unblockorder'),
    url(r'unblockcustomer/(?P<pk>\d+)' , views.unblockcustomer , name = 'unblockcustomer'),
    url(r'unblockproduct/(?P<pk>\d+)' , views.unblockproduct , name = 'unblockproduct'),
    url(r'unblockpost/(?P<pk>\d+)' , views.unblockpost , name = 'unblockpost'),
    url(r'unblockcomment/(?P<pk>\d+)' , views.unblockcomment , name = 'unblockcomment'),
    url(r'unblockseller/(?P<pk>\d+)' , views.unblockseller , name = 'unblockseller'),



    #url('' , include('app1.urls')),
]




if settings.DEBUG :
    urlpatterns += static(settings.STATIC_URL , document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
