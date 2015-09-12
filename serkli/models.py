from django.db import models

# Create your models here.
class Event(models.Model):
    event_id = models.CharField(max_length=50)
    event_name = models.CharField(max_length=200)
    event_date = models.DateTimeField('date of event')

    def __unicode__(self):
        return self.event_name

class Attendee(models.Model):
    event = models.ForeignKey(Event)
    attendee_id = models.CharField(max_length=50)
    attendee_email = models.CharField(max_length=200)
    attendee_name = models.CharField(max_length=100)
    checked_in = models.BooleanField(default=False)

    def __unicode__(self):
        return self.attendee_name


class Circle(models.Model):
    circle_name = models.CharField(max_length=100)
    circle_created_date = models.DateTimeField('date of event')

    def __unicode__(self):
        return self.circle_name


class Member(models.Model):
    circle = models.ForeignKey(Circle)
    member_name = models.CharField(max_length=100)
    member_email = models.CharField(max_length=200, null=True, blank=True)
    member_phone = models.CharField(max_length=25, null=True, blank=True)

    UNDER_20 = '<20'
    BTWN_20_30 = '20-30'
    BTWN_31_45 = '31-44'
    BTWN_46_55 = '45-55'
    OVER_55 = '>55'
    AGE_RANGE_CHOICES = (
        (UNDER_20, 'under 20'),
        (BTWN_20_30, 'between 20 and 30'),
        (BTWN_31_45, 'between 31 and 45'),
        (BTWN_46_55, 'between 46 and 55'),
        (OVER_55, '55 and over'),
    )
    age_range = models.CharField(max_length=5,
                                 choices=AGE_RANGE_CHOICES,
                                 default=BTWN_20_30)

    FEMALE = 'XX'
    MALE = 'XY'
    SEX_CHOICES = (
        (FEMALE, 'XX sex chromosomes (female)'),
        (MALE, 'XY sex chromosomes (male)'),
    )
    sex_range = models.CharField(max_length=2,
                                 choices=SEX_CHOICES,
                                 default=FEMALE)

    WHITE = 'CNH'
    BLACK = 'AFR'
    HISPANIC = 'HIS'
    ASIAN = 'ASI'
    OTHER = 'OTH'
    ETHNICITY_CHOICES = (
        (WHITE, 'Caucasian Non-Hispanic'),
        (BLACK, 'African American'),
        (HISPANIC, 'Hispanic'),
        (ASIAN, 'Asian'),
        (OTHER, 'Other race or ethnicity'),
    )
    ethnicity_range = models.CharField(max_length=3,
                                       choices=ETHNICITY_CHOICES,
                                       default=WHITE)

    BMI_UNDER = '<25'
    BMI_OVER = '25>'
    BMI_CHOICES = (
        (BMI_UNDER, 'is less than 25'),
        (BMI_OVER, 'is 25 or greater'),
    )
    bmi_range = models.CharField(max_length=3,
                                 choices=BMI_CHOICES,
                                 default=BMI_UNDER)

    smoker = models.BooleanField(default=False)
    drinker = models.BooleanField(default=False)
    exercises = models.BooleanField(default=False)

    cancer_family = models.SmallIntegerField(default=0)


    def risk(self):
        risk_percentage = 0.0

        female_under_45 = 0.12

        male = 0.001

        Overall, white women are slightly more likely to develop breast cancer than are African-American women,
        but African-American women are more likely to die of this cancer.
        However, in women under 45 years of age, breast cancer is more common in African- American women. 
        Asian, Hispanic, and Native-American women have a lower risk of developing and dying from breast cancer. 

        Having one immediate relative approximately doubles a womans risk

        Having 2 first-degree relatives increases her risk about 3-fold

        Women who have 2 to 5 drinks daily have about 1.5 times the risk of women who don’t drink alcohol

        Altogether, less than 15% of women with breast cancer have a family member with this disease
        This means that most (over 85%) women who get breast cancer do not have a family history of this disease

        5% to 10% of breast cancer cases are thought to be hereditary

        2 of 3 invasive breast cancers are found in women age 55 or older

        Brisk walking reduced a woman's risk by 18%


        if self.smoker:



        return self.year_in_school in (self.JUNIOR, self.SENIOR)


    def __unicode__(self):
        return self.member_name


#class MemberHistory(models.Model):
