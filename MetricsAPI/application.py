def application(environ, start_response):
    # Set CORS headers for all requests (including OPTIONS)
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),  # Replace '*' with the specific origin you want to allow
        ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
        ('Access-Control-Allow-Methods', 'POST'),
    ]

    if environ['REQUEST_METHOD'] == 'OPTIONS':
        # For OPTIONS requests, respond with 200 OK and return an empty response
        start_response('200 OK', headers)
        return [b'']

    # For other request methods (e.g., POST, GET, etc.), process the request as usual
    # ... Your request handling logic ...

    # Example: Return a response with 'Hello, World!'
    response_body = b'Hello, World!'
    start_response('200 OK', headers)
    return [response_body]
