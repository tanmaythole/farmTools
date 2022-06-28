import json
from tests.test_auth.helpers import login, register


def test_register_user(client):
    doc = {
            "email": "tanmay.thole4@farmtools.com",
            "password": "1234",
            "first_name": "Tanmay",
            "last_name": "Thole",
            "mobile": 1234567890
        }
    

    # adding user with already existed email
    res = register(client, {**doc, 'email':"tanmay.thole@farmtools.com"})
    assert res.status_code == 400
    assert "User already exist" in str(res.json)

    # adding user with already existed mobile
    res = register(client, {**doc, 'mobile':5383745})
    assert res.status_code == 400
    assert "not valid" in str(res.json)

    # adding new user
    # res = register(client, doc)
    # assert res.status_code == 200
    # assert res.json


def test_login_user(client):
    res = login(client, "tanmay.thole@farmtools.com", "12345")
    assert res.status_code == 200
    assert res.json['token']

    # wrong email as input
    res = login(client, "tanmay.thole@farmtool.com", "12345")
    assert res.status_code == 404
    assert "Invalid Credentials" in str(res.json)

    # wrong password as input
    res = login(client, "tanmay.thole@farmtools.com", "1234")
    assert res.status_code == 404
    assert "Invalid Credentials" in str(res.json)

    # wrong password as input
    res = login(client, "", "")
    assert res.status_code == 400
    assert "both fields required" in str(res.json)

