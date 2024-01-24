# Goal 

(1) Reduce computer vision syndrome through behavioral changes and alerting <br /> 
(2) improve good posture while working on the computer

# Functionality
 uses the cameras on your laptop  <br /> 
     -> to detect your posture (ie shoulder ) <br /> 
     -> track eye blinks (ideally around 18 blinks per min is good) <br /> 
     -> tracks time    <br />
         -> every 20 mins take a 20 second eye break  <br />
         -> every 3hrs take a 5 min eye break <br />


# To get started 

### supported on windows only for now

### To run the python code, follow the steps below: 
(0) create a python virtual environment 
    -> if you're using vscode then: <br />
            -> press ctrl+shift+p <br />
            -> click on: Show and run Commands <br />
            -> click on: Python: Create environment... <br />
(0.5) activate the virtual env
    -> if vscode: .\.venv\Scripts\activate
(1) pip install -r requirements.txt <br />
(2) python main.py <br />
(3) A black box will appear on the top left of the screen.  <br />
    -> put up a thumbs up after you set a good posture to start posture checks <br />
(4) enjoy 

### download the .exe file

(1) download the git repo and click main.exe in dist/main folder <br />



# Caveats:

(1) does not support other webcams at this moments, only main camera <br />
(2) not widely tested and in development stage
