from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from main import url_views
from main import test_views

urlpatterns = [
    # Examples:
    # url(r'^$', 'Waihui.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', url_views.url_homepage, name="home"),
    url(r'^signup/$', url_views.url_signup, name="signup"),
    # url(r'^login/$', url_views.url_login, name="login"),
    url(r'^login/$', url_views.url_login_new, name="login"),
    url(r'^logout/$', url_views.url_logout, name='logout'),
    url(r'^user/(\d+)/$', url_views.url_user, name='user'),
    url(r'^tc/(\w*)/$', url_views.url_tc, name='topic_category'),
    url(r'^show/(\d+)/$', url_views.url_tutor, name='tutor'),
    # url(r'^time/plus/(\d+)/$', url_views.url_index, name="index"),
    url(r'^addsku/$', url_views.url_addsku, name='addsku'),
    # url(r'^holdsku/$', url_views.url_holdsku, name='holdsku'),
    url(r'^booksku/(\d+)/(\d+)$', url_views.url_holdsku, name='booksku'),
    url(r'^bookresult/$', url_views.url_bookresult, name='bookresult'),
    url(r'^picktopic/$', url_views.url_picktopic, name='picktopic'),
    url(r'^skuintopic/(\d+)/$', url_views.url_skuintopic, name='skuintopic'),
    url(r'^sku/$', url_views.url_skulist, name='skulist'),
    url(r'^sku/(\d+)/$', url_views.url_showsku, name='showsku'),#TP:showsku.html
    url(r'^sku/(\d+)/addplan/$', url_views.url_addplan, name='addplan'),
    url(r'^plan/(\d+)/modify/$', url_views.url_modifyplan, name='modifyplan'),
    url(r'^sku/(\d+)/reply/$', url_views.url_replytosku, name="replyrts"),
    url(r'^sku/(\d+)/repick/$', url_views.url_provider_repick, name="provider_repick"),
    url(r'^sku/(\d+)/t/ready/$', url_views.url_provider_ready_sku, name="provider_ready_sku"),
    url(r'^sku/(\d+)/b/ready/$', url_views.url_buyer_ready_sku, name="buyer_ready_sku"),
    url(r'^sku/(\d+)/t/finished/$', url_views.url_provider_finished_sku, name="provider_finished_sku"),
    url(r'^sku/(\d+)/t/cancel/$', url_views.url_provider_cancel_sku, name="provider_cancel_sku"),
    url(r'^sku/(\d+)/feedback/$', url_views.url_feedback_sku, name="feedback_sku"),
    url(r'^addorder/$', url_views.url_addorder, name="addorder"),
    url(r'^tutor/(\d+)/$', url_views.url_provider_profile, name="provider_profile"),#TP:provider_profile.html
    url(r'^tutor/$', url_views.url_my_profile, name="self_profile"),#TP:my_profile.html
    url(r'^tutor/edit/$', url_views.url_provider_profile_edit, name="edit_profile"),#TP:provider_profile_edit.html
    url(r'^tutor/avatar/$', url_views.url_provider_profile_avatar, name="provider_avatar"),
    url(r'^tutors/$', url_views.url_providers, name="providers"),
    url(r'^dashboard/$', url_views.url_dashboard, name="dashboard"),
    url(r'^dashboard/cancel/(\d+)/$', url_views.url_buyer_cancel_sku, name="buyer_cancel_sku"),
    url(r'^office/$', url_views.url_office, name="office"),
    url(r'^office/repick/$', url_views.url_repickpool, name="repickpool"),
    url(r'^office/schedule/$', url_views.url_schedule, name="schedule"),
    url(r'^notifications/$', url_views.url_notifications, name="notifications"),
    url(r'^notification/(\d+)/$', url_views.url_notification_go, name="notification_go"),
    url(r'^order/$', url_views.url_orderlist, name='orderlist'),
    url(r'^order/(\d+)/$', url_views.url_showorder, name='showorder'),
    url(r'^order/(\d+)/canceled/$', url_views.url_buyer_cancel_order, name='ordercancel'),
    url(r'^order/(\d+)/paid/$', url_views.url_orderpaid, name='orderpaid'),
    url(r'^wallet/$', url_views.url_walletpage, name='wallet'),
    url(r'^casher/$', url_views.url_casher, name='casher'),
    url(r'^payment_result/$', url_views.url_payment_result, name='payment_result'),
    url(r'^alipay_trade_page_test/(\d+)/$', test_views.url_alipay_webtrade_test, name='alipay_test'),
    url(r'^alipay/return/', test_views.url_alipay_webtrade_return, name='alipay_return')
    # url(r'^reviews/$', url_views.url_reviews, name='reviews'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
