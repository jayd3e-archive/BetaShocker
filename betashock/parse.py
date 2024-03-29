import re
import time
import lxml.html
from datetime import date
from betashock.exc import ParseError
from betashock.cache import set_member_stats

MONTHS = {'Jan' : 1,
		  'Feb' : 2,
		  'Mar' : 3,
		  'Apr' : 4,
		  'May' : 5,
		  'Jun' : 6,
		  'Jul' : 7,
		  'Aug' : 8,
		  'Sep' : 9,
		  'Oct' : 10,
		  'Nov' : 11,
		  'Dec' : 12}

def parse_winnerlist_thread(body):
	members = []
	for tag in lxml.html.fromstring(body).xpath("//div[@id]"):
		is_post = tag.attrib['id'].startswith("post_message")
		if is_post:
			match = re.match("\s+.+: (.+)", tag.text_content())
			added_members = match.group(1).split(", ")
			last_member = added_members.pop()
			last_member = last_member.split(" and ")
		 	last_member[1] = last_member[1].replace("\r", "")
		 	added_members.extend(last_member)
			members.extend(added_members)
	
	i = 0
	for member in members:
		if isinstance(member, unicode):
			members[i] = member.encode("windows-1250", "replace")
		i += 1

	return members

def parse_entrant_name(post):
	path = "./div[@class='page_spacer']/" +\
		   "div/" +\
		   "div[@id]/" +\
		   "div[@class='tborder vbseo_like_postbit_big']/" +\
		   "div[@class='tborder vbseo_like_postbit_big_right']/" +\
		   "table[@id]/" +\
		   "tr[@valign='top']/" +\
		   "td[@class='alt2']/" +\
		   "div[@id]/" +\
		   "a[@class='bigusername']"
	bigusername = post.xpath(path)[0]
	return bigusername.text_content()

def parse_entrant_data(post):
	path = "./div[@class='page_spacer']/" +\
		   "div/" +\
		   "div[@id]/" +\
		   "div[@class='tborder vbseo_like_postbit_big']/" +\
		   "div[@class='tborder vbseo_like_postbit_big_right']/" +\
		   "table[@id]/" +\
		   "tr[@valign='top']/" +\
		   "td[@class='alt2']/" +\
		   "div[@class='smallfont']/" +\
		   "div[@class='postbit_field']"
	
	postbit_fields = post.xpath(path)
	month, day, year = 0, 0, 0
	total_posts = 0
	for postbit_field in postbit_fields:
		stats = postbit_field.text_content().split(": ")
		if stats[0] == "Join Date":
			join_date_list = stats[1].split(" ")
			month_prefix = join_date_list[0]
			month = MONTHS[month_prefix]
			day = 1
			year = int(join_date_list[1])
		elif stats[0] == "Posts":
			# Remove all commas so it can be parsed by int()
			total_posts = stats[1].replace(",", "")

	return {"join_date" : date(year, month, day), "total_posts" : int(total_posts)}

def parse_entrantlist_thread(page):
	html = lxml.html.fromstring(page)
	posts = html.get_element_by_id("posts")

	entrants = []
	for post in posts.xpath("./div[@align='center']"):
		member_name = parse_entrant_name(post)
		# Memcached doesn't like spaces in keys and unicode
		member_name = member_name.replace(" ", "_")
		if isinstance(member_name, unicode):
			member_name = member_name.encode("windows-1250", "replace")
		member_stat = parse_entrant_data(post)
		if not member_name in entrants:
			entrants.append(member_name)
			set_member_stats(member_name, member_stat)
   
	return entrants

def parse_last_page_num(page):
	html = lxml.html.fromstring(page)
	pagenav = html.find_class("pagenav")
	last_td = pagenav[0].xpath(".//td[@nowrap='nowrap']")
	last_link = last_td[0].xpath(".//a[@class='smallfont']")
	href = last_link[0].attrib['href']

	# Get page number
	match = re.match("http://www.playdota.com/forums/\d+-page(\d+)/.+/", href)
	return int(match.group(1))