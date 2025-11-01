from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, connection
from django.utils import timezone
from datetime import date, timedelta, time
from decimal import Decimal
from typing import List

from django.contrib.auth import get_user_model

from apps.organizacion.models import Organizacion
from apps.voluntariado.models import (
    Voluntariado,
    DescripcionVoluntariado,
    Turno,
    InscripcionTurno,
    InscripcionConvocatoria,
)
from apps.persona.models import Voluntario as VoluntarioModel, Delegado as DelegadoModel
from apps.asistencia.models import Asistencia
from apps.capacitacion.models import Capacitacion, InscripcionCapacitacion
from apps.facultad.models import Facultad, Carrera
from apps.ubicacion.models import Pais, Provincia, Departamento, Localidad


DEMO_PREFIX = "DEMO "
DEFAULT_PASSWORD = "testpass123"


class Command(BaseCommand):
    help = "Create a complete demo dataset for local testing: users, personas, ubicaciones, organizaciones, voluntariados, turnos, inscripciones, asistencias y capacitaciones."

    def add_arguments(self, parser):
        parser.add_argument("--orgs", type=int, default=2, help="Cantidad de organizaciones extra a crear (además de UNCuyo)")
        parser.add_argument("--vols-per-org", type=int, default=2, help="Cantidad de voluntariados por organización")
        parser.add_argument("--volunteers-per-org", type=int, default=3, help="Cantidad de voluntarios por organización")
        parser.add_argument("--turnos-per-vol", type=int, default=2, help="Cantidad de turnos por voluntariado")
        parser.add_argument("--caps-per-vol", type=int, default=1, help="Cantidad de capacitaciones por voluntariado")
        parser.add_argument("--with-superuser", action="store_true", help="Crea un superusuario admin@demo.local / testpass123 si no existe")
        parser.add_argument("--admin-email", type=str, default="admin@demo.local")
        parser.add_argument("--admin-pass", type=str, default=DEFAULT_PASSWORD)
        parser.add_argument("--reset", action="store_true", help="Elimina datos DEMO previamente creados por este comando")

    def handle(self, *args, **opts):
        try:
            with transaction.atomic():
                if opts.get("reset"):
                    self._reset_demo_data()

                if opts.get("with_superuser"):
                    self._ensure_superuser(opts["admin_email"], opts["admin_pass"])  # type: ignore

                # 1) Ubicación básica (AR / Mendoza)
                ar, mendoza, dptos, locs = self._ensure_ubicaciones_basicas()
                # 2) Facultad/Carrera básica
                ing, sis = self._ensure_facultad_carrera_basica()

                # 3) Organizaciones (UNCuyo + extras) y delegados por organización
                orgs = self._create_organizaciones(opts["orgs"], default_localidad=locs["Mendoza"])

                # 4) Usuarios voluntarios por organización (personas + users)
                voluntarios_por_org = self._create_voluntarios(orgs, opts["volunteers_per_org"], carrera=sis, localidad=locs["Ciudad de Mendoza"])  # type: ignore

                # 5) Voluntariados en distintos estados + turnos + (capacitaciones si existen tablas)
                today = date.today()
                for org in orgs:
                    for v_idx in range(1, opts["vols_per_org"] + 1):
                        nombre = f"{DEMO_PREFIX}Voluntariado {org.nombre} #{v_idx}"

                        desc = DescripcionVoluntariado.objects.create(
                            descripcion=f"Descripción para {nombre}",
                            resumen=f"Resumen {nombre}",
                        )

                        # Distribuir estados: 1) convocatoria abierta, 2) cursado activo, 3) finalizado
                        stage = (v_idx - 1) % 3
                        if stage == 0:
                            # Convocatoria abierta ahora
                            fecha_inicio_conv = today - timedelta(days=3)
                            fecha_fin_conv = today + timedelta(days=7)
                            fecha_inicio_cursado = today + timedelta(days=14)
                            fecha_fin_cursado = fecha_inicio_cursado + timedelta(days=30)
                        elif stage == 1:
                            # Cursado activo ahora
                            fecha_inicio_conv = today - timedelta(days=30)
                            fecha_fin_conv = today - timedelta(days=15)
                            fecha_inicio_cursado = today - timedelta(days=3)
                            fecha_fin_cursado = today + timedelta(days=27)
                        else:
                            # Finalizado
                            fecha_inicio_conv = today - timedelta(days=90)
                            fecha_fin_conv = today - timedelta(days=60)
                            fecha_inicio_cursado = today - timedelta(days=50)
                            fecha_fin_cursado = today - timedelta(days=20)

                        voluntariado = Voluntariado.objects.create(
                            nombre=nombre,
                            descripcion=desc,
                            organizacion=org,
                            fecha_inicio_convocatoria=fecha_inicio_conv,
                            fecha_fin_convocatoria=fecha_fin_conv,
                            fecha_inicio_cursado=fecha_inicio_cursado,
                            fecha_fin_cursado=fecha_fin_cursado,
                            latitud=-32.890842,
                            longitud=-68.844849,
                            place_id="demo-place",
                        )

                        # Turnos: para activo y finalizado, incluir pasados; para convocatoria, todos futuros
                        created_turnos = []
                        for t_idx in range(opts["turnos_per_vol"]):
                            if stage == 0:  # convocatoria: turnos futuros pos inicio de cursado
                                turno_fecha = fecha_inicio_cursado + timedelta(days=2 + t_idx * 3)
                            elif stage == 1:  # activo: mezclar pasado y futuro alrededor de hoy
                                turno_fecha = today + timedelta(days=-3 + t_idx * 3)
                            else:  # finalizado: todos en el pasado dentro del rango
                                turno_fecha = fecha_inicio_cursado + timedelta(days=2 + t_idx * 4)
                            created_turnos.append(
                                Turno.objects.create(
                                    voluntariado=voluntariado,
                                    fecha=turno_fecha,
                                    hora_inicio=time(hour=9 + (t_idx % 3) * 2, minute=0),
                                    hora_fin=time(hour=12 + (t_idx % 3) * 2, minute=0),
                                    cupo=max(3, min(8, len(voluntarios_por_org[org.id]))),
                                    lugar="Sede Principal",
                                )
                            )

                        # Capacitaciones (solo si la tabla existe)
                        if self._has_table(Capacitacion):
                            for c_idx in range(opts["caps_per_vol"]):
                                cap_fecha = fecha_inicio_conv + timedelta(days=1 + c_idx)
                                Capacitacion.objects.create(
                                    titulo=f"{DEMO_PREFIX}Capacitación {v_idx}-{c_idx} ({org.nombre})",
                                    descripcion="Introducción y buenas prácticas",
                                    fecha=cap_fecha,
                                    hora_inicio=time(18, 0),
                                    hora_fin=time(20, 0),
                                    cupo=50,
                                    voluntariado=voluntariado,
                                )

                        # Inscripciones según estado y completar cupos de un turno
                        turnos = list(voluntariado.turnos.order_by("fecha", "hora_inicio"))
                        vols = voluntarios_por_org[org.id]
                        if turnos and vols:
                            # Seleccionar primer turno para "llenarlo" (cupo == cantidad inscripciones)
                            first_turno = turnos[0]
                            cupo = first_turno.cupo
                            to_inscribe = min(cupo, len(vols))
                            for i in range(to_inscribe):
                                estado = InscripcionTurno.Status.INSCRITO
                                if stage == 2:  # finalizado -> marcar muchos como asistidos
                                    estado = InscripcionTurno.Status.ASISTIO
                                elif stage == 1 and i == 1 and to_inscribe > 1:  # activo -> uno cancelado
                                    estado = InscripcionTurno.Status.CANCELADO
                                insc, _ = InscripcionTurno.objects.get_or_create(
                                    turno=first_turno,
                                    voluntario=vols[i],
                                    defaults={"estado": estado},
                                )
                                # crear asistencia cuando corresponde
                                if estado == InscripcionTurno.Status.ASISTIO:
                                    Asistencia.objects.get_or_create(
                                        inscripcion=insc,
                                        defaults={
                                            "presente": True,
                                            "horas": Decimal("3.0"),
                                            "observaciones": "Registro de demo",
                                        },
                                    )

                            # Si existe un segundo turno y sobran voluntarios, inscribir algunos más
                            if len(turnos) > 1 and len(vols) > to_inscribe:
                                second_turno = turnos[1]
                                extra = min(second_turno.cupo, len(vols) - to_inscribe)
                                for j in range(extra):
                                    InscripcionTurno.objects.get_or_create(
                                        turno=second_turno,
                                        voluntario=vols[to_inscribe + j],
                                        defaults={"estado": InscripcionTurno.Status.INSCRITO},
                                    )

                        # Inscripciones de convocatoria para los que están en etapa de convocatoria
                        if stage == 0:
                            for vol in vols:
                                InscripcionConvocatoria.objects.get_or_create(
                                    voluntariado=voluntariado,
                                    voluntario=vol,
                                    defaults={"estado": InscripcionConvocatoria.Status.INSCRITO},
                                )

                        # Inscripciones a capacitaciones y aprobar uno (si existen tablas)
                        if self._has_table(Capacitacion) and self._has_table(InscripcionCapacitacion):
                            for cap in Capacitacion.objects.filter(voluntariado=voluntariado):
                                for i, vol in enumerate(vols[:3]):
                                    ic, _ = InscripcionCapacitacion.objects.get_or_create(capacitacion=cap, voluntario=vol)
                                    if i == 0:
                                        ic.aprobado = True
                                        ic.save()

                self.stdout.write(self.style.SUCCESS("✓ Demo data created successfully"))

        except Exception as e:
            raise CommandError(f"Failed to create demo data: {e}")

    # ---------------------- Helpers ----------------------
    def _ensure_superuser(self, email: str, password: str):
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser created: {email} / {password}"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser already exists: {email}"))

    def _ensure_ubicaciones_basicas(self):
        ar, _ = Pais.objects.get_or_create(nombre="Argentina")
        mendoza, _ = Provincia.objects.get_or_create(nombre="Mendoza", pais=ar)
        dpto_gc, _ = Departamento.objects.get_or_create(nombre="Godoy Cruz", provincia=mendoza)
        dpto_cap, _ = Departamento.objects.get_or_create(nombre="Capital", provincia=mendoza)
        loc_gc, _ = Localidad.objects.get_or_create(nombre="Luján de Cuyo", departamento=dpto_gc)
        loc_mza, _ = Localidad.objects.get_or_create(nombre="Ciudad de Mendoza", departamento=dpto_cap)
        return ar, mendoza, {"Godoy Cruz": dpto_gc, "Capital": dpto_cap}, {"Luján de Cuyo": loc_gc, "Ciudad de Mendoza": loc_mza, "Mendoza": loc_mza}

    def _ensure_facultad_carrera_basica(self):
        fac, _ = Facultad.objects.get_or_create(nombre="Facultad de Ingeniería")
        car, _ = Carrera.objects.get_or_create(nombre="Ingeniería en Sistemas", facultad=fac)
        return fac, car

    def _create_organizaciones(self, extra_count: int, default_localidad: Localidad) -> List[Organizacion]:
        orgs: List[Organizacion] = []
        uncuyo, _ = Organizacion.objects.get_or_create(
            nombre="UNCuyo",
            defaults={
                "activo": True,
                "descripcion": "Universidad Nacional de Cuyo (organización ejemplo)",
                "contacto_email": "info@uncu.edu.ar",
                "localidad": default_localidad,
            },
        )
        orgs.append(uncuyo)
        for i in range(1, extra_count + 1):
            name = f"{DEMO_PREFIX}Organización {i}"
            org, _ = Organizacion.objects.get_or_create(
                nombre=name,
                defaults={
                    "activo": True,
                    "descripcion": f"Organización de prueba N° {i}",
                    "contacto_email": f"org{i}@demo.local",
                    "localidad": default_localidad,
                },
            )
            orgs.append(org)
            # Crear delegado por organización (persona + user)
            self._ensure_delegado_for_org(org)
        self.stdout.write(self.style.SUCCESS(f"Created/ensured {len(orgs)} organizaciones"))
        return orgs

    def _ensure_delegado_for_org(self, org: Organizacion):
        User = get_user_model()
        email = f"delegado_{org.id}@demo.local"
        if not User.objects.filter(email=email).exists():
            persona = DelegadoModel.objects.create(nombre="Delegado", apellido=org.nombre, dni=f"9{org.id:07d}")
            user = User.objects.create_user(email=email, password=DEFAULT_PASSWORD, role=User.Roles.DELEGADO)
            user.persona = persona
            user.is_staff = True
            user.save()

    def _create_voluntarios(self, orgs: List[Organizacion], per_org: int, carrera: Carrera, localidad: Localidad):
        User = get_user_model()
        result = {}
        for org in orgs:
            vols = []
            for idx in range(1, per_org + 1):
                dni = f"1{org.id:02d}{idx:06d}"
                persona, _ = VoluntarioModel.objects.get_or_create(
                    dni=dni,
                    defaults={
                        "nombre": f"Vol{idx}",
                        "apellido": f"{org.nombre}",
                        "carrera": carrera,
                        "localidad": localidad,
                        "condicion": VoluntarioModel.Condicion.ESTUDIANTE,
                        "fecha_nacimiento": date(1998, (idx % 12) + 1, (idx % 27) + 1),
                        "telefono": f"261-55{idx:03d}-{org.id:02d}",
                        "direccion": f"Av. Demo {idx*10}, {localidad.nombre}",
                    },
                )
                email = f"vol{org.id}_{idx}@demo.local"
                user = User.objects.filter(email=email).first()
                if not user:
                    user = User.objects.create_user(email=email, password=DEFAULT_PASSWORD, role=User.Roles.VOLUNTARIO)
                if not user.persona:
                    user.persona = persona
                    user.save()
                vols.append(persona)
            result[org.id] = vols
        return result

    def _has_table(self, model_cls) -> bool:
        """Return True if the model's DB table exists."""
        try:
            table_name = model_cls._meta.db_table
            with connection.cursor() as cursor:
                tables = connection.introspection.table_names(cursor)
            return table_name in tables
        except Exception:
            return False

    def _reset_demo_data(self):
        """Soft-delete objects created by this script.
        This method is resilient to missing tables (e.g., when some app
        migrations haven't been applied yet) by checking table existence
        before querying.
        """

        # Delete in dependency-friendly order and only if tables exist
        try:
            if self._has_table(InscripcionCapacitacion):
                InscripcionCapacitacion.objects.all().delete()
        except Exception:
            pass

        try:
            if self._has_table(Asistencia):
                Asistencia.objects.all().delete()
        except Exception:
            pass

        try:
            if self._has_table(InscripcionTurno):
                InscripcionTurno.objects.all().delete()
        except Exception:
            pass

        try:
            if self._has_table(InscripcionConvocatoria):
                InscripcionConvocatoria.objects.all().delete()
        except Exception:
            pass

        try:
            if self._has_table(Turno):
                Turno.objects.all().delete()
        except Exception:
            pass

        try:
            if self._has_table(Capacitacion):
                Capacitacion.objects.filter(titulo__startswith=DEMO_PREFIX).delete()
        except Exception:
            pass

        try:
            if self._has_table(Voluntariado):
                Voluntariado.objects.filter(nombre__startswith=DEMO_PREFIX).delete()
        except Exception:
            pass

        try:
            if self._has_table(DescripcionVoluntariado):
                # Only delete orphans created by the demo
                DescripcionVoluntariado.objects.filter(voluntariados__isnull=True).delete()
        except Exception:
            pass

        try:
            if self._has_table(Organizacion):
                Organizacion.objects.filter(nombre__startswith=DEMO_PREFIX).delete()
        except Exception:
            pass

        # Users last (this will cascade soft-delete personas via model delete overrides)
        try:
            User = get_user_model()
            if self._has_table(User):
                for u in User.objects.filter(email__icontains="@demo.local"):
                    u.delete()
        except Exception:
            pass

        self.stdout.write(self.style.WARNING("Previous DEMO data soft-deleted (where tables existed)"))
