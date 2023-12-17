from .cursos import cursos 

def total_duration():
    return sum (cur.dura for cur in cursos )
