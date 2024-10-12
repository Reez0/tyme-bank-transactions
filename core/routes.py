from typing import List, Dict, Any
from flask import Blueprint, jsonify, request
from models import Transaction
from utils import make_response, validate_transaction
from db_operations import add_transaction, get_all_transactions, get_transaction, remove_transaction, update_transaction
import traceback

transaction_bp = Blueprint('transaction', __name__)


@transaction_bp.route('/', methods=['GET'])
def retrieve_all_transactions() -> Dict[str, Any]:
    """
    Retrieve all transactions
    ---
    tags:
      - Transactions
    responses:
      200:
        description: A list of transactions
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              amount:
                type: number
                format: float
              type:
                type: string
              description:
                type: string
              date:
                type: string
                format: date-time
      500:
        description: Unable to retrieve transactions
    """
    try:
        transactions: List[Dict[str, Any]] = get_all_transactions()
        return make_response(status=200, message=None, success=True, data=transactions)
    except Exception:
        return make_response(status=500, message='Unable to retrieve all transactions', success=False)


@transaction_bp.route('/', methods=['POST'])
def create_transaction() -> Dict[str, Any]:
    """
    Create a new transaction
    ---
    tags:
      - Transactions
    parameters:
      - name: transaction
        in: body
        required: true
        schema:
          type: object
          properties:
            amount:
              type: number
              format: float
              description: The amount of the transaction
            type:
              type: string
              description: The type of the transaction (credit or debit)
            description:
              type: string
              description: A brief description of the transaction
            date:
              type: string
              format: date-time
              description: The date of the transaction
    responses:
      201:
        description: Transaction created successfully
      401:
        description: Validation errors
      500:
        description: Unable to create transaction
    """
    try:
        data = request.json
        errors = validate_transaction(data)
        if errors:
            return make_response(status=401, message=errors, success=False, data=None)
        add_transaction(data['amount'], data['type'],
                        data['description'], data['date'])
        return make_response(status=201, message="Transaction created successfully", success=True, data=None)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        return make_response(status=500, message="Something went wrong. Unable to create transaction", success=False)


@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
def get_single_transaction(transaction_id: int) -> Dict[str, Any]:
    """
    Retrieve a single transaction by ID
    ---
    tags:
      - Transactions
    parameters:
      - name: transaction_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: The requested transaction
        schema:
          type: object
          properties:
            id:
              type: integer
            amount:
              type: number
              format: float
            type:
              type: string
            description:
              type: string
            date:
              type: string
              format: date-time
      404:
        description: Transaction not found
      500:
        description: Unable to retrieve transaction
    """
    try:
        transaction: Dict[str, Any] = get_transaction(transaction_id)
        if transaction:
            return make_response(status=200, message=None, success=True, data=transaction)
        else:
            return make_response(status=404, message="This transaction does not exist", success=False)
    except Exception:
        return make_response(status=500, message='Unable to retrieve transaction', success=False)


@transaction_bp.route('/<int:transaction_id>', methods=['PUT'])
def modify_transaction(transaction_id: int) -> Dict[str, Any]:
    """
    Update an existing transaction
    ---
    tags:
      - Transactions
    parameters:
      - name: transaction_id
        in: path
        required: true
        type: integer
      - name: transaction
        in: body
        required: true
        schema:
          type: object
          properties:
            amount:
              type: number
              format: float
            type:
              type: string
            description:
              type: string
            date:
              type: string
              format: date-time
    responses:
      200:
        description: Transaction updated successfully
      400:
        description: Unable to update transaction
    """
    try:
        data = request.json
        update_transaction(
            transaction_id=transaction_id,
            date=data['date'],
            transaction_type=data['type'],
            description=data['description'],
            amount=data['amount']
        )
        return make_response(status=200, message="Transaction updated successfully", success=True, data=None)
    except Exception as e:
        return make_response(status=400, message="Unable to update transaction: " + str(e), success=False)


@transaction_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id: int) -> Dict[str, Any]:
    """
    Delete a transaction by ID
    ---
    tags:
      - Transactions
    parameters:
      - name: transaction_id
        in: path
        required: true
        type: integer
    responses:
      200:
        description: Transaction deleted successfully
      500:
        description: Unable to delete transaction
    """
    try:
        remove_transaction(transaction_id)
        return make_response(status=200, message="Transaction deleted successfully", success=True, data=None)
    except Exception:
        return make_response(status=500, message='Unable to delete transaction', success=False)
