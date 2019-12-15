class DataValidationQueries:

    data_in_github_repos_table = """
        SELECT count(*) != 0
        FROM github_repos
    """

    data_in_github_users_table = """
        SELECT count(*) != 0
        FROM github_users
    """

    data_in_hacker_news_posts_table = """
        SELECT count(*) != 0
        FROM hacker_news_posts
    """

    data_in_github_repo_popularity_table = """
        SELECT count(*) != 0
        FROM github_repo_popularity
    """

    github_repos_owner_null = """
        SELECT count(*)
        FROM github_repos
        WHERE owner_id is NULL
    """

    github_repos_name_null = """
        SELECT count(*)
        FROM github_repos
        WHERE full_name is NULL
            OR full_name = ''
    """

    github_repos_stars_null = """
        SELECT count(*)
        FROM github_repos
        WHERE stars is NULL
    """

    github_repos_forks_null = """
        SELECT count(*)
        FROM github_repos
        WHERE forks is NULL
    """

    github_users_name_null = """
        SELECT count(*)
        FROM github_users
        WHERE name is NULL
            OR name = ''
    """

    hn_posts_ref_github_exist = """
        SELECT count(*) != 0
        FROM hacker_news_posts
        WHERE github_repo_full_name is NULL
            OR github_repo_full_name = ''
    """

    hn_posts_points_null = """
        SELECT count(*)
        FROM hacker_news_posts
        WHERE points is NULL
    """

    hn_posts_num_comments_null = """
        SELECT count(*)
        FROM hacker_news_posts
        WHERE num_comments is NULL
    """
