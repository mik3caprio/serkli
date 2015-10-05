UNDER_20 = "u20"
BTWN_20_29 = "20-29"
BTWN_30_39 = "30-39"
BTWN_40_44 = "40-44"
BTWN_45_49 = "45-49"
BTWN_50_59 = "50-59"
OVER_60 = "60o"

AGE_RANGE_CHOICES = (
    (UNDER_20, "under 20"),
    (BTWN_20_29, "between 20 and 29"),
    (BTWN_30_39, "between 30 and 39"),
    (BTWN_40_44, "between 40 and 44"),
    (BTWN_45_49, "between 45 and 49"),
    (BTWN_50_59, "between 50 and 59"),
    (OVER_60, "60 and over"),
)

FEMALE = "XX"
MALE = "XY"

SEX_CHOICES = (
    (FEMALE, "female (XX)"),
    (MALE, "male (XY)"),
)

WHITE = "CNH"
BLACK = "AFR"
HISPANIC = "HIS"
ASIAN = "ASI"
OTHER = "OTH"

ETHNICITY_CHOICES = (
    (WHITE, "Caucasian"),
    (BLACK, "African American"),
    (HISPANIC, "Hispanic"),
    (ASIAN, "Asian"),
    (OTHER, "Other"),
)

YES = "yes"
NO = "no"

DRINK_CHOICES = (
    (NO, "don't ever"),
    (YES, "do"),
)

SMOKE_CHOICES = (
    (NO, "don't ever"),
    (YES, "do"),
)

EXERCISE_CHOICES = (
    (NO, "don't ever"),
    (YES, "do"),
)

BMI_UNDER = "u25"
BMI_OVER = "25o"

BMI_CHOICES = (
    (BMI_UNDER, "is less than 25"),
    (BMI_OVER, "is 25 or greater"),
)

RELATIVE_CHOICES = (
    ("0", "0"), 
    ("1", "1"), 
    ("2", "2"), 
    ("3", "3")
)
