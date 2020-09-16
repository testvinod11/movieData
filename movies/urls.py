from common.routers import OptionalSlashRouter

from . import views

router = OptionalSlashRouter()

urlpatterns = []

router.register(r'movie', views.MoviesViewSet, basename='movie')
router.register(r'movie-watch-list', views.UserWatchListView, basename='movie_watch_list')
router.register(r'movie-watched', views.UserWatchedView, basename='movie_watched')

urlpatterns += router.urls
