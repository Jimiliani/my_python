from django.db import models


class Item(models.Model):
    gender_choices = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('U', 'Унисекс'),
    ]
    item_type_choices = [
        ('Outwear', 'Верхняя одежда'),
        ('Underwear', 'Нижняя одежда'),
        ('Shoe', 'Обувь'),
        ('Accessory', 'Аксессуары'),
    ]
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.IntegerField(null=False, blank=False)
    image = models.ImageField(null=False, blank=False)
    gender = models.CharField(max_length=8, choices=gender_choices, null=False, blank=False)
    materials = models.CharField(max_length=100, blank=True)
    about = models.CharField(max_length=100, blank=True)
    firm = models.CharField(max_length=100, blank=True)
    item_type = models.CharField(max_length=32, choices=item_type_choices)

    def __str__(self):
        return self.name


class Outwear(Item):
    count_size_34_36 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_36_38 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_38_40 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_40_42 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_42_44 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_44_46 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_46_48 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_48_50 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_50_52 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    def get_count_by_count_sizes(self):
        return [
            ('34 - 36', self.count_size_34_36),
            ('36 - 38', self.count_size_36_38),
            ('38 - 40', self.count_size_38_40),
            ('40 - 42', self.count_size_40_42),
            ('42 - 44', self.count_size_42_44),
            ('44 - 46', self.count_size_44_46),
            ('46 - 48', self.count_size_46_48),
            ('48 - 50', self.count_size_48_50),
            ('50 - 52', self.count_size_50_52),
        ]

    def has_in_stock(self):
        for size, count in self.get_count_by_count_sizes():
            if count > 0:
                return True
        return False

    def get_count_in_stock(self, required_size):
        for size, count in self.get_count_by_count_sizes():
            if size == required_size:
                return count
        raise ValueError

    def buy_items(self, size, count):
        if size == '34 - 36':
            self.count_size_34_36 -= count
        elif size == '36 - 38':
            self.count_size_36_38 -= count
        elif size == '38 - 40':
            self.count_size_38_40 -= count
        elif size == '40 - 42':
            self.count_size_40_42 -= count
        elif size == '42 - 44':
            self.count_size_42_44 -= count
        elif size == '44 - 46':
            self.count_size_44_46 -= count
        elif size == '46 - 48':
            self.count_size_46_48 -= count
        elif size == '48 - 50':
            self.count_size_48_50 -= count
        elif size == '50 - 52':
            self.count_size_50_52 -= count
        self.save()
        return True


class Underwear(Item):
    count_size_28_30 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_30_32 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_32_34 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_34_36 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_36_38 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_38_40 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_40_42 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_42_44 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_44_46 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    def get_count_by_count_sizes(self):
        return [
            ('28 - 30', self.count_size_28_30),
            ('30 - 32', self.count_size_30_32),
            ('32 - 34', self.count_size_32_34),
            ('34 - 36', self.count_size_34_36),
            ('36 - 38', self.count_size_36_38),
            ('38 - 40', self.count_size_38_40),
            ('40 - 42', self.count_size_40_42),
            ('42 - 44', self.count_size_42_44),
            ('44 - 46', self.count_size_44_46),
        ]

    def has_in_stock(self):
        for size, count in self.get_count_by_count_sizes():
            if count > 0:
                return True
        return False

    def get_count_in_stock(self, required_size):
        for size, count in self.get_count_by_count_sizes():
            if size == required_size:
                return count
        raise ValueError

    def buy_items(self, size, count):
        if size == '28 - 30':
            self.count_size_28_30 -= count
        elif size == '30 - 32':
            self.count_size_30_32 -= count
        elif size == '32 - 34':
            self.count_size_32_34 -= count
        elif size == '34 - 36':
            self.count_size_34_36 -= count
        elif size == '36 - 38':
            self.count_size_36_38 -= count
        elif size == '38 - 40':
            self.count_size_38_40 -= count
        elif size == '40 - 42':
            self.count_size_40_42 -= count
        elif size == '42 - 44':
            self.count_size_42_44 -= count
        elif size == '44 - 46':
            self.count_size_44_46 -= count
        self.save()
        return True


class Shoe(Item):
    count_size_32_34 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_34_36 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_36_38 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_38_40 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_40_42 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_42_44 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_44_46 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_46_48 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_48_50 = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    def get_count_by_count_sizes(self):
        return [
            ('32 - 34', self.count_size_32_34),
            ('34 - 36', self.count_size_34_36),
            ('36 - 38', self.count_size_36_38),
            ('38 - 40', self.count_size_38_40),
            ('40 - 42', self.count_size_40_42),
            ('42 - 44', self.count_size_42_44),
            ('44 - 46', self.count_size_44_46),
            ('46 - 48', self.count_size_46_48),
            ('48 - 50', self.count_size_48_50),
        ]

    def has_in_stock(self):
        for size, count in self.get_count_by_count_sizes():
            if count > 0:
                return True
        return False

    def get_count_in_stock(self, required_size):
        for size, count in self.get_count_by_count_sizes():
            if size == required_size:
                return count
        raise ValueError

    def buy_items(self, size, count):
        print('покупаем')
        if size == '32 - 34':
            self.count_size_32_34 -= count
        elif size == '34 - 36':
            self.count_size_34_36 -= count
        elif size == '36 - 38':
            self.count_size_36_38 -= count
        elif size == '38 - 40':
            self.count_size_38_40 -= count
        elif size == '40 - 42':
            self.count_size_40_42 -= count
        elif size == '42 - 44':
            self.count_size_42_44 -= count
        elif size == '44 - 46':
            self.count_size_44_46 -= count
        elif size == '46 - 48':
            self.count_size_46_48 -= count
        elif size == '48 - 50':
            self.count_size_48_50 -= count
        self.save()
        return True


class Accessory(Item):
    count_size_XS = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_S = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_M = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_L = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    count_size_XL = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

    def get_count_by_count_sizes(self):
        return [
            ('XS', self.count_size_XS),
            ('S', self.count_size_S),
            ('M', self.count_size_M),
            ('L', self.count_size_L),
            ('XL', self.count_size_XL),
        ]

    def has_in_stock(self):
        for size, count in self.get_count_by_count_sizes():
            if count > 0:
                return True
        return False

    def get_count_in_stock(self, required_size):
        for size, count in self.get_count_by_count_sizes():
            if size == required_size:
                return count
        raise ValueError

    def buy_items(self, size, count):
        if size == 'XS':
            self.count_size_XS -= count
        elif size == 'S':
            self.count_size_S -= count
        elif size == 'M':
            self.count_size_M -= count
        elif size == 'L':
            self.count_size_L -= count
        elif size == 'XL':
            self.count_size_XL -= count
        self.save()
        return True
