import datetime
import os

from .. import models, user_datastore
from ..util.helpers import hash_password

ROLES_DEFINITION = [
    {
        "description": "admin",
        "name": "admin",
        "permissions": [
            "action_update",
            "sample_state_update",
            "sample_add",
            "sample_update",
            "sample_delete",
            "user_read_all",
            "user_update_all",
            "user_add",
            "user_delete",
            "roles_manage"
        ]
    },
    {
        "description": "superuser",
        "name": "superuser",
        "permissions": [
            "sample_state_update",
            "sample_add",
            "user_read"
        ]
    },
    {
        "description": "user",
        "name": "user",
        "permissions": [
            "user_read"
        ]
    }
]


def ensure_roles():
    db = models.db

    roles = {}
    print("* Creating roles")
    for role in ROLES_DEFINITION:
        if models.Role.query.filter(models.Role.name == role['name']).count() == 0:
            roles[role['name']] = user_datastore.create_role(**role)
            print(f"{roles[role['name']]} {role}")
        else:
            print(f"[WARNING] Skipping Role {role['name']}, already exists!")
    db.session.commit()


def ensure_admin_user():
    admin_username = os.environ.get('STUDYGOV_ADMIN_USERNAME')
    admin_email = os.environ.get('STUDYGOV_ADMIN_EMAIL')
    admin_password = os.environ.get('STUDYGOV_ADMIN_PASSWORD')
    admin_force_update = os.environ.get('STUDYGOV_ADMIN_FORCE_UPDATE')

    if not admin_username or not admin_email or not admin_password:
        print(f'Can only ensure admin account if STUDYGOV_ADMIN_USERNAME, STUDYGOV_ADMIN_EMAIL, and STUDYGOV_ADMIN_PASSWORD are set')
        return

    admin_user = models.User.query.filter_by(username=admin_username).one_or_none()
    print(f'Found admin user: {admin_user}')

    if admin_force_update and admin_user is not None:
        admin_user.password = admin_password
        admin_user.email = admin_email
        admin_user.active = True
        print('Updated admin user details.')
    elif admin_force_update or admin_user is None:
        admin_password = hash_password(admin_password)
        admin_user = user_datastore.create_user(
            username=admin_username,
            password=admin_password,
            name='Administrator Account',
            email=admin_email,
            active=True,
            roles=["admin"],
            confirmed_at=datetime.datetime.now(),
        )

        models.db.session.add(admin_user)
        print('Created admin user.')
    else:
        print('Admin user already exists, skipping creation.')

    if admin_user is not None:
        models.db.session.commit()
        models.db.session.refresh(admin_user)
