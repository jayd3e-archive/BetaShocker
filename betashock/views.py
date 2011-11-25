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
    entrant_stats = get_entrant_stats()
    winner_stats = get_winner_stats()

    winner_avg_total_posts,\
    winner_avg_days,\
    winner_perc_old_300,\
    winner_perc_old_20,\
    winner_perc_random = generate_output(winner_stats)

    entrant_avg_total_posts,\
    entrant_avg_days,\
    entrant_perc_old_300,\
    entrant_perc_old_20,\
    entrant_perc_random = generate_output(entrant_stats)

    return {'title':title,
    		'winner_avg_total_posts':winner_avg_total_posts,
    		'winner_avg_days':winner_avg_days,
            'winner_perc_old_300':winner_perc_old_300,
            'winner_perc_old_20':winner_perc_old_20,
            'winner_perc_random':winner_perc_random,
            'entrant_avg_total_posts': entrant_avg_total_posts,
            'entrant_avg_days':entrant_avg_days,
            'entrant_perc_old_300':entrant_perc_old_300,
            'entrant_perc_old_20':entrant_perc_old_20,
            'entrant_perc_random':entrant_perc_random}

def generate_output(member_stats):
    num_of_members = len(member_stats)

    total_posts = 0
    total_days = 0
    old_300 = 0
    old_20 = 0
    random = 0

    # Statistics
    for name, stats in member_stats.items():
        # Occassionally a winner will have deleted their account
        if stats == None:
            continue
        
        # Get info for averages
        total_posts += stats["total_posts"]
        td = date.today() - stats["join_date"]
        total_days += td.days

        # Get info for percentages
        if stats['total_posts'] > 300 and total_days >= 365:
            old_300 += 1
        elif (stats['total_posts'] < 300 and stats['total_posts'] > 20) and total_days >= 365:
            old_20 += 1
        else:
            random += 1

    avg_total_posts = total_posts / num_of_members
    avg_days = total_days / num_of_members
    perc_old_300 = round(float(old_300) / num_of_members * 100, 2)
    perc_old_20 = round(float(old_20) / num_of_members * 100, 2)
    perc_random = round(float(random) / num_of_members * 100, 2)

    return avg_total_posts, avg_days, perc_old_300, perc_old_20, perc_random