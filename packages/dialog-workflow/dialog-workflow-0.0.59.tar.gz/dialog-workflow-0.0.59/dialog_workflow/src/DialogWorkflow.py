from dotenv import load_dotenv
load_dotenv()
from variable_local.variable import *
from .TablesAsObjects import DialogWorkflowRecord
from .Act import action
from .utils import *
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.Logger import Logger
from circles_local_database_python.generic_crud import GenericCRUD
import random



object_to_insert = {
    'component_id': DIALOG_WORKFLOW_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': DIALOG_WORKFLOW_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'idan.a@circ.zone and guy.n@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)

generic_crud = GenericCRUD(default_schema_name='dialog_workflow')


def get_preferred_language(profile_id: int):
    logger.start(object={'profile_id': profile_id})
    language = logger.user_context.get_effective_profile_preferred_lang_code()
    logger.end(object={'language': language})
    return language

# Get all potential records in a specific state and choose randomly one of them


def get_dialog_workflow_record(profile_curr_state: int, language: str):
    logger.start(
        object={'profile_curr_state': profile_curr_state, 'language': language})
    optional_records = generic_crud.select_multi_tuple_by_where(view_table_name='dialog_workflow_state_view',
                                                                where="state_id = %s AND lang_code = %s", params=(profile_curr_state, language))
    random_index = random.randint(0, len(optional_records)-1)
    dialog_workflow_record = DialogWorkflowRecord(
        optional_records[random_index])
    logger.end(object={'dialog_workflow_record': str(dialog_workflow_record)})
    return dialog_workflow_record


def post_message(profile_id:  int, incoming_message: str):
    """This function is supposed to serve as a POST request later on using REST API.
    It runs until needing input from the user, which it then sends a json to the user with the message and exits
    PARAMS: 
        1. profile_id: the profile id that sent the request
        2. incoming_message: the message he sent"""
    # TODO: remove profile_id an use user context
    logger.start(object={'profile_id': profile_id,
                 'incoming_message': incoming_message})
    if profile_id is None:
        logger.user_context.get_effective_profile_id()
    variables = VariablesLocal()
    profile_curr_state = get_curr_state(profile_id)
    language = get_preferred_language(profile_id)
    got_response = True  # This variable indicates if we must act now as we got a response from the user or as if we should send one to him
    init_action = action(incoming_message, profile_id,
                         language, profile_curr_state, variables)
    while True:
        dialog_workflow_record = get_dialog_workflow_record(
            init_action.profile_curr_state, language)
        is_state_changed, outgoing_message = init_action.act(
            dialog_workflow_record, got_response)
        if outgoing_message != None:
            logger.end(object={'outgoing_message': outgoing_message})
            return outgoing_message
        init_action.profile_curr_state = dialog_workflow_record.next_state_id if is_state_changed == False else init_action.profile_curr_state
        update_profile_curr_state_in_DB(
            init_action.profile_curr_state, profile_id)
        got_response = False
