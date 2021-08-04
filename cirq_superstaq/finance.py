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


def find_min_vol_portfolio(stock_symbols: List[str], desired_return: float) -> Dict:
    """Finds the optimal equal-weight portfolio from a possible pool of stocks
    according to the following rules:
    -All stock must come from the stock_symbols list.
    -All stocks will be equally weighted in the portfolio.
    -The return of the optimal portfolio must exceed the desired_return.
    -The portfolio volatility (or standard deviation of returns) is minimized.

    Args:
        stock_symbols: A list of stock tickers to pick from.
        desired_return: The minimum return needed.

    Return:
        A dictionary containing the assets in the optimal portfolio and
        the portfolio's expected return and standard deviation.

    """

    superstaq_json = {
        "stock_symbols": json.loads(cirq.to_json(stock_symbols)),
        "desired_return": json.loads(cirq.to_json(desired_return)),
    }

    result = requests.post(
        _get_api_url() + "/" + API_VERSION + "/minvol",
        json=superstaq_json,
        headers=_get_headers(),
        verify=_should_verify_requests(),
    )

    result.raise_for_status()
    response = result.json()

    portfolio = cirq.read_json(json_text=response["portfolio_dictionary"])
    return portfolio


def find_max_sharpe_ratio(stock_symbols: List[str], k: float) -> Dict:
    """Finds the optimal equal-weight portfolio from a possible pool of stocks
    according to the following rules:
    -All stock must come from the stock_symbols list.
    -All stocks will be equally weighted in the portfolio.
    -The Sharpe ratio of the portfolio is maximized.

    The Sharpe ratio can be thought of as the ratio of reward to risk.
    The formula for the Sharpe ratio is the portfolio's expected return less the risk-free
    rate divided by the portfolio standard deviation. For the risk-free rate, we will use the
    three month treasury bill rate.


    Args:
        stock_symbols: A list of stock tickers to pick from.
        k: A risk coefficient that balances favoring minimizing risk or maximizing
        expected return in the objective function.

    Return:
        A dictionary containing the assets in the optimal portfolio and
        the portfolio's expected return and standard deviation, as well as the Sharpe ratio
        of the portfolio.

    """

    superstaq_json = {
        "stock_symbols": json.loads(cirq.to_json(stock_symbols)),
        "k": json.loads(cirq.to_json(k)),
    }

    result = requests.post(
        _get_api_url() + "/" + API_VERSION + "/maxsharpe",
        json=superstaq_json,
        headers=_get_headers(),
        verify=_should_verify_requests(),
    )

    result.raise_for_status()
    response = result.json()

    portfolio = cirq.read_json(json_text=response["portfolio_dictionary"])
    return portfolio
