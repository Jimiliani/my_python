def john_and_paul(list_):
    ans = []
    if "John" in list_:
        ans.append("John")
    if "Paul" in list_:
        ans.append("Paul")
    return ans


def main():
    print(john_and_paul(["John", "Pain", "Paul", "Sasha"]))


if __name__ == '__main__':
    main()
