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
    num_of_winners = len(winner_stats)

    winners_total_posts = 0
    winners_total_days = 0
    winners_old_300 = 0
    winners_old_20 = 0
    winners_random = 0

    for name, stats in winner_stats.items():
        # Occassionally a winner will have deleted their account
        if stats == None:
            continue
        
        # Get info for averages
        winners_total_posts += stats["total_posts"]
        td = date.today() - stats["join_date"]
        winners_total_days += td.days

        # Get info for percentages
        if stats['total_posts'] > 300 and winners_total_days >= 365:
            winners_old_300 += 1
        elif (stats['total_posts'] < 300 and stats['total_posts'] > 20) and winners_total_days >= 365:
            winners_old_20 += 1
        else:
            winners_random += 1

    avg_total_posts = winners_total_posts / num_of_winners
    avg_days = winners_total_days / num_of_winners
    perc_old_300 = round(float(winners_old_300) / num_of_winners * 100, 2)
    perc_old_20 = round(float(winners_old_20) / num_of_winners * 100, 2)
    perc_random = round(float(winners_random) / num_of_winners * 100, 2)

    return {'title':title,
    		'avg_total_posts':avg_total_posts,
    		'avg_days':avg_days,
            'perc_old_300':perc_old_300,
            'perc_old_20':perc_old_20,
            'perc_random':perc_random}