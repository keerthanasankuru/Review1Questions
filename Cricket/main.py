
teams = []
valid_teams = []
matches_data = []
team_statistics = {}
pair_count = {}


def get_integer(message, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(message))

            if minimum is not None and value < minimum:
                print("Value must be at least", minimum)
                continue

            if maximum is not None and value > maximum:
                print("Value must not exceed", maximum)
                continue

            return value

        except ValueError:
            print("Enter a valid integer")


def team():
    n = get_integer("Enter number of teams: ", 2)

    i = 0
    while i < n:
        name = input("Enter team name: ").strip()

        if name == "":
            print("Team name cannot be empty")
        elif name in teams:
            print("Team name already exists")
        else:
            teams.append(name)
            i += 1


team()


def team_validation(teams):
    valid_teams = []

    for name in teams:
        if name.strip() != "" and name not in valid_teams:
            valid_teams.append(name)

    count = 0
    for name in valid_teams:
        count += 1

    if count < 2:
        raise ValueError("At least 2 teams must be present")

    return valid_teams


valid_teams = team_validation(teams)


def team_assigning(valid_teams):
    matches = []

    i = 0
    while i < len(valid_teams):
        j = i + 1

        while j < len(valid_teams):
            matches.append([valid_teams[i], valid_teams[j]])
            matches.append([valid_teams[j], valid_teams[i]])
            j += 1

        i += 1

    return matches


matches = team_assigning(valid_teams)

print("\nRequired match pairings:")

i = 0
for match in matches:
    i += 1
    print(i, match[0], "vs", match[1])


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
        raise ValueError("Invalid first team")

    if m["team2"] not in valid_teams:
        raise ValueError("Invalid second team")

    if m["team1"] == m["team2"]:
        raise ValueError("A team cannot play against itself")

    if m["team1"] < m["team2"]:
        pair = m["team1"] + "|" + m["team2"]
    else:
        pair = m["team2"] + "|" + m["team1"]

    if pair in pair_count and pair_count[pair] >= 2:
        raise ValueError("These teams have already played twice")

    for i in [1, 2]:
        if m["runs" + str(i)] < 0:
            raise ValueError("Runs cannot be negative")

        if not 0 <= m["wickets" + str(i)] <= 10:
            raise ValueError("Wickets must be between 0 and 10")

        if not 0 <= m["overs" + str(i)] <= 20:
            raise ValueError("Overs must be between 0 and 20")

        if not 0 <= m["balls" + str(i)] <= 5:
            raise ValueError("Remaining balls must be between 0 and 5")

        if m["overs" + str(i)] == 20 and m["balls" + str(i)] != 0:
            raise ValueError("No extra balls allowed after 20 overs")

    return pair


def match_details(match_id):
    while True:
        try:
            print("\nEnter details for Match", match_id)

            team1 = input("Enter first team: ").strip()
            team2 = input("Enter second team: ").strip()

            m = {
                "id": match_id,
                "team1": team1,
                "team2": team2
            }

            for i in [1, 2]:
                m["runs" + str(i)] = get_integer(
                    "Enter Team " + str(i) + " runs: ", 0
                )

                m["wickets" + str(i)] = get_integer(
                    "Enter Team " + str(i) + " wickets: ", 0, 10
                )

                m["overs" + str(i)] = get_integer(
                    "Enter Team " + str(i) + " completed overs: ", 0, 20
                )

                m["balls" + str(i)] = get_integer(
                    "Enter Team " + str(i) + " remaining balls: ", 0, 5
                )

            pair = match_validation(m, valid_teams)

            matches_data.append(m)

            if pair in pair_count:
                pair_count[pair] += 1
            else:
                pair_count[pair] = 1

            return m

        except ValueError as e:
            print("Invalid match:", e)
            print("Please enter the match details again.")


def match_analysis(m):
    t1 = m["team1"]
    t2 = m["team2"]

    s1 = team_statistics[t1]
    s2 = team_statistics[t2]

    s1["played"] += 1
    s2["played"] += 1

    s1["runs_scored"] += m["runs1"]
    s1["runs_conceded"] += m["runs2"]

    s2["runs_scored"] += m["runs2"]
    s2["runs_conceded"] += m["runs1"]

    balls1 = m["overs1"] * 6 + m["balls1"]
    balls2 = m["overs2"] * 6 + m["balls2"]

    if m["wickets1"] == 10:
        balls1 = 120

    if m["wickets2"] == 10:
        balls2 = 120

    s1["balls_faced"] += balls1
    s1["balls_bowled"] += balls2

    s2["balls_faced"] += balls2
    s2["balls_bowled"] += balls1

    if m["runs1"] > m["runs2"]:
        s1["wins"] += 1
        s1["points"] += 2
        s2["lost"] += 1

    elif m["runs1"] < m["runs2"]:
        s2["wins"] += 1
        s2["points"] += 2
        s1["lost"] += 1

    else:
        s1["tied"] += 1
        s2["tied"] += 1
        s1["points"] += 1
        s2["points"] += 1


match_id = 1

for match in matches:
    m = match_details(match_id)
    match_analysis(m)
    match_id += 1


def calculate_nrr():
    for t in valid_teams:
        stats = team_statistics[t]

        if stats["balls_faced"] > 0 and stats["balls_bowled"] > 0:
            run_rate_scored = (
                stats["runs_scored"] * 6 / stats["balls_faced"]
            )

            run_rate_conceded = (
                stats["runs_conceded"] * 6 / stats["balls_bowled"]
            )

            stats["NRR"] = run_rate_scored - run_rate_conceded


calculate_nrr()


def display_points_table():
    standings = []

    for t in valid_teams:
        standings.append(t)

    i = 0
    while i < len(standings):
        j = i + 1

        while j < len(standings):
            t1 = standings[i]
            t2 = standings[j]

            s1 = team_statistics[t1]
            s2 = team_statistics[t2]

            if (
                s2["points"] > s1["points"]
                or (
                    s2["points"] == s1["points"]
                    and s2["NRR"] > s1["NRR"]
                )
            ):
                standings[i], standings[j] = standings[j], standings[i]

            j += 1

        i += 1

    print("\nFINAL TOURNAMENT POINTS TABLE")

    print(
        f"{'Pos':<5}{'Team':<18}{'Played':<9}{'Won':<7}"
        f"{'Lost':<7}{'Tied':<7}{'Points':<9}"
        f"{'Scored':<10}{'Given':<10}{'Overs Faced':<14}"
        f"{'Overs Bowled':<15}{'NRR':<8}"
    )

    position = 1

    for t in standings:
        s = team_statistics[t]

        overs_faced = s["balls_faced"] / 6
        overs_bowled = s["balls_bowled"] / 6

        print(
            f"{position:<5}{t:<18}{s['played']:<9}"
            f"{s['wins']:<7}{s['lost']:<7}{s['tied']:<7}"
            f"{s['points']:<9}{s['runs_scored']:<10}"
            f"{s['runs_conceded']:<10}"
            f"{overs_faced:<14.2f}{overs_bowled:<15.2f}"
            f"{s['NRR']:<8.3f}"
        )

        position += 1


expected_matches = len(valid_teams) * (len(valid_teams) - 1)

if len(matches_data) == expected_matches:
    display_points_table()
else:
    print("Tournament is incomplete.")
