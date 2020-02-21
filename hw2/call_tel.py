def main():
    code = int(input())
    time = int(input())
    if code == 343:
        print(15 * time)
    elif code == 381:
        print(18 * time)
    elif code == 473:
        print(13 * time)
    elif code == 485:
        print(11 * time)
    else:
        print("Unknown city code")


if __name__ == "__main__":
    main()
