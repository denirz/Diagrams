"""
Архитектура ПРОМ Инсталляции АС 17

Данный код представляет собой диаграмму архитектуры системы, используя библиотеку diagrams.
В коде создаются различные компоненты системы, такие как EC2, RDS, ELB, Firewall и другие, и устанавливаются связи между ними.
Также в коде используются кластеры для группировки компонентов системы.
 В результате получается наглядная диаграмма, которая помогает понять структуру и взаимодействие компонентов системы.

Docs are
https://diagrams.mingrammer.com/docs/guides/cluster
https://graphviz.org/docs/clusters/
https://graphviz.org/docs/attrs/decorate/
"""
from diagrams import Diagram,Cluster,Edge,Node
#AC Hosts
from diagrams.aws.compute import EC2
from diagrams.aws.compute import EC2Instance # Other AC hosts
from diagrams.aws.database import DocumentdbMongodbCompatibility as VectorStore
from diagrams.oci.compute import BMWhite
from diagrams.programming.language import Python
# from diagrams.aws.network import NetworkFirewall as SOWA
from diagrams.aws.network import APIGateway as SOWA
#GigaChat:
# from diagrams.saas.chat import RocketChat
from diagrams.aws.ml import AugmentedAi as Giga
from diagrams.programming.flowchart import Preparation
from diagrams.onprem.client import User
from diagrams.saas.analytics import Snowflake #CodeChat
# from diagrams.onprem.groupware import Nextcloud as Confluence
from diagrams.alibabacloud.compute import FunctionCompute as Confluence



from diagrams.generic.network import Firewall
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
#https://www.graphviz.org/doc/info/attrs.html
graph_attr = {
    "labelloc":"t",
    "fontsize": "24",
    # "bgcolor": "transparent"
    "bgcolor": "white",
    "size": "200.",
    "dpi": "400",
    "ratio": "1:3",
}
# https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$29740274
network = """
Net: 10.44.18.0/28
Range: 10.44.18.2 - 10.44.18.14
Name: main_VDC18
"""
with Diagram("Архитектура АС 17.1", show=False,direction="LR",graph_attr=graph_attr,filename="Architecture_AS17-1") as diag:
    with Cluster("SBERTECH_AD",direction="LR"):
        with Cluster(f"VDC18 \n{network}",direction="LR"):
            #Done DNS Имя https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31088497:serviceCall$request
            # пока временное решение  - потом поменяем с  тестом местами
            api = Python("testfaq.infra.sbt\n vsp-ac17.1-app \n 10.44.18.8",ip="10.44.18.8")
            # заказать DNS имя
            # to order domain name vdb.ac17-1.common.sbt https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31230654:serviceCall$request
            vdb = VectorStore("vsp-ac17.1-db-chroma \n   10.44.18.12\n vdb.ac17-1.common.sbt")
            # заказать DNS имя
            # to order domain name sowa.ac17-1.common.sbt https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31230655:serviceCall$request
            #  Done     https://itsm.infra.sbt/sd/operator/#uuid:task$31037856:task$task - задача на установку SOWA
            sowa = SOWA("SOWA: \n vsp-ac17.1-sowa  \n  10.44.18.4\n sowa.ac17-1.common.sbt", fill="lightblue",stroke="red",labeltooltip ="Для безопасности")


        with Cluster("VDC05/ ",direction="LR",):
            # dev AC17.1
            with Cluster("TEST AC17.1",graph_attr={"bgcolor":"#ECE8F6"}):
                # FAQ.infra.sbt
                apidev = Python("vsp-ac17-db-chroma\n 10.44.5.21")
                sowadev = SOWA("vsp-ac17-sow   \n  10.44.5.22", labeltooltip="Для безопасности")
                apidev >> Edge(label="Вызовы API для функций", headlabel="https:8443 ", decorate="true",
                               style="diagonals", color="black") >> sowadev
            # пром АС17
            as17 = EC2(label="АC17\n 10.44.5.2")
            apidev >>Edge(headlabel="https://cmdb.infra.sbt/ ", decorate="true",
                               style="dashed", color="yellow") >> as17

    with Cluster("In",direction="LR",graph_attr={"bgcolor":"#ECE8F6"}):

        with Cluster("Other AS",direction="LR",graph_attr={"bgcolor":"#EAFF59"}):
            monitoring = EC2Instance("AC 12.2 / Monitoring")
            dlp  = EC2Instance("DC 33/ DLP \n 10.50.13.11")
            avpo  = EC2Instance("AC 34/ AVPO") #https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31150971:serviceCall$request
            pam  = EC2Instance(" AC 32 / PAM \n 10.50.13.35\n 10.50.13.36")
            SOCSIEM  =  EC2Instance("AC 38/ SOC/SIEM\n TBD ")
            ConfluenceDZO = Confluence("Вн 05/ Confluence \n https://sberworks.ru/wiki:443")
            # monitoring >>SOCSIEM >> dlp>> pam
        with Cluster("External Interfaces"):
            #GigaChat Node :
            gigachat = Giga("Gigachat")
            #GigaCode Node:
            gigacode = Giga("GigaCode")

    with Cluster("SBERTECH_OD_PROM ", direction="LR"):
        with Cluster("VDC11", direction="LR"):
            eva = EC2Instance("EVA \n 10.45.51.37 predprom")

    user = User("User")

#todo await  Основная интеграция с ITSM  https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31088491:serviceCall$request
    api >> Edge(label="CC-14: Вызовы API для функций\n https://cmdb.infra.sbt/sd/services/rest/"
                      "" ,headlabel  = "https:443 ",decorate ="true",style="diagonals",color="red")>> as17
    vdb >> Edge(label="CC-14: Индексация",style="bold",decorate ="true",color="red",headlabel  = "https:cmdb.infra.sbt:443")>> as17


    api >> Edge(label="Выбор контекстных \nдокументов ",
                headlabel="https:5000",
                taillabel="Query",
                color="green",style="bold",
                decorate ="true",)>> vdb

    api >> Edge(label="http Запросы в\n GigaChat/GigaCode",
               headlabel="TCP/9443",
               color="green",style="bold",decorate ="true") >> sowa


    vdb >> Edge(label="Индексация документов Confluence",style="normal",decorate ="true",color="red",headlabel  = "httops://sberworks.ru/wiki:443") >> ConfluenceDZO

    api >> Edge(label="Индексация документов Confluence",style="normal",decorate ="true",color="red",headlabel  = "httops://sberworks.ru/wiki:443") >> ConfluenceDZO


    # Await заказать доступ к GigaChat/GigaCode
    # https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31230658:serviceCall$request
    sowa >> Edge(label="Доступ до Gigachat: AUTH + API",
                 headlabel = "HTTPS:\nngw.devices.sberbank.ru:9443\ngigachat.devices.sberbank.ru:443\n",
                 color="red",style="bold",decorate ="true") >> gigachat
    sowa >> Edge(label="Доступ до GigaCode",
                 headlabel = "HTTPS:\ngigacode.ru:443",
                 color="red",style="bold",decorate ="true") >> gigacode



    user >> Edge(label="http  API",
         headlabel="https:/8000",
         color="blue",
         style="dashed", decorate="true", description = "Доступ пользователей в отладочных целях")>>api

    sowa >>Edge(label="ICAP DLP Check",
         headlabel="https://10.50.13.11:1345/icap/full",
         color="black",
         # style="dashed",
                decorate="true", )>> dlp #https://10.50.13.11:1345/icap/full


    monitoring >>Edge(
         headlabel="TCP:10050",
         color="green",
         style="dashed", decorate="true", )>> api
    monitoring>>Edge(
         headlabel="TCP:10050",
         color="green",
         style="dashed", decorate="true", )>>sowa
    monitoring >>Edge(
         headlabel="TCP:10050",
         color="green",
         style="dashed", decorate="true", )>>vdb

##todo await for   в теории работает - вот заявкка на проверку:  https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31150971:serviceCall$request
    api << Edge(
        color="black",
        style="dashed", decorate="true", ) << avpo
    vdb << Edge(
        # taillabel="SSH:22",
        color="black",
        style="dashed", decorate="true", ) << avpo
    sowa << Edge(
        # taillabel="SSH:22",
        color="black",
        style="dashed", decorate="true", ) << avpo

# PAM  done: реализовано https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31038302 :
    api <<  Edge(
         taillabel="SSH:22",
         color="black",
         style="dashed", decorate="true", )<<pam
    vdb << Edge(
        taillabel="SSH:22",
        color="black",
        style="dashed", decorate="true", ) << pam
    sowa << Edge(
        taillabel="SSH:22",
        color="black",
        style="dashed", decorate="true", ) << pam


# SOCSIEM  установить EDR
#done: https://itsm.infra.sbt/sd/operator/#uuid:serviceCall$31150977:serviceCall$extendedSup
    SOCSIEM <<Edge(
         taillabel="soc-edr-app.sbertech.local:9991 \nsoc-edr-app.sbertech.local:9992",
         color="blue",
         style="dashed", decorate="true",)<< api
    SOCSIEM << Edge(
        taillabel="soc-edr-app.sbertech.local:9991\n soc-edr-app.sbertech.local:9992",
        color="blue",
        style="dashed", decorate="true", )<< vdb
    SOCSIEM << Edge(
        taillabel="soc-edr-app.sbertech.local:9991 \nsoc-edr-app.sbertech.local:9992",
        color="blue",
        style="dashed", decorate="true", )<<sowa
    # user>>api>>sowa>>pam>>sowa>>gigachat



    eva >>Edge(
        headlabel="http:8000",
        color="blue",
        style="dashed", decorate="true", ) >> api
    sowadev >>gigachat
    sowadev >>gigacode

