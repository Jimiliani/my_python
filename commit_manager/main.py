from github import Github
from csv_worker import csv_writer
from github_date import GithubDate


def main():
    g = Github()
    file = open("students.txt", 'r')
    csv_file = open('commits.csv', 'w')
    print("Введите дату выдачи задания:")
    deadline_date_from = input()
    print("Введите дату дедалйна:")
    deadline_date_to = input()
    deadline_date_from = GithubDate(deadline_date_from)
    deadline_date_to = GithubDate(deadline_date_to)
    for line in file:
        line = line.strip('\n').split(' ')
        repo = g.get_repo(line[3])
        row = []
        last_date = deadline_date_from
        total_commits = 0
        for commit in repo.get_commits():
            date = GithubDate(str(commit.commit.author.date))
            if deadline_date_from < date < deadline_date_to:
                total_commits += 1
                if last_date < date:
                    last_date = date
                    row = [line[0], line[1], line[2], "Всего коммитов: " + str(total_commits),
                           'https://github.com/' + line[3], str(commit.commit.message)]
        if row:
            csv_writer(csv_file, row)
    file.close()
    csv_file.close()


if __name__ == '__main__':
    main()
