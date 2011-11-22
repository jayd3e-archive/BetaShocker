import urllib
import re
import time
import lxml.html
from datetime import date
from tornado import httpclient 

def parse_post(body):
    match = re.match("\s+.+: (.+)", body) 
    members = match.group(1).split(", ")
    last_member = members.pop()
    last_member = last_member.split(" and ")
    last_member[1] = last_member[1].replace("\r", "")
    members.extend(last_member)
    return members

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
            else:
                continue

def main(num_of_pages):
    posts = []
    members = []
    member_stats = {}
    http_client = httpclient.HTTPClient()
    for current_page_num in range(1, num_of_pages + 1):
        response = get_page(http_client, 
                            "http://www.playdota.com/forums/549614-page" +\
                            str(current_page_num) +\
                            "/daily-draw-winners/",
                            allowed_attempts=3)
        # We need to make sure that the body is unicode and the correct encoding
        # going in, or lxml will guess incorrectly for some of the names
        body = response.body.decode("windows-1250")
        for tag in lxml.html.fromstring(body).xpath("//div[@id]"):
            is_post = tag.attrib['id'].startswith("post_message")
            if is_post:
                added_members = parse_post(tag.text_content())
                members.extend(added_members)
    
    i = 0
    num_of_members = len(members)
    for member in members:
        j = 0
        # playdota doesn't like spaces in the names
        member = urllib.quote(member.encode("windows-1250"))
        member = member.replace(" ", "+")
        response = get_page(http_client,
                            "http://www.playdota.com/forums/members/" + member + "/",
                            allowed_attempts=3)
                   
        body = response.body.decode("windows-1250")
        html = lxml.html.fromstring(body)
            
        try:
            stats_mini = html.get_element_by_id("stats_mini")
            profile = stats_mini.xpath("//dl[@class='smallfont list_no_decoration profilefield_list']")
            stat_names = profile[0].xpath(".//dt")
            stats = profile[0].xpath(".//dd")
            for name in stat_names:
                name = name.text_content()
                if name == "Join Date":
                    join_date_str = stats[j].text_content()
                    join_date_list = join_date_str.split("-")
                    month = int(join_date_list[0])
                    day = int(join_date_list[1])
                    year = int(join_date_list[2])
                elif name == "Total Posts":
                    total_posts = stats[j].text_content()
                    # Remove all commas so it can be parsed by int()
                    total_posts = total_posts.replace(",", "")
                j += 1
            i += 1
            print("Status(" + member + "): " + str(i) + "/" + str(num_of_members - 1))

            member_stats[member] = {"join_date" : date(year, month, day), "total_posts" : int(total_posts)}
        
        except KeyError, e:
            # lxml throws a KeyError if it can't find an element with the specified id, we use this
            # to determine if we are on a profile page, or if the user doesn't exist
            continue 
    
    members_total_posts = 0
    members_total_days = 0
    for name, stats in member_stats.items():
        members_total_posts += stats["total_posts"]
        td = date.today() - stats["join_date"]
        members_total_days += td.days

    average_posts = members_total_posts / num_of_members
    average_days = members_total_days /num_of_members

    print("Average Posts: " + str(average_posts))
    print("Average Days: " + str(average_days))
        
if __name__ == "__main__":
    main(3)
