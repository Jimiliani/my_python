def main():
    text = input().split(" ")
    ans = ""
    for word in text:
        if word[0] != 'м':
            ans += (word + " ")
    print(ans)


if __name__ == '__main__':
    main()
