from flask_restx import fields
from .base import api


action_summary = api.model('ActionSummary', {
    'id': fields.Integer,
    'success': fields.Boolean,
    'return_value': fields.String,
    'uri': fields.Url('api_v2.action')
})

callback_summary = api.model('CallbackSummary', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.callback')
})

callback_execution_summary = api.model('CallbackExecutionSummary', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.callback_execution')
})

cohort_summary = api.model('CohortSummary', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.cohort'),
    'label': fields.String
})

experiment_summary = api.model('ExperimentSummary', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.experiment')
})

role_summary = api.model("RoleSummary", {
    'id': fields.Integer,
    'name': fields.String,
    'uri': fields.Url('api_v2.role')
})

state_summary = api.model('StateSummary', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.state')
})

subject_summary = api.model('SubjectSummary', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.subject')
})

transition_summary = api.model('TransitionSummary', {
    'id': fields.Integer,
    'uri': fields.Url('api_v2.transition')
})

workflow_summary = api.model('WorkflowSummary', {
    'id': fields.Integer,
    'label': fields.String,
    'uri': fields.Url('api_v2.workflow')
})