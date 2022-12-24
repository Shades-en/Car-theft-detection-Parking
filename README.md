#Automated Way of Vehicle Theft Detection in Parking Facilities
Security of parked cars against theft is a long existing concern. We present an automated way of detecting vehicle theft as it happens using moving object detection and barcode scanning for each parking entry. The detected edges of the output should give a clear image of the moving object from the video. The security personnel or the parking lot operator gets notified about the movement.

Installation
The above project has been made with python version==3.11

Clone the repo

  https://github.com/Shades-en/Car-theft-detection-Parking.git
  cd Car-theft-detection-Parking
Create a virtual environment

    py -m venv <environment name>
Install Requirements

    pip install requirements.txt
Usage/Examples
Run the file get_first_frame.py to generate the first frame.

    py get_first_frame.py
Run the file ParkingSpacePick.py to select the parking spaces by right clicking on image (unselect by right clicking the space)

    py ParkingSpacePick.py
Run the file parkSpace2.py

    py parkSpace2.py
scan the required barcode(through webcam window) to allow/disallow vehicles with approriate parking space ID

Key Libraries
Open CV Pyzbar

Contributing
Jeevika Kiran
Maitri P Tadas
Prapti Bopana
