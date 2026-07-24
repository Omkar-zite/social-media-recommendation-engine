import json

# -------------------- Load Dataset --------------------
def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)


# -------------------- Clean Dataset --------------------
def cleaned_data(data):

    # Remove empty users
    valid_user = []
    for user in data["users"]:
        if user["name"].strip():
            valid_user.append(user)
    data["users"] = valid_user

    # Remove duplicate friends
    for user in data["users"]:
        user["friends"] = list(set(user["friends"]))

    # Remove inactive users
    active_user = []
    for user in data["users"]:
        if user["friends"] or user["liked_pages"]:
            active_user.append(user)
    data["users"] = active_user

    # Remove duplicate pages
    unique_pages = {}
    for page in data["pages"]:
        unique_pages[page["id"]] = page
    data["pages"] = list(unique_pages.values())

    return data


# -------------------- People You May Know --------------------
def people_you_may_know(user_id, data):
    user_friend = {}
    for user in data["users"]:
        user_friend[user["id"]] = user["friends"]
    if user_id not in user_friend:
        return []
    direct_friend = user_friend[user_id]
    suggestions = {}
    for friend in direct_friend:
        for mutual_friend in user_friend[friend]:
            if mutual_friend != user_id and mutual_friend not in direct_friend:
                suggestions[mutual_friend] = (suggestions.get(mutual_friend, 0) + 1)
    sorted_suggestion = sorted(suggestions.items(),key=lambda x: x[1],reverse=True)

    return [(user_id, count) for user_id, count in sorted_suggestion]


# -------------------- Pages You Might Like --------------------
def pages_you_might_like(user_id, data):
    user_page = {}
    for user in data["users"]:
        user_page[user["id"]] = set(user["liked_pages"])
    if user_id not in user_page:
        return []
    user_liked_page = user_page[user_id]
    page_suggestion = {}
    for other_user, liked_pages in user_page.items():
        if other_user != user_id:
            shared_page = user_liked_page.intersection(liked_pages)
            for page in liked_pages:
                if page not in user_liked_page:
                    page_suggestion[page] = (page_suggestion.get(page, 0)+ len(shared_page))
    sorted_suggestion = sorted(page_suggestion.items(),key=lambda x: x[1],reverse=True)

    return [(page, score) for page, score in sorted_suggestion]


# -------------------- Main Program --------------------

data = load_data("dataset1.json")

# Clean the dataset
data = cleaned_data(data)

# Save cleaned dataset
with open("cleaned_dataset.json", "w") as f:
    json.dump(data, f, indent=4)

print("Your data is cleaned successfully.\n")

# Friend Recommendation
user_id = 10
recommendation = people_you_may_know(user_id, data)

print("People You May Know")
for friend_id, mutual_count in recommendation:
    print(f"User {friend_id} ({mutual_count} mutual friends)")

print()

# Page Recommendation
user_id = 1
page_recommendation = pages_you_might_like(user_id, data)

print("Pages You Might Like")
for page_id, score in page_recommendation:
    print(f"Page {page_id} (Score: {score})")