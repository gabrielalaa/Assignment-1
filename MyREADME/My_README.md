# Assignment 1  
### Made by Rădulescu Carla Gabriela  

I created this file to describe some aspects I considered important back then. This was my very first Python project.  

---

## Purpose of this **README**  
My intention is to learn how to structure my own md files.

---

## Understanding imports  

> **IMPORTANT!**  
> This documentation is taken from Google or other sites such as:  
> - [GeeksForGeeks](https://www.geeksforgeeks.org/)  
> - [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/index.html)  
> - [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)  

### Flask imports  
- `from flask import jsonify`  
  - Python's **Flask** micro web framework is well-liked and frequently used to create web applications. It offers a simple and flexible approach to developing Python-based web apps and APIs.  
  - The **jsonify()** function is useful in Flask apps because it automatically sets the correct response headers and content type for JSON responses. It simplifies returning JSON-formatted data from route handlers, making API development more convenient.  

- `from flask_restx import Namespace, reqparse, Resource, fields`  
  - **Flask-RESTx**: An extension for Flask that helps build REST APIs efficiently.  
  - **Namespace**: A class containing models and resource declarations.  
  - **reqparse**: A class that helps parse and validate incoming request data, ensuring correct data processing.  
  - **Resource**: A class used to define logic for specific URL endpoints. It determines how to handle HTTP methods like GET, POST, etc.  
  - **fields**: A module assisting in formatting and validating data returned to clients.  
  - **abort**: Terminates a program or operation due to an error.  
  - **random**: Used to simulate unpredictability in responses.  

---

## Some aspects  

### Why did I use `random` instead of **uuid**?  
I focused more on functionality than uniqueness. However, during my research, I found that using `int(str(uuid.uuid4().int)[:8])` could generate an 8-digit random number (or longer if needed).  

> **Note**: The range for IDs in this project follows a structure:  
> - **Newspapers**: `1-999`  
> - **Issues**: `1000-9999`  
> - **Editors**: `10000-99999`  
> - **Subscribers**: `100000-999999`  

### Additional considerations  
- I explored an alternative way of assigning newspapers to editors, considering that an editor might manage more than just issues. This helped me better understand issue transfers.  
- Regarding missing issues, I assumed that when a subscriber subscribes to a newspaper, they expect to receive all available issues. If there were missing issues, I retrieved them and ensured delivery to the subscriber.  

---

## Reflections  
I really enjoyed working on this project! Writing model tests seemed easier than implementing API tests. However, after encountering and fixing multiple errors, I managed to gain a better understanding of debugging and troubleshooting.  
