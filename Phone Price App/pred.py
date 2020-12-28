import pandas as pd
import _pickle as cPickle
# load the model
"Model name is mobclass.pkl "
def get_model(modelname):
    with open(modelname, 'rb') as fid:
        model = cPickle.load(fid)
        return model
#  create datafreame for input datas
def get_value(battery_power, blue,clock_speed,dual_sim,fc,four_g,int_memory,m_dep,mobile_wt,n_cores,pc, px_height,px_width, ram, sc_h, sc_w, talk_time, three_g,touch_screen, wifi):
    data=[{
        'battery_power':battery_power.text,
        'blue':blue.text,
        'clock_speed':clock_speed.text,
        'dual_sim':dual_sim.text,
        'fc':fc.text,
        'four_g':four_g.text,
        'int_memory':int_memory.text,
        'm_dep':m_dep.text,
        'mobile_wt':mobile_wt.text,
        'n_cores':n_cores.text,
        'pc':pc.text,
        'px_height':px_height.text,
        'px_width':px_width.text,
        'ram':ram.text,
        'sc_h':sc_h.text,
        'sc_w':sc_w.text,
        'talk_time':talk_time.text,
        'three_g':three_g.text,
        'touch_screen':touch_screen.text,
        'wifi':wifi.text
    }]
    predData = pd.DataFrame(data)
    # if you want follow dataframe uncomment this rows
    #print(predData.head())
    return predData


# predict model
def get_predict(model,data):
    predicValue = model.predict(data)
    return predicValue

