# Assignment 1
### Made by Rădulescu Carla Gabriela

---

## Purpose of this **README**
My intention is to learn how to structure my own md files.

---

### Understanding imports
> **IMPORTANT !**
> This documentation is taken from Google or other sites such as: https://www.geeksforgeeks.org/, https://flask-restx.readthedocs.io/en/latest/index.html, https://flask.palletsprojects.com/en/3.0.x/.

- `from flask import jsonify`
  - Python's **Flask** micro web framework is well-liked and frequently used to create online apps. It offers a straightforward and adaptable method for developing Python-based web applications and APIs (Application Programming Interfaces).
  - The **jsonify()** function is useful in Flask apps because it automatically sets the correct response headers and content type for JSON responses, and allows you to easily return JSON-formatted data from your route handlers. This makes it easier and more convenient to create APIs that return JSON data.

- `from flask_restx import Namespace, reqparse, Resource, fields`
  - **Flask-restx:** An extension for Flask that adds support for quickly building REST APIs.
  - **Namespace:** A class which contains models and resources declarations
  - **reqparse:** A class that helps you parse and validate incoming request data. It's used to access and validate data that the client sends to the server.
  - **Resource:** A class that you inherit from to define the logic for a specific URL endpoint in your API. It's where you define how to handle different HTTP methods like GET, POST, etc.
  - **fields:** A module which helps you format and validate the data you return to the client.
  - **abort** means ending a program or operation intentionally because of an erro.
  - **random** I used it to simulate unpredictability.

### Some aspects:
Why did I use random and not **uuid**? Because I was more interested in functionality. But in my research I found out about int(str(uuid.uuid4().int)[:8]) which can generate a random number of 8 digits or more if I want to.
Just take care because the range for newspaper IDs is 1:999, issues 1000:9999, editor 10000:99999 and subscriber 100000:999999.

I also considered in adding another method of assigning a newspaper to an editor. Maybe that editor is not only taking care of issues. This makes the idea of transferring issues much clear to me.

And another thing about missing issues, for me delivering issues means that the subscriber subscribed to a special issues. This subscriber can also subscribe to a newspaper. And if this newspaper has more released issues, I am looking for them and delivering them to the subscriber.

I really enjoyed making this project! The tests for the model seemed to me easier to implement than those for the APIs. But after failing several times, I managed to understand the errors and solve them.
