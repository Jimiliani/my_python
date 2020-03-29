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

    deadline_date_to, deadline_date_from = "", ""
    dates = []
    for line in file:
        dates = line.strip('\n').split(' ')
        break

    try:
        deadline_date_from = GithubDate(dates[0])
        deadline_date_to = GithubDate(dates[1])
    except Exception:
        print("Ошибка, некорректный формат дат в students.txt, убедитесь, что вы"
              " не используете пробел в качестве разделительного символа в первой или второй дате")
        exit(1)

    for line in file:
        if line.strip('\n').split(' ') == dates:
            continue
        line = line.strip('\n').split(' ')
        try:
            repo = g.get_repo(line[3])
        except Exception:
            try:
                print("Ошибка, что-то не так с данными \"" + line[0] + ' ' + line[1] +
                      "\" в файле students.txt. Скорее всего ссылка https://github.com/" + line[3] +
                      " недействительна. В случае если данная ошибка возникает для всех или большинства людей файла,"
                      " то вероятно превышен лимит запросов в гитхаб")
                continue
            except Exception:
                print("Ошибка, что-то не так с данными, не удалось "
                      "поделить строку на имя, фамилию, группу и репозиторий.")
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
