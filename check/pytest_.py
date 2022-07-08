#!/usr/bin/env python3

import sys

import applications_superstaq.check


def set_env_vars() -> None:
    """
    Set environment variables for the SuperstaQ integration test.
    """

    import json
    import os
    import boto3

    session = boto3.session.Session()
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
    client = session.client(service_name="secretsmanager")
    get_secret_value_response = client.get_secret_value(SecretId="db_secret")

    if "SecretString" in get_secret_value_response:
        secret = json.loads(get_secret_value_response["SecretString"])
        os.environ["GOOGLE_CLIENT_ID"] = secret["google_client_id"]
        os.environ["GOOGLE_CLIENT_SECRET"] = secret["google_client_secret"]
        os.environ["PRANAV_IBMQ_TOKEN"] = secret["pranav_ibmq_token"]
        os.environ["GOOGLE_API_KEY"] = secret["google_api_key"]
    else:
        raise ValueError(
            "We currently only handle the secret value response having the SecretString key, "
            "but this response doesn't have that key"
        )


if __name__ == "__main__":
    NOTEBOOKS_TO_TENTATIVELY_EXCLUDE = ["examples/aqt_compile.ipynb"]

    exit(
        applications_superstaq.check.pytest_.run(
            *sys.argv[1:], integration_setup=set_env_vars, exclide=NOTEBOOKS_TO_TENTATIVELY_EXCLUDE
        )
    )
