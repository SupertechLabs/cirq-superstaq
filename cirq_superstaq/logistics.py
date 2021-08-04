import json
import os
from typing import Dict, List

import cirq
import requests
from cirq_superstaq import API_URL, API_VERSION


def _get_api_url() -> str:
    return os.getenv("SUPERSTAQ_REMOTE_HOST", default=API_URL)


def _get_headers() -> dict:
    return {
        "Authorization": os.environ["SUPERSTAQ_API_KEY"],
        "Content-Type": "application/json",
    }


def _should_verify_requests() -> bool:
    """Returns the appropriate ``verify`` kwarg for requests.
    When we test locally, we don't have a certificate so we can't verify.
    When running against the production server (API_URL), we should verify.
    """
    return _get_api_url() == API_URL


def tsp(locs: List[str]) -> Dict:
    """Solves the traveling salesperson problem with a tour that
    begins and ends at the first location in the input list.

    Args:
        locs: A list of strings where each string is a location
        we need to visit on our tour.

    Returns:
        A dictionary containing relevant information about the tour.

    """

    superstaq_json = {"locs": json.loads(cirq.to_json(locs))}

    result = requests.post(
        _get_api_url() + "/" + API_VERSION + "/tsp",
        json=superstaq_json,
        headers=_get_headers(),
        verify=_should_verify_requests(),
    )

    result.raise_for_status()
    response = result.json()

    tour = cirq.read_json(json_text=response["tour_dictionary"])
    return tour


def warehouse(k: int, possible_warehouses: List[str], customers: List[str]) -> Dict:
    """
    This function solves the warehouse location problem, which is:
    given a list of customers to be served and  a list of possible warehouse
    locations, find the optimal k warehouse locations such that the sum of
    the distances to each customer from the nearest facility is minimized.

    Args:
        k: An integer representing the number of warehouses in the solution.
        possible_warehouses: A list of possible warehouse locations.
        customers: A list of customer locations.

    Returns:
        A dictionary with:
        -A list of tuples where the first string in the tuple is the warehouse
        and the second is the customer served by that warehouse.
        -The sum of all distances from nearest warehouse to each customer.
        -A link to the map of the warehouse-customer pairings.
        -A list of which k warehouses are open.


    """

    superstaq_json = {
        "k": json.loads(cirq.to_json(k)),
        "possible_warehouses": json.loads(cirq.to_json(possible_warehouses)),
        "customers": json.loads(cirq.to_json(customers)),
    }

    result = requests.post(
        _get_api_url() + "/" + API_VERSION + "/warehouse",
        json=superstaq_json,
        headers=_get_headers(),
        verify=_should_verify_requests(),
    )

    result.raise_for_status()
    response = result.json()

    pairings = cirq.read_json(json_text=response["solution_dictionary"])
    return pairings
