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
