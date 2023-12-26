ip_address = 'localhost' # Enter your IP Address here
project_identifier = 'P2B' # Enter the project identifier i.e. P2A or P2B
#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.simulation_project_library import *

hardware = False
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
arm = qarm(project_identifier,ip_address,QLabs,hardware)
potentiometer = potentiometer_interface()

#--------------------------------------------------------------------------------
# CODE BEGINS
#---------------------------------------------------------------------------------

def pick_up():

    #arm move to pick up position to grasp the containers
    arm.move_arm(0.57, 0.05, 0.044)
    time.sleep(2)
    arm.control_gripper(45)
    time.sleep(2)
    #arm returns to home position with container
    arm.move_arm(0.406,0.0,0.483)
    time.sleep(2)



def rotate_base(Container_ID):

    

   
    # track value of right potentiometer
    old_value = potentiometer.right()

    # Loop to check value of right potentiometer
    while True:

        # Rotate base only when box is not being dropped off
        if potentiometer.left() <= 0.5:
            new_value = potentiometer.right()
            rotate_ratio = new_value - old_value
            # right potentiometer value is turned into degrees
            rotate_angle = rotate_ratio*350
            arm.rotate_base(rotate_angle)
            old_value = new_value

            # check if container and corresponding autoclave are the same colour utilizing container ID

            
            if (arm.check_autoclave('green') == True) and ((Container_ID == 2 or Container_ID == 5) == True):
                break


          

            if (arm.check_autoclave('red') == True) and ((Container_ID == 1 or Container_ID == 4) == True):
                break

         

            if (arm.check_autoclave('blue')==True) and ((Container_ID == 3 or Container_ID == 6) == True):
                break

        time.sleep(2)
        
                

        
def drop_off():




# allows for left potentiometer value to be changed multiple times
    while True:

        time.sleep(4)
        # For small containers; place on top of autoclave
        if potentiometer.left() > 0.5 and potentiometer.left() < 1.0:
                arm.rotate_shoulder(20)
                time.sleep(2)
                arm.rotate_elbow(-20)
                time.sleep(2)
                arm.rotate_shoulder(15)
                time.sleep(2)
                arm.control_gripper(-45)
                time.sleep(2)
                arm.home()
                break
    

        # For large containers; place in autoclave
        elif potentiometer.left() == 1.0:

                arm.activate_autoclaves()
                time.sleep(2)

                # open corresponding autoclave
                arm.open_autoclave('red',arm.check_autoclave('red'))
                arm.open_autoclave('blue',arm.check_autoclave('blue'))
                arm.open_autoclave('green',arm.check_autoclave('green'))

                # drop off container and return home
                time.sleep(2)
                arm.rotate_shoulder(15)
                time.sleep(2)
                arm.rotate_elbow(27)
                time.sleep(2)
                arm.control_gripper(-45)
                time.sleep(2)
                arm.home()
                time.sleep(2)

                #close autoclaves
                arm.open_autoclave('red',False)
                arm.open_autoclave('green',False)
                arm.open_autoclave('blue',False)
                arm.deactivate_autoclaves()
                time.sleep(2)
                break





def terminate():
    # List of all unique container ID's
    Container_ID_List = [1,2,3,4,5,6]

    # Loop until six containers are dropped off
    while len(Container_ID_List) > 0:
        time.sleep(2)
        # Picks a random container ID
        Container_ID = random.choice(Container_ID_List)
        arm.spawn_cage(Container_ID)
        # Deletes Container ID from list
        Container_ID_List.remove(Container_ID)
        time.sleep(2)
        pick_up()
        time.sleep(2)
        # roatate to corresponding container
        rotate_base(Container_ID)
        time.sleep(2)
        # drop off corresponding container
        drop_off()
        time.sleep(3)4



#---------------------------------------------------------------------------------
# CODE ENDS
#---------------------------------------------------------------------------------
