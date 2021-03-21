from detect import detection_and_classification, model

res = detection_and_classification("./data/board1.jpg")
print(res)
print(model.names)
