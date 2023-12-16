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
import enum
import json
import secrets
from typing import Any, Tuple

import isodate

from flask import url_for, request, current_app
from sqlalchemy import and_, func, event
from sqlalchemy.orm.attributes import get_history
from flask_sqlalchemy import SQLAlchemy

from .auth.models import BaseUser
from .auth.models import BaseRole
from .util.helpers import get_uri

# Get the database
db = SQLAlchemy()


class Workflow(db.Model):
    __tablename__ = 'workflow'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), unique=True, nullable=False)

    states = db.relationship("State", back_populates="workflow")


class Cohort(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    subjects = db.relationship("Subject", back_populates="cohort")
    external_system_urls = db.relationship("ExternalCohortUrls", back_populates='cohort')

    @property
    def external_urls(self):
        return {x.external_system.system_name: x.url for x in self.external_system_urls}


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), unique=False, nullable=False)
    date_of_birth = db.Column(db.DATE, nullable=False)

    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id', name='fk_subject_cohort_id_cohort'), nullable=False)
    cohort = db.relationship("Cohort", back_populates='subjects')

    experiments = db.relationship("Experiment", back_populates="subject")
    external_subject_links = db.relationship("ExternalSubjectLinks", back_populates="subject")

    __table_args__ = (db.UniqueConstraint('cohort_id', 'label', name='uix_cohort_id_label'),)


    def __repr__(self):
        return f"<Subject label={self.label}, id={self.id}, dob={self.date_of_birth}>"

    @property
    def external_ids(self):
        return {x.external_system.system_name: x.external_id for x in self.external_subject_links}

    @property
    def api_uri(self) -> str:
        return get_uri(route="subject",
                       id=self.id)

    @property
    def web_uri(self) -> str:
        return get_uri(route="web_subject",
                       id=self.id,
                       blueprint="web")


class ExternalSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    system_name = db.Column(db.VARCHAR(100), unique=True)
    url = db.Column(db.VARCHAR(512))

    external_subject_links = db.relationship("ExternalSubjectLinks", back_populates="external_system")
    external_experiment_links = db.relationship("ExternalExperimentLinks", back_populates="external_system")
    external_cohort_urls = db.relationship("ExternalCohortUrls", back_populates='external_system')

    history = db.relationship('ExternalSystemHistory', back_populates='external_system', lazy=True)

    def __init__(self, id=None, system_name=None, url=None):
        if id is not None:
            self.id = id

        self.system_name = system_name
        self.url = url

    def __repr__(self):
        return "<ExternalSystem {} (id={})>".format(self.system_name, self.id)


class ExternalSystemHistory(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)

    system_id = db.Column(db.INTEGER, db.ForeignKey('external_system.id'), nullable=False)
    external_system = db.relationship('ExternalSystem', back_populates='history', lazy=True)

    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    url = db.Column(db.Text)


@event.listens_for(ExternalSystem, "after_insert")
@event.listens_for(ExternalSystem, "after_update")
def log_history(mapper, connection, target):
    external_system_history_table = ExternalSystemHistory.__table__
    value_changed = get_history(target, 'url').unchanged == ()
    if value_changed:
        connection.execute(
            external_system_history_table.insert().values(system_id=target.id, url=target.url)
        )


class ExternalCohortUrls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.VARCHAR(1024))

    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id', name='fk_external_cohort_links_cohort_id_cohort'))
    cohort = db.relationship("Cohort", back_populates='external_system_urls')

    external_system_id = db.Column(db.Integer, db.ForeignKey('external_system.id', name='fk_external_cohort_urls_external_system_id_external_system'))
    external_system = db.relationship("ExternalSystem", back_populates='external_cohort_urls')

    __table_args__ = (db.UniqueConstraint('cohort_id', 'external_system_id', name='uix_cohort_id_external_system_id'),)


class ExternalSubjectLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(1024))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', name='fk_external_subject_links_subject_id_subject'))
    subject = db.relationship("Subject", back_populates='external_subject_links')

    external_system_id = db.Column(db.Integer, db.ForeignKey('external_system.id', name='fk_external_subject_links_external_system_id_external_system'))
    external_system = db.relationship("ExternalSystem", back_populates='external_subject_links')

    # Make sure every link can only exist once (one external id per combination of experiment and system)
    __table_args__ = (db.UniqueConstraint('subject_id', 'external_system_id', name='uix_subject_id_external_system_id'),)

    def __init__(self, external_id=None, subject=None, external_system=None):
        self.external_id = external_id
        self.subject = subject
        self.external_system = external_system

    def __repr__(self):
        return "<ExternalSubjectLink subject={}, external_id={}, external_system={}>".format(self.subject, self.external_id, self.external_system)


class ExternalExperimentLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.VARCHAR(1024))

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', name='fk_external_experiment_links_experiment_id_experiment'))
    experiment = db.relationship("Experiment", back_populates='external_experiment_links')

    external_system_id = db.Column(db.Integer, db.ForeignKey('external_system.id', name='fk_external_experiment_links_external_system_id_external_system'))
    external_system = db.relationship("ExternalSystem", back_populates='external_experiment_links')

    # Make sure every link can only exist once (one external id per combination of experiment and system)
    __table_args__ = (db.UniqueConstraint('experiment_id', 'external_system_id', name='uix_experiment_id_external_system_id'),)

    def __init__(self, external_id=None, experiment=None, external_system=None):
        self.external_id = external_id
        self.experiment = experiment
        self.external_system = external_system

    def __repr__(self):
        return "<ExternalExperimentLink experiment={}, external_id={}, external_system={}>".format(self.experiment, self.external_id, self.external_system)


class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', name='fk_scan_experiment_id_experiment'))
    experiment = db.relationship("Experiment", back_populates='scans')

    scantype_id = db.Column(db.Integer, db.ForeignKey('scantype.id', name='fk_scan_scantype_id_scantype'))
    scantype = db.relationship("Scantype", back_populates='scans')

    def __init__(self, experiment=None, scantype=None):
        self.experiment = experiment
        self.scantype = scantype

    def __repr__(self):
        return "<Scan experiment={}, scantype={}>".format(self.experiment, self.scantype)


class Scantype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modality = db.Column(db.VARCHAR(100), nullable=False)
    protocol = db.Column(db.VARCHAR(100), nullable=False, unique=True)

    scans = db.relationship("Scan", back_populates='scantype')

    def __init__(self, id=None, modality=None, protocol=None):
        if id is not None:
            self.id = id

        self.modality = modality
        self.protocol = protocol

    def __repr__(self):
        return "<Scantype modality={}, protocol={}, id={}>".format(self.modality, self.protocol, self.id)


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), nullable=False, unique=False)
    scandate = db.Column(db.DateTime, nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', name='fk_experiment_subject_id_subject'))
    subject = db.relationship("Subject", back_populates='experiments')

    scans = db.relationship("Scan", cascade="all, delete-orphan", back_populates='experiment')
    actions = db.relationship("Action", cascade="all, delete-orphan", back_populates='experiment')
    variables = db.relationship("Variable", cascade="all, delete-orphan", back_populates='experiment')
    external_experiment_links = db.relationship("ExternalExperimentLinks",
                                                cascade="all, delete-orphan",
                                                back_populates="experiment")

    __table_args__ = (db.UniqueConstraint('subject_id', 'label', name='uix_subject_id_label'),)

    @property
    def state(self) -> 'State':
        action = self.last_action

        if action is None:
            return None

        return action.transition.destination_state

    @property
    def external_ids(self):
        return {x.external_system.system_name: x.external_id for x in self.external_experiment_links}

    @property
    def variable_map(self):
        return {var.label: VariableType.unpack(var.value, var.type) for var in self.variables}

    @property
    def last_action(self) -> 'Action':
        return Action.query.filter(Action.experiment == self).order_by(Action.start_time.desc(), Action.id.desc()).first()

    @property
    def api_uri(self) -> str:
        return get_uri(route="experiment",
                       id=self.id)

    @property
    def web_uri(self) -> str:
        return get_uri(route="web_experiment",
                       id=self.id,
                       blueprint="web")

    def find_external_id(self, external_system_name):
        result = tuple(x for x in self.external_experiment_links if x.external_system.system_name == external_system_name)
        if len(result) != 1:
            raise ValueError("Found multiple links to external system")

        return result[0].external_system_id

    def __repr__(self):
        return f"<Experiment label={self.label}, id={self.id}, subject={self.subject_id}, scandate={self.scandate}>"


class VariableType(enum.Enum):
    none = 'none'
    bool = 'bool'
    int = 'int'
    float = 'float'
    str = 'str'
    date = 'date'
    datetime = 'datetime'
    time = 'time'
    json = 'json'

    @classmethod
    def pack(cls,
             value: Any) -> Tuple['VariableType', str]:
        if value is None:
            return cls.none, 'None'
        if isinstance(value, bool):
            return cls.bool, str(value)
        elif isinstance(value, int):
            return cls.int, str(value)
        elif isinstance(value, float):
            return cls.float, str(value)
        elif isinstance(value, str):
            return cls.str, value
        elif isinstance(value, datetime.datetime):
            return cls.datetime, value.isoformat()
        elif isinstance(value, datetime.date):
            return cls.date, value.isoformat()
        elif isinstance(value, datetime.time):
            return cls.time, value.isoformat()
        else:
            return cls.json, json.dumps(value)

    @classmethod
    def unpack(cls,
               value: str,
               var_type: 'VariableType') -> Any:
        if not isinstance(var_type, cls):
            raise TypeError('var_type should be a valid VariableType!')

        if var_type == cls.none:
            return None
        elif var_type == cls.bool:
            return value.lower() == 'true'
        elif var_type == cls.int:
            return int(value)
        elif var_type == cls.float:
            return float(value)
        elif var_type == cls.str:
            return value
        elif var_type == cls.datetime:
            return isodate.parse_datetime(value)
        elif var_type == cls.date:
            return isodate.parse_date(value)
        elif var_type == cls.time:
            return isodate.parse_time(value)
        elif var_type == cls.json:
            return json.loads(value)

        raise ValueError(f'Encountered unknown variable type: {var_type}')


class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', name='fk_variable_experiment_id_experiment'))
    experiment = db.relationship("Experiment", back_populates='variables')
    label = db.Column(db.VARCHAR(255))
    type = db.Column(db.Enum(VariableType), nullable=False)
    value = db.Column(db.Text)  # TODO: Should this be varchar? will we allow for (big) json values?

    # Make sure the label of a variable is unique per experiment
    __table_args__ = (db.UniqueConstraint('label', 'experiment_id', name='uix_label_experiment_id'),)


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    success = db.Column(db.Boolean, nullable=False)
    return_value = db.Column(db.Text)
    freetext = db.Column(db.Text)
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)

    # Link executions to the state
    executions = db.relationship("CallbackExecution", back_populates="action")

    transition_id = db.Column(db.Integer, db.ForeignKey('transition.id', name='fk_action_transition_id_transition'))
    transition = db.relationship("Transition", back_populates="actions")

    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id', name='fk_action_experiment_id_experiment'))
    experiment = db.relationship("Experiment", back_populates="actions")

    def __init__(self, experiment=None, transition=None, freetext=None):
        self.experiment = experiment
        self.transition = transition
        self.freetext = freetext
        self.success = False
        self.start_time = datetime.datetime.now()

    def __repr__(self):
        return "<Action transition={}, id={}, experiment={}, start_time={}>".format(self.transition, self.id, self.experiment, self.start_time)

    @property
    def api_uri(self) -> str:
        return get_uri(route="action",
                       id=self.id)

    @property
    def web_uri(self) -> str:
        return get_uri(route="web_action",
                       id=self.id,
                       blueprint="web")


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.VARCHAR(100), nullable=False)

    # Link callbacks to the state
    callbacks = db.relationship("Callback", back_populates="state")

    freetext = db.Column(db.Text)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id', name='fk_state_workflow_id_workflow'))
    workflow = db.relationship("Workflow", back_populates="states")

    # Make sure the combination of label and workflow id stays unique
    transition_sources = db.relationship("Transition",
                                         foreign_keys='Transition.source_state_id',
                                         back_populates="source_state")

    transition_destinations = db.relationship("Transition",
                                              foreign_keys='Transition.destination_state_id',
                                              back_populates="destination_state")

    __table_args__ = (db.UniqueConstraint('label', 'workflow_id', name='uix_label_workflow_id'),)


    def __repr__(self):
        if self.workflow:
            workflow_label = self.workflow.label
        else:
            workflow_label = 'none'

        return "<State state={}, id = {}, workflow = {}>".format(self.label, self.id, workflow_label)

    @property
    def experiments(self):
        # Find last start_time of actions related to a single experiment
        last_times = db.session.query(Action.experiment_id, func.max(Action.start_time).label('last_time')).group_by(Action.experiment_id).subquery()

        # Find last id in case start_times are duplicated
        last_actions = db.session.query(Action.experiment_id, func.max(Action.id).label('latest_action_ids'), Action.start_time).join((last_times, and_(Action.experiment_id == last_times.c.experiment_id, Action.start_time == last_times.c.last_time))).group_by(Action.experiment_id, Action.start_time).subquery()

        # Join Experiment all the way to State
        return db.session.query(Experiment).join(Action).join((last_actions, Action.id == last_actions.c.latest_action_ids)).join(Transition).join(State, Transition.destination_state_id == State.id).filter(State.id == self.id).all()

    def get_transition_to(self, target_state):
        return Transition.query.filter(Transition.source_state == self,
                                       Transition.destination_state == target_state).one_or_none()


class Callback(db.Model):
    """"
    Data model representing the definition of a callback. This defines how a
    callback should be executed, but is not linked to a specific execution.
    """
    id = db.Column(db.Integer, primary_key=True)

    # State the callback belongs to
    state_id = db.Column(db.Integer, db.ForeignKey('state.id', name='fk_callback_state_id_state'))
    state = db.relationship("State", back_populates='callbacks')

    # Create a label that is unique per state
    label = db.Column(db.VARCHAR(128))

    # Link executions to the state
    executions = db.relationship("CallbackExecution", back_populates="callback")

    # Function to call for this callback
    function = db.Column(db.VARCHAR(128), nullable=False)

    # Arguments in json/yaml for the callback function
    callback_arguments = db.Column(db.Text)

    # Define which variables need to be stored
    variable_map = db.Column(db.Text)

    # time after which callback is considered timed-out
    # and fails (int, minutes, default=60 (hour))
    run_timeout = db.Column(db.Integer, default=60)

    # time after which a wait considered timed-out
    # and fails (int, in minutes, default=0, no wait stage)
    wait_timeout = db.Column(db.Integer, default=0)

    # time after which the callback is initiated, for
    # waiting on slow processes that proceeds this
    # operation (seconds)
    initial_delay = db.Column(db.Integer, default=0)

    # Some descriptive text (str, optional)
    description = db.Column(db.Text)

    # A rule to see if the callback can be fired
    # "experiment.vars['qc_T1_usable']"
    condition = db.Column(db.Text)

    __table_args__ = (db.UniqueConstraint('label', 'state_id', name='uix_label_state_id'),)


class CallbackExecutionStatus(str, enum.Enum):
    """"
    Defined the valid states for callback execution
    """
    created = 'created'
    skipped = 'skipped'
    queued = 'queued'
    running = 'running'
    waiting = 'waiting'
    finished = 'finished'

    def __str__(self):
        return self.value

    @property
    def resolved(self):
        return self in [self.skipped, self.finished]

    @property
    def badge_class(self):
        if self.value == 'finished':
            return 'info'
        else:
            return 'success'


class CallbackExecutionResult(str, enum.Enum):
    """"
    Defined the valid result categories for a callback execution
    """
    none = 'none'
    success = 'success'
    failed = 'failed'
    timeout = 'timeout'

    def __str__(self):
        return self.value

    @property
    def badge_class(self):
        if self.value == 'success':
            return 'success'
        elif self.value == 'none':
            return 'secondary'
        else:
            return 'danger'


class CallbackExecution(db.Model):
    """
    Data model representing one execution of a callback. Links back to the
    callback definition and the source action.
    """
    id = db.Column(db.Integer, primary_key=True)

    # Link callback execution to the correct Callback and Action
    callback_id = db.Column(db.Integer, db.ForeignKey('callback.id', name='fk_callbackexecution_callback_id_callback'))
    action_id = db.Column(db.Integer, db.ForeignKey('action.id', name='fk_callbackexecution_action_id_action'))

    callback: Callback = db.relationship("Callback", back_populates='executions')
    action: Action = db.relationship("Action", back_populates='executions')

    # Status/result can be one the defined values in the enum classes
    status = db.Column(db.Enum(CallbackExecutionStatus), default=CallbackExecutionStatus.created)
    result = db.Column(db.Enum(CallbackExecutionResult), default=CallbackExecutionResult.none)

    run_log = db.Column(db.Text)
    result_log = db.Column(db.Text)

    # Result values should be a YAML/JSON encoded string with the result dictionary
    result_values = db.Column(db.Text)

    # Default is to create a 128 bytes (256 hex chars) secret string with the secrets module
    secret_key = db.Column(db.VARCHAR(256), default=lambda: secrets.token_hex(128))

    # Keep track of main changes in status
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    run_start = db.Column(db.DateTime(timezone=True))
    wait_start = db.Column(db.DateTime(timezone=True))
    finished = db.Column(db.DateTime(timezone=True))

    def uri(self, blueprint: str = None) -> str:
        return get_uri(route="callback_execution",
                       id=self.id,
                       blueprint=blueprint)

    @property
    def api_uri(self) -> str:
        return get_uri(route="callback_execution",
                       id=self.id)

    @property
    def web_uri(self) -> str:
        return get_uri(route="web_action",
                       id=self.action.id,
                       blueprint="web")

    @property
    def experiment(self):
        return self.action.experiment

    @property
    def subject(self):
        return self.experiment.subject

    @property
    def cohort(self):
        # Hack for optional cohort to be queryable
        if not self.subject.cohort:
            return {'id': 0, 'label': 'no cohort'}
        return self.subject.cohort

    @property
    def external_systems(self):
        external_systems = {x.system_name: x.url for x in ExternalSystem.query.all()}
        return external_systems


class Transition(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    source_state_id = db.Column(db.Integer, db.ForeignKey('state.id', name='fk_transition_source_state_id_state'))
    source_state = db.relationship("State",
                                   back_populates="transition_sources",
                                   foreign_keys='Transition.source_state_id')

    destination_state_id = db.Column(db.Integer, db.ForeignKey('state.id', name='fk_transition_destination_state_id_state'))
    destination_state = db.relationship("State",
                                        back_populates="transition_destinations",
                                        foreign_keys='Transition.destination_state_id')

    actions = db.relationship("Action", back_populates="transition")

    # Allow a single condition for a transition
    condition = db.Column(db.Text)

    def __init__(self, id=None, source_state=None, destination_state=None, condition=None):
        if id is not None:
            self.id = id

        self.source_state = source_state
        self.destination_state = destination_state
        self.condition = condition

    def __repr__(self):
        return "<Transition: source={} -> destination={}, conditions={}, id={}>".format(self.source_state, self.destination_state, self.condition, self.id)


# User and Role models used for authentication and authorization
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id', name="fk_roles_users_user_id_user")),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id', name="fk_roles_users_role_id_role"))
                       )


class Role(db.Model, BaseRole):
    """ This implements the BaseRole from the .auth.models module.
    In this specific case, the BaseRole is sufficient. """
    __tablename__ = 'role'


class User(db.Model, BaseUser):
    __tablename__ = 'user'
    create_time = db.Column(db.DateTime(timezone=True), default=func.now())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f'<User {self.username} ({self.name})>'
