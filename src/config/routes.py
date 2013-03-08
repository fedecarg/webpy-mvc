# Routes have priority defined by the order of appearance of the routes. The priority 
# goes from top to bottom. The last route in that file is at the lowest priority will 
# be applied last. If no route matches, 404 is returned.
urls = (
    '/users/page/(\d+)',                  {'controller':'users', 'action':'index'},
    '/users/(\d+)/(index|update|delete)', {'controller':'index', 'action':'{1}', 'id':'{0}'},
    '/users/(new|create)',                {'controller':'users', 'action':'{0}'},
    '/users/(\d+)',                       {'controller':'users', 'action':'show'},
    '/users?',                            {'controller':'users', 'action':'index'},
    '/',                                  {'controller':'index', 'action':'index'}
)