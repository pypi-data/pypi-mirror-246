import os
import kfp
from e2enetworks.cloud.tir import client
from typing import Optional
from requests import Request, Session, Response
import e2enetworks.constants as constants

E2E_UI_HOST = "localhost:3000"

class _Client:
    def __init__(self):
        self._api_key = None
        self._access_token = None
        self._project = None
        self._team = None
        self._namespace = None
        self._eos_bucket = None
        self._api_host = None
        self._client = None

    def init(
        self,
        *,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        team: Optional[str] = None,
        project: Optional[str] = None,
        eos_bucket: Optional[str] = None,
    ):
        self._access_token = access_token
        self._api_key = api_key
        self._project = project
        self._team = team
        self._eos_bucket = eos_bucket

    def ready(self): 
        return False if not self.api_key() or not self.access_token() else True
    
    def api_host(self):
        if self._api_host:
            return self._api_host
        if os.environ.get("E2E_TIR_API_HOST"):
            self._api_host = os.environ.get("E2E_TIR_API_HOST")
            return self._api_host
        return constants.MY_ACCOUNT_LB_URL
    
    def access_token(self):
        if self._access_token:
            return self._access_token

        access_token_not_set = (
            "Access Token not set. Please provide a Access Token by:"
            "\n- Using e2enetworks.cloud.tir.init(access_token=)"
            "\n- Setting an environment variable E2E_TIR_ACCESS_TOKEN"
        )

        if os.environ.get("E2E_TIR_ACCESS_TOKEN"):
            self._access_token = os.environ.get("E2E_TIR_ACCESS_TOKEN")
            return self._access_token
        else:
            raise ValueError(access_token_not_set)

    def api_key(self):
        if self._api_key:
            return self._api_key

        api_key_not_set = (
            "API key not set. Please provide api key by:"
            "\n- Using e2enetworks.cloud.tir.init(api_key=)"
            "\n- Setting an environment variable E2E_TIR_API_KEY"
        )

        if os.environ.get("E2E_TIR_API_KEY"):
            self._api_key = os.environ.get("E2E_TIR_API_KEY")
            return self._api_key
        else:
            raise ValueError(api_key_not_set)

    def set_project(self, project):
        self._project = project

    def set_team(self, team):
        self._team = team

    def gpu_projects_path(self, project=None):
        if not project:
            project = self.project()
        
        return "{api_host}/api/v1/gpu/projects/{project}".format(api_host=self.api_host(), project=project)
    
    def project(self):
        if self._project:
            return self._project
        
        project_not_set = (
            "Project ID not set. Please provide a project ID by:"
            "\n- Using e2enetworks.cloud.tir.init(project=)"
            "\n- Setting an environment variable E2E_TIR_PROJECT_ID"
        )

        if os.environ.get("E2E_TIR_PROJECT_ID"):
            self._project = os.environ.get("E2E_TIR_PROJECT_ID")
            return self._project
        else:
            raise ValueError(project_not_set)

    def namespace(self, project=None):
        if not project:
            project = self.project()

        return "p-{}".format(project)

    def team(self):
        if self._team:
            return self._team
        
        team_not_set = (
            "Team ID not set. Please provide a team ID by:"
            "\n- Using e2enetworks.cloud.tir.init()"
            "\n- Setting an environment variable E2E_TIR_TEAM_ID"
        )

        if os.environ.get("E2E_TIR_TEAM_ID"):
            self._team = os.environ.get("E2E_TIR_TEAM_ID")
            return self._team
        else:
            raise ValueError(team_not_set)
    
    def make_request(self, request, stream=None, verify=None, timeout=None) -> Response:
        '''
            make_request(self, request): is common method to prepare a request
            and send to API host. 
            
            input:
            - request: requests.request. the request url must be only the path and 
            should not contain api host. 
            example usage: 
                request = requests.Request("GET", "http://localhost/api/v1/pipelines")
                make_request(request)

            output:
            - http response
            
            The modifications made to the request will be:
            * include auth header and add api key query param
            * append api host to the path 
        '''    
        s = Session()
        prepped = s.prepare_request(request)

        # append api key. we expect caller to send & if query parameters are used.
        # for example:
        #   if the request url has query parameters like below
        #       /pipelines?page=2 
        #   then we expect the caller to set url as /pipelines?page=2& instead of /pipelines?page=2
        # 
        prepped.url = f"{prepped.url}?" if prepped.url[len(prepped.url)-1] == "/" else prepped.url
        prepped.url = "{}apikey={}".format(prepped.url, self.api_key())
        print("prepped.url:", prepped.url)
        prepped.headers["Authorization"] = f"Bearer {self.access_token()}"

        return s.send(prepped, stream=stream, verify=verify, timeout=timeout)

    def print_values(self):
        print(f"apikey - {self.api_key()}")
        print(f"access_token - {self.access_token()}")
        print(f"team - {self.team()}")
        print(f"project - {self.project()}")

# common client set by tir.init(access_token=..., api_key=...)
    @staticmethod
    def help():
        help_text = '''
_Client - E2E Networks TIR Client

This class provides a client for interacting with the E2E Networks TIR API.

        Methods:

        1. init(api_key, access_token, project=None, team=None, eos_bucket=None)
           - Initialize the client with API key and access token.
           - Parameters:
             - api_key (str): Your API key.
             - access_token (str): Your access token.
             - team (str, optional): Team ID. Defaults to None.
             - project (str, optional): Project ID. Defaults to None.
             - eos_bucket (str, optional): EOS bucket. Defaults to None.

        2. ready()
           - Check if the client is ready for API requests.
           - Returns:
             - bool: True if both API key and access token are set, otherwise False.

        3. api_host()
           - Get the API host URL.
           - Returns:
             - str: The API host URL.

        4. access_token()
           - Get the access token. It can be set using `init` or an environment variable.
           - Returns:
             - str: The access token.

        5. api_key()
           - Get the API key. It can be set using `init` or an environment variable.
           - Returns:
             - str: The API key.

        6. set_project(project)
           - Set the project ID.
           - Parameters:
             - project (str): Project ID.

        7. set_team(team)
           - Set the team ID.
           - Parameters:
             - team (str): Team ID.

        8. gpu_projects_path(project=None)
           - Get the URL for GPU projects, optionally specifying a project.
           - Parameters:
             - project (str, optional): Project ID. Defaults to None.
           - Returns:
             - str: The GPU projects URL.

        9. project()
           - Get the project ID. It can be set using `init` or an environment variable.
           - Returns:
             - str: The project ID.

        10. namespace(project=None)
            - Generate a namespace for a project.
            - Parameters:
              - project (str, optional): Project ID. Defaults to None.
            - Returns:
              - str: The generated namespace.

        11. team()
            - Get the team ID. It can be set using `init` or an environment variable.
            - Returns:
              - str: The team ID.
              
        12. print_values()
            - Print values of team, project, access_token, apikey

        12. make_request(request, stream=None, verify=None, timeout=None)
            - Prepare and send a request to the API host.
            - Parameters:
              - request (Request): The request to send.
              - stream (bool, optional): Stream the response. Defaults to None.
              - verify (bool, optional): Verify SSL certificates. Defaults to None.
              - timeout (float, optional): Request timeout. Defaults to None.
            - Returns:
              - Response: The HTTP response.

        Attributes:

        Default
           - A default client instance that can be used for common client interactions.

        Usage:
        ```
        # Initialize the client
        client = _Client()
        client.init(api_key="your_api_key", access_token="your_access_token")

        # Check if the client is ready
        if client.ready():
            print("Client is ready for API requests.")
        else:
            print("Client is not ready.")

        # Access other client methods and attributes as needed.
        '''
        print(help_text)

    # Run the help function to display the documentation


Default = _Client()
