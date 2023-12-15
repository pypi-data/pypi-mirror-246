class Course:
    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    #def __str__(self):
    #    return f"{self.name} [{self.duration}] ({self.link})"

    def __repr__(self):
        return f"{self.name} [{self.duration}] ({self.link})"

# Si no se define el metodo __str__ en la clase Course pero si el metodo __repr__ entonces existe el siguiente comportamiento:

courses = [
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

# Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/") equivale a Course.__repr__(Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/")), 
# Ocurre primero el objeto devuelto por Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"). 
# Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/") devuelve un objeto de la clase Course.
# __repr__ recibe dicho objeto y devuelve una cadena de texto que representa al objeto de la clase Course.


# courses contiene cadena de texto que representa a los objetos de la clase Course (se llama al metodo __repr__ de la clase Course)
# Con un bucle for podemos recorrer la lista courses y mostrar cada uno de los elementos de la lista courses.
# Lo que está dentro de courses siguen siendo objetos de la clase Course, pero ahora son cadenas de texto que representan a los objetos de la clase Course.
# Puedo hacer esto: print(courses[0].name) y me muestra Introducción a Linux

#print(courses)# Muestra [Introducción a Linux [15] (https://hack4u.io/cursos/introduccion-a-linux/), Personalización de Linux [3] (https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/), Introducción al Hacking [53] (https://hack4u.io/cursos/introduccion-al-hacking/)]

# Funcion para listar los cursos
def list_courses():
    for course in courses:
        print(course)

# Función para buscar un curso 
def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course # Devuelve el objeto de la clase Course que coincide con el nombre buscado

    return None # Si no se encuentra el curso se devuelve None

'''
Si no se define el metodo __repr__ en la clase Course pero si el metodo __str__ entonces existe el siguiente comportamiento:

courses = [
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

# courses contiene objetos de la clase Course

print(courses)# Muestra [<main.Course object at 0x7f9b1c1b6d30>, <main.Course object at 0x7f9b1c1b6d60>, <main.Course object at 0x7f9b1c1b6d90>]

for course in courses:
    print(course)# course equivale a course.__str__() que equivale a Course.__str__(course). Esto solo se cumple cuando existe un método __str__ en la clase Course y se llama a print(course)
'''


