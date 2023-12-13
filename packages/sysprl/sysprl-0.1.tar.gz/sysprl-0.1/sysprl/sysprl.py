# The only function of this library receives 5 parameters
# API_KEY:             pass an api key
# RESULT_TOTAL:        a total of results that you want to obtain, max 10 for the public api
# COUNTRY:             prefix of the country to which to make the request ("AR") ------> https://laendercode.net/es/2-letter-list.html
# QUERY_TYPE:          type of request ("vuln_num")
# RESULT_TYPE:         type of result to obtain ("org", "domain", "city", "ip", "port")
#
# -------------------- Example use ------------------------
# import sysprl
#
# response, status = sysprl.Query("prl412_9vmjwutt2ch3aom5ho9t", 10, "AR", "vuln_num", "org")
#
#  for key, value in response.items():
#    print(f"{key}: {value}")
#

import requests

def Query(API_KEY, RESULT_TOTAL, COUNTRY, QUERY_TYPE, RESULT_TYPE):
    if QUERY_TYPE == "vuln_num":
        QUERY_TYPE = "tiene_vulnerabilidad:true"
    else:
        pass

    QUERY = f"pais:{COUNTRY} {QUERY_TYPE}"

    data_query = {
        "query": QUERY,
        "type_data": RESULT_TYPE,
        "cantidad": RESULT_TOTAL,
        "key": API_KEY
    }

    response = requests.get("https://elite6-27.org/prl412/", params=data_query).json()
    result = response.get("results", {})
    status = response.get("status", {})

    return result, status
