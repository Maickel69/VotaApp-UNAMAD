#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Diagramas Académicos UML 2.5 y Arquitectura Cloud v2.0 - VotaApp UNAMAD
Renderiza los diagramas PlantUML (.puml -> .png) mediante Kroki API con skinparam dpi 160
para garantizar alta nitidez sin exceder el límite horizontal de 4096px de PlantUML/Kroki.
"""
import base64
import pathlib
import shutil
import urllib.request
import zlib
from PIL import Image


BASE_DIR = pathlib.Path(__file__).resolve().parent
DIAG_DIR = BASE_DIR / "diagramas"


def render_via_kroki(source_text: str, diagram_type: str = "plantuml", output_format: str = "png") -> bytes:
    url = f"https://kroki.io/{diagram_type}/{output_format}"
    payload = source_text.encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "text/plain; charset=utf-8",
            "User-Agent": "VotaApp-UNAMAD-AcademicDiagrams/2.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            return resp.read()
    except Exception:
        compressed = zlib.compress(payload, 9)
        encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
        get_url = f"https://kroki.io/{diagram_type}/{output_format}/{encoded}"
        req_get = urllib.request.Request(
            get_url,
            headers={"User-Agent": "VotaApp-UNAMAD-AcademicDiagrams/2.0"},
            method="GET",
        )
        with urllib.request.urlopen(req_get, timeout=40) as resp:
            return resp.read()


# ==============================================================================
# 1. FIGURA 1: DIAGRAMA DE CASOS DE USO (UML 2.5 - VotaApp UNAMAD v2.0 Cloud)
# ==============================================================================
PUML_FIG1_CASOS_USO = """@startuml fig1_casos_uso
set separator none
left to right direction
skinparam dpi 160
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam shadowing false
skinparam packageStyle rectangle

skinparam ArrowColor #1B4F72
skinparam ArrowThickness 1.2

skinparam actor {
    BackgroundColor #D4E6F1
    BorderColor #1A5276
    FontSize 11
}

skinparam usecase {
    BackgroundColor #EBF5FB
    BorderColor #2980B9
    FontSize 11
}

actor "Administrador / Creador\\n(Docente / Delegado UNAMAD)" as Admin
actor "Participante / Votante\\n(Estudiante UNAMAD)" as Votante
actor "Firebase Cloud\\n(Auth & Firestore)" as Cloud

rectangle "Sistema Móvil de Encuestas y Votaciones Cloud (VotaApp UNAMAD v2.0)" {
    usecase "RF01: Iniciar Sesión / Google OAuth\\ny Registro de Perfil Universitario" as UC_Auth
    usecase "RF02: Crear Encuesta con Filtro de\\nCarrera UNAMAD y Padrón .TXT/.CSV" as UC_Crear
    usecase "RF03: Gestionar Preguntas\\n(Selección Única y Múltiple)" as UC_Preg
    usecase "RF04: Consultar, Buscar y Filtrar\\nEncuestas por Categoría y Estado" as UC_Listar
    usecase "RF05: Editar / Eliminar Encuesta\\ny Reiniciar Conteo en la Nube" as UC_Editar
    usecase "RF06: Emitir Voto Único Verificado\\nen Tiempo Real" as UC_Votar
    usecase "RF07: Visualizar Resultados Donut\\nen Tiempo Real y Exportar Acta" as UC_Res

    usecase "Validar Acceso por Escuela Profesional\\n(12 Carreras) y Padrón de Códigos" as UC_Filtro
    usecase "Verificar Voto Único por UID\\n(encuestas/{id}/votos/{uid})" as UC_Unico
    usecase "Extraer Códigos desde Archivo\\n.TXT / .CSV o Portapapeles" as UC_Padron

    UC_Crear ..> UC_Padron : <<include>>
    UC_Votar ..> UC_Filtro : <<include>>
    UC_Votar ..> UC_Unico : <<include>>
}

Admin --> UC_Auth
Admin --> UC_Crear
Admin --> UC_Preg
Admin --> UC_Listar
Admin --> UC_Editar
Admin --> UC_Res

Votante --> UC_Auth
Votante --> UC_Listar
Votante --> UC_Votar
Votante --> UC_Res

UC_Auth --> Cloud
UC_Crear --> Cloud
UC_Votar --> Cloud
UC_Res --> Cloud
@enduml
"""

# ==============================================================================
# 2. FIGURA 2: ARQUITECTURA EN 3 CAPAS + CLOUD FIRESTORE + CI/CD
# ==============================================================================
PUML_FIG2_ARQUITECTURA = """@startuml fig2_arquitectura
set separator none
top to bottom direction
skinparam dpi 160
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam shadowing false
skinparam packageStyle rectangle

skinparam ArrowColor #1B4F72
skinparam ArrowThickness 1.2

package "CAPA 1: PRESENTACIÓN (UI / Activities, Custom Views & Edge-to-Edge)" as LayerUI #EBF5FB {
    class LoginActivity {
        + iniciarSesionConCorreo()
        + registrarConCorreo()
        + iniciarGoogleSignIn()
        + autenticarConGoogleEnFirebase()
    }
    class MainActivity {
        + cargarEncuestasDesdeNube()
        + aplicarFiltrosLocales()
        + mostrarDialogoPerfilYCuenta()
        + mostrarDialogoEliminar()
    }
    class CrearEncuestaActivity {
        + importarCodigosDesdeUri()
        + pegarCodigosDesdePortapapeles()
        + guardarEncuesta()
    }
    class GestionarPreguntasActivity {
        + cargarEncuestaYPreguntas()
        + guardarPregunta()
        + renderizarListaPreguntas()
    }
    class RegistrarVotoActivity {
        + cargarEncuestaDesdeNube()
        + construirCuestionarioDinamico()
        + procesarVoto()
    }
    class ResultadosActivity {
        + cargarResultados()
        + renderizarGraficasPreguntas()
        + compartirActaResultados()
    }
    class DonutChartView {
        + setData(alternativas, total)
        # onDraw(canvas: Canvas)
    }
    class UiInsetsHelper {
        + configurarEdgeToEdgeConHeader()
        + esModoOscuroActivo()
        + alternarModoOscuro()
    }

    LoginActivity -[hidden]right-> MainActivity
    MainActivity -[hidden]right-> CrearEncuestaActivity
    CrearEncuestaActivity -[hidden]right-> GestionarPreguntasActivity

    LoginActivity -[hidden]down-> RegistrarVotoActivity
    RegistrarVotoActivity -[hidden]right-> ResultadosActivity
    ResultadosActivity -[hidden]right-> DonutChartView
    DonutChartView -[hidden]right-> UiInsetsHelper
}

package "CAPA 2: DOMINIO Y MODELOS (Models.kt & CatalogoUnamad)" as LayerDomain #E8F8F5 {
    class "Modelos de Dominio (Models.kt)" as DomainModels {
        + UsuarioPerfil (uid, nombre, codigoUniversitario, carrera, email)
        + Encuesta (id, titulo, categoria, activa, carreraRestringida, codigosPermitidos, preguntas)
        + Encuesta.verificarAcceso(perfil, uidActual): Pair<Boolean, String>
        + Pregunta (id, texto, tipo: UNICA | MULTIPLE, alternativas)
        + Alternativa (id, texto, votos)
        + PreguntaEstadistica & AlternativaEstadistica (porcentaje, esGanadora)
    }
    class "CatalogoUnamad (12 Escuelas Profesionales)" as Catalogo {
        + CARRERAS_UNAMAD : List<String> (12 carreras oficiales UNAMAD)
        + OPCIONES_FILTRO_CARRERA : List<String>
        + extraerCodigosDesdeTexto(textoBruto: String) : List<String>
    }
    DomainModels -[hidden]right-> Catalogo
}

package "CAPA 3: DATOS, NUBE Y DEVOPS (Firebase Cloud + Respaldo SQLite + CI/CD)" as LayerData #FEF9E7 {
    class "FirebaseRepository.kt (Repositorio Cloud)" as Repo {
        + guardarPerfilUsuario() / obtenerPerfilUsuario()
        + listarEncuestas() / obtenerEncuestaPorId()
        + crearEncuesta() / actualizarEncuesta() / eliminarEncuesta()
        + guardarPreguntasEncuesta() / sembrarEncuestasDemo()
        + yaVotoUsuario() / registrarVoto() / obtenerResultados()
    }
    class "Firebase Cloud (votaapp-unamad-2026)" as FirebaseCloud {
        + Firebase Authentication (Email/Password & Google OAuth 2.0)
        + Cloud Firestore: users/{uid}
        + Cloud Firestore: encuestas/{encuestaId}
        + Subcolección: encuestas/{encuestaId}/votos/{uid}
    }
    class "DatabaseHelper.kt (SQLite Local Fallback)" as LocalDB {
        + encuestas_unamad.db (SQLiteOpenHelper)
        + Tablas: encuestas, preguntas, alternativas, respuestas
        + PRAGMA foreign_keys = ON (Integridad Referencial)
    }
    class "GitHub Actions CI/CD" as CICD {
        + Workflow: android-ci.yml
        + Gradle 9.4.1 / AGP 9.1.0 / Kotlin 2.2.10
        + Compilación y Verificación Automática APK
    }
    Repo --> FirebaseCloud : "SDK Firebase BoM 33.10.0\\nSincronización en Tiempo Real"
    Repo ..> LocalDB : "Persistencia Local\\nde Respaldo"
    Repo -[hidden]right-> CICD
}

ResultadosActivity --> DonutChartView : "renderiza"
RegistrarVotoActivity --> DomainModels : "valida y modela"
CrearEncuestaActivity --> Catalogo : "filtra carrera y padrón"
DomainModels --> Repo : "sincroniza entidades"
Catalogo --> Repo : "valida códigos"
@enduml
"""

# ==============================================================================
# 3. FIGURA 3 (Y FIGURA 6): MODELO DE DATOS HÍBRIDO CLOUD FIRESTORE + SQLITE ER
# ==============================================================================
PUML_FIG3_MODELO_ER = """@startuml fig3_modelo_er
set separator none
hide circle
skinparam dpi 160
skinparam linetype ortho
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam shadowing false
skinparam packageStyle rectangle

skinparam class {
    BackgroundColor #FFFFFF
    BorderColor #1A5276
    HeaderBackgroundColor #D4E6F1
}

package "Motor Principal en la Nube: Cloud Firestore (Proyecto: votaapp-unamad-2026)" as PkgCloud #EBF5FB {
    entity "users / {uid}" as fs_users {
        * **uid** : String <<PK, Firebase Auth UID>>
        --
        * nombre : String
        * codigoUniversitario : String <<Índice Único>>
        * carrera : String (12 Carreras UNAMAD)
        * email : String
        * fechaRegistro : Long (Epoch ms)
    }

    entity "encuestas / {encuestaId}" as fs_encuestas {
        * **encuestaId** : String <<PK, Auto-ID>>
        --
        * titulo : String
        * descripcion : String
        * categoria : String ('Académica'|'Satisfacción'|'Votación'|'General')
        * activa : Boolean
        * fechaCreacion : String
        * creadorUid : String <<FK -> users/{uid}>>
        * creadorNombre : String
        * carreraRestringida : String ('TODAS' o Escuela Profesional)
        * codigosPermitidos : String (Padrón CSV/TXT)
        * **preguntas** : Array<Map> <<Subdocumento Embebido>>
    }

    entity "Pregunta Embebida (en preguntas[])" as fs_preguntas {
        * **id** : String <<UUID>>
        --
        * texto : String
        * tipo : String ('UNICA' | 'MULTIPLE')
        * **alternativas** : Array<Map {id, texto}>
    }

    entity "encuestas / {encuestaId} / votos / {uid}" as fs_votos {
        * **uid** : String <<PK, ID Documento = UID Votante>>
        --
        * participante : String (Nombre + Código)
        * fechaVoto : String
        * **respuestas** : Map<preguntaId, List<alternativaId>>
    }

    fs_users ||--o{ fs_encuestas : "crea (creadorUid)"
    fs_encuestas *--|{ fs_preguntas : "contiene embebidas (1:N)"
    fs_encuestas ||--o{ fs_votos : "subcolección votos (1:N)"
    fs_users ||--o{ fs_votos : "emite 1 voto único por encuesta (uid)"
}

package "Motor Local de Respaldo: SQLite (encuestas_unamad.db - DatabaseHelper.kt)" as PkgSQLite #FEF9E7 {
    entity "encuestas (SQLite)" as sq_enc {
        * **id_encuesta** : INTEGER <<PK>>
        --
        * titulo, descripcion, categoria : TEXT
        * activa : INTEGER (1|0)
        * fecha_creacion : TEXT
    }

    entity "preguntas (SQLite)" as sq_preg {
        * **id_pregunta** : INTEGER <<PK>>
        --
        * id_encuesta : INTEGER <<FK CASCADE>>
        * texto_pregunta, tipo_pregunta : TEXT
    }

    entity "alternativas (SQLite)" as sq_alt {
        * **id_alternativa** : INTEGER <<PK>>
        --
        * id_pregunta : INTEGER <<FK CASCADE>>
        * texto_alternativa : TEXT
        * votos : INTEGER
    }

    entity "respuestas (SQLite)" as sq_resp {
        * **id_respuesta** : INTEGER <<PK>>
        --
        * id_encuesta, id_pregunta, id_alternativa : INTEGER <<FK>>
        * participante, fecha_voto : TEXT
    }

    sq_enc ||--|{ sq_preg : "1:N CASCADE"
    sq_preg ||--|{ sq_alt : "1:N CASCADE"
    sq_alt ||--o{ sq_resp : "1:N"
}
@enduml
"""

# ==============================================================================
# 4. FIGURA 4: DIAGRAMA DE CLASES UML 2.5 (VotaApp UNAMAD v2.0 Cloud)
# ==============================================================================
PUML_FIG4_CLASES = """@startuml fig4_clases
set separator none
top to bottom direction
skinparam dpi 160
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 10
skinparam shadowing false
skinparam packageStyle rectangle
skinparam ArrowColor #1B4F72
skinparam ArrowThickness 1.2

skinparam class {
    BackgroundColor #FDFEFE
    BorderColor #2874A6
    HeaderBackgroundColor #D4E6F1
}

class UsuarioPerfil <<data class>> {
    + uid : String
    + nombre : String
    + codigoUniversitario : String
    + carrera : String
    + email : String
    + fechaRegistro : Long
}

class CatalogoUnamad <<object>> {
    + CARRERAS_UNAMAD : List<String>
    + OPCIONES_FILTRO_CARRERA : List<String>
    + extraerCodigosDesdeTexto(textoBruto: String) : List<String>
}

class Encuesta <<data class>> {
    + id : String
    + titulo : String
    + descripcion : String
    + categoria : String
    + activa : Boolean
    + creadorUid : String
    + creadorNombre : String
    + carreraRestringida : String
    + codigosPermitidos : String
    + preguntas : List<Pregunta>
    + totalPreguntas : Int
    + totalVotos : Int
    + listaCodigosAutorizados() : List<String>
    + tieneRestriccionAcceso() : Boolean
    + etiquetaRestriccion() : String
    + verificarAcceso(perfil: UsuarioPerfil?, uid: String?) : Pair<Boolean, String>
}

class Pregunta <<data class>> {
    + id : String
    + texto : String
    + tipo : String
    + alternativas : List<Alternativa>
}

class Alternativa <<data class>> {
    + id : String
    + texto : String
    + votos : Int
}

class FirebaseRepository <<object>> {
    - db : FirebaseFirestore
    - auth : FirebaseAuth
    + currentUid() : String?
    + currentDisplayName() : String
    + guardarPerfilUsuario(...)
    + obtenerPerfilUsuario(uid: String, ...)
    + listarEncuestas(filtro: String, ...)
    + obtenerEncuestaPorId(id: String, ...)
    + crearEncuesta(...)
    + actualizarEncuesta(...)
    + guardarPreguntasEncuesta(...)
    + eliminarEncuesta(id: String, ...)
    + yaVotoUsuario(encuestaId: String, uid: String, ...)
    + registrarVoto(encuestaId: String, participante: String, respuestas: Map, ...)
    + obtenerResultados(encuestaId: String, ...)
}

class DonutChartView <<Custom View>> {
    - slices : List<Slice>
    - totalVotos : Int
    - animProgress : Float
    + setData(alternatives: List<AlternativaEstadistica>, total: Int)
    # onDraw(canvas: Canvas)
}

class LoginActivity <<AppCompatActivity>> {
    - auth : FirebaseAuth
    - modoRegistro : Boolean
    + iniciarSesionConCorreo()
    + registrarConCorreo()
    + iniciarGoogleSignIn()
}

class MainActivity <<AppCompatActivity>> {
    - cacheEncuestas : List<Encuesta>
    - perfilActual : UsuarioPerfil?
    + cargarEncuestasDesdeNube()
    + aplicarFiltrosLocales()
    + mostrarDialogoPerfilYCuenta()
}

class CrearEncuestaActivity <<AppCompatActivity>> {
    - idEncuestaEdicion : String?
    + importarCodigosDesdeUri(uri: Uri)
    + pegarCodigosDesdePortapapeles()
    + guardarEncuesta()
}

class GestionarPreguntasActivity <<AppCompatActivity>> {
    - idEncuesta : String
    - preguntasActuales : ArrayList<Pregunta>
    + cargarEncuestaYPreguntas()
    + guardarPregunta()
}

class RegistrarVotoActivity <<AppCompatActivity>> {
    - idEncuesta : String
    - mapaRadioGroups : HashMap<String, RadioGroup>
    - mapaCheckBoxes : HashMap<String, List<CheckBox>>
    + cargarEncuestaDesdeNube()
    + construirCuestionarioDinamico()
    + procesarVoto()
}

class ResultadosActivity <<AppCompatActivity>> {
    - idEncuesta : String
    - estadisticasActuales : List<PreguntaEstadistica>
    + cargarResultados()
    + renderizarGraficasPreguntas()
    + compartirActaResultados()
}

Encuesta "1" *-- "1..*" Pregunta : contiene >
Pregunta "1" *-- "2..4" Alternativa : contiene >
Encuesta ..> CatalogoUnamad : valida padrón >
Encuesta ..> UsuarioPerfil : verifica acceso >

FirebaseRepository --> Encuesta : gestiona >
FirebaseRepository --> UsuarioPerfil : persiste >

LoginActivity --> FirebaseRepository
LoginActivity --> CatalogoUnamad
MainActivity --> FirebaseRepository
CrearEncuestaActivity --> FirebaseRepository
CrearEncuestaActivity --> CatalogoUnamad
GestionarPreguntasActivity --> FirebaseRepository
RegistrarVotoActivity --> FirebaseRepository
ResultadosActivity --> FirebaseRepository
ResultadosActivity *-- DonutChartView : renderiza >
@enduml
"""

# ==============================================================================
# 5. FIGURA 5: DIAGRAMA DE NAVEGACIÓN ENTRE PANTALLAS
# ==============================================================================
PUML_FIG5_NAVEGACION = """@startuml fig5_navegacion
set separator none
skinparam dpi 160
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam shadowing false
skinparam roundCorner 10

skinparam ArrowColor #1B4F72
skinparam ArrowThickness 1.3

skinparam state {
    BackgroundColor #EBF5FB
    BorderColor #1A5276
    FontSize 11
    FontName Arial
}

[*] --> LoginActivity : Inicio de App (LAUNCHER)

state LoginActivity {
    [*] --> Autenticacion
    Autenticacion : • Correo y Contraseña (Firebase Auth)
    Autenticacion : • Google Sign-In (OAuth 2.0)
    Autenticacion : • Registro con Código y Carrera UNAMAD
}

LoginActivity --> MainActivity : Sesión autenticada (currentUser != null)\\n[startActivity + finish()]
MainActivity --> LoginActivity : Cerrar Sesión en «Mi Cuenta UNAMAD»\\n[Firebase.auth.signOut()]

state MainActivity {
    [*] --> DashboardCloud
    DashboardCloud : • KPIs en vivo (Encuestas, Activas, Votos)
    DashboardCloud : • Búsqueda por texto + Chips de Categoría
    DashboardCloud : • Diálogo «Mi Cuenta UNAMAD» y Modo Oscuro
}

MainActivity --> CrearEncuestaActivity : Clic «+ Crear Nueva Encuesta» o «Editar»\\n[Intent opcional con EXTRA_ID_ENCUESTA]
CrearEncuestaActivity --> MainActivity : «Guardar y Volver» / «Cancelar»\\n[finish() -> onResume() recarga Firestore]
CrearEncuestaActivity --> GestionarPreguntasActivity : «Guardar y Configurar Preguntas»\\n[EXTRA_ID_ENCUESTA + finish()]

GestionarPreguntasActivity --> MainActivity : «Finalizar Configuración»\\n[Valida >= 1 pregunta -> finish()]

MainActivity --> RegistrarVotoActivity : Clic «Votar» en tarjeta activa\\n[Pre-valida encuesta.verificarAcceso(perfil, uid)]
RegistrarVotoActivity --> MainActivity : «Cancelar» o acceso restringido\\n[finish()]
RegistrarVotoActivity --> ResultadosActivity : procesarVoto() exitoso en Firestore\\n[Diálogo -> «Ver Resultados» + finish()]

MainActivity --> ResultadosActivity : Clic «Resultados» en tarjeta\\n[EXTRA_ID_ENCUESTA]
ResultadosActivity --> RegistrarVotoActivity : Clic «Ir a Votar» (si encuesta activa)
ResultadosActivity --> MainActivity : «Volver al Panel Principal»\\n[finish()]

state ResultadosActivity {
    [*] --> EscrutinioEnVivo
    EscrutinioEnVivo : • Gráfico Circular Animado (DonutChartView)
    EscrutinioEnVivo : • Barras Porcentuales + Insignia Ganadora
    EscrutinioEnVivo : • Exportar Acta Oficial (ACTION_SEND)
    EscrutinioEnVivo : • Reiniciar Conteo a 0 (Solo Creador)
}
@enduml
"""

# ==============================================================================
# 6. FIGURA 6: DIAGRAMA DE SECUENCIA (VOTACIÓN ÚNICA VERIFICADA EN FIRESTORE)
# ==============================================================================
PUML_FIG6_SECUENCIA = """@startuml fig6_secuencia
set separator none
skinparam dpi 160
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam shadowing false
skinparam roundCorner 8
skinparam ArrowColor #1B4F72
skinparam ArrowThickness 1.2

skinparam participant {
    BackgroundColor #EBF5FB
    BorderColor #1A5276
    FontSize 11
}
skinparam actor {
    BackgroundColor #D4E6F1
    BorderColor #1A5276
}
skinparam database {
    BackgroundColor #FEF9E7
    BorderColor #B7950B
}

actor "Estudiante\\nUNAMAD" as User
participant "RegistrarVotoActivity" as VotoUI
participant "Encuesta\\n(Models.kt)" as Model
participant "FirebaseRepository" as Repo
database "Cloud Firestore\\n(votaapp-unamad-2026)" as Firestore
participant "ResultadosActivity\\n+ DonutChartView" as ResUI

User -> VotoUI : Selecciona «Votar» (EXTRA_ID_ENCUESTA)
activate VotoUI

VotoUI -> Repo : obtenerEncuestaPorId(idEncuesta)
activate Repo
Repo -> Firestore : GET encuestas/{idEncuesta}
Firestore --> Repo : Documento Encuesta + Preguntas
Repo --> VotoUI : Encuesta
deactivate Repo

VotoUI -> Repo : obtenerPerfilUsuario(uid)
activate Repo
Repo -> Firestore : GET users/{uid}
Firestore --> Repo : UsuarioPerfil (código, carrera)
Repo --> VotoUI : UsuarioPerfil
deactivate Repo

VotoUI -> Model : encuesta.verificarAcceso(perfil, uid)
activate Model
Model --> VotoUI : Pair(true, "Autorizado")
deactivate Model

VotoUI -> Repo : yaVotoUsuario(idEncuesta, uid)
activate Repo
Repo -> Firestore : GET encuestas/{id}/votos/{uid}
Firestore --> Repo : doc.exists() == false
Repo --> VotoUI : votoPrevio = false
deactivate Repo

VotoUI -> VotoUI : construirCuestionarioDinamico()
User -> VotoUI : Marca opciones y pulsa «Enviar Voto»

VotoUI -> Repo : registrarVoto(idEncuesta, participante, respuestasMap)
activate Repo
Repo -> Firestore : SET encuestas/{id}/votos/{uid}\\n{uid, participante, fechaVoto, respuestas}
Firestore --> Repo : WriteResult (Éxito)
Repo --> VotoUI : onComplete(true, null)
deactivate Repo

VotoUI -> User : Muestra MaterialAlertDialog «¡Voto Registrado!»
User -> VotoUI : Pulsa «Ver Resultados»
VotoUI -> ResUI : startActivity(Intent + EXTRA_ID_ENCUESTA)
deactivate VotoUI
activate ResUI
ResUI -> Repo : obtenerResultados(idEncuesta)
Repo -> Firestore : GET encuestas/{id} + subcolección votos
Firestore --> Repo : Documentos de votación en tiempo real
Repo --> ResUI : Estadísticas + Ganadora + Participantes
ResUI -> ResUI : Renderiza DonutChartView y ProgressBars
deactivate ResUI
@enduml
"""


def main():
    DIAG_DIR.mkdir(parents=True, exist_ok=True)

    diagrams = [
        ("fig1_casos_uso", PUML_FIG1_CASOS_USO),
        ("fig2_arquitectura", PUML_FIG2_ARQUITECTURA),
        ("fig3_modelo_er", PUML_FIG3_MODELO_ER),
        ("fig4_clases", PUML_FIG4_CLASES),
        ("fig5_navegacion", PUML_FIG5_NAVEGACION),
        ("fig6_secuencia", PUML_FIG6_SECUENCIA),
    ]

    for name, puml_content in diagrams:
        puml_path = DIAG_DIR / f"{name}.puml"
        png_path = DIAG_DIR / f"{name}.png"
        puml_path.write_text(puml_content.strip() + "\n", encoding="utf-8")
        print(f"Renderizando {name}.png via Kroki...")
        png_bytes = render_via_kroki(puml_content, "plantuml", "png")
        png_path.write_bytes(png_bytes)

        with Image.open(png_path) as im:
            w, h = im.size
        print(f"  -> OK: {png_path.name} ({w}x{h} px, {len(png_bytes)} bytes)")
        if w >= 4096 or h >= 4096:
            print(f"  [ADVERTENCIA] {png_path.name} alcanza {w}x{h} px (posible recorte Kroki)")

    # Mantener sincronizado fig6_base_datos_er.png/.puml con fig3_modelo_er para compatibilidad
    shutil.copyfile(DIAG_DIR / "fig3_modelo_er.puml", DIAG_DIR / "fig6_base_datos_er.puml")
    shutil.copyfile(DIAG_DIR / "fig3_modelo_er.png", DIAG_DIR / "fig6_base_datos_er.png")
    print("  -> Sincronizado fig6_base_datos_er.png con fig3_modelo_er.png")


if __name__ == "__main__":
    main()
