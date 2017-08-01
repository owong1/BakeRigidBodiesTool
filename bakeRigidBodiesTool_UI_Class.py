import maya.cmds as mc

def selectActive(*args):
    #select type all rigid body nodes
    rigid = mc.ls(type = "rigidBody")
    active = []
    #make list for active rigid body nodes
    for body in rigid:
        if mc.rigidBody(body, query = True, active = True) == 'true':
            active.append(body)      
    #make list for parents of active rigid nodes (transform nodes)
    activeParent = mc.listRelatives(active, p = True)
    #select all parent nodes (transform nodes)
    mc.select(activeParent)
    
#bake simulation for time slider
def bakeTimeSlider(*args):
    timeStart = mc.playbackOptions(query = True, minTime = True)
    timeEnd = mc.playbackOptions(query = True, maxTime = True)
    
    mc.bakeResults( time = (timeStart, timeEnd), simulation = True)

#def bakeStartEnd():
def bakeStartEnd(*args):
    startFrame = mc.intField(bakeToolWindow.startFrameControl, query = True, value = True)
    endFrame = mc.intField(bakeToolWindow.endFrameControl, query = True, value = True)
    
    mc.bakeResults( time = (startFrame, endFrame), simulation = True)


#delete all by type: rigid bodies
def deleteRigids(*args):
    rigid = mc.ls(type = "rigidBody")
    mc.select(rigid)
    mc.DeleteRigidBodies()
    
#full baking execution
def fullBake(*args):
    selectActive()
    bakeTimeSlider()
    deleteRigids()
    
#select all rigid bodies within selected group
def selectInGroup(*args):    
    rigidGrouped = []
    grouped = mc.listRelatives(c = True)
    mc.select(grouped)
    for obj in grouped:
        children = mc.listRelatives(c = True)
        print children
        for node in children:
            if mc.objectType(node) == "rigidBody":
                rigidGrouped.append(node)
             
    mc.select(rigidGrouped)

class helpMenuUI(object):
    def __init__(self, title):
        
        winID = title
    
        if mc.window(winID, exists = True):
            mc.deleteUI(winID)

        wind = mc.window(winID, wh = (512, 512))

        mc.columnLayout(adjustableColumn = True)

        mc.menuBarLayout()

        mc.menu(label = "Help", helpMenu = True)
        mc.menuItem(label = "About", command = "aboutWindow()")
        

    def aboutWindow():
        #shows about information
        """
        aboutWindow constructs about information window
        """
        aboutWin = mc.window(title = "About", wh = (256, 256), mnb = 0, mxb = 0, s = 0)
        aboutColumn = mc.columnLayout(adjustableColumn = 1, p = aboutWin)
        mc.separator(h = 25, style = "none")
        mc.text(label = "Bake Rigid Bodies Tool V 2.0", al = "center")
        mc.text(label = "by Olivia Wong", al = "center")
        mc.text(label = "oliviaw.2580@gmail.com", al = "center")
        mc.separator(h = 20, style = "none")
        mc.text(label = "For SWE449, Tools Programming", al = "center")
        mc.text(label = "Mira Nikolic", al = "center")
        mc.separator(h = 10, style = "none")
        mc.showWindow(aboutWin)
        
    def createWindow(*args):
        mc.showWindow()
        

def bakeToolLayout():
    #frame 0 = outer
    frame0 = mc.frameLayout(labelVisible = False, borderVisible = True, marginWidth = 3, marginHeight = 3)
    
    #frame 1 = full execution, default baking
    frame1 = mc.frameLayout(label = "Bake Simulation Full Execution", width = 512, marginWidth = 3, marginHeight = 3)
    mc.button(label = "Bake Simulation", command = "fullBake()")
    mc.setParent("..")
    
    #frame 2 = more options
    frame2 = mc.frameLayout(label = "More Options", width = 512)
    
    #frame 2a for baking
    frame2a = mc.frameLayout(label = "Baking", width = 512, marginWidth = 3, marginHeight = 3, collapsable = True)
    row = mc.rowLayout(numberOfColumns = 4, columnAlign1 = "right")
    mc.text("Time Range:")
    bakeToolWindow.startFrameControl = mc.intField()
    bakeToolWindow.endFrameControl = mc.intField()

    mc.button(label = "Bake Simulation for Time Range", command = "bakeStartEnd()")
    
    mc.setParent("..")
    mc.button(label = "Bake Simulation for Time Slider", command = "bakeTimeSlider()")
    mc.button(label = "Delete all Rigid Bodies", command = "deleteRigids()")
    mc.setParent("..")
    
    #frame 2b for selection
    frame2b = mc.frameLayout(label = "Selection", width = 512, marginWidth = 3, marginHeight = 3, collapsable = True)
    mc.button(label = "Select Active Rigid Body Objects at Current Frame", command = "selectActive()")
    mc.button(label = "Select All Rigid Bodies in Selected Group", command = "selectInGroup()")
    mc.setParent("..")
    mc.setParent("..")
    
    mc.setParent("..")

toolWindow = helpMenuUI(title = "Bake Rigid Bodies Tool")
bakeToolLayout()
toolWindow.createWindow()
