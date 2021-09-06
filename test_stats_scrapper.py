from stats_scrapper import generate_facebook_stats_url, extract_facebook_stats

with open('urls.txt') as f:
    for url in f.readlines():
        stats_url = generate_facebook_stats_url(url)
        likes_shares_comments_count = extract_facebook_stats(stats_url, url)
        print(f"{url.strip()} - {likes_shares_comments_count}")
