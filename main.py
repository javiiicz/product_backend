from flask import Flask, jsonify, request
import serving_logic
import os
import glob
import shutil
from score_and_save import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://rd-luthr.github.io"}})

SESSIONS_UNTIL_REPRODUCTION = 15
generation = 0
count = 0


@app.route('/get_session', methods=['GET'])
def serve_json():
    data = serving_logic.json_serve_new_session()
    
    return jsonify(data), 200


@app.route('/session_complete', methods=['POST'])
def receive_data():
    data = request.get_json()
    session_id = data["session_id"]
    
    serving_logic.save_session_data(session_id, data)
    global count
    global generation
    count = len([file for file in os.listdir("sessions") if file.endswith('.json')])
    
    print("Saved session to server.")
    
    if count == SESSIONS_UNTIL_REPRODUCTION: # I dont know how many sessions we want before running our stuff but here it goes
        print("Reached threshhold, reproducing:")
        count = 0
        
        if os.path.exists(TRACKING_FILE):
            with open(TRACKING_FILE, 'r') as file:
                tracking_data = json.load(file)
                generation = max(len(data["counts"]) for data in tracking_data.values())

        print("Loading Scores from files..")
        X = load_scores()
        
        print("Populating...")
        X = populate(X)
        update_tracking(X, generation)
        create_population_json(X)

        # Perform analysis
        # print("Starting attribute analysis...")
        # attribute_analysis()

        # print("Starting product analysis...")
        # product_analysis()

        # print("Plotting tracking data...")
        # plot_tracking_data()

        # print("Analysis complete.")
        
        # Update population Files
        
        # Save population to archive
        source_file = "population.json"
        destination_dir = "archive"
        destination_file = "generation" + str(generation) + "_population.json"
        destination_file = os.path.join(destination_dir, os.path.basename(destination_file))
        shutil.copy2(source_file, destination_file)
        
        # Save new_population to population
        source_file = "new_population.json"
        destination_file = "population.json"
        shutil.copy2(source_file, destination_file)
        
        generation += 1
        
        # TESTING STUFF
        files = glob.glob(os.path.join("sessions", '*'))

        # Loop through and delete each file
        for file in files:
            if os.path.isfile(file):  # Only delete files, not directories
                os.remove(file)

    return jsonify({"message": "Session data saved successfully"})

if __name__ == '__main__':
    app.run(debug=True)

