from common.routers import OptionalSlashRouter
from . import views

urlpatterns = []

router = OptionalSlashRouter()

router.register(r'user/signup', views.SignupView, basename='signup')
router.register(r'user/login', views.LoginView, basename='login')

urlpatterns += router.urls
