from django.db import models


class Game(models.Model):
    class TurnChoice(models.IntegerChoices):
        PLAYER_1 = 1, "Player 1"
        PLAYER_2 = 2, "Player 2"

    class Status(models.IntegerChoices):
        WAITING = 0, "Waiting"
        PLAYING = 1, "Playing"
        FINALIZED = 2, "Finalized"

    class Type(models.IntegerChoices):
        PVP = 1, "PVP"
        PVE = 2, "PVE"

    matrix = models.JSONField(default=list)
    turn = models.IntegerField(choices=TurnChoice.choices, default=1)
    player1 = models.CharField(max_length=20, null=True)
    player2 = models.CharField(max_length=20, null=True)
    winner = models.CharField(max_length=20, null=True)
    status = models.IntegerField(choices=Status.choices, default=0)
    moves = models.IntegerField(default=0)
    size = models.IntegerField(default=7)
    type_game = models.IntegerField(choices=Type.choices, default=1)
    posible_moves = models.JSONField(default=list)

    def check_tied_game(self):
        self.moves += 1
        is_tied = (self.size * self.size) == self.moves and not self.winner
        if is_tied:
            self.winner = "TIED GAME"
        self.save()
        return is_tied

    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1
        self.save()

    def set_winner(self, user):
        self.moves += 1
        self.status = 2
        self.winner = user
        self.save()

    def set_matrix(self, matrix):
        self.matrix = matrix
        self.save()

    def is_full(self):
        return bool(self.player1 and self.player2)

    def set_player1(self, user):
        self.player1 = user
        self.save()

    def set_player2(self, user):
        self.player2 = user
        self.save()

    def start_game(self):
        self.status = self.Status.PLAYING
        self.save()

    def get_user_code(self, user):
        if user == self.player1:
            return 1
        return 2

    def initilize_matrix(self):
        self.matrix = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        self.save()

    def generate_posible_moves(self):
        moves = []
        for row in range(self.size):
            for column in range(self.size):
                moves.append(f"{row},{column}")
        self.posible_moves = moves
        self.save()

    def pop_move(self, value):
        moves = self.posible_moves
        index = moves.index(value)
        moves.pop(index)
        self.posible_moves = moves
        self.save()

    def get_user_by_turn(self):
        if self.turn == 1:
            return self.player1
        return self.player2

    def surrender(self, user):
        if user == self.player1:
            self.winner = self.player1
        else:
            self.winner = self.player2
        self.save()

    def set_type_game(self, type):
        self.type_game = type
        self.save()
