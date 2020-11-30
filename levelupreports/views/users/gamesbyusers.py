import sqlite3
from django.shortcuts import render
from levelupapi.models import Game
from levelupreports.views import Connection

def usergame_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                g.id,
                g.title,
                g.maker,
                g.gametype_id,
                g.number_of_players,
                g.skill_level,
                u.id user_id,
                u.first_name || ' ' || u.last_name AS full_name
            FROM
                levelupapi_game g
            JOIN
                levelupapi_gamer gr ON g.added_by_id = gr.id
            JOIN
                auth_user u ON gr.user_id = u.id
            """)

            dataset = db_cursor.fetchall()
            games_by_user = {}

            for row in dataset:
                game = Game()
                game.title = row["title"]
                game.maker = row["maker"]
                game.skill_level = row["skill_level"]
                game.number_of_players = row["number_of_players"]
                game.gametype_id = row["gametype_id"]

                uid = row["user_id"]

                if uid in games_by_user:
                    games_by_user[uid]['games'].append(game)
                else:
                    games_by_user[uid] = {}
                    games_by_user[uid]["id"] = uid
                    games_by_user[uid]["full_name"] = row["full_name"]
                    games_by_user[uid]["games"] = [game]
                
        list_of_users_with_games = games_by_user.values()

        template = 'users/list_with_games.html'

        context = {'usergame_list': list_of_users_with_games}

        return render(request, template, context)

