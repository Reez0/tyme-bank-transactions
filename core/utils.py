from typing import Any, Dict, List, Optional, Union
from flask import jsonify


def row_to_dict(row):
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


def make_response(status: int = None, message: Optional[str] = None, success: bool = None, data: Union[dict, None, List[dict]] = None):
    return jsonify({"success": success, "message": message, "data": data}), status


def validate_transaction(transaction: Dict[str, str]) -> Any:
    errors = []
    required: List[str] = ['amount', 'type', 'description', 'date']
    available_keys = transaction.keys()
    if not set(required) == set(available_keys):
        missing_items = list(set(required).difference(set(available_keys)))
        for missing in missing_items:
            errors.append({missing: "Must be provided"})
    if float(transaction['amount']) <= 0:
        errors.append({"amount": "Amount must be greater than 0"})
    if transaction['type'] not in ['credit', 'debit']:
        errors.append({"type": "Must be one of credit or debit"})
    if len(transaction['description']) < 1:
        errors.append(
            {"description": "Description must contain more than 1 character"})
    return errors
