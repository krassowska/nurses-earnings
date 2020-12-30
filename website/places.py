from unidecode import unidecode

wojewodztwa_list = [
    "dolnośląskie",
    "kujawsko-pomorskie",
    "lubelskie",
    "lubuskie",
    "łódzkie",
    "małopolskie",
    "mazowieckie",
    "opolskie",
    "podkarpackie",
    "podlaskie",
    "pomorskie",
    "śląskie",
    "świętokrzyskie",
    "warmińsko-mazurskie",
    "wielkopolskie",
    "zachodniopomorskie"
]

wojewodztwa_dict = {
    'Województwa': [
        {
            'id': unidecode(wojewodztwo),
            'label': wojewodztwo,
            'name': unidecode(wojewodztwo)
        }
        for wojewodztwo in wojewodztwa_list
    ]
}