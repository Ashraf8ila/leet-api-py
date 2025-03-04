import requests
import argparse
import datetime

BASE_URL = "https://leetcode.com/graphql"
HEADERS = {"Content-Type": "application/json", "Referer": "https://leetcode.com"}


def fetch_user_info(username):
    """Fetch LeetCode user information."""
    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
          reputation
        }
      }
    }
    """
    response = requests.post(BASE_URL, json={"query": query, "variables": {"username": username}}, headers=HEADERS)

    if response.status_code == 200:
        data = response.json().get("data", {}).get("matchedUser")
        if not data:
            return "User not found."
        user_info = {
            "username": data['username'],
            "ranking": data['profile']['ranking'],
            "reputation": data['profile']['reputation'],
            "solved_problems": data["submitStatsGlobal"]["acSubmissionNum"]
        }
        return user_info
    else:
        return "Error fetching user info."


def fetch_daily_questions(start_date, end_date):
    """Fetch LeetCode daily questions for a given timeframe."""
    query = """
    query getDailyCodingChallenge($year: Int!, $month: Int!) {
      dailyCodingChallengeV2(year: $year, month: $month) {
        challenges {
          date
          link
          question {
            title
            titleSlug
            difficulty
          }
        }
      }
    }
    """

    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    current = start
    questions = []
    while current <= end:
        year, month = current.year, current.month
        response = requests.post(BASE_URL, json={"query": query, "variables": {"year": year, "month": month}},
                                 headers=HEADERS)

        if response.status_code == 200:
            challenges = response.json().get("data", {}).get("dailyCodingChallengeV2", {}).get("challenges", [])
            for challenge in challenges:
                challenge_date = challenge["date"]
                if start_date <= challenge_date <= end_date:
                    question = challenge["question"]
                    questions.append({
                        "date": challenge_date,
                        "title": question['title'],
                        "difficulty": question['difficulty'],
                        "link": f"https://leetcode.com{challenge['link']}"
                    })
        else:
            questions.append(f"Error fetching daily questions for {year}-{month}")

        # Move to next month
        next_month = (current.month % 12) + 1
        next_year = current.year if next_month != 1 else current.year + 1
        current = datetime.datetime(next_year, next_month, 1)
    
    return questions


def main():
    parser = argparse.ArgumentParser(description="LeetCode CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # User Info Command
    user_parser = subparsers.add_parser("user-info", help="Fetch LeetCode user stats")
    user_parser.add_argument("--username", required=True, help="LeetCode username")

    # Daily Questions Command
    daily_parser = subparsers.add_parser("daily-questions", help="Fetch daily coding challenge questions")
    daily_parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    daily_parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")

    args = parser.parse_args()

    if args.command == "user-info":
        user_info = fetch_user_info(args.username)
        if isinstance(user_info, str):
            print(user_info)
        else:
            print(f"\nLeetCode User: {user_info['username']}")
            print(f"Ranking: {user_info['ranking']}")
            print(f"Reputation: {user_info['reputation']}")
            print("Solved Problems:")
            for item in user_info["solved_problems"]:
                print(f"  {item['difficulty']}: {item['count']} problems")
    elif args.command == "daily-questions":
        questions = fetch_daily_questions(args.start, args.end)
        for question in questions:
            if isinstance(question, str):
                print(question)
            else:
                print(f"\n[{question['date']}] {question['title']} ({question['difficulty']})")
                print(f"  Link: {question['link']}\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
