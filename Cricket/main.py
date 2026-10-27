
teams = []
valid_teams = []
matches_data = []
team_statistics = {}
pair_count = {}


def team():
    while True:
        try:
            n = int(input("Enter number of teams: "))

            if n < 2:
                print("Enter at least 2 teams")
                continue

            break

        except ValueError:
            print("Enter a valid number")

    for i in range(n):
        while True:
            name = input("Enter team name: ").strip()

            if name == "":
                print("Team name cannot be empty")
                continue

            if name.lower() in [t.lower() for t in teams]:
                print("Team already exists")
                continue

            teams.append(name)
            break

    return teams


def team_validation(teams):
    for t in teams:
        if t not in valid_teams:
            valid_teams.append(t)

    return valid_teams


def team_assigning(valid_teams):
    matches = []

    for i in range(len(valid_teams)):
        for j in range(i + 1, len(valid_teams)):
            matches.append([valid_teams[i], valid_teams[j]])
            matches.append([valid_teams[j], valid_teams[i]])

    return matches


teams = team()
valid_teams = team_validation(teams)
matches = team_assigning(valid_teams)


def initialize_statistics(teams):
    for t in teams:
        team_statistics[t] = {
            "played": 0,
            "wins": 0,
            "lost": 0,
            "tied": 0,
            "points": 0,
            "runs_scored": 0,
            "runs_conceded": 0,
            "balls_faced": 0,
            "balls_bowled": 0,
            "NRR": 0.0
        }


initialize_statistics(valid_teams)


def match_validation(m, valid_teams):
    if m["team1"] not in valid_teams:
        raise ValueError("Team 1 does not exist")

    if m["team2"] not in valid_teams:
        raise ValueError("Team 2 does not exist")

    if m["team1"] == m["team2"]:
        raise ValueError("Both teams cannot be the same")

    for key in ["runs1", "runs2"]:
        if m[key] < 0:
            raise ValueError("Runs cannot be negative")

    for key in ["wickets1", "wickets2"]:
        if m[key] < 0 or m[key] > 10:
            raise ValueError("Wickets must be between 0 and 10")

    for key in ["overs1", "overs2"]:
        if m[key] < 0 or m[key] > 20:
            raise ValueError("Overs must be between 0 and 20")

    for key in ["balls1", "balls2"]:
        if m[key] < 0 or m[key] > 5:
            raise ValueError("Balls must be between 0 and 5")

    if m["overs1"] == 20 and m["balls1"] != 0:
        raise ValueError("Balls must be 0 after 20 overs")

    if m["overs2"] == 20 and m["balls2"] != 0:
        raise ValueError("Balls must be 0 after 20 overs")


def match_details():
    for i in range(len(matches)):
        m = {}
        m["id"] = i + 1
        m["team1"] = input("Enter Team 1: ")
        m["team2"] = input("Enter Team 2: ")
        m["runs1"] = int(input("Enter Team 1 runs: "))
        m["wickets1"] = int(input("Enter Team 1 wickets: "))
        m["overs1"] = int(input("Enter Team 1 overs: "))
        m["balls1"] = int(input("Enter Team 1 balls: "))
        m["runs2"] = int(input("Enter Team 2 runs: "))
        m["wickets2"] = int(input("Enter Team 2 wickets: "))
        m["overs2"] = int(input("Enter Team 2 overs: "))
        m["balls2"] = int(input("Enter Team 2 balls: "))

        match_validation(m, valid_teams)
        matches_data.append(m)

        if m["team1"] < m["team2"]:
            pair = m["team1"] + "|" + m["team2"]
        else:
            pair = m["team2"] + "|" + m["team1"]

        pair_count[pair] = pair_count.get(pair, 0) + 1


def match_analysis(m):
    team1 = m["team1"]
    team2 = m["team2"]

    runs1 = m["runs1"]
    runs2 = m["runs2"]

    wickets1 = m["wickets1"]
    wickets2 = m["wickets2"]

    balls1 = m["overs1"] * 6 + m["balls1"]
    balls2 = m["overs2"] * 6 + m["balls2"]

    if wickets1 == 10:
        balls1 = 120

    if wickets2 == 10:
        balls2 = 120

    team_statistics[team1]["played"] += 1
    team_statistics[team2]["played"] += 1

    team_statistics[team1]["runs_scored"] += runs1
    team_statistics[team1]["runs_conceded"] += runs2

    team_statistics[team2]["runs_scored"] += runs2
    team_statistics[team2]["runs_conceded"] += runs1

    team_statistics[team1]["balls_faced"] += balls1
    team_statistics[team1]["balls_bowled"] += balls2

    team_statistics[team2]["balls_faced"] += balls2
    team_statistics[team2]["balls_bowled"] += balls1

    if runs1 > runs2:
        team_statistics[team1]["wins"] += 1
        team_statistics[team1]["points"] += 2
        team_statistics[team2]["lost"] += 1

    elif runs2 > runs1:
        team_statistics[team2]["wins"] += 1
        team_statistics[team2]["points"] += 2
        team_statistics[team1]["lost"] += 1

    else:
        team_statistics[team1]["tied"] += 1
        team_statistics[team2]["tied"] += 1
        team_statistics[team1]["points"] += 1
        team_statistics[team2]["points"] += 1


match_details()

for m in matches_data:
    match_analysis(m)


def calculate_nrr():
    for team in valid_teams:
        stats = team_statistics[team]

        if stats["balls_faced"] > 0 and stats["balls_bowled"] > 0:
            run_rate_scored = (
                stats["runs_scored"] * 6 / stats["balls_faced"]
            )
            run_rate_conceded = (
                stats["runs_conceded"] * 6 / stats["balls_bowled"]
            )
            stats["NRR"] = round(
                run_rate_scored - run_rate_conceded, 3
            )
        else:
            stats["NRR"] = 0.0


def display_points_table():
    sorted_teams = valid_teams.copy()

    for i in range(len(sorted_teams)):
        for j in range(len(sorted_teams) - i - 1):
            team1 = sorted_teams[j]
            team2 = sorted_teams[j + 1]

            stats1 = team_statistics[team1]
            stats2 = team_statistics[team2]

            if (stats1["points"] < stats2["points"] or (stats1["points"] == stats2["points"]and stats1["NRR"] < stats2["NRR"])):
                sorted_teams[j], sorted_teams[j + 1] = (sorted_teams[j + 1],sorted_teams[j])

    print("\nPOINTS TABLE")

    print(
        f"{'Team':<15}{'P':<5}{'W':<5}{'L':<5}"
        f"{'T':<5}{'Points':<8}{'Runs Scored':<13}"
        f"{'Runs Conceded':<15}{'Overs Faced':<13}"
        f"{'Overs Bowled':<13}{'NRR':<8}"
    )

    for team in sorted_teams:
        stats = team_statistics[team]

        overs_faced = stats["balls_faced"] / 6
        overs_bowled = stats["balls_bowled"] / 6

        print(
            f"{team:<15}{stats['played']:<5}"
            f"{stats['wins']:<5}{stats['lost']:<5}"
            f"{stats['tied']:<5}{stats['points']:<8}"
            f"{stats['runs_scored']:<13}"
            f"{stats['runs_conceded']:<15}"
            f"{overs_faced:<13.1f}{overs_bowled:<13.1f}"
            f"{stats['NRR']:<8.3f}"
        )


def check_tournament_complete():
    for i in range(len(valid_teams)):
        for j in range(i + 1, len(valid_teams)):
            team1 = valid_teams[i]
            team2 = valid_teams[j]

            if team1 < team2:
                pair = team1 + "|" + team2
            else:
                pair = team2 + "|" + team1

            if pair_count.get(pair, 0) != 2:
                return False

    return True


if check_tournament_complete():
    calculate_nrr()
    display_points_table()
else:
    print("Tournament is incomplete")
