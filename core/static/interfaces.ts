export interface Transaction {
    id: number;
    amount: number;
    date: Date,
    type: string,
    description: string
}

export interface Response {
    message: string,
    success: boolean
}

export interface Account {
    id: number;
    account_name: string;
    account_balance: number;
}

export interface TransactionRetrievalResponse extends Response {
    data: Transaction[] | Transaction;
}

export interface AccountRetrievalResponse extends Response {
    data: Account
}