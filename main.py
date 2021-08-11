import random
import tkinter as tk
import game
import field
import names
import teams


class Football:
    def __init__(self):
        self.root = tk.Tk()

        self.container = tk.LabelFrame(self.root)
        self.container.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.frm_team_1 = tk.LabelFrame(self.container, text=" ", borderwidth=0)
        self.frm_team_1.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.lbx_team_1 = tk.Listbox(self.frm_team_1, width=30, height=5)
        self.lbx_team_1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.frm_team_2 = tk.LabelFrame(self.container, text=" ", borderwidth=0)
        self.frm_team_2.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.lbx_team_2 = tk.Listbox(self.frm_team_2, width=30, height=5)
        self.lbx_team_2.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.frm_buttons = tk.Frame(self.container)
        self.frm_buttons.grid(row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.btn_set = tk.Button(
            self.frm_buttons,
            text="Set Match",
            width=30,
            height=3,
            command=self.set_game,
        )
        self.btn_set.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.btn_start = tk.Button(
            self.frm_buttons, text="Start Match", width=30, height=3, state="disabled"
        )
        self.btn_start.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.field = field.Field(self.container)

        self.frm_right_panel = tk.Frame(self.container)
        self.frm_right_panel.grid(
            row=0, column=2, rowspan=3, padx=5, pady=5, sticky=tk.NSEW
        )

        self.lbx_events = tk.Listbox(self.frm_right_panel, width=60, height=40)
        self.lbx_events.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.frm_scoreboard = tk.Frame(self.frm_right_panel)
        self.frm_scoreboard.grid(row=1, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.lbl_team_1 = tk.Label(self.frm_scoreboard, font="Default 18 bold")
        self.lbl_team_1.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NSEW)
        self.lbl_score_1 = tk.Label(self.frm_scoreboard, font="Default 18 bold")
        self.lbl_score_1.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

        self.lbl_team_2 = tk.Label(self.frm_scoreboard, font="Default 18 bold")
        self.lbl_team_2.grid(row=0, column=2, padx=10, pady=10, sticky=tk.NSEW)
        self.lbl_score_2 = tk.Label(self.frm_scoreboard, font="Default 18 bold")
        self.lbl_score_2.grid(row=0, column=3, padx=10, pady=10, sticky=tk.NSEW)

        self.root.mainloop()

    def set_teams(self):
        t = teams.teams
        team_1 = random.choice(t)
        t.remove(team_1)
        team_2 = random.choice(t)

        return (team_1, team_2)

    def set_players(self, team_name, id):
        players = []
        for i in range(5):
            name = random.choice(names.first) + " " + random.choice(names.last)
            number = i + 1
            position = ""
            if i == 0:
                position = "GK"
            elif i == 1:
                position = "DR"
            elif i == 2:
                position = "DL"
            elif i == 3:
                position = "MF"
            elif i == 4:
                position = "ST"
            player = game.Player(name, number, position + id, team_name)
            players.append(player)

        return players

    def set_game(self):
        teams = self.set_teams()
        colors = ["blue", "yellow"]
        players_1 = self.set_players(teams[0], "1")
        players_2 = self.set_players(teams[1], "2")
        self.field.players(players_1 + players_2, colors)

        team_1 = game.Team(teams[0], colors[0], players_1)
        team_2 = game.Team(teams[1], colors[1], players_2)

        self.frm_team_1["text"] = team_1.name
        self.frm_team_2["text"] = team_2.name
        self.populate_team(team_1, self.lbx_team_1)
        self.populate_team(team_2, self.lbx_team_2)

        match = game.Match([team_1, team_2], self.field)

        self.lbl_team_1["text"] = team_1.name
        self.lbl_team_1["fg"] = team_1.color
        self.lbl_score_1["text"] = "0"
        self.lbl_team_2["text"] = team_2.name
        self.lbl_team_2["fg"] = team_2.color
        self.lbl_score_2["text"] = "0"

        self.btn_set["state"] = "disabled"
        self.btn_start.config(
            command=lambda: [
                match.start(
                    self.lbx_events, self.root, self.lbl_score_1, self.lbl_score_2
                ),
                self.btn_start.config(state="disabled"),
            ]
        )
        self.btn_start["state"] = "normal"

    def populate_team(self, team, listbox):
        listbox.delete(0, tk.END)
        for i, player in enumerate(team.players):
            listbox.insert(
                i,
                "[%s] %s - %s"
                % (
                    player.number,
                    player.name,
                    player.position.replace("1", "").replace("2", ""),
                ),
            )


def main():
    app = Football()


if "__main__" in __name__:
    main()
