from pyramid.view import view_config
from pyramid.exceptions import NotFound
from betashock.retrieve import get_winner_stats
from betashock.retrieve import get_entrant_stats
from datetime import date

@view_config(context=NotFound,
             renderer='exceptions/not_found.mako')
def notFound(request):
    title = 'Page Not Found'
    return {'title':title}

@view_config(route_name='index', renderer='index.mako')
def index(request):
    title = "BetaShocker"
    #member_stats = get_winner_stats()
    entrant_stats = get_entrant_stats()
    num_of_members = len(member_stats)

    members_total_posts = 0
    members_total_days = 0
    members_old_300 = 0
    members_old_20 = 0
    members_random = 0

    for name, stats in member_stats.items():
        # Get info for averages
        members_total_posts += stats["total_posts"]
        td = date.today() - stats["join_date"]
        members_total_days += td.days

        # Get info for percentages
        if stats['total_posts'] > 300 and members_total_days >= 365:
            members_old_300 += 1
        elif (stats['total_posts'] < 300 and stats['total_posts'] > 20) and members_total_days >= 365:
            members_old_20 += 1
        else:
            members_random += 1

    avg_total_posts = members_total_posts / num_of_members
    avg_days = members_total_days / num_of_members
    perc_old_300 = round(float(members_old_300) / num_of_members * 100, 2)
    perc_old_20 = round(float(members_old_20) / num_of_members * 100, 2)
    perc_random = round(float(members_random) / num_of_members * 100, 2)

    return {'title':title,
    		'avg_total_posts':avg_total_posts,
    		'avg_days':avg_days,
            'perc_old_300':perc_old_300,
            'perc_old_20':perc_old_20,
            'perc_random':perc_random}