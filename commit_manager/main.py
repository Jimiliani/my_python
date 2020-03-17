from github import Github
from spreadsheet import Spreadsheet
from github_date import GithubDate
import webbrowser


def main():
    g = Github(login_or_token="", password="")  # TODO
    file = open("students.txt", 'r')
    deadline_date = input()
    deadline_date = GithubDate(deadline_date)
    sheet = Spreadsheet(deadline_date.get_str())
    for line in file:
        line = line.strip('\n').split(' ')
        repo = g.get_repo(line[2])
        for commit in repo.get_commits():
            date = GithubDate(str(commit.commit.author.date))
            if date > deadline_date:
                sheet.add_line(line[0], line[1], 'https://github.com/' + line[2])
                break
    webbrowser.open(sheet.get_link())


if __name__ == '__main__':
    main()
