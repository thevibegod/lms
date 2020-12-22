# from django.contrib import messages
#
# from base.models import Profile
# from django.contrib.auth.models import User
#
#
# def social_user(backend, uid, user=None, *args, **kwargs):
#     provider = backend.name
#     social = backend.strategy.storage.user.get_social_auth(provider, uid)
#     if social:
#         users = User.objects.filter(email=social.user.email)
#         if not profiles.exists():
#             return backend.strategy.redirect('/error/')
#         if user and social.user != user:
#             return backend.strategy.redirect('/login/')
#
#         elif not user:
#             user = social.user
#     else:
#         user = None
#     return {'social': social,
#             'user': user,
#             'is_new': user is None,
#             'new_association': social is None}
