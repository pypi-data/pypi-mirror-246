#!/usr/bin/env python
# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run(args=None):
    import argparse
    from studygovernor import create_app

    parser = argparse.ArgumentParser(description="Run the webserver. Never use this for production!!!")
    parser.add_argument('--debug', action='store_true', default=False, help="Run the server in debug mode.")
    parser.add_argument('--host', default=None, help="Define the host, leave empty for localhost. (e.g. 0.0.0.0)")
    parser.add_argument('--port', default=None, type=int, help="Define the port, leave empty for 5000")
    args = parser.parse_args(args=args)

    app = create_app()
    app.run(host=args.host, port=args.port, debug=args.debug)


def run_gunicorn(args=None):
    try:
        from gunicorn.app.base import BaseApplication
    except ImportError:
        print("In order to run the server with gunicorn install it with: pip install gunicorn")
        return False

    from studygovernor import create_app
    app = create_app()

    class WSGIServer(BaseApplication):
        def __init__(self, app):
            self.application = app
            super(WSGIServer, self).__init__("%(prog)s [OPTIONS]")

        def load_config(self):
            parser = self.cfg.parser()
            args = parser.parse_args()

            for k, v in args.__dict__.items():
                if v is None:
                    continue
                if k == 'args':
                    continue
                self.cfg.set(k.lower(), v)

        def load(self):
            return self.application

    WSGIServer(app).run()


def db_init(args=None):
    from studygovernor import create_app
    from studygovernor.models import db

    # Create app for the context
    app = create_app()

    # Create the database
    with app.app_context():
        db.create_all()


def db_clean(args=None):
    import argparse
    from studygovernor import create_app
    from studygovernor.models import db

    parser = argparse.ArgumentParser(description='Clean the study governor database')
    parser.add_argument('-f', '--force', action="store_true", help="Force (do not prompt for confirmation)")
    args = parser.parse_args()

    if args.force or input("Are you sure you want to empty the database [yes/no]: ") == 'yes':
        # Create app for the context
        app = create_app()

        with app.app_context():
            db.drop_all()
            db.create_all()
        print("Database is empty!")
    else:
        print("Cancelled database clean action.")


def onboarding(args=None):
    from . import create_app
    from .util.onboarding import ensure_roles
    from .util.onboarding import ensure_admin_user

    print("*** Start onboarding ...")
    app = create_app()
    with app.app_context():
        ensure_roles()
        ensure_admin_user()


def config_from_file(args=None):
    import argparse

    parser = argparse.ArgumentParser(description="Configure the study governor user/roles from a config json file.")
    parser.add_argument('config', metavar="JSON", help="A json file containing the config for the study governor.")
    args = parser.parse_args(args=args)

    from . import create_app
    from studygovernor.util.import_config import load_config_file
    app = create_app()
    load_config_file(app, args.config)


def create_subject(args=None):
    import argparse
    import datetime
    import requests

    def to_date(value):
        return datetime.datetime.strptime(value, '%Y-%m-%d').date()

    parser = argparse.ArgumentParser(description='Initialise the workflow: fill the DB with states and its possible transitions.')
    parser.add_argument('--host', type=str, help='The server to add the subject to', required=True)
    parser.add_argument('-l', '--label', type=str, help='The label of the subject', required=True)
    parser.add_argument('-d', '--date_of_birth', type=to_date, required=True)
    args = parser.parse_args()

    subject = {
        'label': args.label,
        'date_of_birth': str(args.date_of_birth),
    }

    server = args.host.rstrip('/')

    if input("Are you sure you want add new subject '{}' to {} [yes/no]: ".format(subject, server)) == 'yes':
        response = requests.post('{}/api/v1/subjects'.format(server), json=subject)
        print("\n * Committed to the REST api: [{}] {}.".format(response.status_code, response.text))
    else:
        print("\n * Cancelled adding the subject.")


def create_experiment(args=None):
    import argparse
    from flask_restx import inputs
    import requests

    parser = argparse.ArgumentParser(description='Initialise the workflow: fill the DB with states and its possible transitions.')
    parser.add_argument('--host', type=str, help='The server to add the subject to', required=True)
    parser.add_argument('-l', '--label', type=str, help='The label of the experiment', required=True)
    parser.add_argument('-s', '--subject', type=str, help='The subject this experiment belongs to', required=True)
    parser.add_argument('-d', '--scandate', type=inputs.datetime_from_iso8601, help='The timestamp when the experiment was acquired', required=True)
    args = parser.parse_args()

    server = args.host.rstrip('/')
    subject = args.subject

    if not (server.startswith('http://') or server.startswith('https://')):
        server = 'http://{}'.format(server)

    if not subject.startswith('/api/v1/subjects/'):
        subject = '/api/v1/subjects/{}'.format(subject)

    experiment = {
        'label': args.label,
        'subject': subject,
        'scandate': args.scandate.isoformat(),
    }

    if input("Are you sure you want add new experiment '{}' to {} [yes/no]: ".format(experiment, server)) == 'yes':
        response = requests.post('{}/api/v1/experiments'.format(server), json=experiment)
        print("\n * Committed to the REST api: [{}] {}.".format(response.status_code, response.text))
    else:
        print("\n * Cancelled adding the subject.")


def workflow_init(args=None):
    import argparse
    from .util.helpers import initialize_workflow

    parser = argparse.ArgumentParser(description='Initialise the workflow: fill the DB with states and its possible transitions.')
    parser.add_argument('workflow', type=str, help='The workflow definition (JSON)')
    parser.add_argument('-f', '--force', action='store_true', default=False, help="Do not ask questions, just do it")
    parser.add_argument('-u', '--upgrade', action='store_true', default=False, help="Allow for the workflow to be upgraded if already present")
    args = parser.parse_args()

    from studygovernor import create_app
    app = create_app()

    initialize_workflow(args.workflow, app=app, verbose=True, force=args.force, upgrade=args.upgrade)


def visualize_workflow(args=None):
    import argparse
    import yaml
    import os
    import subprocess

    from studygovernor.util.visualization import visualize_from_config
    from studygovernor.util.visualization import visualize_from_db
    from studygovernor.util.visualization import write_visualization_to_file

    parser = argparse.ArgumentParser(description='Plot the workflow using graphviz.')
    parser.add_argument('-d', '--from-database', action='store_true', help="Visualize the workflow(s) from the database, instead of the YAML")
    parser.add_argument('-w', '--workflow', metavar='WORKFLOW.yaml', type=str, help='The workflow definition (YAML)')
    parser.add_argument('-f', '--format', type=str, default="svg", help="The image format for the visualization file(s)")
    args = parser.parse_args()

    if args.from_database:
        from studygovernor import create_app

        app = create_app()
        with app.app_context():
            visualizations = visualize_from_db()
            for vis in visualizations:
                write_visualization_to_file(vis, args.format)

    if args.workflow:
        visualization = visualize_from_config(args.workflow)
        write_visualization_to_file(visualization, args.format)


def validate_workflow():
    import argparse
    import yaml
    from pathlib import Path
    from jsonschema import Draft7Validator

    parser = argparse.ArgumentParser(description='Validate a workflow definition file.')
    parser.add_argument('-w', '--workflow', metavar='WORKFLOW.yaml', type=str, required=True,
                        help='The workflow definition (YAML)')
    args = parser.parse_args()

    with open(args.workflow) as fh:
        workflow_definition = yaml.safe_load(fh)

    with open(Path(__file__).parent / 'static' / 'workflow.schema.json') as fh:
        workflow_schema = yaml.safe_load(fh)

    # Collect all errors
    validator = Draft7Validator(workflow_schema)
    errors = list(validator.iter_errors(workflow_definition))

    # Print the outcome
    if not errors:
        print(f'Workflow is {workflow_definition["label"]} valid (loaded from {args.workflow}).')
    else:
        print(f'Workflow is not {workflow_definition["label"]} valid (loaded from {args.workflow}), errors:')
        print('-' * 80)
        for error in errors:
            data_path = _improve_data_path(workflow_definition, error.absolute_path)
            print(f'data path: {"/".join(str(x) for x in data_path)}')
            print(f'schema path: {"/".join(str(x) for x in error.absolute_schema_path)}')
            print(f'message: {error.message}')
            print('-' * 80)


def _improve_data_path(workflow, path):
    current_level = workflow
    new_path = []
    for index in path:
        current_level = current_level[index]
        new_index = index
        if isinstance(current_level, dict) and 'label' in current_level:
            new_index = f"{index}[label={current_level['label']}]"

        new_path.append(new_index)

    return new_path


def validate_template():
    import argparse
    import json
    import yaml
    from pathlib import Path
    from jsonschema import Draft7Validator

    parser = argparse.ArgumentParser(description='Validate a ViewR template file.')
    parser.add_argument('-t', '--template', metavar='TEMPLATE.yaml', type=str, required=True,
                        help='The ViewR template (YAML/JSON)')
    args = parser.parse_args()

    with open(args.template) as fh:
        template_definition = yaml.safe_load(fh)

    with open(Path(__file__).parent / 'static' / 'viewr_template.schema.json') as fh:
        template_schema= yaml.safe_load(fh)

    # Collect all errors
    validator = Draft7Validator(template_schema)
    errors = list(validator.iter_errors(template_definition))

    # Print the outcome
    if not errors:
        print(f'Template structure is {template_definition["template_name"]} valid (loaded from {args.template}).')
    else:
        print(f'Template structure is not {template_definition["template_name"]} valid (loaded from {args.template}), errors:')
        print('-' * 80)
        for error in errors:
            print_schema_error(error)

    if 'contexts' in template_definition:
        contexts = template_definition['contexts']
        mdl_spec = template_definition.get('mdl_layout')

        if mdl_spec:
            for context in contexts.keys():
                if f'{{{context}}}' not in mdl_spec:
                    print(f'[ERROR] Context {context} not used in MDL specification')
    else:
        contexts = {'default': template_definition}


    for context in contexts.values():
        scans = set(context['scans'])

        if context['annotations']:
            annotations = set(context['annotations'])
        else:
            annotations = set()

        for viewport in context['viewports']:
            if viewport['scan'] not in scans:
                print(f'[ERROR] Viewport {viewport["name"]} references scan {viewport["scan"]} which is not found!')

            annotation = viewport.get('annotation')
            if annotation and annotation not in annotations:
                print(f'[ERROR] Viewport {viewport["name"]} references annotation {annotation} which is not found!')

        context_mdl = context.get('mdl_layout')

        if context_mdl:
            if '{editor}' not in context_mdl:
                print(f'[ERROR] Context mdl need to place the editor MDL template')

            if '{viewports}' not in context_mdl:
                print(f'[ERROR] Context mdl need to place the viewports MDL template')

            if '{qa_fields}' not in context_mdl:
                print(f'[ERROR] Context mdl need to place the qa_fields MDL template')


def print_schema_error(error, indent=0):
    indent_str = ' ' * indent
    print(f'{indent_str} data path: {"/".join(str(x) for x in error.absolute_path)}')
    print(f'{indent_str} schema path: {"/".join(str(x) for x in error.absolute_schema_path)}')
    print(f'{indent_str} message: {error.message}')
    if error.context:
        for sub_error in error.context:
            print(f'{indent_str}{"-" * 80}')
            print_schema_error(sub_error, indent=indent+4)



def flask_manager(args=None):
    from flask_script import Manager
    from flask_migrate import Migrate, MigrateCommand

    from studygovernor import create_app
    from studygovernor.models import db

    app = create_app(use_sentry=False)
    migrate = Migrate()
    migrate.init_app(app=app, db=db, directory='migrations')
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    manager.run()


def run_callback():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='Run a callback')
    parser.add_argument('-c', '--callback_execution_url', type=str, help="URL of the callback execution", required=True)
    args = parser.parse_args()

    from studygovernor import create_app
    from studygovernor import models
    from studygovernor.util.helpers import get_object_from_arg
    callback_execution_id = None

    app = create_app()

    if args.action_url:
        parts = args.action_url.split('/')
        if parts[-2] == 'callback_executions': # get action id from url
            callback_execution_id = int(parts[-1])

    if callback_execution_id is None:
        print('Invalid callback_execution url {}'.format(args.callback_execution_url))
        sys.exit(-1)

    with app.app_context():
        callback_execution = get_object_from_arg(callback_execution_id, models.CallbackExecution)

        if not callback_execution:
            print('No callback_execution found for {}'.format(args.callback_execution_url))
            sys.exit(-1)

        from studygovernor.callbacks import master_callback

        callback: 'models.Callback' = callback_execution.callback  # Typehint because it's a backreference

    master_callback(callback_function=callback.function,
                    callback_arguments=callback.callback_arguments,
                    callback_execution_url=callback_execution.uri(),
                    callback_execution_secret=callback_execution.secret_key,
                    config=dict(app.config))

'''
Add a user to the StudyGovernor instance.
'''
def create_user(args=None):
    import argparse

    from datetime import datetime

    from studygovernor import create_app
    from studygovernor import models
    from studygovernor import user_datastore
    from flask_security import hash_password

    parser = argparse.ArgumentParser(description="Add a user to the StudyGovernor instance.")
    parser.add_argument('-u', '--username', required=True, help="Username")
    parser.add_argument('-p', '--password', required=True, help="Password")
    parser.add_argument('-n', '--full-name', required=True, help="Full name of the user")
    parser.add_argument('-e', '--email', required=True, help="User e-mail.")
    parser.add_argument('-i', '--inactive', default=False, action='store_true', help="If the user starts active or not", required=False)
    parser.add_argument('-f', '--force', action='store_true', default=False, help="Do not ask questions, just do it")
    args = parser.parse_args(args=args)

    app = create_app()
    with app.app_context():
        db = models.db

        user = {"username": args.username,
                "password": hash_password(args.password),
                "name": args.full_name,
                "email": args.email,
                "active": not args.inactive,
                "confirmed_at": datetime.now()
                }
        db_user = user_datastore.create_user(**user)

        doit = False
        if not args.force:
            doit = input("Are you sure you want to commit user [{}], to database '{}' [yes/no]: ".format(user['username'], app.config['SQLALCHEMY_DATABASE_URI'])) == 'yes'
        if doit or args.force:
            db.session.commit()
            print("\n * Committed to the database.")
        else:
            db.session.rollback()
            print("\n * Cancelled.")

'''
Populate the database with generated values
'''
def bootstrap_db(args=None):
    import argparse
    import random
    import datetime
    from studygovernor import create_app
    from studygovernor.models import db, Action, Cohort, Experiment, Scan, Scantype, State, Subject, Transition, Workflow
    from studygovernor.util.helpers import initialize_workflow
    from studygovernor.control import create_experiment

    parser = argparse.ArgumentParser(description="Bootstrap the db with generated values for testing purposes")
    parser.add_argument('--wipe', action='store_true', default=False, help="Wipe the tables before populating")
    parser.add_argument('--workflow-file', default="./resources/test-data-celery/workflow/studygovernor-workflow.yaml")
    parser.add_argument('-e', '--experiments', type=int, default=100, help="Number of experiments, default is 1000")
    parser.add_argument('-s', '--subjects', type=int, default=100, help="Number of subjects, default is 1000")
    parser.add_argument('--scans', type=int, default=100, help="Number of scans, default is 1000")

    args = parser.parse_args(args=args)
    
    app = create_app()
    
    with app.app_context():
        if args.wipe:
            Action.query.delete()
            Transition.query.delete()
            State.query.delete()
            Scan.query.delete()
            Experiment.query.delete()
            Subject.query.delete()
            Cohort.query.delete()
            Workflow.query.delete()
            db.session.commit()

        # Create a workflow from the template file
        initialize_workflow(args.workflow_file, app=app, verbose=True, upgrade=True)
        workflow = Workflow.query.one()
        print(f"Using workflow: {workflow}")

        # Make a cohort
        test_cohort = Cohort(label="Test_cohort", description="Test cohort")
        db.session.add(test_cohort)
        db.session.commit()

        # Add subjects
        subjects = list()
        for i in range(args.subjects):
            subject = Subject(label=f"generated_subject_{i}", date_of_birth=datetime.datetime(2022,12,1), cohort=test_cohort)
            db.session.add(subject)
            subjects.append(subject)

        # Add experiments
        experiments = list()
        for i in range(args.experiments):
            experiment = create_experiment(workflow, label=f"generated_experiment_{i}", scandate=datetime.datetime(2022,12,1), subject=random.choice(subjects))
            db.session.add(experiment)
            experiments.append(experiment)
        # Add scans
        scantype = Scantype.query.first() 
        scans = list()
        for i in range(args.scans):
            scan = Scan(experiment=random.choice(experiments), scantype=scantype)
            db.session.add(scan)
            scans.append(scan)

        db.session.commit()
        print("Finished populating the database with generated values.")




if __name__ == "__main__":
    import sys
    sys.exit("This is where entry points are defined. Look for studygov-* executables on the path.")
