def choices_switch(CHOICES,input_keyword):
    GENDER_CHOICES = [
        '不急加重',
        '不急',
        '正常',
        '紧急',
        '加急',
        '重要',
        '加重',
        '不急重要'
    ]   
    GENDER_CHOICES1 = [
        '未启动',
        '进行中',
        '完成',
    ]
    if CHOICES == "GENDER_CHOICES":
        index = GENDER_CHOICES.index(input_keyword)
    else:
        index = GENDER_CHOICES1.index(input_keyword)
    return index

choices_switch("GENDER_CHOICES1","完成")
