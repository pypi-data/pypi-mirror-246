import os

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

from trail.exception.auth import InvalidCredentialsException
from trail.exception.trail import TrailUnavailableException
from trail.libconfig import libconfig
from trail.userconfig import MainConfig
from trail.util import auth

FETCH_ALL_PROJECTS = """
    query {
        allProjects {
            id
            title
        }
    }
"""


def get_user_credentials():
    username = input("Username: ")
    password = input("Password: ")

    return username, password


def sign_in():
    while True:
        username, password = get_user_credentials()

        try:
            token = auth.authenticate(username, password)
        except InvalidCredentialsException as e:
            print(e)
            continue

        return username, password, token


def select_project_and_parent_experiment(id_token: str):
    try:
        transport = AIOHTTPTransport(
            libconfig.gql_endpoint_url,
            headers={'authorization': f'Bearer {id_token}'}
        )
        client = Client(transport=transport)
        result = client.execute(document=gql(FETCH_ALL_PROJECTS))
        projects = {
            project["id"]: project
            for project in result["allProjects"]
        }
    except TransportQueryError as e:
        raise TrailUnavailableException() from e

    print("Your projects are listed below:\n")
    print("Project ID | Project Title")
    for project in sorted(projects.values(), key=lambda x: x["id"]):
        print(f"{project['id']}     | {project['title']}")

    while True:
        project_id = input("Select a project ID: ")
        if project_id in projects:
            break

    # TODO: validate parent_experiment ID
    parent_experiment_id = input("Select a parent experiment ID: ")

    return project_id, parent_experiment_id


def create_config(username, password, project_id, parent_experiment_id):
    config = MainConfig(
        os.path.join(os.getcwd(), libconfig.PRIMARY_USER_CONFIG_PATH),
        {
            'username': username,
            'password': password,
            'projects': {
                'id': project_id,
                'parentExperimentId': parent_experiment_id
            },
        }
    )
    config.save()


def init_environment():
    print(f"Don't have an account yet? Sign up here: {libconfig.TRAIL_SIGN_UP_URL}\n")

    print("Your configuration file will be stored in the current directory. "
          "Make sure that you are in the root directory of your project.")

    username, password, user_id_token = sign_in()
    project_id, parent_experiment_id = select_project_and_parent_experiment(user_id_token)
    create_config(username, password, project_id, parent_experiment_id)

    print("Initialization completed.")
