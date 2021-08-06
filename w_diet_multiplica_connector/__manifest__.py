# -*- encoding: utf-8 -*-

{
    'name': 'WEDOO | Diet Multiplica Connector',
    'author': 'TELEMATEL ©',
    'category': 'Extra Tools',
    'sequence': 50,
    'website': 'https://www.telematel.com',
    'version': '13.0.1.1',
    'description': """
Diet Multiplica Connector
=========================
Integration with Multiplica procedures.  
    """,
    'depends': [
        'base',
        'w_custom_events_auth_signup'
    ],
    'installable': True,
    'data': [
        #'security/ir.model.access.csv',
        #'views/assets.xml',
        #'views/templates.xml',
        #'views/inherit_res_config_settings_view.xml',
        'views/inherit_website.xml'
    ],
    'demo': [],
    'qweb': [],
    'application': False,
}

