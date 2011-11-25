import urllib
import time
from betashock.cache import cached
from betashock.cache import mc_pool
from betashock.cache import get_member_stats
from betashock.parse import parse_winnerlist_thread
from betashock.parse import parse_entrantlist_thread
from betashock.parse import parse_last_page_num
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

def get_last_page_num(http_client, url):
    response = get_page(http_client, 
                        url,
                        allowed_attempts=5)
    body = response.body.decode("windows-1250")
    return parse_last_page_num(body)

@cached("winners", 86400)
def get_winner_list():
    http_client = httpclient.HTTPClient()
    num_of_pages = 3
    winners = []

    for current_page_num in range(1, num_of_pages + 1):
        print("(Winners)On Page: " + str(current_page_num) + "/" + str(num_of_pages))
        response = get_page(http_client, 
                            "http://www.playdota.com/forums/549614-page" +\
                            str(current_page_num) +\
                            "/daily-draw-winners/",
                            allowed_attempts=5)
        body = response.body
        added_winners = parse_winnerlist_thread(body)
        winners.extend(added_winners)

    return winners

def get_winner_stats():
    winner_stats = {}
    winners = get_winner_list()

    for winner in winners:
        winner_stats[winner] = get_member_stats(winner)
    
    return winner_stats

@cached("entrants", 86400)
def get_entrant_list():
    http_client = httpclient.HTTPClient()
    num_of_pages = get_last_page_num(http_client, "http://www.playdota.com/forums/549077-page1/playdota-beta-key-draw/")

    entrants = []
    for current_page_num in range(1, num_of_pages + 1):
        print("(Entrants)On Page: " + str(current_page_num) + "/" + str(num_of_pages))
        response = get_page(http_client, 
                        "http://www.playdota.com/forums/549077-page" +\
                        str(current_page_num) +\
                        "/playdota-beta-key-draw/",
                        allowed_attempts=5)
        
        body = response.body
        added_entrants = parse_entrantlist_thread(body)
        entrants.extend(added_entrants)
    return entrants

def get_entrant_stats():
    entrant_stats = {}
    entrants = get_entrant_list()

    for entrant in entrants:
        entrant_stats[entrant] = get_member_stats(entrant)
    
    return entrant_stats