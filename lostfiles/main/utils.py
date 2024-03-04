menu = [
    {'title': "Войти", 'url_name': 'login'}
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        #if not self.request.user.is_authenticated:
            #user_menu.pop(1) # здесь надо указывать индекс элемента меню, который надо убрать

        context['menu'] = user_menu

        return context
