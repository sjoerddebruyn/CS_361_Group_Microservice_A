CS_361_Group_Microservice_A 

Pre-requistes for the program to work:
    The program has a list of requirements (which can be found in requirements.txt) for the program to work. It also requires the user to implement the socket connection to their own API, as is modeled in the example api (e_api).

Notes on requesting/recieving data:
    This program isn't convential in terms of requesting and recieving data, as it 
    uses lifespan and all data is requested when the program is started, not by indivual calls.
    Furthermore, data is recieved once daily after the program has been started, in form of a confirmation that the days media of the selected websites has been scraped.

Requesting Data:
    Using socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket, the program sends a JSON payload once socket has been connected using client_socket.connect()

Receiving Data:
    For receiving data the same socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket is established and the payload is read via client_socket.recv().decode()

Execution Instructions:
    1. Begin the microservice_a to listen for activation call on local host
        - python microservice_a.py
    2. Start your API 
        The JSON payload will be sent to the localhost 
    3. The microservice receives payload and scrapes data
    4. Microservice sends a confirmation over local host and will continue to do so daily