#!/usr/bin/env python

import requests

import argparse, urllib

import http.client, urllib


def requestsLib(server, parameters):
    url = urllib.parse.urljoin("http://"+server, "api/miningoperation/Adn")
    return requests.post(url, data=parameters)


def builtinLib(server, path, params):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    connection = http.client.HTTPConnection(server)
    connection.request("POST", path, urllib.parse.urlencode(params), headers)
    response = connection.getresponse()
    return response, response.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demonstrates web polling from Germine")
    parser.add_argument("server", help="Url of the Germine web server to communicate with")
    parser.add_argument("--endpoint", default="dict", help="Queried endpoint")
    args = parser.parse_args()

    url = urllib.parse.urljoin("http://"+args.server, args.endpoint)
    response = requests.get(url)

    template = "Mining app: {mining_app[name]}, Algo: {currency[algorithm][name]}"
    print("### DICT ###")
    print(response.json())
    print(template.format(**response.json()))

    print("\n### MINING OPERATION ###")
    parameters = {"mininghardware": "1080Ti", "system": "6600_Ubuntu"}

    response = requestsLib(args.server, parameters)
    print("lib requests response({}): {}".format(response.status_code, response.text))

    response, body = builtinLib(args.server, "api/miningoperation/Adn", parameters)
    print("builtin response({}): {}".format(response.status, body))

