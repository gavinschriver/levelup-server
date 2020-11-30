import sqlite3
from django.shortcuts import render
from levelupapi.models import Event
from levelupreports.views import Connection

def userevent_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                e.id,
                e.date,
                e.time,
                g.title AS game_name,
                u.id user_id,
                u.first_name || ' ' || u.last_name AS full_name
            FROM
                levelupapi_event e
            JOIN
                levelupapi_game g ON g.id = e.game_id
            JOIN 
                levelupapi_eventgamer eg ON eg.event_id = e.id
            JOIN
                levelupapi_gamer gr ON gr.id = eg.gamer_id
            JOIN
                auth_user u ON gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()
            events_by_user = {}

            for row in dataset:
                event = Event()
                event.id = row["id"]
                event.date = row["date"]
                event.time = row["time"]
                event.game_name = row["game_name"]

                uid = row["user_id"]

                if uid in events_by_user:
                    events_by_user[uid]['events'].append(event)
                else:
                    events_by_user[uid] = {}
                    events_by_user[uid]["id"] = uid
                    events_by_user[uid]["full_name"] = row["full_name"]
                    events_by_user[uid]["events"] = [event]
                
        list_of_users_with_events = events_by_user.values()

        template = 'users/list_with_events.html'

        context = {'userevent_list': list_of_users_with_events}

        return render(request, template, context)

