"""
URL request class

Handles HTTP JSON-RPC requests for RANDOM.ORG
"""

__author__ = u"Mike Caprio"
__version__ = u"$Revision: 0.1 $"
__date__ = u"$Date: 2013/09/13 00:36:15 $"
__copyright__ = u""
__license__ = u"Python"

import requests
import time
import json


def dorequest(url, params_dict, method=u"POST", debug=False):
    # Wait time in seconds
    wait_time = 5

    for key in params_dict:
        # Remove keys with no value
        if (key is None):
            del params_dict[key]

# Might still need this on staging / production, must test
#    conn = httplib2.Http(disable_ssl_certificate_validation=True)

    headers_dict = {}
    headers_dict["User-Agent"] = u"RANDOM.ORG fetch " + __version__
    headers_dict["Content-type"] = u"application/json-rpc"
    headers_dict["Accept"] = u"application/json-rpc"

#    request_source = u"User-Agent:" + headers_dict["User-Agent"]

#    request_sent = method + u" " + url + u" HTTP/1.1\n" + request_source + \
#        u"\nContent-type: " + headers_dict["Content-type"] + u"\nAccept: " + \
#        headers_dict["Accept"] + u"\n\n" + unicode(params_dict)

#    if (debug):
#        print request_sent

    response = None
    final_val = None

    data_json = json.dumps(params_dict)

    # Keep trying until we get a successful response - POST only supported
    while True:
        try:
            response = requests.post(url, data=data_json, headers=headers_dict)
        except requests.exceptions.HTTPError:
            return None

        if (response is not None):
            if (response.status_code is not None):
                if (response.status_code != requests.codes.ok):
                    # Check for error, wait and try again
                    time.sleep(wait_time)
                else:
                    if (response.text is not None):
                        if (debug):
                            print response.text

                        final_val = response.text

                        break
                    else:
                        # No response, try again
                        time.sleep(wait_time)

    return final_val
