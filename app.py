from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from cdmn.API import DMN
import time
import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

#from utils.bmi import calculate_bmi

def calculate_bmi(spec,height,weight,waist,gender):
    spec.set_value('weight', weight)
    spec.set_value('length', height)

    spec.propagate()
    # if spec.is_certain('bmi'):
    #     print('BMI:', spec.value_of('bmi'))

    if (gender == 'Male' or gender == 'Female'):
        spec.set_value('sex', gender)
        # if spec.is_certain('BMILevel'):
        #     print('BMILevel:', spec.value_of('BMILevel'))
        # else:
        #     print('BMILevel is still unknown.')

    spec.set_value('waist', waist)
    # if spec.is_certain('riskLevel'):
    # print('riskLevel:', spec.value_of('riskLevel'))

    Input_weight = weight
    Input_hight = height
    Input_sex = gender
    Input_waist = waist
    Bmi = spec.value_of('bmi')
    Bmilevel = spec.value_of('BMILevel')
    RiskLevel = spec.value_of('riskLevel')
    if spec.is_certain('bmi') and float(spec.value_of('bmi')) > 25:
        # print('Your BMI is too high!')
        # print('Ideal BMI is 25 ')
        # print("This is a difference of {} ".format(round(float(spec.value_of('bmi'))-25,2)))
        # Get current weight.
        cur_weight = spec.value_of('weight')

        # Calculate ideal weight.
        spec.set_value('weight', None)
        spec.set_value('bmi', 25)
        ideal_weight = float(spec.value_of('weight'))
        ideal_waist = float(spec.value_of('waist'))
        # print("For a healthy bmi, you should weigh {} kg.".format(ideal_weight))
        # print("This is a difference of {} kg.".format(round(cur_weight - ideal_weight, 2)))

        return f''' Your Weight - {Input_weight}<br/> 
            Your Hight - {Input_hight}<br/> 
            Your Gender - {Input_sex}<br/>
            Your Waist - {Input_waist}<br/>
            BMI :- {Bmi}<br/>
            BMI Level :- {Bmilevel}<br/>
            Risk Level :- {RiskLevel}<br/>
            Your BMI is too high!<br/>
            Ideal BMI is 25<br/>
            This is a difference of {round(float(spec.value_of('bmi')) - 25, 2)}<br/>
            For a healthy bmi, you should weigh {ideal_weight} kg.<br/>
            This is a difference of {round(cur_weight - ideal_weight, 2)} kg.
        '''

    else:
        # print('Your BMI is Normal !')
        cur_weight = spec.value_of('weight')

        # Calculate ideal weight.
        spec.set_value('weight', None)
        spec.set_value('bmi', 25)
        ideal_weight = float(spec.value_of('weight'))

        # print("For a healthy bmi, you should weigh {} kg.".format(ideal_weight))
        # print("This is a difference of {} kg.".format(round(cur_weight - ideal_weight, 2)))

        return f'''Your Weight - {Input_weight}<br/> 
            Your Hight - {Input_hight}<br/> 
            Your Gender - {Input_sex}<br/>
            Your Waist - {Input_waist}<br/>
            BMI :- {Bmi}<br/>
            BMI Level :- {Bmilevel}<br/>
            Risk Level :- {RiskLevel}<br/>
            Your BMI Normal !<br/>
            For a healthy bmi, you should weigh {ideal_weight} kg.<br/>
            This is a difference of {round(cur_weight - ideal_weight, 2)} kg.
        '''



app = Flask(__name__)
#path = 'BMILevel.dmn'
#spec = DMN(path)


# start an app routepython3 -m  pipreqs.pipreqs
@app.route('/')
# declare function
def main():
    return render_template('app.html')
    
    
# form submission route
@app.route('/predict', methods=["POST"])
def predict():
    if request.method == 'POST':
        resp = request.form
        # start pulling data from input

        spec = DMN('BMILevel.dmn')
        spec.clear()
        weight = resp.get('weight', type=float)
        hight = resp.get('hight', type=float)
        gender = resp.get('sex', type=str)
        waist = resp.get('waist', type=float)

        res = calculate_bmi(spec, hight, weight, waist, gender)

        #Weight = resp.get('weight',type=float)
        #hight = resp.get('hight',type=float)
        #sex = resp.get('sex',type=str)
        #waist = resp.get('waist',type=float)
        #peration = request.form.get('operation')
        #weigth = float(Weight)
        #hight = float(hight)
        #sex = str(sex)
        #sex = sex.title()
        #waist = float(waist)

        #print(Weight,hight,sex,waist)
        
        # set value for DMN
        #spec.set_value('weight', Weight)
        #spec.set_value('length', hight)
        #spec.set_value('sex', sex)
        #spec.set_value('waist', waist)

        #spec.propagate()
        #bmi = spec.value_of('bmi')
        #bmilevel = spec.value_of('BMILevel')
        #riskLevel = spec.value_of('riskLevel')
        #print(bmi,bmilevel,riskLevel)
        return render_template('app.html', BMI=res )
    else:
        return render_template('app.html')
                
        
        


if __name__ == '__main__':
    app.run(debug=True)