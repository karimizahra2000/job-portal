from .users import urlpatterns as user_patterns
from .profiles import urlpatterns as profile_patterns
from .jobs import urlpatterns as job_patterns

urlpatterns = []
urlpatterns += user_patterns
urlpatterns += profile_patterns
urlpatterns += job_patterns
