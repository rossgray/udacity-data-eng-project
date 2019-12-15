class SqlQueries:
    create_staging_github_repos = """
        CREATE TABLE IF NOT EXISTS staging_github_repos (
            id int,
            owner_id int,
            owner_name varchar(256),
            full_name varchar(256),
            repo_detail_url varchar(512),
            is_fork boolean,
            repo_commits_url varchar(512),
            language varchar(128),
            licence varchar(128),
            size int,
            stars int,
            forks int,
            open_issues int,
            created_at timestamp
        );
    """

    create_staging_hacker_news_posts = """
        CREATE TABLE IF NOT EXISTS staging_hacker_news_posts (
            id int,
            title varchar(512),
            post_type varchar(128),
            author varchar(256),
            created_at timestamp,
            url varchar(8192),
            points int,
            num_comments real
        );
    """

    create_github_repos = """
        CREATE TABLE IF NOT EXISTS github_repos (
            id int PRIMARY KEY,
            owner_id int,
            full_name varchar(256),
            repo_detail_url varchar(512),
            is_fork boolean,
            repo_commits_url varchar(512),
            language varchar(128),
            licence varchar(128),
            size int,
            stars int,
            forks int,
            open_issues int,
            created_at timestamp
        );
    """

    insert_github_repos = """
        SELECT
            id,
            owner_id,
            full_name,
            repo_detail_url,
            is_fork,
            repo_commits_url,
            language,
            licence,
            size,
            stars,
            forks,
            open_issues,
            created_at
        FROM staging_github_repos
    """

    create_github_users = """
        CREATE TABLE IF NOT EXISTS github_users (
            id int PRIMARY KEY,
            name varchar(256)
        );
    """

    insert_github_users = """
        SELECT DISTINCT owner_id as ID, owner_name AS name
        FROM staging_github_repos
    """

    create_hacker_news_posts = """
        CREATE TABLE IF NOT EXISTS hacker_news_posts (
            id int PRIMARY KEY,
            title varchar(512),
            post_type varchar(128),
            author varchar(256),
            created_at timestamp,
            url varchar(8192),
            github_repo_full_name varchar(256),
            points int,
            num_comments int
        );
    """

    insert_hacker_news_posts = r"""
        SELECT
            id,
            title,
            post_type,
            author,
            created_at,
            url,
            REGEXP_SUBSTR(
                url,
                'github.com/([_a-zA-Z0-9\-]+/[_a-zA-Z0-9\-]+)', 0, 1, 'e'
            ) AS github_repo_full_name,
            points,
            num_comments::integer
        FROM staging_hacker_news_posts
    """

    create_github_repo_popularity = """
        CREATE TABLE IF NOT EXISTS github_repo_popularity  (
            github_repo_id int PRIMARY KEY,
            stars int,
            forks int,
            total_hn_points int,
            total_hn_comments int
        );
    """

    insert_github_repo_popularity = """
        SELECT
            gr.id AS github_repo_id,
            max(gr.stars),
            max(gr.forks),
            sum(hnp.points) as total_hn_points,
            sum(hnp.num_comments) as total_hn_comments
        FROM github_repos gr
        JOIN hacker_news_posts hnp
        ON hnp.github_repo_full_name = gr.full_name
        GROUP BY gr.id
    """
