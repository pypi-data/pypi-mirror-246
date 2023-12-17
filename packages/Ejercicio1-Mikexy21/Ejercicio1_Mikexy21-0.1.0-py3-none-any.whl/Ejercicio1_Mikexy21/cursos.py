#!/usr/bin/env python3


class Curso:

    def __init__(self,name,dura,link):
        self.name = name 
        self.dura = dura 
        self.link = link


    def __repr__(self):
        return f"Curso:{self.name} dura: {self.dura}, link:{self.link}"



cursos = [ 
    Curso("Intro linux",15 ,"a"),
    Curso("Personaliza linux",3 ,"b"),
    Curso("Intro Hacking",56,"c")
]

def list_curso():    
    for curso in cursos:    
        print(curso)   

def search_by_name(name):
    for curso in cursos:
        if curso.name == name:
            return Curso

    return None


