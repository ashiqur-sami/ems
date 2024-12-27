{
    "name": "Lunch Menu Mangement",
    "version": "1.0.0",
    "summary": "A module for Lunch menu management ",
    "description": """
    This module is for seamlessly manage 
    a office lunch system
    """,
    "author": "Sami",
    "category": "Practice",
    # "website": ""
    "license":"LGPL-3",
    "depends": ["base", "web"], #, "mail"
    "data": [
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/lunch_view.xml',
        'views/lunch_menu_management_menu.xml',
    ],
    # "auto_install": True,
    "application": True,
}
