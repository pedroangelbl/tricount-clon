from uuid import UUID
from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit


def calculate_group_settlement(group_id: UUID, db: Session):

    members = db.query(Member).filter(Member.group_id == group_id).all()

    balances = {member.id: 0 for member in members}

    expenses = db.query(Expense).filter(Expense.group_id == group_id).all()

    splits = (
        db.query(ExpenseSplit)
        .join(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    # sumar pagos
    for expense in expenses:
        balances[expense.paid_by_member_id] += float(expense.amount)

    # restar deudas
    for split in splits:
        balances[split.member_id] -= float(split.amount)

    balances_list = [[member_id, balance] for member_id, balance in balances.items()]

    transactions = []

    def get_min_index():
        return min(range(len(balances_list)), key=lambda i: balances_list[i][1])

    def get_max_index():
        return max(range(len(balances_list)), key=lambda i: balances_list[i][1])

    def settle():

        min_index = get_min_index()
        max_index = get_max_index()

        min_balance = balances_list[min_index][1]
        max_balance = balances_list[max_index][1]

        if abs(min_balance) < 0.01 and abs(max_balance) < 0.01:
            return

        amount = min(-min_balance, max_balance)

        debtor_id = balances_list[min_index][0]
        creditor_id = balances_list[max_index][0]

        balances_list[min_index][1] += amount
        balances_list[max_index][1] -= amount

        transactions.append(
            {
                "from_member_id": debtor_id,
                "to_member_id": creditor_id,
                "amount": round(amount, 2),
            }
        )

        settle()

    settle()

    return transactions