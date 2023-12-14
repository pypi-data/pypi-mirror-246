 The only function of this library receives 5 parameters
 API_KEY:             pass an api key
 RESULT_TOTAL:        a total of results that you want to obtain, max 10 for the public api
 COUNTRY:             prefix of the country to which to make the request ("AR") ------> https://laendercode.net/es/2-letter-list.html
 QUERY_TYPE:          type of request ("vuln_num")
 RESULT_TYPE:         type of result to obtain ("org", "domain", "city", "ip", "port")

-------------------- Example use ------------------------
import sysprl

response, status = sysprl.Query("prl412_9vmjwutt2ch3aom5ho9t", 10, "AR", "vuln_num", "org")

for key, value in response.items():
    print(f"{key}: {value}")
