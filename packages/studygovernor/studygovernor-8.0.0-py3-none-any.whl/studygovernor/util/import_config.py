import datetime
import os
import yaml

from .. import models, user_datastore
from ..util.helpers import hash_password


def load_config(config, overwrite=False, silent=True):
    db = models.db

    updated_objects = {
        'roles': list(),
        'users': list(),
        'external_systems': list(),
        'scantypes': list()
    }

    if 'roles' in config:
        if not silent:
            print("\n Adding Roles:")
        updated_objects['roles'] = load_roles(config['roles'], overwrite, silent)
    
    if 'users' in config:
        if not silent:
            print("\nAdding users:")
        updated_objects['users'] = load_users(config['users'], overwrite, silent)
    
    if 'external_systems' in config:
        if not silent:
            print("\nAdding external_systems:")
        updated_objects['external_systems'] = load_external_systems(config['external_systems'], overwrite, silent)

    if 'scantypes' in config:
        if not silent:
            print("\nAdding scantypes:")
        updated_objects['scantypes'] = load_scantypes(config['scantypes'], overwrite, silent)
    return updated_objects

def load_roles(roles_config, overwrite, silent):
    updated_roles = list()
    for role in roles_config:
        role_query = models.Role.query.filter(models.Role.name == role['name'])
        existing_role = role_query.first()
        if existing_role is None:
            new_role = user_datastore.create_role(**role)
            updated_roles.append(new_role)
            if not silent:
                print(f"Created {new_role}")
        elif overwrite:
            if role.get('permissions'):
                role['permissions'] = ",".join(role['permissions'])
            role_query.update(role)
            updated_roles.append(existing_role)
            if not silent:
                print(f"Updated {existing_role}")
        else:
            if not silent:
                print(f"[WARNING] Skipping Role {role['name']}, already exists!")
    return updated_roles

def load_users(users_config, overwrite, silent):
    updated_users = list()
    for user in users_config:
        user_query = models.User.query.filter((models.User.username == user['username']) | (models.User.email == user['email']))
        
        existing_user = user_query.first()
        # Make sure user is confirmed
        if existing_user is None:
            user['confirmed_at'] = datetime.datetime.now()
            user['password'] = hash_password(user['password'])
            new_user = user_datastore.create_user(**user)
            updated_users.append(new_user)
            if not silent:
                print(f"Adding {new_user}")
        elif overwrite:
            user['confirmed_at'] = datetime.datetime.now()
            user['password'] = hash_password(user['password'])
            if user.get('roles'):
                user_roles = [user_datastore.find_role(role) for role in user['roles']]
                user.pop('roles')
                existing_user.roles = user_roles
            user_query.update(user)
            updated_users.append(existing_user)
            if not silent:
                print(f"Updated {existing_user}")
        else:
            if not silent:
                print(f"[WARNING] Skipping User {user['username']} / {user['email']}, user and/or username already used!")
    return updated_users

def load_external_systems(external_systems_config, overwrite, silent):
    db = models.db
    updated_external_systems = list()
    
    for external_system in external_systems_config:
        external_system_query = models.ExternalSystem.query.filter(models.ExternalSystem.system_name == external_system['system_name'])
        existing_external_system = external_system_query.first()
        
        if existing_external_system is None:
            new_external_system = models.ExternalSystem(system_name=external_system['system_name'], url=external_system['url'])
            db.session.add(new_external_system)
            updated_external_systems.append(new_external_system)
            if not silent:
                print(f"Adding {external_system['system_name']}")
        elif overwrite:
            external_system_query.update(external_system)
            updated_external_systems.append(existing_external_system)
            if not silent:
                print(f"Updated {existing_external_system}")
        else:
            if not silent:
                print(f"[WARNING] Skipping ExternalSystem {external_system['system_name']}, already exists!")
    return updated_external_systems

def load_scantypes(scantypes_config, overwrite, silent):
    db = models.db
    updated_scantypes = list()
    
    for scan_type in scantypes_config:
        scan_type_query = models.Scantype.query.filter(models.Scantype.protocol == scan_type['protocol'])
        existing_scan_type = scan_type_query.first()
        
        if existing_scan_type is None:
            new_scantype = models.Scantype(modality=scan_type['modality'], protocol=scan_type['protocol'])
            db.session.add(new_scantype)
            updated_scantypes.append(new_scantype)
            if not silent:
                print(f"Adding {scan_type['modality']} {scan_type['protocol']}")
        elif overwrite:
            scan_type_query.update(scan_type)
            updated_scantypes.append(existing_scan_type)
            if not silent:
                print(f"Updated {existing_scan_type}")
        else:
            if not silent:
                print(f"[WARNING] Skipping ScanType {scan_type['protocol']}, already exists!")
    return updated_scantypes


def load_config_file(app, file_path, silent=False):
    db = models.db
    file_path = str(file_path)

    if not os.path.isfile(file_path):
        print(f"[ERROR] The file ({file_path}) does not exist")

    with open(file_path) as fh:
        try:
            config = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            print(f"[ERROR] Config file is not a valid YAML file. {exc}")
            return

    with app.app_context():      
        load_config(config, silent=silent)
        db.session.commit()
