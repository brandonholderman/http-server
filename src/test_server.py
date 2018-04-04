import requests
from cowpy import cow
import pytest
import json

def test_server_sends_200_response():
    response = requests.post('http://127.0.0.1:3000')
    assert response.status_code == 200
    assert response.text == '''
    <!DOCTYPE html>
<html>
<head>
    <title> cowsay </title>
</head>
<body>
    <header>
        <nav>
        <ul>
            <li><a href="/cowsay">cowsay</a></li>
        </ul>
        </nav>
    <header>
    <main>
        <!-- project description -->
    </main>
</body>
</html>'''

def test_server_sends_404_response():
    response = requests.get('http://127.0.0.1:3000/monkey')
    assert response.status_code == 404
    assert response.text == 'Not Found'

def test_server_sends_qs_back():
    response = requests.get(
        'http://127.0.0.1:3000/cow?msg="hello world"')
    assert response.status_code == 200
    assert response.text == cow.Cheese().milk('"hello world')