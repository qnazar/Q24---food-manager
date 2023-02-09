import datetime

from sqlalchemy.orm import relationship

from application import db


class Profile(db.Model):
    __tablename__ = 'profile'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    sex = db.Column(db.String(10))
    birthday = db.Column(db.Date)

    weight = db.Column(db.Float())
    height = db.Column(db.Integer)
    constitution = db.Column(db.String(32))
    activity = db.Column(db.Float())

    BMI = db.Column(db.Float())  # індекс маси тіла
    BMR = db.Column(db.Integer)  # основний обмін
    DKI = db.Column(db.Integer)  # денна норма ккал
    DWN = db.Column(db.Integer)  # денна норма води
    IW = db.Column(db.Float())   # ідеальна вага
    min_weight = db.Column(db.Float())
    max_weight = db.Column(db.Float())

    daily_stock_subscription = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship('User', back_populates='profile')
    dynamics = db.relationship('ProfileDynamic', backref='profile', lazy=True)

    def body_mass_index(self):
        BMI = self.weight / (self.height / 100) ** 2
        return round(BMI, 2)

    def basic_metabolism_rate(self):
        """Формула Міффліна - Сан Жеора"""
        age = (datetime.date.today() - self.birthday).total_seconds() // (60 * 60 * 24 * 365)
        k = 5 if self.sex == 'Чоловіча' else -161
        BMR = 9.99 * self.weight + 6.25 * self.height - 4.92 * age + k
        return round(BMR)

    def daily_kcal_intake(self):
        BMR = self.basic_metabolism_rate()
        SDFE = BMR / 10  # специфічно-динамічна дія їжі
        return round((BMR + SDFE) * self.activity)

    def water_norm(self):
        hnw = self.max_normal_weight()
        overweight = self.weight - hnw if self.weight > hnw else 0
        return round(35 * self.weight + overweight * 20)

    def ideal_weight(self):
        iw = (self.height - 100) - (self.height - 150) / 4
        if self.constitution == 'Астенік':
            iw = iw - iw/10
        elif self.constitution == 'Гіперстенік':
            iw = iw + iw/10
        return round(iw, 1)

    def max_normal_weight(self):
        """Розрахунок Кетле"""
        return round(25 * (self.height/100)**2, 1)

    def min_normal_weight(self):
        """Розрахунок Кетле"""
        return round(18.5 * (self.height/100)**2, 1)

    def __str__(self):
        return f'<Profile: {self.first_name} {self.last_name}>'


class ProfileDynamic(db.Model):
    __tablename__ = 'profile_dynamic'

    id = db.Column(db.Integer, primary_key=True)
    current_weight = db.Column(db.Float())
    current_activity = db.Column(db.Float())
    BMR = db.Column(db.Integer)
    BMI = db.Column(db.Float())
    DKI = db.Column(db.Integer)
    DWN = db.Column(db.Integer)
    entry_date = db.Column(db.Date, default=datetime.date.today())

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
