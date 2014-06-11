columns = ["LFG1","LFG10","LFG11","LFG12","LFG13","LFG14","LFG15","LFG16","LFG17","LFG18","LFG19","LFG2","LFG20","LFG21","LFG22","LFG23","LFG24","LFG25","LFG26","LFG27","LFG28","LFG29","LFG3","LFG30","LFG31","LFG32","LFG33","LFG34","LFG35","LFG36","LFG37","LFG38","LFG39","LFG4","LFG40","LFG41","LFG42","LFG43","LFG44","LFG45","LFG46","LFG47","LFG48","LFG49","LFG5","LFG50","LFG51","LFG52","LFG53","LFG54","LFG55","LFG56","LFG57","LFG58","LFG59","LFG6","LFG60","LFG61","LFG62","LFG63","LFG64","LFG7","LFG8","LFG9","LFS1","LFS2","LFS3","LFS4"]

included_fields = [{"fieldName":"class", "fieldType":"int"},
        {"fieldName":"latency","fieldType":"float"},
        {"fieldName":"MAD","fieldTyp":"float"},
        {"fieldName":"IQR","fieldType":"float"}]+[{"fieldName":x, "fieldType":"float"} for x in columns]
inference_args = {"predictionSteps": [1], "predictedField": "class"}
stream_def =   {"info": "Kaggle-EEG", "version": 0.1,
    "streams": [
      {
        "info": "KaggleData.csv",
        "source": "file://KaggleData.csv",
        "columns": [
          "*"
        ]
      }
    ]
  "aggregation": {
  "hours": 1,
  "microseconds": 0,
  "seconds": 0,
  "fields": [
    [
      "value", # CHANGED
      "sum"
    ],
    # Note: The lines referring to the field 'gym' which is 
    # no longer present have been removed
    [
      "dttm", # CHANGED
      "first"
    ]
  ],
  "weeks": 0,
  "months": 0,
  "minutes": 0,
  "days": 0,
  "milliseconds": 0,
  "years": 0
  }
}


SWARM_DESCRIPTION = {"includedFields":included_fields, "streamDef":stream_def,
"aggregation":aggregation, "inferenceType": "MultiStep", "inferenceArgs": ,
  "iterationCount": -1,
  "swarmSize": "medium"
