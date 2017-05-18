#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, json, urllib


#TODO Convert auth obeject payload from str to dict and the use JSON dumps to create the payload

class AOSSAuth():
    """
    This class requests and stores an authentication cookie for the Aruba AOS
    Switch Software.
    """
    def __init__(self, switchip, username, password, version="v3", protocol = "http"):
        url_login =  protocol + "://" + switchip + "/rest/"+version+"/login-sessions"
        payload_dict = {"userName" : username, "password" : password }
        requests.packages.urllib3.disable_warnings()
        get_cookie = requests.request("POST", url_login, data=json.dumps(payload_dict),
                                      verify=False)
        r_cookie = get_cookie.json()['cookie']
        self.cookie = r_cookie
        self.ipaddr = switchip
        self.version = version


    def logout(self):
        url_login = "http://" + self.ipaddr + "/rest/v1/login-sessions"
        headers = {'cookie': self.cookie}
        r = requests.delete(url_login, headers=headers)
        return r.status_code



def get_rest_version(auth):
    """
    Function to get API version number from Aruba OS switch
    :param auth:  AOSSAuth class object returned by pyarubaoss.auth
    :return
    :rtype
    """
    headers = {'cookie': auth.cookie}
    url_rest_version = "http://" + auth.ipaddr + "/rest/"+auth.version+"/version"
    try:
        r = requests.get(url_rest_version, headers=headers)
        rest_version = json.loads(r.text)
        return rest_version
    except requests.exceptions.RequestException as error:
        return "Error:\n" + str(error) + " get_rest_version: An Error has occured"





