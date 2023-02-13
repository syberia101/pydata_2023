from owlready2 import *
import werkzeug.serving
from create_onto import create_tea_ontology

file = "data/tea2.owl"
create_tea_ontology(file)
onto = get_ontology(file).load()  # Change the path of the ontology

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def page_entry():
    html = """<html><body>
<h3>Entrez some characteristics of the tea</h3>
<form action="/result">
    Method :<br/>
    <input type="radio" name="mode" value="Oxidation"/> Oxidation<br/>
    <input type="radio" name="mode" value="Smoking"/> Smoking<br/>
 
    Ingredient :<br/>
    <select name="hasI" multiple="multiple">
        <option value="Bergamote">Bergamote</option>
        <option value="Jasmin">Jasmin</option>
        <option value="Vanilla">Vanilla</option>
        <option value="Mango">Mango</option>
        <option value="Apple">Apple</option>
    </select><br/>
   
    <input type="submit"/>
</form>  
</body></html>"""
    return html


ONTO_ID = 0


@app.route("/result")
def page_result():
    global ONTO_ID
    ONTO_ID = ONTO_ID + 1

    onto_tmp = get_ontology("http://tmp.org/onto_%s.owl#" % ONTO_ID)

    mode = request.args.get("mode", "")
    ingredients = request.args.getlist("hasI")
    with onto_tmp:
        tea = onto.Tea()
        if mode == "Oxidation":
            preparation_mode = onto[mode]
            tea.has_preparation = preparation_mode()
        elif mode == "Smoking":
            preparation_mode = onto[mode]
            tea.has_preparation = preparation_mode()

        for ingredient in ingredients:
            ingredient_class = onto[ingredient]
            tea.has_ingredient.append(ingredient_class())
            # print(ingredient)

        close_world(tea)
        sync_reasoner([onto, onto_tmp])

        classes_names = []
        for c in tea.is_a:
            if isinstance(c, ThingClass):
                for l in c.__label:
                    classes_names.append(l)
        classes_names = ", ".join(classes_names)
        # print(classes_names)

        html = (
            """<html><body>
            <h3>Resultat : %s</h3>
            </body></html>"""
            % classes_names
        )

    onto_tmp.destroy()

    return html


werkzeug.serving.run_simple("localhost", 5001, app)
