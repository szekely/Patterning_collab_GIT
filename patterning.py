#! /usr/local/bin/python2.5
from psychopy import *
import os
import datetime
import random
import math
import pickle
import numpy


def options(lastTen):
    return [2+(1*lastTen), 5+(1*lastTen)]

#variable for whether trial is odd or even (odd = 1, if not, then = -1)
odd = 1

#--------------------------------------------------GET USER INFO
dlg = gui.Dlg(title="Decision Making Experiment")
dlg.addText('')
dlg.addField('Subject Number:', 99)
dlg.addText('')
dlg.show()
SN = int(dlg.data[0])

if dlg.OK:
    fileOut = 'RL_' + str(SN)
    print fileOut
else:
    print 'user cancelled'
    core.quit()




#--------------------------------------------------INITIALISE STIMULI

# create a window to draw in
#win=visual.Window((1280,1024),fullscr=0,bitsMode=None, units='norm', winType='pyglet', rgb=[1.0,1.0,1.0])
win=visual.Window((1200,850),fullscr=1,bitsMode=None,units='norm',winType='pyglet',color=[1.0,1.0,1.0])


queryPos = (0, .5)
choice1Pos = (-.4, .7)
choice2Pos = (.4, .7)
centerPos = (0,0)

slot1 = visual.PatchStim(win,tex='slot1.png', mask=None,pos=(-.4,0.0),size=(.5,.8),sf=(1.0, 1.0))
slot1g = visual.PatchStim(win,tex='slot1g.png',mask=None,pos=(-.4,0.0),size=(.5,.8),sf=(1.0, 1.0))
slot2 = visual.PatchStim(win,tex='slot2.png',mask=None,pos=(.4,0.0),size=(.5,.8),sf=(1.0, 1.0))
slot2g = visual.PatchStim(win,tex='slot2g.png',mask=None,pos=(.4,0.0),size=(.5,.8),sf=(1.0, 1.0))
heading1 = visual.TextStim(win, text='\n\nSlot Machine 1', alignHoriz='center', color=-1, height=.1, pos=choice1Pos)
heading2 = visual.TextStim(win, text='\n\nSlot Machine 2', alignHoriz='center', color=-1, height=.1, pos=choice2Pos)
outcomemess = visual.TextStim(win, text='\n\n', alignHoriz='center', color=-1, height=.1, pos=centerPos)


#slot1.setColorSpace('gray')
#slot1.setColorSpace('rgb')

# Hide mouse
mouse = event.Mouse(win)
mouse.setVisible(0)

#--------------------------------------------------TASK PARAMETERS


#--------------------------------------------------INITIALISE DATA STRUCTURE
#list = []
expData = []
lastTen = [0,1,0,1,0,1,0,1,0,1]
totalrew = 0

#--------------------------------------------------OUTPUT FILE
f=open(fileOut+'.dlm', 'a')
f.write('\n\nExperiment began at: '+str(datetime.datetime.now()) + '\n\n')
f.flush()


#--------------------------------------------------INSTRUCTIONS
# Wait for a keypress to begin
message = visual.TextStim(win, pos=(0.0,0.0), text='   Hi! Today we would like you to play our computer game and earn some money. The way to make the most money is to get as many points as possible in our game. We will pay you one penny for every point you earn. It may not sound like much, but an expert can make as many as 700 points and can win up to $7.00 in a short time. The rules of the game are easy. On the computer screen in front of you are two boxes/slotmachines. You can choose the left one using the left arrow key or the right one using the right arrow key. Different choices have different outcomes.  After you make your choice, the points you earned will flash on the screen. Your goal is to earn the most points. The first four choices (turns) in the game you are free to select left or right. However, on the next four choices, the screen will change color and you will only be allowed to select the same four that you selected previously.  You do not have to remember what you selected.   If you have any questions about these instructions or how  to use the keyboard to make choices, please ask the experimenter.', height=.05, color=-1., colorSpace='rgb')
message.draw()
win.flip()
response = 0
while not event.getKeys():
    pass
# clear the screen
win.flip(clearBuffer=True)
message = visual.TextStim(win, text='Experimenter, press any key to begin.', alignHoriz='center', color=(-1, -1, -1), height=.1, pos=[0,0])
message.draw()
win.flip()
# wait for a response
event.getKeys()
while not event.getKeys():
    pass
win.flip(clearBuffer=True)
core.wait(2, hogCPUperiod = 2)

#--------------------------------------------------RUN TASK

        #    
#trial task stuff
#dictionary d
d={}
nTrials = 60
for trial in range(nTrials):

    expData.append({})
    expData[trial]['time'] = datetime.datetime.now()


    if trial % 4 == 0 and trial > 0:
        odd = odd*-1

    if odd == 1:
        win.setColor([1, 1, 1.])
#        message = visual.TextStim(win, text='\n\n' + 'ODD', alignHoriz='center', color=-1, height=.1, pos=[0,0])
#        message.draw()
    else:
        win.setColor([.8, .8, .8])
        message = visual.TextStim(win, text= '\n\n' + 'EVEN', alignHoriz='center', color=-1, height=.1, pos=[0,0])
        message.draw()
    # clear the screen
    win.flip(clearBuffer=True)

    ops = options(len(numpy.nonzero(numpy.array(lastTen)>.5)[0]))
 #print trial
#    message = visual.TextStim(win, text= trial, alignHoriz='center', color=-1, height=.1, pos=[0,0])
#    message.draw()
 # Determine if odd or even


        
 # Swap the 2 options for every other subject
    if SN % 2:
        ops  = [ops[1],ops[0]]

    # present the choice
    if odd == 1:
        slot1.draw()
        slot2.draw()
    if odd == -1 and expData[trial-4]['choice'] == SN % 2:
        slot1g.draw()
        slot2.draw()
    elif odd == -1 and expData[trial-4]['choice'] != SN % 2:
        slot2g.draw()
        slot1.draw()
    #heading1.draw()
    #heading2.draw()

    win.flip()
    timer = core.Clock()

# wait for a response
    response = ''
    rt = 0
    loop = 1
    #print 'delay=' + str(expData[trial]['delay'])


    #If ODD/FREE BLOCK THEN
    if odd == 1:
        #win.setRGB([0., 1., 0.])
        # Clear the key buffer
        event.getKeys()
        while loop:
            for key in event.getKeys():
                rt = timer.getTime()
                if key in ['left']:
                    response = key
                elif key in ['right']:
                    response = key
                # Allow user to quit out by pressing the delete key
                elif key in ['delete']:
                    #mouse.setVisible(1)
                    core.quit()
               # d["t{0}".format(trial)]= response
                #print d
            # test to see if we have a response
            loop =  response == ''
    #If EVEN/FORCED BLOCK THEN
    if odd == -1:
        # Clear the key buffer
        event.getKeys()
        while loop:
            for key in event.getKeys():
                rt = timer.getTime()
                print 'trial-4:' , expData[trial-4]
                if key in ['left'] and expData[trial-4]['choice'] != SN % 2:
                #if key in ['left'] and expData[trial-4] == 'left':
                    response = key
                if key in ['right'] and expData[trial-4]['choice'] == SN % 2:
                #elif key in ['right'] and list [trial-4] == 'right':
                    response = key
                # Allow user to quit out by pressing the delete key
                elif key in ['delete']:
                    #mouse.setVisible(1)
                    core.quit()
                #print d
                #print list
            # test to see if we have a response
            loop =  response == ''

    # log response taking into account which side the 2 options were on
    if response == 'left':
        expData[trial]['choice'] = 1
        if SN % 2:
            expData[trial]['choice'] = 0
    if response == 'right':
        expData[trial]['choice'] = 0
        if SN % 2:
            expData[trial]['choice'] = 1
    expData[trial]['rt'] = rt

    timer.reset()
    waittext = ''
    while timer.getTime() < 1.5:
        if response == 'left':
            slot1.draw()
            heading1.draw()
            message.setPos((choice1Pos[0], choice1Pos[1]-1.3))
        if response == 'right':
            slot2.draw()
            heading2.draw()
            message.setPos((choice2Pos[0], choice2Pos[1]-1.3))
        message.setText(waittext)
        message.draw()
        win.flip()
        if waittext == '. . . . .':
            waittext = ''
        else:
            waittext = '. . . . .'
        core.wait(.2, hogCPUperiod = .2)

    # present the outcome
    if response == 'left':
        rew = ops[0]
        expData[trial]['reward'] = rew
        totalrew = totalrew + rew
        expData[trial]['totalrew'] = totalrew
    elif response == 'right':
        rew = ops[1]
        expData[trial]['reward'] = rew
        totalrew = totalrew + rew
        expData[trial]['totalrew'] = totalrew
    #outcomemess = visual.TextStim(win, text='\n\n' + str(rew) + ' tokens', alignHoriz='center', rgb=-1, height=.1, pos=centerPos)
    outcomemess.setText(str(rew) + ' points')
    if response == 'left':
        outcomemess.setPos((choice1Pos[0], choice1Pos[1]-1.3))
    elif response == 'right':
        outcomemess.setPos((choice2Pos[0], choice2Pos[1]-1.3))
    if response == 'left':
        slot1.draw()
        heading1.draw()
    else:
        slot2.draw()
        heading2.draw()
    outcomemess.draw()
    win.flip()

    # log the trial
    mess = 'time:\t'+str(expData[trial]['time']) + '\ttrial:\t' + str(trial) + '\tchoice:\t'+str(expData[trial]['choice']) + '\trt:\t' + str(expData[trial]['rt']) + '\trew:\t' + str(expData[trial]['reward']) + '\tttl:\t' + str(expData[trial]['totalrew']) + '\n'
    f.write(mess)
    f.flush()
    #print(mess)
    #print trial

#    event.getKeys()
#    done = 0
#    while not done:
#        for key in event.getKeys():
#            if key in ['space']:
#                done = 1
#    win.flip(clearBuffer=True)
    core.wait(2, hogCPUperiod = 2)

    # clear the screen
    #message = visual.TextStim(win, text='\n\n' + str(totalrew) + ' points', alignHoriz='center', rgb=-1, height=.1, pos=[0,0])
    #message.draw()
#    win.flip()

    lastTen.pop(0)
    lastTen.append(expData[trial]['choice'])


# clean up the log file
f.close()

# pickle the data
f=open(fileOut+'.pkl', 'wb')
pickle.dump(expData, f)
f.close()


#--------------------------------------------------FINISH UP
message = visual.TextStim(win,pos=(0,0), text='Done!\n\nPlease let the experimenter know you are done.', color=[-1,-1,-1])
message.draw()
win.flip()
core.wait(5, hogCPUperiod = 5)
#message = visual.TextStim(win, text='\n\n' + str(totalrew) + ' points\nPress any key to exit.', alignHoriz='center', rgb=-1, height=.1, pos=[0,0])
#message.draw()
#win.flip()
while 1:
    if event.getKeys():
        break

mouse.setVisible(1)
win.close()
core.quit()