# Get site navigation

def get_navigation(navbar=None, sidebar=None):
    data = {
        'main': {
            'title': 'Главная',
            'menu': 'main',
            'link': '/',
            'sidebar_navs': [
                {
                    'title': 'Главная',
                    'name': 'mail',
                    'is_active': True,
                    'link': '/',
                },
            ]
        },
        'profile': {
            'title': 'Профиль',
            'menu': 'profile',
            'link': '/profile',
            'sidebar_navs': [
                {
                    'title': 'Профиль',
                    'name': 'profile',
                    'is_active': False,
                    'link': '/profile',
                },
            ]
        },
    }
    if navbar is None and sidebar is None:
        return navigation
    navigation = data.get(navbar, {})
    for i, sidebar_nav in enumerate(navigation.get('sidebar_navs', [])):
        if sidebar_nav['name'] == sidebar:
            navigation['sidebar_navs'][i]['is_active'] = True
            break
    return navigation
