def main():
    text = input().split(' ')
    nums = []
    for word in text:
        try:
            nums.append(float(word))
        except Exception:
            pass
    print("Всего чисел:", len(nums))
    print("Сумма чисел:", sum(nums))
    print("Максимальное число:", max(nums))


if __name__ == '__main__':
    main()
