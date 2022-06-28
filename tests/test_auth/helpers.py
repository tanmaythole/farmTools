def register(client, data):
    return client.simulate_post('/api/auth/register/', json=data)

def login(client, email, password):
    doc = {
            "email": email,
            "password": password
        }

    return client.simulate_post('/api/auth/login/', json=doc)