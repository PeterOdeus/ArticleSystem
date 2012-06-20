import java.io as io
import java.lang as lang
#---------------------------------------------------------------------------------------#
# Global properties                                                                     #
#---------------------------------------------------------------------------------------#

cell = AdminConfig.showAttribute(AdminConfig.list("Cell"), "name")
node = AdminConfig.showAttribute(AdminConfig.list("Node"), "name")
server = AdminConfig.showAttribute(AdminConfig.list("Server"), "name")
scope = "/Cell:" + cell + "/Node:" + node + "/Server:" + server + "/"

was_home_ext_openjpa = "${WAS_LIBS_DIR}/openjpa"
was_home_ext_jpasupport = "${WAS_LIBS_DIR}/jvs-jpasupport"
openJPAClasspath = ""

was_home = lang.System.getProperty("was.install.root")
openjpa_home = io.File(was_home + "/lib/openjpa")
jpasupport_home = io.File(was_home + "/lib/jvs-jpasupport")
openjpa_listDirs = openjpa_home.list();
jpasupport_listDirs = jpasupport_home.list();

for x in range(0, len(openjpa_listDirs), 1):
	if openjpa_listDirs[x].endswith(".jar"):
		print "Adding dependency: " + openjpa_listDirs[x]
		openJPAClasspath += was_home_ext_openjpa + "/" + openjpa_listDirs[x] + ";"
for x in range(0, len(jpasupport_listDirs), 1):
	if jpasupport_listDirs[x].endswith(".jar"):
		print "Adding dependency: " + jpasupport_listDirs[x]
		openJPAClasspath += was_home_ext_jpasupport + "/" + jpasupport_listDirs[x] + ";"

openJPAgenericJVMArgument = "-Xquickstart -javaagent:" + was_home_ext_openjpa + "/openjpa-1.2.2.jar"

#---------------------------------------------------------------------------------------#
# Procedures                                                                            #
#---------------------------------------------------------------------------------------#

def save():
        global AdminConfig
        AdminConfig.save()
        print "Changes Saved.."
#endDef 

def setClasspath( classpath ):
	global AdminTask
	ATTRIB_CLASSPATH = "[-serverName " + server + " -classpath " + classpath + "]"
	AdminTask.setJVMProperties(ATTRIB_CLASSPATH)
	print "Added classpath for OpenJPA.."
#endDef


def setGenericJVMarguments ( genericJVMArgument ):
	global AdminTask, AdminConfig, scope
# 	This should work but there seems to be a bug in WAS 6.1, no parameter starting with "-" can be added...
#	ATTRIB_GENERIC_JVM_PARAMETERS = "[-serverName " + server + " -nodeName " + node + " -genericJvmArguments  " + genericJVMArgument + "]"
#	AdminTask.setGenericJVMArguments(ATTRIB_GENERIC_JVM_PARAMETERS)

#	A bit unintuitive but working workaround to get the same result
	scope_id = AdminConfig.getid(scope)
	jvm = AdminConfig.list('JavaVirtualMachine', scope_id)
	AdminConfig.modify(jvm, [['genericJvmArguments', openJPAgenericJVMArgument]])
	print "Added generic JVM arguments for OpenJPA.."
#endDef


#---------------------------------------------------------------------------------------#
# Main                                                                                  #
#---------------------------------------------------------------------------------------#

setClasspath(openJPAClasspath)
setGenericJVMarguments(openJPAgenericJVMArgument)
save()