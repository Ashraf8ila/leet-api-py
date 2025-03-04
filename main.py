import requests
import datetime
import json
import random

BASE_URL = "https://leetcode.com/graphql"
HEADERS = {"Content-Type": "application/json", "Referer": "https://leetcode.com"}

def fetch_user_info(username):
    """Fetch comprehensive LeetCode user information."""
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
          realName
          aboutMe
          userAvatar
        }
        submitStats {
          acSubmissionNum {
            difficulty
            count
          }
        }
        problemsSolvedBeatsStats {
          difficulty
          percentage
        }
        languageProblemCount {
          languageName
          problemsSolved
        }
      }
    }
    """
    try:
        response = requests.post(BASE_URL, json={"query": query, "variables": {"username": username}}, headers=HEADERS)

        if response.status_code == 200:
            data = response.json().get("data", {}).get("matchedUser")
            if not data:
                return None
            
            # Calculate additional statistics
            total_solved = sum(item['count'] for item in data['submitStatsGlobal']['acSubmissionNum'])
            difficulty_breakdown = {item['difficulty']: item['count'] for item in data['submitStatsGlobal']['acSubmissionNum']}
            problem_beats = {item['difficulty']: item['percentage'] for item in data.get('problemsSolvedBeatsStats', [])}
            
            # Calculate advanced stats
            total_problems = 2500  # Approximate total LeetCode problems
            completion_rate = round((total_solved / total_problems) * 100, 1)
            difficulty_completion = {
                'Easy': round((difficulty_breakdown.get('Easy', 0) / 800) * 100, 1),  # ~800 easy problems
                'Medium': round((difficulty_breakdown.get('Medium', 0) / 1200) * 100, 1),  # ~1200 medium problems
                'Hard': round((difficulty_breakdown.get('Hard', 0) / 500) * 100, 1)  # ~500 hard problems
            }
            
            user_info = {
                "username": data['username'],
                "ranking": data['profile'].get('ranking', 'N/A'),
                "reputation": data['profile'].get('reputation', 0),
                "real_name": data['profile'].get('realName', 'Not specified'),
                "about_me": data['profile'].get('aboutMe', 'No bio'),
                "avatar": data['profile'].get('userAvatar', 'default_avatar.png'),
                "total_solved": total_solved,
                "acceptance_rate": data.get('profile', {}).get('acceptanceRate', 0),
                "contribution_points": data.get('profile', {}).get('contributionPoints', 0),
                "solved_problems": data["submitStatsGlobal"]["acSubmissionNum"],
                "difficulty_breakdown": difficulty_breakdown,
                "problem_beats": problem_beats,
                "language_stats": data.get('languageProblemCount', []),
                "top_languages": sorted(
                    data.get('languageProblemCount', []),
                    key=lambda x: x['problemsSolved'],
                    reverse=True
                )[:3],
                "ranking_percentile": round((1 - (data['profile'].get('ranking', 0) / 100000)) * 100, 1) if data['profile'].get('ranking') else 0,
                "completion_rate": completion_rate,
                "difficulty_completion": difficulty_completion,
                "average_beats": round(sum(problem_beats.values()) / len(problem_beats) if problem_beats else 0, 1),
                "rank_tier": get_rank_tier(data['profile'].get('ranking', 0)),
                "next_tier_progress": calculate_next_tier_progress(data['profile'].get('ranking', 0))
            }
            
            # Add topic analysis
            try:
                topics_query = """
                query getUserTopics($username: String!) {
                  matchedUser(username: $username) {
                    tagProblemCounts {
                      tag
                      problemsSolved
                      totalProblems
                    }
                  }
                }
                """
                topics_response = requests.post(BASE_URL, 
                                             json={"query": topics_query, "variables": {"username": username}},
                                             headers=HEADERS)
                
                if topics_response.status_code == 200:
                    topics_data = topics_response.json().get("data", {}).get("matchedUser", {}).get("tagProblemCounts", [])
                    
                    # Calculate topic percentages and sort
                    topic_stats = []
                    for topic in topics_data:
                        solved = topic['problemsSolved']
                        total = topic['totalProblems']
                        percentage = round((solved / total * 100), 1) if total > 0 else 0
                        topic_stats.append({
                            'name': topic['tag'],
                            'solved': solved,
                            'total': total,
                            'percentage': percentage
                        })
                    
                    # Sort by percentage for strengths and weaknesses
                    sorted_topics = sorted(topic_stats, key=lambda x: x['percentage'], reverse=True)
                    user_info['top_topics'] = sorted_topics[:5]
                    user_info['weak_topics'] = sorted_topics[-5:]
                    
            except Exception as e:
                print(f"Error fetching topic stats: {e}")
                user_info['top_topics'] = []
                user_info['weak_topics'] = []
            
            return user_info
        else:
            return None
    except Exception as e:
        print(f"Error fetching user info: {e}")
        return None

def get_rank_tier(ranking):
    """Calculate user's rank tier."""
    if ranking == 0:
        return "Unranked"
    elif ranking <= 100:
        return "Elite"
    elif ranking <= 1000:
        return "Master"
    elif ranking <= 10000:
        return "Expert"
    elif ranking <= 50000:
        return "Advanced"
    else:
        return "Beginner"

def calculate_next_tier_progress(ranking):
    """Calculate progress to next tier."""
    tiers = [(0, 100), (101, 1000), (1001, 10000), (10001, 50000)]
    
    for i, (lower, upper) in enumerate(tiers):
        if lower <= ranking <= upper:
            progress = round(((upper - ranking) / (upper - lower)) * 100, 1)
            next_tier = ["Elite", "Master", "Expert", "Advanced"][i]
            return {
                "next_tier": next_tier,
                "progress": progress,
                "remaining": upper - ranking
            }
    return None

def fetch_daily_questions(start_date, end_date):
    """Fetch LeetCode daily questions with enhanced details."""
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
            topicTags {
              name
            }
            likes
            dislikes
          }
        }
      }
    }
    """

    try:
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
                            "link": f"https://leetcode.com{challenge['link']}",
                            "tags": [tag['name'] for tag in question.get('topicTags', [])],
                            "likes": question.get('likes', 0),
                            "dislikes": question.get('dislikes', 0),
                            "like_ratio": round(question.get('likes', 0) / (question.get('likes', 0) + question.get('dislikes', 1)) * 100, 2)
                        })
            else:
                print(f"Error fetching daily questions for {year}-{month}")

            # Move to next month
            next_month = (current.month % 12) + 1
            next_year = current.year if next_month != 1 else current.year + 1
            current = datetime.datetime(next_year, next_month, 1)
        
        return questions
    except Exception as e:
        print(f"Error in fetch_daily_questions: {e}")
        return []

def get_coding_resources():
    """Generate a list of coding resources and practice recommendations."""
    resources = [
        {
            "name": "Algorithm Masterclass",
            "description": "Comprehensive guide to algorithm design and analysis",
            "difficulty": "Advanced",
            "url": "https://example.com/algorithm-masterclass"
        },
        {
            "name": "Data Structures Bootcamp",
            "description": "Deep dive into essential data structures",
            "difficulty": "Intermediate",
            "url": "https://example.com/data-structures-bootcamp"
        },
        {
            "name": "System Design Interview Prep",
            "description": "Prepare for system design interviews with real-world scenarios",
            "difficulty": "Advanced",
            "url": "https://example.com/system-design-prep"
        }
    ]
    
    # Add some randomization to recommend resources
    recommended = random.sample(resources, min(len(resources), 2))
    return recommended

def generate_practice_plan(user_info=None):
    """Generate a personalized coding practice plan."""
    if not user_info:
        return {
            "overall_recommendation": "Complete beginner problems across all difficulties",
            "focus_areas": ["Arrays", "Strings", "Hash Tables"],
            "daily_goal": "Solve 3 problems"
        }
    
    # Create a personalized plan based on user's solving history
    difficulty_breakdown = user_info.get('difficulty_breakdown', {})
    
    # Determine weakest difficulty
    weakest_difficulty = min(difficulty_breakdown, key=difficulty_breakdown.get)
    
    practice_plan = {
        "overall_recommendation": f"Focus on {weakest_difficulty} difficulty problems",
        "focus_areas": [
            "Dynamic Programming" if difficulty_breakdown.get('Hard', 0) < 10 else "Graph Algorithms",
            "Greedy Algorithms",
            "Recursion and Backtracking"
        ],
        "daily_goal": f"Solve {min(5, 3 + difficulty_breakdown.get('Easy', 0) // 10)} problems",
        "suggested_topics": [
            "Array Manipulation",
            "String Processing",
            "Sorting and Searching"
        ]
    }
    
    return practice_plan