def save_profile_picture(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        picture_url = response.get('picture')
        if picture_url:
            profile = getattr(user, 'studentprofile', None)
            if profile:
                profile.profile_picture = picture_url
                profile.save()
