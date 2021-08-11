import random
import tkinter as tk
from time import sleep


class Player:
    def __init__(self, name, number, position, team, ball=None):
        self.name = name
        self.number = number
        self.position = position
        self.team = team
        self.ball = ball

    def passes(self):
        self.ball = None

    def shoots(self):
        self.ball = None
        side = ["left", "right"]
        return random.choice(side)

    def jumps(self):
        self.ball = None
        side = ["left", "right"]
        return random.choice(side)

    def has_the_ball(self):
        # return self.ball
        if self.ball:
            return True
        # return False


class Team:
    def __init__(self, name, color, players):
        self.name = name
        self.color = color
        self.players = players

    def __str__(self):
        return self.name


class Match:
    def __init__(self, teams, field):
        self.team_1 = teams[0]
        self.team_2 = teams[1]
        self.field = field
        self.score_board = Score(self.team_1.name, self.team_2.name)
        self.all_players = self.team_1.players + self.team_2.players
        self.goalkeepers = [self.team_1.players[0], self.team_2.players[0]]
        self.strikers = [self.team_1.players[4], self.team_2.players[4]]
        self.ball = Ball()

    def start(self, listbox, parent, *args):
        self.ball_to_striker(self.team_1, "1")
        self.play(listbox, parent, args[0], args[1])

    def play(self, listbox, parent, score_1, score_2, duration=30):
        action = 0
        side_shoot = ""
        side_jump = ""

        print()

        for p in self.all_players:
            print(p.name, p.has_the_ball())

        for i, player in enumerate(self.all_players):
            if player.has_the_ball():
                self.highlight_player(i + 1, "bold")

                action = random.randint(0, 9)
                if action in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                    player.passes()

                    listbox.insert(
                        0,
                        "(%s) %s of %s makes a pass."
                        % (player.number, player.name, player.team),
                    )

                    player_2 = random.choice(
                        [p for p in self.all_players if p != player]
                    )
                    player_2.ball = self.ball
                    listbox.insert(
                        0,
                        "(%s) %s of %s has the ball."
                        % (player_2.number, player_2.name, player_2.team),
                    )

                    break
                elif action == 0:
                    side_shoot = player.shoots()

                    listbox.insert(
                        0,
                        "(%s) %s of %s shoots to the %s."
                        % (player.number, player.name, player.team, side_shoot),
                    )

                    for gk in self.goalkeepers:
                        if gk.team == player.team:
                            continue
                        else:
                            side_jump = gk.jumps()
                            if side_shoot == side_jump:
                                gk.ball = self.ball

                                listbox.insert(
                                    0,
                                    "(%s) %s of %s catches the ball!"
                                    % (gk.number, gk.name, gk.team),
                                )
                                break
                            else:
                                listbox.insert(
                                    0,
                                    "(%s) %s of %s scores and it's a GOOOOOOAAAAAALLLLLL!"
                                    % (player.number, player.name, player.team),
                                )

                                self.score_board.set_score(player.team)

                                listbox.insert(0, "")
                                listbox.insert(
                                    0,
                                    "The score is: %s for %s, %s for %s."
                                    % (
                                        self.score_board.score[self.team_1.name],
                                        self.team_1,
                                        self.score_board.score[self.team_2.name],
                                        self.team_2,
                                    ),
                                )
                                listbox.insert(0, "")

                                self.update_scoreboard(
                                    [score_1, score_2],
                                    [
                                        self.score_board.score[self.team_1.name],
                                        self.score_board.score[self.team_2.name],
                                    ],
                                )

                                if gk.team == self.team_1.name:
                                    self.ball_to_striker(self.team_1, "1")
                                elif gk.team == self.team_2.name:
                                    self.ball_to_striker(self.team_2, "2")

                                break
        for i, p in enumerate(self.all_players):
            if not p.has_the_ball():
                self.highlight_player(i + 1, "")
            # else:
            #     self.highlight_player(i + 1, "")
            #     continue

        if duration == 0:
            listbox.insert(0, "")
            listbox.insert(0, "Well, the match has ended.")
            if self.score_board.is_a_tie():
                listbox.insert(0, "")
                listbox.insert(
                    0,
                    "The final score is: %s %s, %s %s."
                    % (
                        self.team_1,
                        self.score_board.score[self.team_1.name],
                        self.team_2,
                        self.score_board.score[self.team_2.name],
                    ),
                )
                listbox.insert(0, "AND IT'S A TIE!")
            else:
                winner = self.score_board.is_a_win()
                listbox.insert(0, "")
                listbox.insert(
                    0,
                    "The final score is: %s %s, %s %s."
                    % (
                        self.team_1,
                        self.score_board.score[self.team_1.name],
                        self.team_2,
                        self.score_board.score[self.team_2.name],
                    ),
                )
                listbox.insert(0, "AND THE WINNER IS %s!!!" % (winner.upper()))

            parent.after_cancel(self.play)
            self.play = None

        duration -= 1
        parent.after(1000, self.play, listbox, parent, score_1, score_2, duration)

    def highlight_player(self, i, font):
        self.field.field.itemconfig(i, font="Default 14 " + font)

    def update_scoreboard(self, scoreboard, score):
        scoreboard[0]["text"] = score[0]
        scoreboard[1]["text"] = score[1]

    def ball_to_striker(self, team, number):
        for player in team.players:
            if player.position == "ST" + number:
                player.ball = self.ball


class Ball:
    pass


class Score:
    def __init__(self, team_1, team_2):
        self.team_1 = team_1
        self.team_2 = team_2
        self.score = {self.team_1: 0, self.team_2: 0}

    def set_score(self, team):
        self.score[team] += 1

    def is_a_tie(self):
        return self.score[self.team_1] == self.score[self.team_2]

    def is_a_win(self):
        if self.score[self.team_1] > self.score[self.team_2]:
            return self.team_1
        else:
            return self.team_2
