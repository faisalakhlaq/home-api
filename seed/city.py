import logging

from apps.core.models import City

logger = logging.getLogger(__name__)


macedonia_cities = [
    "Skopje",
    "Tetovo",
    "Bitola",
    "Kumanovo",
    "Prilep",
    "Ohrid",
    "Veles",
    "Štip",
    "Gostivar",
    "Kočani",
    "Dračevo",
    "Struga",
    "Debar",
    "Strumica",
    "Vinica",
    "Probištip",
    "Aračinovo",
    "Kičevo",
    "Kavadarci",
    "Gevgelija",
    "Vrapčište",
    "Radoviš",
    "Berovo",
    "Kruševo",
    "Sveti Nikole",
    "Demir Kapija",
    "Kučevište",
    "Delčevo",
    "Bogdanci",
    "Rašče",
    "Negotino",
    "Vevčani",
    "Debrešte",
    "Labuništa",
    "Gradsko",
    "Valandovo",
    "Kriva Palanka",
    "Kratovo",
    "Krivogaštani",
    "Zrnovci",
    "Pehčevo",
    "Plasnica",
    "Mogila",
    "Tearce",
    "Novaci",
    "Rosoman",
    "Novo Selo",
    "Bosilovo",
    "Konče",
    "Rostuša",
    "Jegunovce",
    "Rankovce",
    "Sopište",
    "Obleševo",
    "Karbinci",
    "Vasilevo",
    "Petrovec",
    "Makedonski Brod",
    "Staro Nagoričane",
    "Demir Hisar",
    "Lozovo",
    "Centar Župa",
    "Brvenica",
    "Belčišta",
    "Dolneni",
    "Čučer-Sandevo",
    "Zelenikovo",
    "Želino",
    "Star Dojran",
    "Studeničani",
    "Bogovinje",
    "Ilinden",
    "Lipkovo",
    "Makedonska Kamenica",
    "Resen",
]


def create_city(city: str) -> City | None:
    try:
        return City.objects.create(name=city, country="North Macedonia")
    except Exception as ex:
        logger.exception(msg=f"Seed: Unable to create City={ex}.")
        return None


created_cities = list(map(create_city, macedonia_cities))
