import asyncio
import websockets
import json
import jwt

from src import database_module as db


JWT_SECRET = 'this_is_our_secret'
JWT_ALGORITHM = 'HS256'


async def get_request(websocket, path):
    input_json = await websocket.recv()

    data = json.loads(input_json.read())
    if data['method'] == 'is_verified':
        try:
            res = db.is_verified(login=data['params'][0])
        except Exception as error:
            res = error
        else:
            res = 'OK'

    elif data['method'] == 'verify':
        try:
            db.verify(login=data['params'][0])
        except Exception as error:
            res = error
        else:
            res = 'OK'

    elif data['method'] == 'get_all_volunteers':
        try:
            res = db.get_all_volunteers()
        except Exception as error:
            res = error

    elif data['method'] == 'get_all_tasks':
        try:
            res = db.get_all_tasks()
        except Exception as error:
            res = error

    elif data['method'] == 'accept_task':
        try:
            db.add_volunteer_to_task(task_id=data['params'][0],
                                     volunteer_id=data['params'][1])
        except Exception as error:
            res = error
        else:
            res = 'ОК'

    elif data['method'] == 'sign_up':
        try:
            db.add_volunteer(login=data['params'][0], password=data['params'][1], name=data['params'][2])
        except Exception as error:
            res = error
        else:
            res = 'OK'

    elif data['method'] == 'done_work':
        try:
            db.update_task_status(task_id=data['params'][0], is_done=True)
            db.update_volunteer_score(login=data['params'][1], delta_score=25)
            db.add_volunteer_money(login=data['params'][1], delta_money=25)
        except Exception as error:
            res = error
        else:
            res = 'OK'

    elif data['method'] == 'buy':
        try:
            buy = db.buy_product(volunteer_login=data['params'][0],
                                 prod_id=data['params'][1])
            if buy:
                res = 'OK'
            else:
                res = 'This product not found'
        except Exception as error:
            res = error
    if data['method'] == 'authentification':  # 0 - login, 1 - password
        try:
            payload = {'volunteer_login': db.Volunteer.get(db.Volunteer.login == data['params'][0] and\
                                                           db.Volunteer.password == data['params'][1]).login}
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            json_string = json.dumps({'token': jwt_token.decode('utf-8')})
        except Exception as error:
            res = error
    else:
        json_string = json.dumps({"jsonrpc": "2.0", "result": res, "id": data['method']})

    print(f"< {json.loads(input_json)}")

    await websocket.send(json_string)
    print(f"> {json_string}")


start_server = websockets.serve(get_request, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


"""
Methods List
1) is_verified   проверка на верификацию params[0] = login

2) verify   верифицировать params[0] = login

3) get_all_volunteers   получить список всех волонтеров (login, name, photo, score)

4) get_all_tasks   получить список всех заданий (id, task_description, client_name, client_phone, address, is_done, photo)

5) accept_task   волонтер принял задание params[0] = task_id, params[1] = login

6) sign_up     params[0] = login, params[1] = password, params[2] = name

7) done_work   волонтер сделал работу params[0] = task_id, params[1] = login

8) buy   params[0] = login, params[1] = product_id

9) authentification     params[0] = login, params[1] = password

"""