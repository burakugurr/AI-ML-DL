from flask.helpers import flash
import pandas as pd
from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, abort
import pickle

app = Flask(__name__, template_folder='templates')
api = Api(app)
db_string = 'sqlite:///model.db'
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

################ NEW TABLE ##############################


class AdminModel(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    EducationSector = db.Column(db.Text(), nullable=True)
    IndividualProject = db.Column(db.Text(), nullable=True)
    Age = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.Text(), nullable=False)
    City = db.Column(db.Text(), nullable=True)
    Influenced = db.Column(db.Text(), nullable=True)
    Perseverance = db.Column(db.Integer, nullable=False)
    DesireToTakeInitiative = db.Column(db.Integer, nullable=False)
    Competitiveness = db.Column(db.Integer, nullable=False)
    SelfReliance = db.Column(db.Integer, nullable=False)
    StrongNeedToAchieve = db.Column(db.Integer, nullable=False)
    SelfConfidence = db.Column(db.Integer, nullable=False)
    GoodPhysicalHealth = db.Column(db.Integer, nullable=False)
    MentalDisorder = db.Column(db.Text(), nullable=True)
    KeyTraits = db.Column(db.Text(), nullable=True)
    result = db.Column(db.Integer, nullable=False)


############# MODEL LOAD ##############

path = 'Deploy\lib\models\model.pkl'
loaded_model = pickle.load(open(path, 'rb'))
"""

            userdata.EducationSector, userdata.IndividualProject, userdata.Age,
            userdata.Gender, userdata.City, userdata.Influenced,
            userdata.Perseverance, userdata.DesireToTakeInitiative, userdata.DesireToTakeInitiative,
            userdata.Competitiveness, userdata.SelfReliance,
            userdata.StrongNeedToAchieve, userdata.SelfConfidence, userdata.GoodPhysicalHealth,
            userdata.GoodPhysicalHealth, userdata.MentalDisorder,
            userdata.KeyTraits

"""


def createDataframe(EducationSector, IndividualProject, Age, Gender, City,
                    Influenced, Perseverance, DesireToTakeInitiative,
                    Competitiveness, SelfReliance, StrongNeedToAchieve,
                    SelfConfidence, GoodPhysicalHealth, MentalDisorder,
                    KeyTraits):

    data = {
        'EducationSector': EducationSector,
        'IndividualProject': IndividualProject,
        'Age': Age,
        'Gender': Gender,
        'City': City,
        'Influenced': Influenced,
        'Perseverance': Perseverance,
        'DesireToTakeInitiative': DesireToTakeInitiative,
        'Competitiveness': Competitiveness,
        'SelfReliance': SelfReliance,
        'StrongNeedToAchieve': StrongNeedToAchieve,
        'SelfConfidence': SelfConfidence,
        'GoodPhysicalHealth': GoodPhysicalHealth,
        'MentalDisorder': MentalDisorder,
        'KeyTraits': KeyTraits
    }
    data = pd.DataFrame(data=data, index=[0])
    from sklearn import preprocessing
    le = preprocessing.LabelEncoder()
    data['IndividualProject'] = le.fit_transform(data['IndividualProject'])
    data['Gender'] = le.fit_transform(data['Gender'])
    data['City'] = le.fit_transform(data['City'])
    data['Influenced'] = le.fit_transform(data['Influenced'])
    data['MentalDisorder'] = le.fit_transform(data['MentalDisorder'])
    data['KeyTraits'] = le.fit_transform(data['KeyTraits'])
    data['EducationSector'] = le.fit_transform(data['EducationSector'])
    return data


@app.route('/persona/login', methods=['GET', 'POST'])
def create_persona():
    data = request.form
    new_admins = AdminModel(
        name=str(data['name']).capitalize(),
        EducationSector=str(data['EducationSector']).capitalize(),
        IndividualProject=str(data['IndividualProject']).capitalize(),
        Age=data['Age'],
        Gender=str(data['Gender']).capitalize(),
        City=str(data['City']).capitalize(),
        Influenced=str(data['Influenced']).capitalize(),
        Perseverance=data['Perseverance'],
        DesireToTakeInitiative=data['DesireToTakeInitiative'],
        Competitiveness=data['Competitiveness'],
        SelfReliance=data['SelfReliance'],
        StrongNeedToAchieve=data['StrongNeedToAchieve'],
        SelfConfidence=data['SelfConfidence'],
        GoodPhysicalHealth=data['GoodPhysicalHealth'],
        MentalDisorder=data['MentalDisorder'],
        KeyTraits=str(data['KeyTraits']).capitalize(),
    )
    db.session.add(new_admins)
    db.session.commit()

    if request.method == 'GET':
        return render_template('homepage.html')

    if request.method == 'POST':

        userdata = AdminModel.query.filter_by(
            name=str(data['name']).capitalize()).first()
        if not userdata:
            return jsonify({'message': "Kullanıcı bilgisine erişilemedi"})
        data = createDataframe(
            userdata.EducationSector, userdata.IndividualProject, userdata.Age,
            userdata.Gender, userdata.City, userdata.Influenced,
            userdata.Perseverance, userdata.DesireToTakeInitiative,
            userdata.Competitiveness, userdata.SelfReliance,
            userdata.StrongNeedToAchieve, userdata.SelfConfidence,
            userdata.GoodPhysicalHealth, userdata.MentalDisorder,
            userdata.KeyTraits)

        prediction = loaded_model.predict(data)
        # new predicton result appended database
        userdata.result = prediction
        db.session.commit()

        return render_template(
            'output.html',
            original_input={
                'EducationSector': userdata.EducationSector,
                'IndividualProject': userdata.IndividualProject,
                'Age': userdata.Age,
                'Gender': userdata.Gender,
                'City': userdata.City,
                'Influenced': userdata.Influenced,
                'Perseverance': userdata.Perseverance,
                'DesireToTakeInitiative': userdata.DesireToTakeInitiative,
                'Competitiveness': userdata.Competitiveness,
                'SelfReliance': userdata.SelfReliance,
                'StrongNeedToAchieve': userdata.StrongNeedToAchieve,
                'SelfConfidence': userdata.SelfConfidence,
                'GoodPhysicalHealth': userdata.GoodPhysicalHealth,
                'MentalDisorder': userdata.MentalDisorder,
                'KeyTraits': userdata.KeyTraits
            },
            result=prediction,
        )


if __name__ == '__main__':
    app.run(port=8082)
