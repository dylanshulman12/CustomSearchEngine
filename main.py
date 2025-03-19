from distutils.log import debug 
from fileinput import filename 
from flask import *  
import os
import yaml
import shutil
from search import duckduckgo_search




app = Flask(__name__)  


def load_Config():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config
config = load_Config()  # Load the current settings

def get_Setting(setting):
    value = config.get(setting)
    return value

def save_Config(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

def clear_Temp():
    for file_name in os.listdir(os.path.join(app.root_path, 'static', 'tmp')):
        file_path = os.path.join(os.path.join(app.root_path, 'static', 'tmp'),  file_name)
        os.remove(file_path)

def get_Temp_File():
    folder_path = os.path.join(app.root_path, 'static', 'tmp')
    name = next(iter(os.listdir(folder_path)), None)
    return name


selected_color = "#404041"
@app.route('/')
def main():
    clear_Temp()
    
    return render_template("index.html", logo=get_Setting('logo'), footer=get_Setting('footer'), custom_color=get_Setting('background-color'))

@app.route('/settings')
def settings():
    
    available_logos = os.listdir(os.path.join(app.root_path, 'static'))
    available_logos.remove('tmp')        
    available_logos.remove('default')
    available_logos.remove('default.jpg')


    return render_template("settings.html", preview=get_Temp_File(), available_logos=available_logos, custom_color=get_Setting('background-color'))

@app.route('/search', methods=['GET', 'POST'])  
def search():
    #POST METHOD
    if request.method == 'POST':
        query = request.form.get('query')   
        return render_template("response.html", item=query, finishedQuery=query, custom_color=get_Setting('background-color'))  
    #GET METHOD
    if request.method == 'GET':
        query = request.args.get('query')
        # Get results
        results = duckduckgo_search(query)
        # results = []
        return render_template("response.html", results=results, finishedQuery=query, custom_color=get_Setting('background-color'))  

@app.route("/set_color", methods=["POST"])
def set_color():
    global selected_color  # Save the selected color
    if request.form.get("color_Select_Button") == "reset":
        selected_color = "#404041"
        
    else:
        selected_color = request.form.get("colorPicker")        
    
    config['background-color'] =  selected_color # Change yaml setting 
    save_Config(config)
    return redirect('/')





#General Settings menu
@app.route('/preview', methods = ['POST'])   
def previewImage():   
    if request.method == 'POST': 
        clear_Temp()
        file = request.files['file']

        file_path = os.path.join(app.root_path, 'static', 'tmp', file.filename)
        file.save(file_path)
        return redirect("/settings")   
        # return "success"

        
        # except Exception as e:
        #     return render_template("settings.html", error=e)   

@app.route('/upload', methods = ['POST'])   
def success():   
    if request.method == 'POST': 
        try:   
            file_path = os.path.join(app.root_path, 'static', 'tmp', get_Temp_File())
            static_file_path = os.path.join(os.getcwd(), 'static', get_Temp_File())
            
            config['logo'] =  get_Temp_File() # Change yaml setting 
            save_Config(config)
            shutil.copy(file_path, static_file_path)

            return redirect('/settings')
        except Exception as e:
            return f"Error: {str(e)}"  
@app.route('/resetIcon', methods = ['POST'])   
def reset_Icon():   
    if request.method == 'POST': 
        try:  
            config['logo'] =  "default.jpg" # Change yaml setting 
            save_Config(config)
            clear_Temp()
            file_path = os.path.join(os.getcwd(), 'static', "default.jpg")
            static_file_path = os.path.join(app.root_path, 'static', 'tmp', "default.jpg")
            
            shutil.copy(file_path, static_file_path)
            
            return redirect('/settings')
        except Exception as e:
            return f"Error: {str(e)}"  

@app.route('/selectAvailableLogo', methods = ['POST'])   
def select_Available_Logo():   
    if request.method == 'POST': 
        try:  
            clear_Temp()
            selectedLogo = request.form.get('selected_logo')
            config['logo'] =  selectedLogo # Change yaml setting 
            save_Config(config)
            
            file_path = os.path.join(os.getcwd(), 'static', selectedLogo)
            static_file_path = os.path.join(app.root_path, 'static', 'tmp', selectedLogo)
            
            shutil.copy(file_path, static_file_path)
            
            return redirect('/settings')
        except Exception as e:
            return f"Error: {str(e)}"  

@app.route('/deleteAvailableLogo', methods = ['POST'])   
def delete_Logo():   
    if request.method == 'POST': 
        try:  
            clear_Temp()
            selectedLogo = request.form.get('selected_logo')
            
            file_path = os.path.join(os.getcwd(), 'static', selectedLogo)
            os.remove(file_path) 

            return redirect('/settings')
        except Exception as e:
            return f"Error: {str(e)}"  






@app.route("/settings/search")
def set_Setting():   
    if request.method == 'POST': 
            color = request.form.get('bgColorPicker')
            config['background-color'] = color  # Change yaml setting
            save_Config(config)
            bg_color = "#3498db"  # Make sure this is a valid CSS color format
            print("Background color:" + bg_color)  # Debugging line

            return render_template("index.html")  
            # return render_template("index.html", bgColor=get_Setting('background-color'))
        

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=8123, debug=True)