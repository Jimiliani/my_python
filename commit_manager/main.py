from github import Github
from spreadsheet import Spreadsheet
from github_date import GithubDate
import webbrowser


def main():
    g = Github(login_or_token="", password="")  # TODO
    file = open("students.txt", 'r')
    print("Введите дату выдачи задания:")
    deadline_date_from = input()
    print("Введите дату дедалйна:")
    deadline_date_to = input()
    deadline_date_from = GithubDate(deadline_date_from)
    deadline_date_to = GithubDate(deadline_date_to)
    sheet = Spreadsheet(deadline_date_from.get_str(), deadline_date_to.get_str())
    for line in file:
        line = line.strip('\n').split(' ')
        repo = g.get_repo(line[2])
        for commit in repo.get_commits():
            date = GithubDate(str(commit.commit.author.date))
            if deadline_date_from < date < deadline_date_to:
                sheet.add_line(line[0], line[1], 'https://github.com/' + line[2])
                break
    webbrowser.open(sheet.get_link())


if __name__ == '__main__':
    main()
