# hackday-2017-autonomous-car
Protacon Hackday 2017 project to develop autonomously driving RC car. Car uses Raspberry Pi with camera to detect surroundings and machine learning to combine picture with correct steering instructions
## Support for PS4 bluetooth controller
PS4 controller is used to control the vehicle via bluetooth while teaching the AI.
<br>Install dependencies: 
* pip install ds4drv 
* pip install pygame

ds4drv should be started on system boot so the controller can be connected. controller_listener.py listens to the controller inputs.
