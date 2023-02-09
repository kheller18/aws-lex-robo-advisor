### Required Libraries ###
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from botocore.vendored import requests

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")

def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }

def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }

def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

    # validates slots based on DialogCodeHook event
    if source == 'DialogCodeHook':
        all_slots = get_slots(intent_request)

        # validate inputs from lex age and investment amount 
        validation_result = validate_inputs(age, investment_amount)

        if not validation_result['isValid']:
            all_slots[validation_result["violatedSlot"]] = None

            # returns asking for new data if inputs don't match constraints
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                all_slots,
                validation_result["violatedSlot"],
                validation_result["message"]
            )

        # Fetch current session attributes
        session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(session_attributes, all_slots)

    # required slots are validated and ready to provide portfolio recommendation
    portfolio_recommendation = get_recommendation(risk_level)

    # final return message with recommended portfolio percentages
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": f"Thank you! The recommended diversification for you based on your risk level is: {portfolio_recommendation}"
        },
    )

### gives advice based users' choice of aggressiveness ###
def get_recommendation(risk_level):
    """Returns percentage split for bonds and equities based on users' agressiveness"""

    if risk_level == 'None':
        return '100% bonds (AGG), 0% equities (SPY).'
    elif risk_level == 'Low':
        return '60% bonds (AGG), 40% equities (SPY).'
    elif risk_level == 'Medium':
        return '40% bonds (AGG), 60% equities (SPY).'
    elif risk_level == 'High':
        return '20% bonds (AGG), 80% equities (SPY).'
    else:
        return '100% bonds (AGG), 0% equities (SPY) - (Invalid risk-level, default portfolio recommended).'

### validates age and investment amount ###
def validate_inputs(age, investment_amount):
    """ Checks to make sure age is valid so you don't try and change NaN to float """
    if age is not None:
        age = float(age)

        """ Age constraint """
        if age <= 0 or age >= 65:
            return build_validation_result(
                False,
                'age',
                'The age you entered is invalid. Please enter an age between 0 and 65.'
            )

    """ Checks to make sure investment amount is valid so you don't try and change NaN to float """
    if investment_amount is not None:
        investment_amount = float(investment_amount)

        """ Checks against constraint """
        if investment_amount < 5000:
            return build_validation_result(
                False,
                'investmentAmount',
                'The investment amount you entered is invalid. Please enter an amount greater than or equal to $5000.'
            )

    return build_validation_result(True, None, None)

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "recommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")

### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
