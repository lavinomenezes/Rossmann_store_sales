import pickle
import os
import pandas as pd
import xgboost
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann

#loading model
model = pickle.load(open(r'\Users\Lavin\Documents\Comunidade DS\Ds_em_producao\model\model_rossman_xgb.pkl','rb'))

app = Flask(__name__)

@app.route('/rossmann/predict',methods=['POST'])
def rossmann_predict():
    test_json = request.get_json()
    
    if test_json: #there is data
        
        if isinstance(test_json,dict): #UNique example
            test_raw = pd.DataFrame(test_json,index=[0])
        else: # Multiple Examples
            test_raw = pd.DataFrame(test_json,columns=test_json[0].keys())
        
        # Instantiate Rossman class
        pipeline = Rossmann()
        
        #data cleaning
        df1 = pipeline.data_cleaning(test_raw)
        # feature engeneering
        df2 = pipeline.feature_engineering(df1)
        # data preparation
        df3 = pipeline.data_preparation(df2)
        # prediction
        df_response = pipeline.get_prediction(model,test_raw,df3)
        
        return df_response
    
    else:
        return Response('{}',status=200,mimetype='application/json')

if __name__ == '__main__':
    port = os.environ.get( 'PORT', 5000)
    app.run('192.168.0.5',port=port)