from github import Github
from csv_worker import csv_writer
from github_date import GithubDate


def get_deadline_date_from():
    try:
        print("Введите дату выдачи задания:")
        deadline_date_from = input()
        return GithubDate(deadline_date_from)
    except Exception:
        print("Неверно введена дата, будет использовано значение по умолчанию: 2000-01-01 00:00:00")
        return GithubDate("2000-01-01 00:00:00")


def get_deadline_date_to():
    try:
        print("Введите дату дедалйна:")
        deadline_date_to = input()
        return GithubDate(deadline_date_to)
    except Exception:
        print("Неверно введена дата, будет использовано значение по умолчанию: 2100-01-01 00:00:00")
        return GithubDate("2100-01-01 00:00:00")


def main():
    g = Github("")  # TODO
    file = open("students.txt", 'r')
    csv_file = open('commits.csv', 'w')

    deadline_date_from = get_deadline_date_from()
    deadline_date_to = get_deadline_date_to()

    for line in file:
        line = line.strip('\n').split(' ')
        try:
            repo = g.get_repo(line[3])
        except Exception:
            print("Ошибка, что-то не так с данными \"" + line[0] + ' ' + line[1] +
                  "\" в файле students.txt. Скорее всего ссылка https://github.com/" + line[3] + " недействительна.")
            continue
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
            row[3] = total_commits
            csv_writer(csv_file, row)

    file.close()
    csv_file.close()


if __name__ == '__main__':
    main()
