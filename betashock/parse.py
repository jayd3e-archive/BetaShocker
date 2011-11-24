import re
import time
import lxml.html
from datetime import date
from betashock.exc import ParseError

def parse_memberlist_thread(body):
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
	return members

def parse_profile_page(page):
	try:
		html = lxml.html.fromstring(page)
		stats_mini = html.get_element_by_id("stats_mini")
		profile = stats_mini.xpath("//dl[@class='smallfont list_no_decoration profilefield_list']")
		stat_names = profile[0].xpath(".//dt")
		stats = profile[0].xpath(".//dd")

		i = 0
		for name in stat_names:
		    name = name.text_content()
		    if name == "Join Date":
		        join_date_str = stats[i].text_content()
		        join_date_list = join_date_str.split("-")
		        month = int(join_date_list[0])
		        day = int(join_date_list[1])
		        year = int(join_date_list[2])
		    elif name == "Total Posts":
		        total_posts = stats[i].text_content()
		        # Remove all commas so it can be parsed by int()
		        total_posts = total_posts.replace(",", "")
		    i += 1

		return {"join_date" : date(year, month, day), "total_posts" : int(total_posts)}
	except KeyError, e:
		# lxml throws a KeyError if it can't find an element with the specified id, we use this
		# to determine if we are on a profile page, or if the user doesn't exist
		raise ParseError("The page passed in is not a profile page.")