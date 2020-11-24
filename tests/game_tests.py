import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game

class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """

        # register a user
        url = "/register"
        data = {
            "username": "disboy",
            "password": "disboy",
            "email": "disboy@disboy.disboy",
            "address": "666 up ya bum",
            "phone_number": "77777777",
            "first_name": "dis",
            "last_name": "bouy",
            "bio": "the only one"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        # store token for future tests
        self.token = json_response['token']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # store a gametype in database for future tests
        gametype = GameType()
        gametype.name = "Board game"
        gametype.save()

    def test_create_game(self):
        """
        Ensure we can create a new game
        """
        url = "/games"
        data = {
            "gameTypeId": 1,
            "skillLevel": 5,
            "title": "Clue",
            "numberOfPlayers": 5,
            "maker": "hasbroz"
        }

        # set HTTP Authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Make POST request to url with data object
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        # ensure you got a HTTP 201 response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # ensure that properties on the created resource are all accurate
        self.assertEqual(json_response['title'], 'Clue')
        self.assertEqual(json_response['skill_level'], 5)
        self.assertEqual(json_response['number_of_players'], 5) 

        game = Game.objects.get(title='Clue')
        self.assertEqual(game.title, 'Clue')
        self.assertEqual(game.gametype.id, 1)
        self.assertEqual(game.skill_level, 5)
        self.assertEqual(game.number_of_players, 5)
        self.assertEqual(game.added_by.id, 1)

    
    def test_get_game(self):
        game = Game()
        game.title = "Managanma"
        game.maker = "ya mama"
        game.added_by_id = 1
        game.gametype_id = 1
        game.skill_level = 5
        game.number_of_players = 3
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/games/{game.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], "Managanma")
        self.assertEqual(json_response["maker"], "ya mama")
        self.assertEqual(json_response["skill_level"], 5)
        self.assertEqual(json_response["number_of_players"], 3)

    def test_get_all_games(self):
        pass

    def test_change_game(self):
        game = Game()
        game.gametype_id = 1
        game.skill_level = 5
        game.title = "yes please"
        game.maker = "these guys"
        game.number_of_players = 3
        game.added_by_id = 1
        game.save()

        data = {
            "gameTypeId": 1,
            "skillLevel": 3,
            "title": "no thanks",
            "maker": "those peeps",
            "numberOfPlayers" : 4
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["title"], "no thanks")
        self.assertEqual(json_response["maker"], "those peeps")
        self.assertEqual(json_response["number_of_players"], 4)
        self.assertEqual(json_response["skill_level"], 3)


    def test_delete_game(self):
        """
        Ensure we can delete an existing game
        """
        game = Game()
        game.gametype_id = 1
        game.skill_level = 3
        game.title = "Sorry"
        game.maker = "sorrynotsorry"
        game.number_of_players = 4
        game.added_by_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Delete the game we just created and verify a 204 response
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Try to delete the same game again and verify a 404 respons
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
