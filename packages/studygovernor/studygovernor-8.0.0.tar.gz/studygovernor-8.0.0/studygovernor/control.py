import datetime
import traceback

from jsonpointer import resolve_pointer
from flask import url_for, current_app, request
from sqlalchemy.exc import MultipleResultsFound
import yaml

from . import exceptions, models
from .callbacks import dispatch_callback
from .util.helpers import get_object_from_arg
from typing import Any, List, Optional, Union

db = models.db


def set_variable(experiment: models.Experiment,
                 label: str,
                 value: Any) -> models.Variable:
    """
    Pack a variable and set/update it for the experiment

    :param experiment: Experiment to set variable for
    :param label: Name of the variable
    :param value: The value of the variable
    :return: created/updated variable object
    """
    var_type, value = models.VariableType.pack(value)

    variable = models.Variable.query.filter(
        (models.Variable.experiment_id == experiment.id) &
        (models.Variable.label == label)
    ).one_or_none()

    if variable is None:
        variable = models.Variable(experiment_id=experiment.id,
                                   label=label,
                                   value=value,
                                   type=var_type)
        models.db.session.add(variable)
    else:
        variable.value = value
        variable.type = var_type

    # TODO: should we commit & refresh here or let it be done by the views?
    return variable


def get_variable(experiment: models.Experiment,
                 label: str) -> Any:
    # Get an unpacked variable for an experiment
    variable = models.Variable.query.filter(
        models.Variable.experiment_id == experiment.id,
        models.Variable.label == label
    ).one_or_none()

    if variable is None:
        raise KeyError(f'Variable {label} not found for {experiment}')

    return models.VariableType.unpack(variable.value, variable.type)


def get_variables(experiment: models.Experiment):
    variables = models.Variable.query.filter(models.Variable.experiment_id == experiment.id).all()
    return {var.label: models.VariableType.unpack(var.value, var.type) for var in variables}


def update_callback_execution_state(callback_execution: models.CallbackExecution,
                                    status: Union[models.CallbackExecutionStatus, str]):
    # The the argument and construct the correct enum
    if isinstance(status, str):
        status = models.CallbackExecutionStatus[status]

    # No action needed
    if callback_execution.status == status:
        return

    callback_execution.status = status

    if status == models.CallbackExecutionStatus.running and callback_execution.run_start is None:
        callback_execution.run_start = datetime.datetime.now()

    if status == models.CallbackExecutionStatus.waiting and callback_execution.wait_start is None:
        callback_execution.wait_start = datetime.datetime.now()

    if status.resolved and not callback_execution.finished:
        callback_execution.finished = datetime.datetime.now()

    # Check if variables need to be set
    if (status.resolved
            and callback_execution.result == models.CallbackExecutionResult.success
            and callback_execution.result_values
            and callback_execution.callback.variable_map):
        result_values = yaml.safe_load(callback_execution.result_values)
        variable_map = yaml.safe_load(callback_execution.callback.variable_map)

        # Set variables based on the variable map
        for target, source in variable_map.items():
            # Resolve a JSON pointer, if the source is just an string with a source, prepend / to turn it into a
            # valid JSON pointer. If the pointer cannot be resolved, use a None instead.
            if source != '' and source[0] != '/':
                source = '/' + source

            variable_value = resolve_pointer(result_values, source, None)
            set_variable(experiment=callback_execution.experiment,
                         label=target,
                         value=variable_value)


def get_subjects(cohort_label: Optional[str] = None,
                 offset: Optional[int] = None,
                 limit: Optional[int] = None,
                 order: Optional[str] = None):
    query = models.Subject.query
    
    if cohort_label is not None:
        query = query.filter(models.Subject.cohort.has(label=cohort_label))
    
    count = query.count()

    if order == 'asc':
        query = query.order_by(models.Subject.id.asc())
    elif order == 'desc':
        query = query.order_by(models.Subject.id.desc())

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    subjects = query.all()

    return subjects, count


def get_experiments(subject: Optional[str] = None,
                    scandate: Optional[datetime.datetime] = None,
                    state: Optional[str] = None,
                    offset: Optional[int] = None,
                    limit: Optional[int] = None,
                    order: Optional[str] = None):
    query = models.Experiment.query

    if subject is not None:
        query = query.filter(models.Experiment.subject_id == subject)

    if scandate is not None:
        query = query.filter(models.Experiment.scandate == scandate)

    if order == 'asc':
        query = query.order_by(models.Experiment.id.asc())
    elif order == 'desc':
        query = query.order_by(models.Experiment.id.desc())

    # This should move to the DB if possible, but querying on state is problematic
    if state is not None:
        state = get_object_from_arg(state, models.State, models.State.label)
        experiments = query.all()
        experiments = [x for x in experiments if x.state == state]

        # Do limit and offset post-hoc, as we can't use the DB for that
        count = len(experiments)
        if offset:
            experiments = experiments[offset:]

        if limit:
            experiments = experiments[:limit]
    else:
        # Count is safe as there shouldn't be duplicates possible in this list
        count = query.count()

        # Add limit and offset to query
        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        experiments = query.all()

    return experiments, count


def create_experiment(workflow: models.Workflow,
                      subject: models.Subject,
                      label: str,
                      scandate: datetime.datetime) -> models.Experiment:
    experiment = models.Experiment(
        subject=subject,
        label=label,
        scandate=scandate
    )

    # Find the one state in the workflow that has no incoming transitions
    try:
        root_state = models.State.query.filter(
            models.State.workflow == workflow
        ).filter(~models.State.transition_destinations.any()).one()
    except MultipleResultsFound:
        root_states = models.State.query.filter(
            models.State.workflow == workflow
        ).filter(~models.State.transition_destinations.any()).any()
        logging.error(f"Found multiple possible root states: {'|'.join(root_states)}")
        raise exceptions.StateChangeError()

    initial_transition = models.Transition.query.filter(models.Transition.source_state == root_state).one()
    transition_experiment(experiment, initial_transition)

    return experiment


class CallbackExecutionWrapper:
    def __init__(self,
                 callback_execution: 'models.CallbackExecution'):
        self.status = callback_execution.status
        self.result = callback_execution.result

        # If result values is set, unpack the data
        result_values = callback_execution.result_values
        if isinstance(result_values, str):
            yaml.safe_load(result_values)

        self.result_values = result_values


class ExperimentWrapper:
    def __init__(self,
                 experiment: 'models.Experiment'):
        # Copy out accessible data
        self.label = experiment.label
        self.scandate = experiment.scandate
        self.variables = {var.label: models.VariableType.unpack(var.value, var.type) for var in experiment.variables}
        self.state = experiment.state.label

    def __repr__(self):
        return f"<ExperimentWrapper label={self.label}, scandate={self.scandate}, state={self.state}, variables={self.variables}>"


def check_condition(condition: Optional[str],
                    experiment: 'models.Experiment',
                    callbacks: Optional[List['models.CallbackExecution']] = None) -> bool:
    # If there is no condition, it is True
    if condition is None or condition.strip() == '':
        return True

    # Create local environment for the condition
    if callbacks is None:
        callbacks = []

    local_vars = {
        'experiment': ExperimentWrapper(experiment),
        'callbacks': {x.callback.label: CallbackExecutionWrapper(x) for x in callbacks}
    }

    # Expose datetime module
    global_vars = {
        'datetime': datetime
    }
    print(f'Evaluating condition: {condition} for experiment: {experiment}')
    try:
        # Use eval to test the rule
        result = eval(condition, local_vars, global_vars)
    except Exception:
        stacktrace = traceback.format_exc()
        print(f'Error evaulating Callback Execution, experiment: { experiment}, condition: {condition}')
        print(f'  condition evaluation stacktrace: {traceback.format_exc()}')
        raise exceptions.ConditionFunctionCallFailedError(condition=condition, stacktrace=stacktrace)

    return bool(result)


def update_state(experiment: 'models.Experiment'):
    action = experiment.last_action

    # Help with type hinting as sqlachemy hasn't figured out it's a one-to-many
    executions: List['models.CallbackExecution'] = action.executions
    print(f'Updating state for experiment: { experiment}, last action: {action}')
    for execution in executions:
        # Check if all callback execution has finished
        if not execution.status.resolved:
            print(f'Callback execution {execution} not resolved yet!')
            return

    state = experiment.state

    # Mark action as ended
    action.end_time = datetime.datetime.now()
    action.success = True

    # Help with type hinting as sqlachemy hasn't figured out it's a one-to-many
    transitions: List['models.Transition'] = state.transition_sources

    transition_results = [{
        'transition_id': x.id,
        'destination': x.destination_state.label,
        'condition': x.condition,
        'test_result': None,
    } for x in transitions]

    for transition, result in zip(transitions, transition_results):
        print(f'Check transition: {transition}')
        if check_condition(transition.condition, experiment, executions):
            print(f'transition: {transition} returned True')
            result['test_result'] = True
            action.return_value = yaml.safe_dump(transition_results)
            db.session.commit()
            transition_experiment(experiment, transition)
            break
        else:
            result['test_result'] = False
            print(f'transition: {transition} returned False')


def set_state(experiment: 'models.Experiment',
              target_state: 'models.State',
              api_prefix: str = 'api_v1',
              freetext: Optional[str] = None):
    transition = experiment.state.get_transition_to(target_state)
    print(f'Desired transition: {transition}')

    if transition is None:
        raise exceptions.NoValidTransitionError(experiment.state, target_state)

    if freetext is None:
        freetext = "Transition triggered by setting state to {} ({})".format(
            target_state.label,
            target_state.id,
        )

    transition_experiment(experiment, transition, api_prefix, freetext)


def transition_experiment(experiment: models.Experiment,
                          transition: models.Transition,
                          api_prefix: str = 'api_v1',
                          freetext: Optional[str] = None):
    # Query all callbacks of the current state for checking the condition
    action = models.Action.query.filter(
        models.Action.experiment == experiment).order_by(
        models.Action.start_time.desc(), models.Action.id.desc()).first()

    if action is not None:
        callback_executions = action.executions
    else:
        callback_executions = []

    if transition.condition:
        result = check_condition(condition=transition.condition,
                                 experiment=experiment,
                                 callbacks=callback_executions)

        if not result:
            raise exceptions.ConditionNotMetError(experiment=experiment, transition=transition, condition=transition.condition)

    # Do the actual transition by creating an Action
    print('[INFO] Adding action')

    action = models.Action(experiment=experiment,
                           transition=transition,
                           freetext=freetext)

    print('Adding action: {}'.format(action))
    db.session.add(action)
    db.session.commit()
    print('Committed')

    # Dispatch the callback, or set to done if there is no callback
    if transition.destination_state.callbacks:
        print('Dispatching callbacks')
        for callback in transition.destination_state.callbacks:
            print(f'Dispatching callback {callback.label}')

            callback_execution = models.CallbackExecution(
                callback=callback,
                action=action,
            )
            db.session.add(callback_execution)
            db.session.commit()

            if check_condition(callback.condition, experiment=experiment):
                dispatch_callback(callback_execution,
                                  current_app.config)
            else:
                callback_execution.status = models.CallbackExecutionStatus.skipped
                db.session.commit()

        print('Dispatching done')

    else:
        action.success = True
        action.end_time = datetime.datetime.now()
        action.return_value = 'No callback for state'

