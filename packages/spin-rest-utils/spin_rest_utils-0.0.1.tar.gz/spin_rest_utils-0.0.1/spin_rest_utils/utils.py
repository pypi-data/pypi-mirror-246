def base_request(terminal_id, auth_key):
    return {}

def sale_request_dict(dollar_amount, payment_type, ref_id, capture_signature):
    return {}

def txn_status_request_dict(payment_type, ref_id):
    return {}

def error_message_from_response(response_json):
    return ''

def api_response_successful(response_json):
    return False

def insecure_entry_type(response_json):
    return True

def approved_amount(response_json):
    return 0

def signature_from_response(response_json):
    return ''

def txn_info_from_response(response_json):
    return {}

def processed_response_info(response_json):
    return '', {}, {}, ''

def no_retry_error(response_json):
    return False

def better_error_message(error_message, response, terminal_id, format_currency):
    return {'error': "SPIn Terminal API not implemented"}

def get_call_url(base_url, type=''):
    return ''