from Task.models import tasks ,task_point
"""返回任务前十，显示在主页"""
"""排序依据是什么: 创建的时间"""

def Top_tasks():
    """任务"""
    taskinfolist = tasks.objects.all().filter(status!=2).order_by(c_time)
    for task in task_point:
        print(task.c_time)
        print(task.f_time)
        print(task.title)
        print(task.status)
        #task_schedule
        print(task_point.object.filter(task_id=task.id).count())
        print(task_point.object.filter(task_id=task.id,status=2).count())
      
        
    ## 开始时间
    ## 结束时间
    ## 任务名称
    ## 任务状态
    ## 进度 
    
