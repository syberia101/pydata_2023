from owlready2 import *
import werkzeug.serving
from flask import Flask, request
from collections import Counter

app = Flask(__name__)


ontology_dinto = "data/DINTO_1.2.owl"
default_world.set_backend(filename="data/DINTO.sqlite3")
onto = get_ontology(ontology_dinto).load()
default_world.save()
obo = get_namespace("http://purl.obolibrary.org/obo/")


@app.route("/")
def page_entry():
    html = """<html><body>
    <h3>Enter the names of the drugs</h3>
    <form action="/result">
        Drug 1  <input type="text" name="drug1"/> <br/>
        Drug 2  <input type="text" name="drug2"/> <br/>  
        <input type="submit"/>
    </form>  
    </body></html>"""
    return html


def interaction(medicament):
    interaction = set()
    for l in medicament.DINTO_000499:
        # print(f"medicament {medicament.label}, interact with, {l.label}")
        interaction.add(l)
    medicament_second_level = []
    for m_interaction in interaction:
        for pp in m_interaction.DINTO_000499:
            medicament_second_level.append(pp)

            # print(f"{p.label}, interact with, {pp.label}")
    number_of_occurance = Counter(medicament_second_level)
    result_drug_1 = []
    for k, v in number_of_occurance.items():
        if v > 10:
            # print(k, v)
            if k != medicament:
                result_drug_1.append(k.label[0])

    return medicament.label[0], result_drug_1


@app.route("/result")
def page_result():
    drug1 = request.args.get("drug1", "")
    drug2 = request.args.get("drug2", "")
    med1 = onto.search(label=f"{drug1}", _case_sensitive=False)
    med2 = onto.search(label=f"{drug2}", _case_sensitive=False)
    # print(med1.first())
    medicament_1_interaction, drug_interaction_1 = interaction(med1.first())
    # print("medicament ", medicament_1_interaction)
    medicament_2_interaction, drug_interaction_2 = interaction(med2.first())
    # print("medicament ", medicament_2_interaction)

    html = """ <html><body> """
    html += f"""<h4>Which drugs could interact with</h4>"""
    html += f"""<p>{medicament_1_interaction} and {medicament_2_interaction}</p>"""
    html += f"""<h4>List of drug that could interact:</h4>"""
    for drug in set(drug_interaction_1) & set(drug_interaction_2):
        html += f"""{drug}<br/>"""

    return html


import werkzeug.serving

werkzeug.serving.run_simple("localhost", 5001, app)
