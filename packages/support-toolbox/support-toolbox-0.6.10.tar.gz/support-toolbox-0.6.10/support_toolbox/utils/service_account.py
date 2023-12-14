import requests
import json


# Create Service Account payloads
SERVICE_ACCOUNTS = [
    {
        "desiredUsername": "ctk",
        "displayName": "DDW Catalog Toolkit Service"
    },
    {
        "desiredUsername": "ddwmetrics",
        "displayName": "DDW Platform Metrics Service"
    }
]

CIRCLECI_PROJECTS = ["catalog-config", "mca"]


def create_env_variable(circleci_project, name, value, circleci_api_token):
    url = f"https://circleci.com/api/v2/project/github/datadotworld/{circleci_project}/envvar"

    headers = {
        "Circle-Token": circleci_api_token
    }

    payload = {
        "name": name,
        "value": value
    }

    response = requests.post(url, payload, headers=headers)

    if response.status_code == 201:
        print(f"Added '{name}' to the '{circleci_project}' project environment variables in CircleCI ")
    else:
        print(f"Error: Unable to create environment variables. Status Code: {response.status_code}")


def create_service_account(api_url, api_token, payload):
    create_service_account_url = f"{api_url}/serviceaccount/datadotworldsupport"

    header = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    cookies = {
        'adminToken': api_token
    }

    body = json.dumps(payload)

    # Create the service account
    response = requests.post(create_service_account_url, body, cookies=cookies, headers=header)

    # Verify the creation
    if response.status_code == 200:
        response_json = response.json()

        service_account = response_json['serviceAccountUsername']
        service_account_token = response_json['token']
        print(f"created service account: {service_account}")
        print(f"token: {service_account_token}")
        return service_account_token
    else:
        print(response.text)


def deploy_service_accounts(api_url, api_token, site_slug, circleci_api_token, existing_customer):
    for i, sa in enumerate(SERVICE_ACCOUNTS):
        token = create_service_account(api_url, api_token, sa)

        # Configure parameters for CircleCI API
        circleci_project = CIRCLECI_PROJECTS[i]

        # If existing customer and deploying SA to Metrics, add "_PI" before "_API_TOKEN"
        if existing_customer and circleci_project == 'mca':
            name = site_slug.upper() + "_PI_API_TOKEN"
            create_env_variable(circleci_project, name, token, circleci_api_token=circleci_api_token)
        # If not existing customer, skip deploying token to CircleCI for Metrics
        elif not existing_customer and circleci_project == 'mca':
            continue
        else:
            name = site_slug.upper() + "_API_TOKEN"
            create_env_variable(circleci_project, name, token, circleci_api_token=circleci_api_token)


def deploy_ctk_service_account(api_url, api_token, site_slug, circleci_api_token):
    token = create_service_account(api_url, api_token, SERVICE_ACCOUNTS[0])

    # Configure parameters for CircleCI API
    circleci_project = CIRCLECI_PROJECTS[0]
    name = site_slug.upper() + "_API_TOKEN"
    create_env_variable(circleci_project, name, token, circleci_api_token=circleci_api_token)