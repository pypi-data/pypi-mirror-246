from .courses import courses 

def total_duration():
    return sum(course.duration for course in courses)

# course.duration for course in courses devuelve un iterable de duraciones de los cursos.
# sum() recibe el iterable, lo recorre y devuelve la suma de todos los elementos course.duration
