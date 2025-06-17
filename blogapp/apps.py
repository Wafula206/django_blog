from django.apps import AppConfig

class BlogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blogapp'

    def ready(self):
        # Import signals
        import blogapp.signals

        # ✅ Import User & Profile INSIDE ready()
        from django.contrib.auth.models import User
        from blogapp.models import Profile

        # ✅ Define property
        def get_profile(self):
            profile, created = Profile.objects.get_or_create(user=self)
            return profile

        # ✅ Monkey patch once
        if not hasattr(User, 'profile'):
            User.add_to_class('profile', property(get_profile))
