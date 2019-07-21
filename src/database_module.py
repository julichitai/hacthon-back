from peewee import *
import random, string, os


db = SqliteDatabase('database.db')


class Volunteer(Model):  # класс описывает таблицу волонтеров
    login = CharField(unique=True)
    photo = BlobField()
    password = CharField()
    name = CharField()
    is_verified = BooleanField()
    score = IntegerField()
    money = IntegerField()

    class Meta:
        database = db


class Task(Model):  # класс описывает таблицу заданий
    task_description = CharField()
    client_name = CharField()
    client_phone = CharField()
    address = CharField()
    is_done = BooleanField()
    volunteer_login = CharField()
    photo = BlobField()
    code = CharField()

    class Meta:
        database = db


class Product(Model):  # класс описывает таблицу продуктов
    name = CharField()
    photo = BlobField()
    description = CharField()
    cost = IntegerField()
    quantity = CharField()

    class Meta:
        database = db


######################################################################################

def gen_code():
    length = 6
    chars = string.digits
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))


######################################################################################


def add_volunteer(login, password, name):  # добавление клиента в базу
    '''если логин уже есть, то вернет False'''
    try:
        Volunteer.create(login=login,
                         password=password,
                         name=name,
                         is_verified=False,
                         score=0,
                         money=0,
                         photo=b'0')
    except IntegrityError:
        return False


def get_volunteer_id(login):
    try:
        return Volunteer.get(Volunteer.login == login).id
    except:
        return False


def update_volunteer_score(login, delta_score):
    Volunteer.update(score=get_volunteer_score(login)+delta_score).where(Volunteer.login == login).execute()


def add_volunteer_money(login, delta_money):
    Volunteer.update(money=get_volunteer_money(login)+delta_money).where(Volunteer.login == login).execute()


def minus_volunteer_money(login, delta_money):
    Volunteer.update(money=get_volunteer_money(login)-delta_money).where(Volunteer.login == login).execute()


def get_volunteer_score(login):
    try:
        return Volunteer.get(Volunteer.login == login).score
    except:
        return False


def get_volunteer_money(login):
    try:
        return Volunteer.get(Volunteer.login == login).money
    except:
        return False


def verify(login):
    Volunteer.update(is_verified=True).where(Volunteer.login == login).execute()


def is_verified(login):
    try:
        return Volunteer.get(Volunteer.login == login).is_verified
    except:
        return False


def get_all_volunteers():
    Volunteers = Volunteer.select()
    data = []
    for vol in Volunteers:
        data.append(get_volunteer(vol.login))
    return data


def get_volunteer(login):
    return {
        'login': Volunteer.login,
        'name': Volunteer.get(Volunteer.login == login).name,
        'photo': Volunteer.get(Volunteer.login == login).photo,
        'score': Volunteer.get(Volunteer.login == login).score
    }


def del_volunteer(login):
    '''если волонтера нет в бд, то False, иначе он удаляется и возвращается True'''
    try:
        Volunteer.get(Volunteer.login == login).delete_instance()
    except:
        return False
    return True


######################################################################################


def add_task(client_name, address, client_phone, code=gen_code(), task_description='Цифровое решение'):
    Task.create(client_name=client_name, client_phone=client_phone,
                address=address, is_done=False, volunteer_login=-1,
                code=code, photo=b'0', task_description=task_description)


def add_volunteer_to_task(task_id, volunteer_id):
    Task.update(volunteer_id=volunteer_id).where(Task.id == task_id).execute()


def add_photo_to_task(task_id, photo):
    Task.update(photo=photo).where(Task.id == task_id).execute()


def update_task_status(task_id, is_done):
    Task.update(is_done=is_done).where(Task.id == task_id).execute()


def get_volunteer_login(task_id):
    return Task.get(Task.id == task_id).volunteer_login


def get_all_tasks():
    Tasks = Task.Select()
    data = []
    for tsk in Tasks:
        data.append(get_volunteer(tsk.id))
    return data


def get_task(task_id):
    try:
        return {'id': Task.id,
                'task_description': Task.get(Task.id == task_id).task_description,
                'client_name': Task.get(Task.id == task_id).client_name,
                'client_phone': Task.get(Task.id == task_id).client_phone,
                'address': Task.get(Task.id == task_id).address,
                'is_done': Task.get(Task.id == task_id).is_done,
                'photo': Task.get(Task.id == task_id).photo,
                }
    except:
        return False


def del_task(task_id):
    try:
        Task.get(Task.id == task_id).delete_instance()
    except:
        return False
    return True


######################################################################################


def get_products():
    Products = Product.Select()
    data = []
    for prd in Products:
        data.append(get_volunteer(prd.id))
    return data


def get_product(prod_id):
    return {
        'name': Product.get(Task.id == prod_id).name,
        'description': Product.get(Task.id == prod_id).description,
        'cost': Product.get(Task.id == prod_id).cost,
        'quantity': Product.get(Task.id == prod_id).quantity
    }


def buy_product(volunteer_login, prod_id):
    if Product.get(Product.id == prod_id).quantity <= 0:
        return False
    else:
        Product.update(quantity=Product.get(Product.id == prod_id).quantity - 1).where(Product.id == prod_id).execute()
        minus_volunteer_money(volunteer_login, delta_money=Product.get(Product.id == prod_id).cost)
        return True


def add_product(prod_id):
    Product.update(quantity=Product.get(Product.id == prod_id).quantity + 1).where(Product.id == prod_id).execute()


######################################################################################


if __name__ == '__main__':
    Volunteer.create_table()
    Task.create_table()
    Product.create_table()

    add_volunteer('123', 'password', 'Ivan')
    add_volunteer('1', '1123', 'Ivan')

    add_task('213', '123', '89812931')

    data = {'params': ['123', 'password']}
    print(data['params'][0])
    # #
    print(Volunteer.login == data['params'][0] and Volunteer.password == data['params'][1])


