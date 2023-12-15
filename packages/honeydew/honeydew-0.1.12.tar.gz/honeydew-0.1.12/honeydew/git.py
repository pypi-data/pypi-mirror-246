import os
from git import Repo
import pandas as pd

class GitConnector:
    """
    Instantiate a Github connector
    """
    def __init__(self, proxy=''):
        self.proxy = proxy
        if proxy != '':
            os.environ['HTTP_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy

    # Get file commit authors
    def get_file_commit_authors(self, repo_path):
        repo = Repo(repo_path)

        # Dictionary to store file and corresponding commit authors
        file_commit_authors = {}

        # Iterate through all files in the repository
        for item in repo.tree().traverse():
            if item.type == 'blob':
                file_path = os.path.join(repo_path, item.path)
                
                # Get the list of commit authors for the file
                commit_authors = set()
                try:
                    blame = repo.blame('HEAD', file_path)
                    for commit, lines in blame:
                        commit_authors.add(commit.author.name)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

                file_commit_authors[item.path] = list(commit_authors)

        return file_commit_authors
    
    # Get file commit authors
    def get_file_commit_authors_to_dataframe(self, repo_path):
        repo = Repo(repo_path)

        # Dictionary to store file and corresponding commit authors
        file_commit_authors = {}

        # Iterate through all files in the repository
        for item in repo.tree().traverse():
            if item.type == 'blob':
                file_path = os.path.join(repo_path, item.path)
                
                # Get the list of commit authors for the file
                commit_authors = set()
                try:
                    blame = repo.blame('HEAD', file_path)
                    for commit, lines in blame:
                        commit_authors.add(commit.author.name)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

                file_commit_authors[item.path] = list(commit_authors)

        df = pd.DataFrame.from_dict(file_commit_authors, orient='index', columns=['commit_authors'])
        df.index.name = 'file_path'
        return df
    
    # Get file commit authors
    def get_file_commit_authors_to_csv(self, repo_path, output_file):
        self.get_file_commit_authors_to_dataframe(repo_path).to_csv(output_file)
        return 'OK'
    
    # Get file commit authors
    def get_file_commit_authors_to_json(self, repo_path, output_file):
        self.get_file_commit_authors_to_dataframe(repo_path).to_json(output_file)
        return 'OK'
    
    # Get list of  dictionary which consist of list of committed files with dictionary list of commit authors and commit dates
    def get_file_commit_authors_with_date(self, repo_path):
        repo = Repo(repo_path)

        # List to store file and corresponding commit authors
        file_commit_authors = []

        # Iterate through all files in the repository
        for item in repo.tree().traverse():
            if item.type == 'blob':
                file_path = os.path.join(repo_path, item.path)
                
                # Get the list of commit authors for the file
                commits = []
                try:
                    blame = repo.blame('HEAD', file_path)
                    for commit, lines in blame:
                        author_data = {
                            "author": commit.author.name,
                            "date": commit.committed_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                            "message": commit.message.replace('\n', '')
                        }
                        commits.append(author_data)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

                data = {
                    "file_path": file_path,
                    "commits": commits,
                }
                file_commit_authors.append(data)

        return file_commit_authors     
     
    
    # Search keywords in file contents in a directory
    def search_keywords_in_files(self, repo_path, keywords):
        repo = Repo(repo_path)

        # Dictionary to store file and corresponding commit authors
        file_keywords = {}

        # Iterate through all files in the repository
        for item in repo.tree().traverse():
            if item.type == 'blob':
                file_path = os.path.join(repo_path, item.path)
                
                # Get the list of commit authors for the file
                keywords_found = set()
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            for keyword in keywords:
                                if keyword in line:
                                    keywords_found.add(keyword)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

                file_keywords[item.path] = list(keywords_found)

        return file_keywords
    

    # Search keywords in file contents in a directory
    def search_keywords_in_files_to_dataframe(self, repo_path, keywords):
        repo = Repo(repo_path)

        # Dictionary to store file and corresponding commit authors
        file_keywords = []

        # Iterate through all files in the repository
        for item in repo.tree().traverse():
            if item.type == 'blob':
                file_path = os.path.join(repo_path, item.path)
                # Get the list of commit authors for the file
                keywords_found = set()
                try:
                    with open(file_path, 'r') as f:
                        for line in f:
                            for keyword in keywords:
                                if keyword in line:
                                    keywords_found.add(keyword)
                except Exception as e:
                    # print(f"Error processing file {file_path}: {e}")
                    pass
                if len(keywords_found) > 0:
                    data = {
                        "file_path": file_path,
                        "keywords_found": list(keywords_found)
                    }
                    file_keywords.append(data)
        df = pd.DataFrame()
        try:
            df = pd.DataFrame(file_keywords)
            # df = pd.DataFrame.from_dict(file_keywords, orient='index')
            # df.index.name = 'file_path'
        except Exception as e2:
            print(f"Error converting dictionary to dataframe: {e2}")
        return df

    # Clone a repository
    def clone_repo(self, repo_url, repo_path):
       Repo.clone_from(repo_url, repo_path)
       return 'OK'    

    # Delete a directory
    def delete_directory(self, directory):
        import shutil
        shutil.rmtree(directory)
        return 'OK'
    

