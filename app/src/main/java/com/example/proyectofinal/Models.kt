package com.example.proyectofinal

/**
 * ============================================================================
 * CLASES DE MODELO DE DATOS - SISTEMA DE ENCUESTAS Y VOTACIONES (UNAMAD EPISI)
 * ============================================================================
 * Modelos sincronizados con Cloud Firestore y Firebase Authentication.
 */

data class UsuarioPerfil(
    val uid: String = "",
    val nombre: String = "",
    val codigoUniversitario: String = "",
    val carrera: String = "",
    val email: String = "",
    val fechaRegistro: Long = 0L
)

object CatalogoUnamad {
    val CARRERAS_UNAMAD = listOf(
        "Ingeniería de Sistemas e Informática",
        "Ingeniería Forestal y Medio Ambiente",
        "Ingeniería Agroindustrial",
        "Medicina Veterinaria y Zootecnia",
        "Enfermería",
        "Derecho y Ciencias Políticas",
        "Educación: Matemática y Computación",
        "Educación: Primaria e Informática",
        "Educación: Inicial y Especial",
        "Ecoturismo",
        "Administración y Negocios Internacionales",
        "Contabilidad y Finanzas"
    )

    val OPCIONES_FILTRO_CARRERA = listOf("Todas las carreras (Abierta)") + CARRERAS_UNAMAD

    /**
     * Extrae códigos de estudiante desde un bloque de texto pegado de Excel,
     * Bloc de Notas (.txt) o archivo .csv (incluso si incluye nombres o columnas).
     */
    fun extraerCodigosDesdeTexto(textoBruto: String): List<String> {
        if (textoBruto.isBlank()) return emptyList()
        // Primero buscamos códigos numéricos/alfanuméricos típicos de matrícula (4 a 14 dígitos)
        val regexCodigo = Regex("\\b\\d{4,14}[A-Za-z0-9-]*\\b")
        val encontrados = regexCodigo.findAll(textoBruto)
            .map { it.value.trim().uppercase() }
            .distinct()
            .toList()
        if (encontrados.isNotEmpty()) return encontrados

        // Fallback si usan códigos alfanuméricos personalizados separados por coma, salto o tab
        return textoBruto.split(',', ';', '\n', '\r', '\t', ' ')
            .map { it.trim().uppercase() }
            .filter { it.length >= 3 }
            .distinct()
    }
}

data class Alternativa(
    val id: String = "",
    val texto: String = "",
    var votos: Int = 0
)

data class Pregunta(
    val id: String = "",
    val texto: String = "",
    val tipo: String = "UNICA", // "UNICA" o "MULTIPLE"
    val alternativas: List<Alternativa> = emptyList()
)

data class Encuesta(
    val id: String = "",
    val titulo: String = "",
    val descripcion: String = "",
    val categoria: String = "General",
    val activa: Boolean = true,
    val fechaCreacion: String = "",
    val creadorUid: String = "",
    val creadorNombre: String = "",
    val carreraRestringida: String = "TODAS",
    val codigosPermitidos: String = "",
    val preguntas: List<Pregunta> = emptyList(),
    var totalPreguntas: Int = 0,
    var totalVotos: Int = 0
) {
    fun listaCodigosAutorizados(): List<String> =
        CatalogoUnamad.extraerCodigosDesdeTexto(codigosPermitidos)

    fun tieneRestriccionAcceso(): Boolean =
        (carreraRestringida.isNotBlank() && carreraRestringida != "TODAS") ||
            listaCodigosAutorizados().isNotEmpty()

    fun etiquetaRestriccion(): String {
        val cods = listaCodigosAutorizados()
        val tieneCarrera = carreraRestringida.isNotBlank() && carreraRestringida != "TODAS"
        return when {
            tieneCarrera && cods.isNotEmpty() -> "$carreraRestringida • ${cods.size} cód."
            tieneCarrera -> "Solo: $carreraRestringida"
            cods.isNotEmpty() -> "Grupo cerrado (${cods.size} códigos)"
            else -> "Abierta a toda la UNAMAD"
        }
    }

    /**
     * Verifica si un estudiante cumple la carrera y/o lista de códigos de la encuesta.
     * El creador de la encuesta siempre tiene acceso.
     */
    fun verificarAcceso(perfil: UsuarioPerfil?, uidActual: String?): Pair<Boolean, String> {
        if (!uidActual.isNullOrBlank() && uidActual == creadorUid) {
            return true to "Creador de la encuesta"
        }

        val tieneCarrera = carreraRestringida.isNotBlank() && carreraRestringida != "TODAS"
        val cods = listaCodigosAutorizados()

        if (!tieneCarrera && cods.isEmpty()) {
            return true to "Acceso abierto"
        }

        val miCodigo = perfil?.codigoUniversitario?.trim()?.uppercase() ?: ""
        val miCarrera = perfil?.carrera?.trim() ?: ""

        if (tieneCarrera) {
            if (miCarrera.isBlank()) {
                return false to "Falta seleccionar tu Escuela Profesional en «Cuenta» para participar en esta encuesta de $carreraRestringida."
            }
            if (!miCarrera.equals(carreraRestringida, ignoreCase = true)) {
                return false to "Esta encuesta es exclusiva para estudiantes de $carreraRestringida (tu perfil indica: $miCarrera)."
            }
        }

        if (cods.isNotEmpty()) {
            if (miCodigo.isBlank()) {
                return false to "Esta encuesta requiere validar tu código universitario. Regístralo en el botón «Cuenta» arriba a la derecha."
            }
            val autorizado = cods.any { token ->
                miCodigo == token || (token.length in 4..6 && miCodigo.startsWith(token))
            }
            if (!autorizado) {
                return false to "Tu código universitario ($miCodigo) no se encuentra en el padrón autorizado de esta encuesta (${cods.size} estudiantes habilitados)."
            }
        }

        return true to "Autorizado"
    }
}

data class ParticipanteRegistro(
    val uid: String = "",
    val nombre: String = "",
    val fechaVoto: String = ""
)

data class AlternativaEstadistica(
    val id: String,
    val texto: String,
    val votos: Int,
    val porcentaje: Float,
    val esGanadora: Boolean
)

data class PreguntaEstadistica(
    val pregunta: Pregunta,
    val totalVotosPregunta: Int,
    val alternativas: List<AlternativaEstadistica>
)
