import urllib
from betashock.cache import cached
from betashock.parse import parse_memberlist_thread
from betashock.parse import parse_profile_page
from betashock.exc import ParseError
from tornado import httpclient

def get_page(http_client, url, allowed_attempts=0, **kwargs):
    """
    Noticed that some of the requests were just timing out for no apparent reason.
    This function virtually guarentees that a response is returned.
    """
    attempts = 0
    while True:
        try:
            response = http_client.fetch(url, **kwargs)
            return response
        except httpclient.HTTPError, e:
            attempts += 1
            if attempts == allowed_attempts:
                print "Error:", e
                break
            else:
                time.sleep(2*attempts)
                continue

@cached("members", 86400)
def get_member_stats():
    num_of_pages = 3
    posts = []
    members = []
    member_stats = {}
    http_client = httpclient.HTTPClient()
    for current_page_num in range(1, num_of_pages + 1):
        response = get_page(http_client, 
                            "http://www.playdota.com/forums/549614-page" +\
                            str(current_page_num) +\
                            "/daily-draw-winners/",
                            allowed_attempts=5)
        # We need to make sure that the body is unicode and the correct encoding
        # going in, or lxml will guess incorrectly for some of the names
        body = response.body.decode("windows-1250")
        added_members = parse_memberlist_thread(body)
        members.extend(added_members)

    i = 0
    num_of_members = len(members)

    for member in members:
        i += 1
        print("Building Cache: " + str(i) + "/" + str(num_of_members) + " members")

        # playdota doesn't like spaces in the names
        try:
            member = urllib.quote(member.encode("windows-1250"))
        except UnicodeEncodeError, e:
            # if we can't form the url, just skip that user
            continue
        member = member.replace(" ", "+")
        response = get_page(http_client,
                            "http://www.playdota.com/forums/members/" + member + "/",
                            allowed_attempts=5)
        
        body = response.body.decode("windows-1250")
        try:
            member_stats[member] = parse_profile_page(body)
        except ParseError, e:
            print(e.message)
            continue
    
    return member_stats