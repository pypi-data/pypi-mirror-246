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

import datetime
import os
import textwrap
import yaml
from functools import wraps
from pathlib import Path
from typing import Dict, Optional, Type, TypeVar, Union
from urllib.parse import urljoin

from flask import url_for, request, current_app
from flask_security import SQLAlchemyUserDatastore, current_user
from flask_security.utils import hash_password
from flask_security.decorators import _check_http_auth, handle_csrf, set_request_attr
from sqlalchemy.orm.attributes import QueryableAttribute

from .. import models
from .. import exceptions

T = TypeVar("T")


def get_object_from_arg(id: Optional[Union[str, int]],
                        model: Type[T],
                        model_name: QueryableAttribute = None,
                        skip_id: bool = False,
                        allow_none: bool = False,
                        filters: Dict = None) -> T:
    # Set initial return data to None already
    data = None

    # Check if id is already a valid instance of model
    if isinstance(id, model):
        return id

    if id is not None:
        # If we have a URI/path we just want the last part
        if isinstance(id, str) and '/' in id:
            id = id.rsplit('/', 1)[1]

        # For id try to cast to an int
        if not skip_id:
            try:
                id = int(id)
            except (TypeError, ValueError) as e:
                pass
        else:
            id = str(id)

        # Create base query
        if isinstance(id, int):
            query = model.query.filter(model.id == id)
        elif model_name is not None:
            query = model.query.filter(model_name == id)
        else:
            query = None
        
        # If there is a query, add filters and run query
        if query is not None:
            if filters is not None:
                for key, value in filters.items():
                    query = query.filter(key == value)
                
            data = query.one_or_none()
        
    # Check if there is data or None is allowed
    if data is None and not allow_none:
        raise exceptions.CouldNotFindResourceError(id, model)

    return data


def get_uri(route: str,
            id: Union[str, int],
            blueprint: str = None):
    if blueprint is None:
        blueprint = request.blueprint or 'api_v1'

    if current_app.config.get('STUDYGOV_EXTERNAL_HOSTNAME', None):
        external_hostname = current_app.config['STUDYGOV_EXTERNAL_HOSTNAME']
        external_proto = current_app.config.get('STUDYGOV_EXTERNAL_PROTO', 'http')
        external_port = current_app.config.get('STUDYGOV_EXTERNAL_PORT', 8000)
        relative_url = url_for(f'{blueprint}.{route}', id=id)
        exec_url = urljoin(f"{external_proto}://{external_hostname}:{external_port}", relative_url)
    else:
        exec_url = url_for(f'{blueprint}.{route}', id=id, _external=True)

    return exec_url

 
def create_workflow(workflow_definition, verbose=False):
    
    db = models.db

    if verbose:
        def do_print(message):
            print(message)
    else:
        def do_print(message):
            pass

    workflow_label = workflow_definition['label']
    workflow = models.Workflow(label=workflow_label)

    do_print("\n * Importing states:")
    states = dict()
    transitions = []
    for state in workflow_definition.get('states'):
        # Allow callback to be defined as nested JSON rather than a string containing escaped JSON
        states[state['label']] = models.State(label=state['label'],
                                                freetext=state['freetext'],
                                                workflow=workflow)
        db.session.add(states[state['label']])

        do_print(f"\t - {state['label']}")

        # Add callbacks
        if state.get('callbacks'):
            callbacks = []
            for callback in state['callbacks']:
                arguments = callback['callback_arguments']
                variable_map = callback.get('variable_map') or ''

                if not isinstance(arguments, str):
                    arguments = yaml.safe_dump(arguments)

                if not isinstance(variable_map, str):
                    variable_map = yaml.safe_dump(variable_map)

                callback = models.Callback(
                    label=callback['label'],
                    function=callback['function'],
                    callback_arguments=arguments,
                    variable_map=variable_map,
                    run_timeout=callback.get('run_timeout'),
                    wait_timeout=callback.get('wait_timeout'),
                    initial_delay=callback.get('initial_delay'),
                    description=callback.get('description'),
                    condition=callback.get('condition'),
                )

                db.session.add(callback)
                callbacks.append(callback)
                do_print(f"\t  +- callback {callback.label}")

            # Add callback links to state object
            states[state['label']].callbacks = callbacks
        else:
            do_print('\t  +- no callbacks!')

        # Add transitions to list to create
        if state.get('transitions'):
            for transition in state['transitions']:
                transitions.append((state['label'],
                                    transition['destination'],
                                    transition.get('condition')))
                do_print(f'\t  +- transitions to {transition["destination"]}')
        else:
            do_print('\t  +- no transitions!')

    do_print("\n * Importing transitions:")
    for source, destination, condition in transitions:
        db.session.add(models.Transition(source_state=states[source],
                                            destination_state=states[destination],
                                            condition=condition))
        do_print("\t - {} -> {} (condition {})".format(states[source],
                                                        states[destination],
                                                        condition))
    return workflow
    
def initialize_workflow(workflow, app, verbose=False, force=True, upgrade=False):
    
    if verbose:
        def do_print(message):
            print(message)
    else:
        def do_print(message):
            pass
    
    if isinstance(workflow, (str, Path)):
        try:
            with open(workflow) as fh:
                workflow_definition = yaml.safe_load(fh)
        except IOError as error:
            print("IOError: {}".format(error))
            print("Please specify a valid YAML file.")
            return
    else:
        workflow_definition = workflow

    db = models.db

    try:
        workflow_label = workflow_definition['label']
    except KeyError:
        print(f'Workflow definition should contain a label to manage multiple versions.')
        return

    with app.app_context():
        workflow = models.Workflow.query.filter(models.Workflow.label == workflow_label).one_or_none()
        if not upgrade:
            if workflow is not None:
                print(f"Workflow {workflow_label} already exists. Set upgrade parameter to upgrade existing workflow.")
                return
            try:
                workflow = create_workflow(workflow_definition, verbose=verbose)
            except Exception as exc:
                print(f"Workflow definition is invalid. Original error message: {exc}")
                return
        else:
            if workflow is None:
                print(f"Workflow {workflow_label} does not exist. If you want to create a new workflow, remove upgrade parameter.")
                return
            try:
                upgrade_result = upgrade_workflow(workflow=workflow,
                                                workflow_definition=workflow_definition,
                                                db=db,
                                                verbose=verbose)
            except Exception as exc:
                print(f"Workflow definition is invalid. Original error message: {exc}")
                return

            if not upgrade_result:
                print("[ERROR] Cannot perform workflow upgrade")
                return

        if 'external_systems' in workflow_definition:
            print("[WARNING] External systems are no longer defined as part of a workflow, "
                  "but as part of the config! Ignoring external_systems section")

        if 'scantypes' in workflow_definition:
            print("[WARNING] Scantypes are no longer defined as part of a workflow, "
                  "but as part of the config! Ignoring scantypes section")

        doit = False
        if not force:
            doit = input("Are you sure you want to commit this to '{}' [yes/no]: ".format(app.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)[1])) == 'yes'

        if doit or force:
            db.session.commit()
            do_print("\n * Committed to the database.")
        else:
            db.session.rollback()
            do_print("\n * Cancelled the initialisation of the workflows.")


def upgrade_workflow(workflow, workflow_definition, db, verbose: bool = False):
    if verbose:
        def do_print(message):
            print(message)
    else:
        def do_print(message):
            pass
    
    new_states = []
    edit_states = []
    old_states = {x.label: x for x in workflow.states}
    old_transitions = models.Transition.query.filter(
        models.Transition.source_state.has(models.State.workflow == workflow) |
        models.Transition.destination_state.has(models.State.workflow == workflow)
    ).all()

    new_transitions = []
    edit_transitions = []
    old_transitions = {(x.source_state.label, x.destination_state.label): x for x in old_transitions}

    # Check what to do with states
    for new_state in workflow_definition['states']:
        old_state = old_states.pop(new_state['label'], None)
        if old_state is not None:
            edit_states.append(new_state)
        else:
            new_states.append(new_state)

    # Check what to do with transitions
    for new_transition in workflow_definition['transitions']:
        old_transition = old_transitions.pop((new_transition['source'], new_transition['destination']), None)

        if old_transition is not None:
            edit_transitions.append(new_transition)
        else:
            new_transitions.append(new_transition)

    old_transitions = list(old_transitions.values())
    old_states = list(old_states.values())

    safe_delete = True
    # Check if transitions can be deleted
    for old_transition in old_transitions:
        action_count = len(old_transition.actions)
        if action_count > 0:
            do_print(f"[WARNING] Transition {old_transition} should be deleted but"
                  f" cannot be due to related {action_count} actions")
            safe_delete = False

    # Check if states can be deleted
    for old_state in old_states:
        action_count = models.Action.query.filter(models.Action.transition.has(
            (models.Transition.source_state == old_state) |
            (models.Transition.destination_state == old_state)
        )).count()
        if action_count > 0:
            do_print(f"[WARNING] State {old_state.label} should be deleted but"
                  f" cannot be due to {action_count} related actions")
            safe_delete = False

        for old_transition in old_state.transition_sources:
            if old_transition not in old_transitions:
                do_print(f"[WARNING] State {old_state.label} should be deleted but "
                      f"cannot because transition {old_transition} is not to be "
                      f"deleted!")
                safe_delete = False

        for old_transition in old_state.transition_destinations:
            if old_transition not in old_transitions:
                do_print(f"[WARNING] State {old_state.label} should be deleted but "
                      f"cannot because transition {old_transition} is not to be "
                      f"deleted!")
                safe_delete = False

    if not safe_delete:
        do_print(f"[ERROR] Not all resources that should be deleted can be deleted, aborting!")
        return None

    do_print(f"[INFO] Ready to start applying changes")
    do_print("\n * Importing new states:")
    states = {}
    for state in new_states:
        callback = state['callback']

        # Allow callback to be defined as nested JSON rather than a string containing escaped JSON
        if not isinstance(callback, str) and callback is not None:
            callback = yaml.safe_dump(callback)

        state_obj = models.State(label=state['label'],
                                 callback=callback,
                                 freetext=state['freetext'],
                                 workflow=workflow)
        states[state['label']] = state_obj
        db.session.add(state_obj)
        do_print("\t - {}".format(state['label']))

    do_print("\n * Updating existing states:")
    for state in edit_states:
        callback = state['callback']

        # Allow callback to be defined as nested YAML/JSON rather than a string containing escaped YAML/JSON
        if callback is None:
            callback_data = None
            callback_str = None
        elif not isinstance(callback, str):
            callback_str = yaml.safe_dump(callback)
            callback_data = callback
        else:
            callback_str = callback
            callback_data = yaml.safe_load(callback)

        # Get current state
        current_state = models.State.query.filter(
            (models.State.label == state['label']) &
            (models.State.workflow == workflow)
        ).one()

        if current_state.callback is None:
            current_callback_data = None
        else:
            current_callback_data = yaml.safe_load(current_state.callback)

        # Update fields
        changes = {}
        if current_callback_data != callback_data:
            changes['callback'] = "\n" + textwrap.indent(f"FROM:\n{current_state.callback}\nTO:\n{callback_str}", "\t\t | ")
            current_state.callback = callback_str
        if current_state.freetext != state['freetext']:
            changes['freetext'] = state['freetext']
            current_state.freetext = state['freetext']

        states[state['label']] = current_state

        if changes:
            do_print(f"\t - {state['label']}")
            for key, value in changes.items():
                do_print(f"\t\t - set {key}={value}")

    do_print("\n * Deleting old states:")
    for state in old_states:
        db.session.delete(state)
        do_print(f"\t - {state.label}")

    do_print("\n * Importing new transitions:")
    for transition in new_transitions:
        db.session.add(models.Transition(source_state=states[transition['source']],
                                         destination_state=states[transition['destination']]))
        do_print(f"\t - {transition['source']} -> {transition['destination']}")

    do_print("\n * Keeping existing transitions transitions:")
    for transition in edit_transitions:
        do_print(f"\t - {transition['source']} -> {transition['destination']}")

    do_print("\n * Deleting old transitions:")
    for transition in old_transitions:
        db.session.delete(transition)
        do_print(f"\t - {transition.source_state.label} -> {transition.destination_state.label}")

    return workflow


def has_permission_any(*args):
    return any(current_user.has_permission(perm) for perm in args)


def has_permission_all(*args):
    return all(current_user.has_permission(perm) for perm in args)


def http_auth_optional(realm):
    """Decorator that protects endpoints using Basic HTTP authentication.

    :param realm: optional realm name

    If authentication fails, this version will continue normally! This is to
    enable secondary fall-back with tokens.

    Once authenticated, if so configured, CSRF protection will be tested.

    ... warning::
        Auth is optional, so this will not prohibit access to the route without further logic!

    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if _check_http_auth():
                handle_csrf("basic")
                set_request_attr("fs_authn_via", "basic")
            return fn(*args, **kwargs)

        return wrapper

    if callable(realm):
        return decorator(realm)
    return decorator
