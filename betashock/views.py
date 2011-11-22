from pyramid.view import view_config
from pyramid.exceptions import NotFound
from betashock.cache import get_member_stats
from datetime import date

@view_config(context=NotFound,
             renderer='exceptions/not_found.mako')
def notFound(request):
    title = 'Page Not Found'
    return {'title':title}

@view_config(route_name='index', renderer='index.mako')
def index(request):
    title = "BetaShocker"
    member_stats = get_member_stats()
    num_of_members = len(member_stats)

    members_total_posts = 0
    members_total_days = 0
    for name, stats in member_stats.items():
        members_total_posts += stats["total_posts"]
        td = date.today() - stats["join_date"]
        members_total_days += td.days

    avg_total_posts = members_total_posts / num_of_members
    avg_days = members_total_days / num_of_members

    return {'title':title,
    		'avg_total_posts':avg_total_posts,
    		'avg_days':avg_days}