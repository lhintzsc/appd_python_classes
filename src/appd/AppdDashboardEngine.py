import yaml
import json


class AppdDashboardEngine:

    def __init__(self,
        templateDir,
        outputDir
    ):

        self._templateName = None
        self.__templateDir = templateDir
        self.__outputDir = outputDir
        self.__configFile  = "mapping.yml"
        self._dashboards = []

    def show(self, p = None):
        if not p:
            return str(vars(self))
        elif hasattr(self, p):
            return (getattr(self,p))
        else:
            return f" >> no attribute '{p}'"

    def setTemplateName(self, templateName):
        self._templateName = templateName

    def loadConfigYml(self):
        ''' 
        Load configuration via yaml file
        '''
        fileDir = self.__templateDir + "/" + self._templateName + "/"+ self.__configFile
        with open(fileDir, "r") as f:
            config = yaml.safe_load(f)
            # ini value from config yaml file
        return config["dashboards"]

    def readTemplateJson(self,templateName):
        fileDir = self.__templateDir + "/" + self._templateName + "/"+ templateName +".json"
        with open(fileDir, "r") as f:
            template = f.read()
        return template

    def replaceTemplateVariable(self, template, key, value):
        template = template.replace("{"+key+"}",value)
        return template

    def getDashboardProperties(self, idx):
        return self.__configData["dashboards"][idx]

    def generateDashboards(self):
        return

    def writeDashboardFile(self, dashboard):
        fileName = self.__outputDir + "/" + dashboard["TITLE"] + ".json"
        with open(fileName, 'w') as f:
            f.write(dashboard["JSON"])
            print("Generated Dashboard File: {}".format(fileName))

    def writeDashboardFiles(self):
        for dashboard in self._dashboards:
            self.writeDashboardFile(dashboard)

    def prettifyJsonDashboards(self):
        dashboards=[]
        for dashboard in self._dashboards:
            print(type(dashboard["JSON"]))
            json_object = json.loads(dashboard["JSON"])
            dashboard["JSON"] = json.dumps(json_object, indent = 3)

class AppdDashboardBuilder(AppdDashboardEngine):

    def __init__(self):

        AppdDashboardEngine.__init__(self,
            templateDir= "./dashboardBuilder/template",
            outputDir="./dashboardBuilder/output"
        )

    def generateDashboards(self, templateName = "RabbitMQ-Basic"):
        
        self.setTemplateName(templateName)
        configData = self.loadConfigYml()
        template = self.readTemplateJson(templateName)
        self._dashboards = []
        for config in configData:
            dashboard = {}
            dashboard["TITLE"] = config["TITLE"]
            dashboard["JSON"] = self.replaceTemplateVariable(template, "TITLE", config["TITLE"])
            for key, value in config["VALUES"].items():
                dashboard["JSON"] = dashboard["JSON"].replace("{"+key+"}",value)
            self._dashboards.append(dashboard)
        return
    

class AppdWidgetBuilderPerRow(AppdDashboardEngine):

    def __init__(self,template=None):
        
        AppdDashboardEngine.__init__(self,
            templateDir= "./widgetBuilderPerRow/template",
            outputDir="./widgetBuilderPerRow/output"
        )

    def generateDashboards(self, templateName = "RabbitMQ-Basic"):
        
        self.setTemplateName(templateName)
        configData = self.loadConfigYml()
        self._dashboards = []
        for config in configData:
            dashboard = {}
            dashboard["TITLE"] = config["TITLE"]
            dashboard["JSON"] = self.generateDasshboard(config)
            self._dashboards.append(dashboard)
        return

    def generateDasshboard(self, config):
        #dashboard = self.readTemplateJson()
        dashboard = self.readTemplateJson(self._templateName)
        rows = self.generateRows(config["ROWS"])
        dashboard = self.replaceTemplateVariable(dashboard, "ROWS", rows)
        dashboard = self.replaceTemplateVariable(dashboard, "TITLE", config["TITLE"])
        for key, value in config["VALUES"].items():
            dashboard = self.replaceTemplateVariable(dashboard, key, value)
        return dashboard

    def generateWidget(self,widgetName,properties):
        print("generate widget:", widgetName)
        widget = self.readTemplateJson(widgetName)
        for key, property in properties.items():
            widget = self.replaceTemplateVariable(widget, str(key), str(property))
        return widget

    def generateRow(self,rowItem):
        row = ""
        for widgetName, properties in rowItem.items():
            widget = self.generateWidget(widgetName, properties)
            if row != "": row=row+","
            row = row+widget
        return row
    
    def generateRows(self,listOfRows):
        rows = ""
        for rowItem in listOfRows:
            row = self.generateRow(rowItem)
            if rows != "": rows=rows+","
            rows = rows + row
        return rows 

if __name__ == "__main__":
    #template = 'RabbitMQ-Basic'
    engine = AppdDashboardBuilder()
    engine.generateDashboards("RabbitMQ-Basic")
    engine.writeDashboardFiles()

    #widgetBuilder = AppdWidgetBuilderPerRow()
    #widgetBuilder.generateDashboards("RabbitMQ-ProcessWidgets")
    #widgetBuilder.generateDashboards("RabbitMQ-ListOfQueues")
    #widgetBuilder.prettifyJsonDashboards()
    #widgetBuilder.writeDashboardFiles()

    