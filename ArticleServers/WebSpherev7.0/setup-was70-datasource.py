
#---------------------------------------------------------------------------------------#
# Global properties                                                                     #
#---------------------------------------------------------------------------------------#

cell = AdminConfig.showAttribute(AdminConfig.list("Cell"), "name")
node = AdminConfig.showAttribute(AdminConfig.list("Node"), "name")
server = AdminConfig.showAttribute(AdminConfig.list("Server"), "name")
scope = "/Cell:" + cell + "/Node:" + node + "/Server:" + server + "/"

dbName = "<CHANGE_THIS>"
jndiName = "jdbc/DataSource"
dbJAASAlias = dbName + "_Alias" 
dbUser = "APP"
dbPassword = "whatever"	

#---------------------------------------------------------------------------------------#
# Procedures                                                                            #
#---------------------------------------------------------------------------------------#
def createDerbyXaJDBCProvider():
	
	if (AdminConfig.getid(scope + "JDBCProvider:Derby Network Server Using Derby Client (XA)/") == "" ):
		print "Creating Derby (XA) JDBC Provider.."
		
		scopeAttr = "Node=" + node + ",Server=" + server
		databaseTypeAttr = "Derby"
		providerTypeAttr = '"Derby Network Server Using Derby Client"'
		implementationTypeAttr = '"XA data source"'
		nameAttr = '"Derby Network Server Using Derby Client (XA)"'
		descriptionAttr = '"Derby Network Server (XA) Provider that uses the Derby Client. This provider is only configurable in version 6.1 and later nodes"'
		classpathAttr = "${DERBY_JDBC_DRIVER_PATH}/derbyclient.jar"
		nativePathAttr = ""
		createAttrs = "[ -scope " + scopeAttr + " -databaseType " + databaseTypeAttr + " -providerType " + providerTypeAttr + " -implementationType " + implementationTypeAttr + " -name " + nameAttr + " -description "  + descriptionAttr + " -classpath " + classpathAttr + " -nativePath " + nativePathAttr + " ]"
		AdminTask.createJDBCProvider(createAttrs)
	else:
		print "Derby (XA) JDBC Provider already exists.."
	#endIf
	
#enddef

def createDerbyJDBCProvider():
	
	if (AdminConfig.getid(scope + "JDBCProvider:Derby Network Server Using Derby Client/") == "" ):
		print "Creating Derby JDBC Provider.."
		
		scopeAttr = "Node=" + node + ",Server=" + server
		databaseTypeAttr = "Derby"
		providerTypeAttr = '"Derby Network Server Using Derby Client"'
		implementationTypeAttr = '"Connection pool data source"'
		nameAttr = '"Derby Network Server Using Derby Client"'
		descriptionAttr = '"Derby Network Server Provider that uses the Derby Client. This provider is only configurable in version 6.1 and later nodes"'
		classpathAttr = "${DERBY_JDBC_DRIVER_PATH}/derbyclient.jar"
		nativePathAttr = ""
		createAttrs = "[ -scope " + scopeAttr + " -databaseType " + databaseTypeAttr + " -providerType " + providerTypeAttr + " -implementationType " + implementationTypeAttr + " -name " + nameAttr + " -description "  + descriptionAttr + " -classpath " + classpathAttr + " -nativePath " + nativePathAttr + " ]"
		AdminTask.createJDBCProvider(createAttrs)
	else:
		print "Derby JDBC Provider already exists.."
	#endIf
	
#enddef

def createDerbyXaDatasource(name, jndiName, dbName):
	
	deleteDataSource(name)
	
	print "Creating Derby (XA) JDBC DataSource: " + name 
	
	jdbcProviderId = AdminConfig.getid(scope + "JDBCProvider:Derby Network Server Using Derby Client (XA)/")
	
   	nameAttr = name
   	jndiNameAttr = jndiName
   	dataStoreHelperClassNameAttr = "com.ibm.websphere.rsadapter.DerbyNetworkServerDataStoreHelper"
   	componentManagedAuthenticationAliasAttr = dbJAASAlias
   	configureResourcePropertiesAttr = "[[databaseName java.lang.String "+ dbName + "]]"
        createAttrs = "[ -name " + nameAttr + " -jndiName " + jndiNameAttr + " -dataStoreHelperClassName " + dataStoreHelperClassNameAttr + " -componentManagedAuthenticationAlias " + componentManagedAuthenticationAliasAttr + " -configureResourceProperties " + configureResourcePropertiesAttr + " ]"
	dataSourceId = AdminTask.createDatasource(jdbcProviderId, createAttrs)
	
	propSet = AdminConfig.showAttribute(dataSourceId, 'propertySet')
	resourcePropsList = wsadminToList(AdminConfig.showAttribute(propSet, 'resourceProperties'))
	for resourceProp in resourcePropsList:
		if ("connectionAttributes" == AdminConfig.showAttribute(resourceProp, "name")):
			AdminConfig.modify(resourceProp, [['value', 'create=false']])
			break
		#endif
	#endfor

#enddef

def createDerbyDatasource(name, jndiName, dbName):
	
	deleteDataSource(name)
	
	print "Creating Derby JDBC DataSource: " + name 
	
	jdbcProviderId = AdminConfig.getid(scope + "JDBCProvider:Derby Network Server Using Derby Client/")
	
   	nameAttr = name
   	jndiNameAttr = jndiName
   	dataStoreHelperClassNameAttr = "com.ibm.websphere.rsadapter.DerbyNetworkServerDataStoreHelper"
   	componentManagedAuthenticationAliasAttr = dbJAASAlias
   	configureResourcePropertiesAttr = "[[databaseName java.lang.String "+ dbName + "]]"
        createAttrs = "[ -name " + nameAttr + " -jndiName " + jndiNameAttr + " -dataStoreHelperClassName " + dataStoreHelperClassNameAttr + " -componentManagedAuthenticationAlias " + componentManagedAuthenticationAliasAttr + " -configureResourceProperties " + configureResourcePropertiesAttr + " ]"
	dataSourceId = AdminTask.createDatasource(jdbcProviderId, createAttrs)
	
	propSet = AdminConfig.showAttribute(dataSourceId, 'propertySet')
	name = ['name', 'nonTransactionalDataSource']
	customProps = [name]
	AdminConfig.create('J2EEResourceProperty', propSet, customProps)
	resourcePropsList = wsadminToList(AdminConfig.showAttribute(propSet, 'resourceProperties'))
	for resourceProp in resourcePropsList:
		if ("nonTransactionalDataSource" == AdminConfig.showAttribute(resourceProp, "name")):
			AdminConfig.modify(resourceProp, [['value', 'true'], ['description', 'nonTransactional flag']])
		if ("connectionAttributes" == AdminConfig.showAttribute(resourceProp, "name")):
			AdminConfig.modify(resourceProp, [['value', 'create=true']])
		#endif
	#endfor
	

#enddef

def deleteDataSource(name):
	scopeId = AdminConfig.getid(scope)
        resourceList = wsadminToList(AdminConfig.list("DataSource" , scopeId))
        for resource in resourceList:
        	resourceName = AdminConfig.showAttribute(resource, "name" )
        	if (name == resourceName):
        		print "Deleting DataSource: " + name
        		AdminConfig.remove(resource)
        	#endIf 
        #endFor 
#endDef

def createJAASAuthData(alias, userId, password, description):
	global AdminConfig

	deleteJAASAuthData(alias)
	
	print "Creating JAASAuthData: " + alias

        secId = AdminConfig.getid("/Security:/" )
        aliasAttrib = ["alias", alias ]
        userIdAttrib = ["userId", userId ]
        passwordAttrib = ["password", password ]
        descriptionAttrib = ["description", description ]
        createAttrs = [aliasAttrib, userIdAttrib, passwordAttrib, descriptionAttrib]
        AdminConfig.create("JAASAuthData", secId, createAttrs)
#endDef 

def deleteJAASAuthData(alias):
        global AdminConfig

        resourceList = wsadminToList(AdminConfig.list('JAASAuthData' ))
        for resource in resourceList:
                resourceName = AdminConfig.showAttribute(resource, "alias" )
                if (alias == resourceName):
                        print "Deleting JAASAuthData: " + alias
                        AdminConfig.remove(resource )
                        break 
                #endIf 
        #endFor 

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

def save():
        global AdminConfig
        AdminConfig.save()
        print "Changes Saved.."
#endDef 

#---------------------------------------------------------------------------------------#
# Main                                                                                  #
#---------------------------------------------------------------------------------------#
createDerbyXaJDBCProvider()
createDerbyJDBCProvider()
createJAASAuthData( dbJAASAlias, dbUser, dbPassword, dbName + " user" )
createDerbyXaDatasource(dbName, jndiName, dbName)
createDerbyDatasource(dbName + "_NoTx", jndiName + "_NoTx", dbName)
save()
