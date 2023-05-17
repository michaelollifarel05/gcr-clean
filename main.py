import subprocess as sp
import os
import sys
from datetime import datetime
from time import sleep

ImageMaxLimit= int(sys.argv[1])


print("\n\n\n!!WARNING!!\n\n\nThe maximum number of images on each Registry will be set to a maximum of "+str(ImageMaxLimit)+" images")
print("This program will be executed in 5 seconds")
sleep(5)
print("program running")


for registry in sp.getoutput('gcloud container images list --repository=gcr.io/project-wkwk ').splitlines() :
    if registry == "NAME":
        continue
    CountCommand = 'gcloud container images list-tags '+registry+' | wc -l'
    TotalImage = sp.getoutput(CountCommand) 
    ImageTotalInteger = int(TotalImage) - 1
    ImageTotalString = str(ImageTotalInteger)
    if ImageTotalInteger > ImageMaxLimit :
        Limit = ImageTotalInteger - ImageMaxLimit 
        LimitString = str(Limit)
        Out = registry +' have '+ImageTotalString+" images | and excess "+LimitString+" images"
        print(Out)
        ImageTagsToDeleteList = sp.getoutput("gcloud container images list-tags "+registry+" --format='get(digest)' --sort-by='TIMESTAMP' --limit="+LimitString).splitlines()
        
        f = open("gcr_clean_logs.log", "a")
        f.write("--------------------------- registry : " +registry+" ----------------------------\n")
        f.write("Total Image:" + ImageTotalString + "  and will be delete " + LimitString + " images \n" )
        f.close()
        
        print("working on " + registry)

        for ImagesTags in ImageTagsToDeleteList:
            DeleteCommand = "gcloud container images delete "+registry+"@"+ImagesTags+" --force-delete-tags --quiet"
            print(DeleteCommand)
            print(ImagesTags+" deleted")
            f = open("gcr_clean_logs.log", "a")
            f.write(datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')+"\n"+sp.getoutput(DeleteCommand)+"\n")
            f.close()
    else:
        Out = registry+' have '+ImageTotalString+' images'
        print(Out)

print("everything is done, have a great days")
