
#---------------------------------------------------------------------------------------#
# Global properties                                                                     #
#---------------------------------------------------------------------------------------#

cell = AdminConfig.showAttribute(AdminConfig.list("Cell"), "name")
node = AdminConfig.showAttribute(AdminConfig.list("Node"), "name")
server = AdminConfig.showAttribute(AdminConfig.list("Server"), "name")
scope = "/Cell:" + cell + "/Node:" + node + "/Server:" + server + "/"

serviceIntegrationBus = "JvsSIBus"
connectionFactory = "ConnectionFactory" 
destinationQueueName = "SampleDestinationQueue"
queue = "SampleQueue"


#---------------------------------------------------------------------------------------#
# Procedures                                                                            #
#---------------------------------------------------------------------------------------#

def createServiceIntegrationBus():
	if (AdminConfig.getid("/SIBus:"+serviceIntegrationBus) == "" ):
		print "Creating SIB: " + serviceIntegrationBus
		description = '"POS Integration Bus"'
		security = "FALSE"	
		createAttrs = " -bus " + serviceIntegrationBus + " -description " + description + " -busSecurity " + security
		AdminTask.createSIBus(createAttrs)
	else:
		print "Service Integration Bus: " + serviceIntegrationBus + ", allready exists..."
#		AdminTask.deleteSIBus(" -bus " + serviceIntegrationBus)
	#endif		
#enddef


def addSIBusMembers():
	print "Adding members to SIB..."
	print "Found SIB: " + AdminConfig.getid(scope)

	print "Member: " + AdminTask.showSIBusMember("-bus " + serviceIntegrationBus + " -node " + node + " -server " + server)

	if (AdminTask.showSIBusMember("-bus " + serviceIntegrationBus + " -node " + node + " -server " + server) == "" ):	
		removeAttrs =  " -bus " + serviceIntegrationBus + " -node " + node + " -server " + server
		AdminTask.removeSIBusMember(removeAttrs)
		createAttrs = removeAttrs + " -fileStore"
		AdminTask.addSIBusMember(createAttrs)	
	else:
		print "Bus member already exists..."
	#endif	
#enddef

def save():
        global AdminConfig
        AdminConfig.save()
        print "Changes Saved.."
#endDef 


def wsadminToList(inStr):
        outList=[]
        if (len(inStr)>0 and inStr[0]=='[' and inStr[-1]==']'):
                tmpList = inStr[1:-1].split() #splits space-separated lists,
        else:
                tmpList = inStr.split("\n")   #splits for Windows or Linux
        for item in tmpList:
                item = item.rstrip();         #removes any Windows "\r"
                if (len(item)>0):
                        outList.append(item)
        return outList
#endDef

def scopeToAttrib(lscope):
	lscopeList = lscope[1:-1].split('/')
	
	if(len(lscopeList) == 2):
		return " -cluster " + lscopeList[1].split(':')[1]
	elif(len(lscopeList) == 3):
		return " -node " + lscopeList[1].split(':')[1] + " -server " + lscopeList[2].split(':')[1]
	#endIf
#endDef


def createSIBus ( name, datasourceJndiName ):
        global AdminTask, AdminConfig, scope
	sibusList = wsadminToList(AdminConfig.list('SIBus'))
	
	for sibus in sibusList:
		if ( name == AdminConfig.showAttribute(sibus, "name") ):
			print "Existing SIBus: " + name
        		return
        	#endIf	
	#endFor
	
        ATTRIB_BUS = "[-bus " + name + "]"
        ATTRIB_BUS_MEMBER = "[-bus " + name + scopeToAttrib(scope)
        if(datasourceJndiName != ""):
       	    ATTRIB_BUS_MEMBER = ATTRIB_BUS_MEMBER + " -datasourceJndiName " + datasourceJndiName
        #endIf
        ATTRIB_BUS_MEMBER = ATTRIB_BUS_MEMBER  + "]"
        
	print "Creating SIBus: " + name
	
        sib = AdminTask.createSIBus(ATTRIB_BUS)
        AdminTask.addSIBusMember(ATTRIB_BUS_MEMBER)
        
        return sib
#endDef 

def deleteSIBus ( name ):
        global AdminTask

        ATTRIB_BUS = "[ -bus " + name + "]"
        print "Deleting SIBus: " + name
        AdminTask.deleteSIBus(ATTRIB_BUS )
#endDef 

def createSIBDestinationQueue ( destName, busName ):
        global AdminTask, scope
        
        deleteSIBDestination(destName)
        
	print "Creating SIBDestination Queue: " + destName + " on bus: " + busName
	
        ATTRIB_DEST = "[-bus " + busName + " -type Queue -name " + destName + scopeToAttrib(scope) + "]"

        return AdminTask.createSIBDestination(ATTRIB_DEST)
#endDef 


def deleteSIBDestination ( name ):
        global AdminConfig

        destList = wsadminToList(AdminConfig.list("SIBDestination"))
        for dest in destList:
                destName = AdminConfig.showAttribute(dest, "identifier" )
                if (name == destName):
                        print "Deleting SIBDestination: "+ name
                        AdminConfig.remove(dest )
                        break 
                #endIf 
        #endFor 
        
#endDef 




def createJMSConnFactory ( name, jndiName, busName ):
        global AdminConfig, AdminTask, scope

	deleteSIBJNDIConnFactory(name)

	print "Creating JMSConnectionFactory: " + name + " to bus: " + busName

        server_id = AdminConfig.getid(scope )
	
        ATTRIB_CONN = "[-name " + name + " -jndiName " + jndiName + " -busName " + busName + "]"
        return AdminTask.createSIBJMSConnectionFactory(server_id, ATTRIB_CONN )
#endDef 


def deleteSIBJNDIConnFactory ( name ):
        deleteResource('J2CConnectionFactory', name)
#endDef 


def deleteResource ( clazz, name ):
        global AdminConfig

	scope_id = AdminConfig.getid(scope)
	
        resourceList = wsadminToList(AdminConfig.list(clazz, scope_id))
        for resource in resourceList:
            resourceName = AdminConfig.showAttribute(resource, "name" )
            if (name == resourceName):
                print "Deleting " + clazz + ": " + name
                AdminConfig.remove(resource )

            #endIf 
        #endFor 
#endDef 



def createSIBJNDIQueue ( name, jndiName, destName, busName ):
        global AdminConfig, AdminTask, scope, WAS_ENV

	deleteSIBJNDIQueue(name)
	
	print "Creating SIBJMSQueue: " + name + " on bus: " + busName
	
        server_id = AdminConfig.getid(scope )

        ATTRIB_DEST_JNDI = "[-name " + name + " -jndiName " + jndiName + " -queueName " + destName + " -busName " + busName + "]"
        return AdminTask.createSIBJMSQueue(server_id, ATTRIB_DEST_JNDI )

#endDef 

def deleteSIBJNDIQueue ( name ):
	deleteResource('J2CAdminObject', name)
#endDef 


#---------------------------------------------------------------------------------------#
# Main                                                                                  #
#---------------------------------------------------------------------------------------#


createSIBus( serviceIntegrationBus, "" )
createJMSConnFactory( connectionFactory, "jms/"+connectionFactory, serviceIntegrationBus )
createSIBDestinationQueue( destinationQueueName, serviceIntegrationBus )
createSIBJNDIQueue( queue, "jms/"+queue, destinationQueueName, serviceIntegrationBus )
save()