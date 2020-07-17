#!/usr/bin/env python
# coding: utf-8

# In[29]:


from tensorflow.keras.models import load_model
import numpy as np
from flask import Flask,request,jsonify,render_template
import os
import uuid

app = Flask(__name__)


# In[30]:


Expected = {
"cylinders":{"min":3,"max":8},
"displacement":{"min":68.0,"max":455.0},
"horsepower":{"min":46.0,"max":230.0},
"weight":{"min":1613,"max":5140},
"acceleration":{"min":8.0,"max":24.8},
"year":{"min":70,"max":82},
"origin":{"min":1,"max":3}
}


# In[31]:


os.chdir(r'C:\Users\user\Flask')
model = load_model(os.path.join(os.getcwd(),"mpg_model.h5"))


# In[32]:


model.summary()


# In[33]:


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    content = [int(x) for x in request.form.values()]
    received = {"cylinders":content[0],"displacement":content[1],"horsepower":content[2],
               "weight":content[3],"acceleration":content[4],"year":content[5],"origin":content[6]}
    
    errors = []
    for name in received:
        if name in Expected:
            expec_min = Expected[name]['min']
            expec_max = Expected[name]['max']
            value = received[name]
            if value < expec_min or value > expec_max:
                errors.append(f"The given values for {name} are out of Range, it should be between {expec_min} and {expec_max}")
        else:
            errors.append(f'Unexpected field {(name)} received as input')
    for name in Expected:
        if name not in received:
            errors.append(f'one of the required field{(name)} is missingin the input data')
    if len(errors) <1:
        x = np.zeros((1,7))
        x[0,0] = received['cylinders']
        x[0,1] = received['displacement']
        x[0,2] = received['horsepower']
        x[0,3] = received['weight']
        x[0,4] = received['acceleration']
        x[0,5] = received['year']
        x[0,6] = received['origin']
        
        prediction = model.predict(x)
        mpg = float(prediction[0])
        response = {'ID': str(uuid.uuid4()),'The calculated Milage':mpg,'Errors': errors}
    else:
        response = {'ID':str(uuid.uuid4()),'Errors': errors}
    return render_template('index.html', prediction_text='Your prediction result is below $ {}'.format(response))


# In[34]:


if __name__ == "__main__":
    app.run(debug = True,use_reloader = False,)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




