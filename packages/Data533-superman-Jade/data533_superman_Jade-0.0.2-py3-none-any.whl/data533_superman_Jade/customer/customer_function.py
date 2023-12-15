import sqlite3
from datetime import datetime
import uuid
from distutils.util import execute
import members
import transactions
try:
    cnx = sqlite3.connect("Supermarket.db")
    cursor = cnx.cursor()
    sql_query = """SELECT name FROM sqlite_master 
    WHERE type='table';"""
    cursor.execute(sql_query)
    print("List of tables\n")
    print(cursor.fetchall())
except sqlite3.Error as err:
    print(err)

class MyCustomError(Exception):
    def __init__(self, message="A custome error occured"):
        self.message=message
        super().__init__(self.message)
def CustomeError(value):
    if float(value) <0:
        raise MyCustomError("This value should be a non-negative value")
    
def login():
    member_status = input("Are you a new member? Input yes or no\n")
    if member_status.lower() == 'yes':
        # 'member' object
        global member
        global member_id
        member = members.create_new_member()  # prompt info request
        try:
            new_member_info_dict = member.get_member_info()
            member_id = new_member_info_dict['id']
            name = new_member_info_dict['name']
            email = new_member_info_dict['email']
            phone = new_member_info_dict['phone']
            address = new_member_info_dict['address']
            write_new_member_query = "INSERT INTO members VALUES (?, ?, ?, ?, ?, 0, 0, 0, FALSE)"
            cursor.execute(write_new_member_query,(member_id, name, email, phone, address))
            cnx.commit()
        except KeyError as err:
            print("Something wrong happened")
            print(err)

    else:
        member_id = input("Please input your customer id\n")
        old_member_info_sql = "SELECT * from members where id=?"
        cursor.execute(old_member_info_sql, (member_id,))
        result=cursor.fetchone()
        if result:
            try:
                id=result[0]
                name=result[1]
                email=result[2]
                phone=result[3]
                address=result[4]
                deposit=result[5]
                credits=result[6]
                total_consumption=result[7]
                premium_status=result[8]
            except IndexError as err:
                print("Something went wrong here.")
                print(err)
            member=members.member(id, name, email, phone, address, deposit, credits, total_consumption, premium_status)
        while True:
            login_choice = input("Do you want to\n1. check your membership information\n2. change your membership information\n3. check your history transactions\nPlease enter 'exit' to proceed checking out\n")
            if login_choice == "1":
                print(member.get_member_info())
            elif login_choice == "2":
                change_prompt = input(
                    "You can only change\na: email\nb: phone number\nc: address\n")
                if change_prompt == "a":
                    new_email = input("Please input your new email\n")
                    member.change_email(new_email)
                    change_email_sql = "UPDATE members set email=? where id=?"
                    cursor.execute(change_email_sql, (new_email, member_id))
                    cnx.commit()
                elif change_prompt == "b":
                    new_phone = input("Please input your new phone number")
                    member.change_phone(new_phone)
                    change_phone_sql = "UPDATE members set phone=? where id=?"
                    cursor.execute(change_phone_sql, (new_phone, member_id))
                    cnx.commit()
                elif change_prompt == "c":
                    new_address = input("Please input your new address")
                    member.change_address(new_address)
                    change_address_sql = "UPDATE members set address=? where id=?"
                    cursor.execute(change_address_sql, (new_address, member_id))
                    cnx.commit()
            elif login_choice == "3":
                member_transaction_sql = "SELECT * from transactions where customer_id=?"
                cursor.execute(member_transaction_sql, (member_id, ))
                for row in cursor:
                    print(row)
                
            elif login_choice.lower()=='exit':
                print("Continue your checking out\n")
                break

def checkout():
    transaction_time=datetime.now()
    customer_id=member_id
    global transaction_id
    transaction_id=transaction_time.minute+transaction_time.second+int(str(uuid.uuid4().int)[:4])# randomly generate transactionid according to time and uuid
    transaction_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    items_name=''
    items_quantity=''
    items_price=''
    items_value=''
    while True:
        item_name=input("Please input your purchased item name\n")
        item_quantity=input("Please input the item quantity\n")
        item_price=input("Please input the item price($/qty)\n")
        try:
            CustomeError(item_quantity)
            CustomeError(item_price)
        except MyCustomError as e:
            print(f"Error: {e}")
        try:
            item_value=str(float(item_quantity)*float(item_price))
        except ArithmeticError as err:
            print("Something went wrong here")
            print(err)
        items_name=items_name+item_name+','
        items_quantity=items_quantity+item_quantity+','
        items_price=items_price+item_price+','
        items_value=items_value+item_value+','
        add_more_request=input("Do you want to add more items? yes/no\n")
        if add_more_request.lower()=='no':
            break
    transaction_record_sql="INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)"
    cursor.execute(transaction_record_sql, (customer_id, transaction_id, items_name, items_quantity, items_price, items_value, transaction_time, '', ''))
    cnx.commit()
    new_transaction=transactions.transaction(customer_id, transaction_id, items_name, items_quantity, items_price, items_value, transaction_time, '', '')
    return new_transaction

def payment_and_rate():
    total_consumption_update_sql="UPDATE members SET total_consumption=? where id=?"
    credits_update_sql="UPDATE members SET credits=? where id=?"
    deposit_update_sql="UPDATE members SET deposit=? where id=?"
    login()
    new_transaction=checkout()
    total_value=transactions.get_order_total(new_transaction)#new_transaction.items_value
    print(f"Your total transaction value is {total_value}")
    try:
        print(f"Your account deposit is {member.deposit}")
    except NameError as err:
        print("Member is not defined")
        print(err)
    deposit_request=input("Do you want to add your account deposit, yes/no\n")
    if deposit_request.lower()=='yes':
        deposit_amount=input("How much you want to deposit\n")
        #add deposit and credits added too         
        member.add_deposit(float(deposit_amount))
       
    payment_choice_request=input("Do you want to pay with your account deposit, yes/no\n")
    if payment_choice_request.lower()=='yes':
        if member.deposit-total_value<0:
            print("Fail for not enough deposit. Cannot use deposit now.\n")#stop and use new money
            #go to the bottom else
            final_payment_choice='no'
        else:
            #use deposit to pay the total transaction value does not boost member total_consumption & credits, because deposit 
            #when adding deposit, the same money generates 1.05times deposit
            final_payment_choice='yes'
            new_deposit=member.deposit-total_value
            member.deposit=new_deposit   #add_deposit(new_deposit)
            print("Payment successful\n")
    if payment_choice_request.lower()=='no' or final_payment_choice.lower()=='no':
        #pay with cash & not enough deposist, total value added to total consumption
        #credits changed at the same time
        member.add_consumption(total_value)
        if member.check_premium_status():
            new_credit = total_value/10
        else:
            new_credit = total_value/100
        member.add_credits(new_credit)

    cursor.execute(total_consumption_update_sql, (member.total_consumption, member_id))
    cnx.commit()
    cursor.execute(credits_update_sql, (member.account_credits, member_id))
    cnx.commit()
    cursor.execute(deposit_update_sql, (member.deposit, member_id))
    cnx.commit()

    transactions.new_review(new_transaction)
    review_update_sql="UPDATE transactions SET order_review=? where customer_id=? and transaction_id=?"
    cursor.execute(review_update_sql, (new_transaction.order_review, member_id, transaction_id))
    cnx.commit()
    transactions.new_rate(new_transaction)
    rate_update_sql="UPDATE transactions SET order_rate=? where customer_id=? and transaction_id=?"
    cursor.execute(rate_update_sql, (new_transaction.order_rate, member_id, transaction_id))
    cnx.commit()
    
    print("Thank you!\n")

payment_and_rate()

cnx.close()
