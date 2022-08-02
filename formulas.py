class User:
    def __init__(self, sex, age, weight, height):
        self.sex = sex
        self.age = age
        self.weight = weight
        self.height = height
        self.bmr = self.basic_metabolism_rate()

    def basic_metabolism_rate(self):
        if self.sex in 'mM':
            BMR = 88.36 + (13.4 * self.weight) + (4.8 * self.height) - (5.7 * self.age)
        elif self.sex in 'fF':
            BMR = 447.6 + (9.2 * self.weight) + (3.1 + self.height) - (4.3 * self.age)
        else:
            raise ValueError
        return BMR

    def daily_kcal_intake(self):
        return self.bmr * 1.35, self.bmr * 1.5, self.bmr * 1.9

    def body_mass_index(self):
        BMI = self.weight / (self.height/100)**2
        return BMI

    def highest_normal_weight(self):
        return 25 * (self.height/100)**2

    def water_norm(self):
        return 30 * self.weight


if __name__ == '__main__':
    kostya = User('M', 26, 76, 178)
    print('Basic Metabolism Rate: ', kostya.bmr)
    print(kostya.daily_kcal_intake())
    print(kostya.body_mass_index())
    print(kostya.highest_normal_weight())
    print(kostya.water_norm())
