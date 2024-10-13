import { TransactionRetrievalResponse, Transaction, AccountRetrievalResponse } from './interfaces';

document.addEventListener("DOMContentLoaded", async () => {
    await retrieveTransactions();
    // @ts-ignore
    MicroModal.init();
});

const showCreateTransactionModalBtn = document.getElementById('showCreateTransactionModal') as HTMLElement;

async function validateForm(form: FormData): Promise<{ valid: boolean; errors?: string[] }> {
    const errors: string[] = [];
    
    const amount = parseFloat(form.get('amount') as string);
    const date = form.get('date') as string;
    const type = form.get('type') as string;
    const description = form.get('description') as string;

    if (isNaN(amount) || amount <= 0) {
        errors.push('Amount must be a positive number');
    }

    if (!date) {
        errors.push('Date is required');
    } else if (isNaN(new Date(date).getTime())) {
        errors.push('Invalid date format');
    }

    const validTypes = ['credit', 'debit'];
    if (!validTypes.includes(type)) {
        errors.push('Type must be either "credit" or "debit"');
    }

    if (!description) {
        errors.push('Description is required');
    } else if (description.length < 5) {
        errors.push('Description must be at least 5 characters long');
    }

    return {
        valid: errors.length === 0,
        errors: errors.length > 0 ? errors : undefined,
    };
}

async function populateCreateTransactionModal(): Promise<void> {
    const modalContent = document.getElementById('modalContent2') as HTMLElement;
    modalContent.innerHTML = `
        <form class="transaction-form" id="transactionForm2">
            <div>
                <label for="amount">Amount:</label>
                <input type="number" id="amount" name="amount" required step="0.01">
            </div>
            <div>
                <label for="date">Date:</label>
                <input type="date" id="date" name="date" required>
            </div>
            <div>
                <label for="type">Type:</label>
                <select id="type" name="type" required>
                    <option value="credit">Credit</option>
                    <option value="debit">Debit</option>
                </select>
            </div>
            <div>
                <label for="description">Description:</label>
                <textarea id="description" name="description" required></textarea>
            </div>
        </form>`;
}

showCreateTransactionModalBtn.addEventListener('click', () => {
    populateCreateTransactionModal();
    const createTransactionBtn = document.getElementById("createTransaction") as HTMLElement;
    createTransactionBtn.addEventListener("click", createTransaction);
    // @ts-ignore
    MicroModal.show('modal-2');
});

async function createTransaction(): Promise<void> {
    const transactionForm = document.getElementById('transactionForm2') as HTMLFormElement;
    const formData = new FormData(transactionForm);
    let formValidation = validateForm(formData)
    if (!(await formValidation).valid) {
        // @ts-ignore
        MicroModal.close('modal-2');
        // @ts-ignore
        Swal.fire({
            title: "Your form has errors",
            text: `${(await formValidation).errors?.map(item => { return item + "\n"})}`,
            icon: 'error',
            confirmButtonText: 'Okay',
        });
        return;
    }
    const data = {
        amount: parseFloat(formData.get('amount') as string),
        date: new Date(formData.get('date') as string),
        type: formData.get('type') as string,
        description: formData.get('description') as string
    };

    try {
        const response = await fetch('http://localhost:5000/transactions/', {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        let responseData: TransactionRetrievalResponse = await handleResponse(response);
        console.log(responseData)
        // @ts-ignore
        Swal.fire({
            title: responseData.message,
            icon: 'success',
            confirmButtonText: 'Okay',
        });
        retrieveTransactions();
    } catch (error) {
        console.error('Fetch error:', error);
        alert("Something went wrong");
    }
}

function formatDateForInput(date: Date): string {
    const pad = (num: number) => String(num).padStart(2, '0');
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

async function showModalWithContent(transactionId: number): Promise<void> {
    try {
        const response = await fetch(`http://localhost:5000/transactions/${transactionId}`);
        const data: TransactionRetrievalResponse = await handleResponse(response);

        if (!Array.isArray(data.data)) {
            const modalContent = document.getElementById('modalContent') as HTMLElement;
            const dateObject = new Date(data.data.date);
            const formattedDate = formatDateForInput(dateObject);
            modalContent.innerHTML = `
                <form class="transaction-form" id="transactionForm">
                    <div>
                        <label for="amount">Amount:</label>
                        <input type="number" id="amount" name="amount" value="${data.data.amount}" required step="0.01">
                    </div>
                    <div>
                        <label for="date">Date:</label>
                        <input type="date" id="date" name="date" value="${formattedDate}" required>
                    </div>
                    <div>
                        <label for="type">Type:</label>
                        <select id="type" name="type" required>
                            <option value="credit" ${data.data.type === 'credit' ? 'selected' : ''}>Credit</option>
                            <option value="debit" ${data.data.type === 'debit' ? 'selected' : ''}>Debit</option>
                        </select>
                    </div>
                    <div>
                        <label for="description">Description:</label>
                        <textarea id="description" name="description" required>${data.data.description}</textarea>
                    </div>
                </form>`;
            document.getElementById('deleteTransaction')?.addEventListener('click', () => deleteTransaction(transactionId));
            document.getElementById('updateTransaction')?.addEventListener('click', () => updateTransaction(transactionId));
            // @ts-ignore
            MicroModal.show('modal-1');
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert("Something went wrong");
    }
}

async function addTransactionEvents(): Promise<void> {
    const modifiableTransactions = document.querySelectorAll('.handle-transaction');
    modifiableTransactions.forEach((element) => {
        element.addEventListener('click', () => {
            const transactionId = Number(element.querySelector('#id')?.textContent);
            showModalWithContent(transactionId);
        });
    });
}

const transactionElementTemplate = (transaction: Transaction): string => `
    <tr class="handle-transaction"> 
        <td hidden id="id">${transaction.id}</td>
        <td id="amount">${transaction.type == 'credit' ? "+" : "-"}R${transaction.amount}</td>
        <td id="description">${transaction.description}</td>
        <td id="date">${transaction.date}</td>
        <td><small id="type" class="${transaction.type}-pill">${transaction.type}</small></td>
    </tr>
`;

async function retrieveTransactions(): Promise<void> {
    try {
        const response = await fetch("http://localhost:5000/transactions/");
        const data: TransactionRetrievalResponse = await handleResponse(response);

        const transactionListElement = document.getElementById('transactionList') as HTMLElement;
        transactionListElement.innerHTML = '';
        if (data.success && Array.isArray(data.data)) {
            if (data.data.length > 0) {
                data.data.forEach(transaction => {
                    if (document.getElementById('noTransactions')) {
                        document.getElementById('noTransactions')?.remove()
                    }
                    const transactionElement = transactionElementTemplate(transaction);
                    transactionListElement.innerHTML += transactionElement; 
                });
            } else {
                let element = document.createElement('p');
                element.textContent = 'No transactions right now...'
                element.id = 'noTransactions'
                element.style['textAlign'] = 'center';
                document.querySelector('.table-container')!.appendChild(element)
            }

        }
        addTransactionEvents();
        updateBalance();
    } catch (error) {
        console.error('Fetch error:', error);
        alert("Something went wrong");
    }
}

async function deleteTransaction(transactionId: number): Promise<void> {
    try {
        const response = await fetch(`http://localhost:5000/transactions/${transactionId}`, { method: "DELETE" });
        const data: TransactionRetrievalResponse = await handleResponse(response);
        
        if (data.message) {
            // @ts-ignore
            MicroModal.close('modal-1');
            // @ts-ignore
            Swal.fire({
                title: data.message,
                icon: 'success',
                confirmButtonText: 'Okay',
            });
        }

        retrieveTransactions();
    } catch (error) {
        // @ts-ignore
        MicroModal.close('modal-1');
        console.error('Fetch error:', error);
        alert("Something went wrong");
    }
}

async function updateTransaction(transactionId: number): Promise<void> {
    try {
        const transactionForm = document.getElementById('transactionForm') as HTMLFormElement;
        const formData = new FormData(transactionForm);
        let formValidation = validateForm(formData)
        if (!(await formValidation).valid) {
            // @ts-ignore
            Swal.fire({
                title: "Your form has errors",
                text: `${(await formValidation).errors?.map(item => { return item + "\n"})}`,
                icon: 'error',
                confirmButtonText: 'Okay',
            });
            return;
        }
        const data = {
            amount: parseFloat(formData.get('amount') as string),
            date: new Date(formData.get('date') as string),
            type: formData.get('type') as string,
            description: formData.get('description') as string
        };

        const response = await fetch(`http://localhost:5000/transactions/${transactionId}`, {
            method: "PUT",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const responseData: TransactionRetrievalResponse = await handleResponse(response);
        if (responseData.success) {
            // @ts-ignore
            Swal.fire({
                title: responseData.message,
                icon: 'success',
                confirmButtonText: 'Okay',
            });
            // @ts-ignore
            MicroModal.close('modal-1');
            retrieveTransactions();
        }
    } catch (error) {
        // @ts-ignore
        MicroModal.close('modal-1');
        console.error('Fetch error:', error);
        alert("Something went wrong");
    }
}

async function updateBalance() {
    console.log("UPDATING BALANCE")
    try {
        const response = await fetch(`http://localhost:5000/account`);
        console.log(response)
        const responseData: AccountRetrievalResponse = await response.json()
        if (responseData.success) {
                let balanceP = document.getElementById('balance')
                balanceP!.innerText = String("R " + responseData.data.account_balance)
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert("Something went wrong");
    }  
}

async function handleResponse(response: Response): Promise<any> {
    if (!response.ok) {
        // @ts-ignore
        Swal.fire({
            title: "Something went wrong",
            icon: 'error',
            confirmButtonText: 'Okay',
        });
        return;
    }
    return await response.json();
}
