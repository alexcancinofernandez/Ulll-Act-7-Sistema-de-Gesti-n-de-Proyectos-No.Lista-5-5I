from django.db import models

class EmpleadoProyecto(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    carga = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    habilidades = models.TextField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Proyecto(models.Model):
    nombre_proyecto = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    estado_proyecto = models.CharField(max_length=50)
    presupuesto = models.DecimalField(max_digits=15, decimal_places=2)
    gerente = models.ForeignKey(
        EmpleadoProyecto, 
        on_delete=models.CASCADE, 
        related_name="proyectos_gerenciados"
    )

    def __str__(self):
        return self.nombre_proyecto


class Tarea(models.Model):
    nombre_tarea = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField()
    estado_tarea = models.CharField(max_length=50)
    prioridad = models.CharField(max_length=20)
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="tareas"
    )
    asignado = models.ForeignKey(
        EmpleadoProyecto,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tareas_asignadas"
    )

    def __str__(self):
        return self.nombre_tarea


class AsignacionTarea(models.Model):
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name="asignaciones"
    )
    empleado = models.ForeignKey(
        EmpleadoProyecto,
        on_delete=models.CASCADE,
        related_name="asignaciones"
    )
    fecha_asignacion = models.DateTimeField()
    fecha_entrega = models.DateField()
    progreso = models.IntegerField()
    comentarios = models.TextField()

    def __str__(self):
        return f"Asignación {self.id} - {self.tarea}"


class Hito(models.Model):
    nombre_hito = models.CharField(max_length=255)
    fecha_estimada = models.DateField()
    fecha_completado = models.DateField(null=True, blank=True)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="hitos"
    )
    estado_hito = models.CharField(max_length=50)
    responsable = models.ForeignKey(
        EmpleadoProyecto,
        on_delete=models.SET_NULL,
        null=True,
        related_name="hitos_responsables"
    )

    def __str__(self):
        return self.nombre_hito


class Documento(models.Model):
    nombre_documento = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=50)
    fecha_subida = models.DateTimeField()
    url_documento = models.CharField(max_length=255)
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE,
        related_name="documentos"
    )
    autor_documento = models.ForeignKey(
        EmpleadoProyecto,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documentos_creados"
    )
    version = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre_documento


class Comentario(models.Model):
    tarea = models.ForeignKey(
        Tarea,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    empleado = models.ForeignKey(
        EmpleadoProyecto,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )
    fecha_comentario = models.DateTimeField()
    texto_comentario = models.TextField()
    documento_adjunto = models.ForeignKey(
        Documento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comentarios"
    )

    def __str__(self):
        return f"Comentario {self.id}"
