from requests_html import HTMLSession
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
class InflationRate(Resource):
    def get(self,country):
        '''get_last_updated_inflation_rate'''
        response_dict={}
        session = HTMLSession()
        if ' ' in country.strip():
            country='-'.join(country.strip().split(' ')).lower()
        try:
            response = session.get(f'https://www.rateinflation.com/inflation-rate/{country}-inflation-rate/')
            last_updated = response.html.find('div[class="css-0 ewgn69j1"]')[0].text.split(':')[1].strip()
            month = response.html.find('div[class="css-in3yi3 e1x5eoea4"]')[0].text
            inflation_rate = response.html.find('div[class="css-in3yi3 e1x5eoea5"]')[0].text
            response_dict = {'country':country,
                'last_updated':last_updated,
                'for the month of':month,
                'inflation_rate':inflation_rate,
                }
        except:
            response_dict = {'country':country,
                'response':"Requested country not availabe, pls check the country name"
                }
        return response_dict

api.add_resource(InflationRate,'/<string:country>')

if __name__=="__main__":
    app.run(debug=True)