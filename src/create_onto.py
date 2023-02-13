from owlready2 import *

onto = get_ontology("http://deribaupierre/tea#")


def create_tea_ontology(file: str) -> None:

    with onto:

        class Ingredient(Thing):
            pass

        class Bergamote(Ingredient):
            pass

        class Jasmin(Ingredient):
            pass

        class Vanilla(Ingredient):
            pass

        class Verbena(Ingredient):
            pass

        class Mango(Ingredient):
            pass

        class Apple(Ingredient):
            pass

        AllDisjoint([Bergamote, Jasmin, Mango, Apple, Verbena])

        class Preparation(Thing):
            pass

        class Oxidation(Preparation):
            pass

        class Smoking(Preparation):
            pass

        class HalfSmoked(Preparation):
            pass

        class Dried(Preparation):
            pass

        AllDisjoint([Oxidation, Smoking, HalfSmoked, Dried])

        class Tea(Thing):
            pass

        AllDisjoint([Tea, Preparation, Ingredient])

        class is_ingredient_of(Ingredient >> Tea):
            pass

        class has_ingredient(Tea >> Ingredient):
            pass

        class has_preparation(Tea >> Preparation, FunctionalProperty):
            pass

        class is_preparation_of(Preparation >> Tea, FunctionalProperty):
            inverse = has_preparation

        class Oxidised(Tea):
            equivalent_to = [
                Tea & has_preparation.some(Oxidation) & has_preparation.only(Oxidation)
            ]

        class Smoked(Tea):
            equivalent_to = [
                Tea & has_preparation.some(Smoking) & has_preparation.only(Smoking)
            ]

        class Lapsong(Smoked):
            equivalent_to = [
                Tea
                & has_preparation.some(Smoking)
                & has_preparation.only(Smoking)
                & has_ingredient.some(Bergamote)
            ]

        class JasminTea(Oxidised):
            equivalent_to = [
                Tea
                & has_preparation.some(Oxidation)
                & has_preparation.only(Oxidation)
                & has_ingredient.some(Jasmin)
            ]

        class PleinJasmin(Oxidised):
            equivalent_to = [
                Tea
                & has_preparation.some(Oxidation)
                & has_preparation.only(Oxidation)
                & has_ingredient.some(Jasmin)
                & has_ingredient.only(Jasmin)
            ]

        class BlueOfLondon(Oxidised):
            equivalent_to = [
                Tea
                & has_preparation.some(Oxidation)
                & has_preparation.only(Oxidation)
                & has_ingredient.some(Bergamote)
                & has_ingredient.only(Bergamote)
            ]

        BlueOfLondon.label = ["Blue of London"]
        Lapsong.label = ["Lapsong"]
        PleinJasmin.label = ["Plein Jasmin"]
        JasminTea.label = ["Jasmin Tea", "Thé de Jasmin"]

    onto.save(file)
