from collections import defaultdict

def build_recommendations(issues):
    grouped = defaultdict(list)

    for issue in issues:
        grouped[issue["priority"]].append({
            "category": issue["category"],
            "message": issue["message"],
            "fix": issue["fix"]
        })

    return grouped
