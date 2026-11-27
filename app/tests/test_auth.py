

def test_register_and_login(client):
    response = client.post('/auth/register', json={
        'email': 'testuser@gmail.com',
        'password': '12345678'
    })
    assert response.status_code == 201
    assert response.json()['email'] == 'testuser@gmail.com'
    assert response.json()['role'] == 'user'

    response = client.post('/auth/login', data={
        'username': 'testuser@gmail.com',
        'password': '12345678'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()