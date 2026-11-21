package com.example.proyectofinal

/**
 * ============================================================================
 * CLASES DE MODELO DE DATOS - SISTEMA DE ENCUESTAS Y VOTACIONES (UNAMAD EPISI)
 * ============================================================================
 * Representan las entidades del negocio y facilitan el paso de información
 * entre la base de datos SQLite y las interfaces de usuario (Activities).
 */

/**
 * 1. Modelo de Encuesta
 * Representa una encuesta general creada en la institución.
 */
data class Encuesta(
    val id: Long = 0,
    val titulo: String,
    val descripcion: String,
    val categoria: String,
    val activa: Boolean = true,
    val fechaCreacion: String,
    var totalPreguntas: Int = 0,
    var totalVotos: Int = 0
)

/**
 * 2. Modelo de Pregunta
 * Representa un enunciado dentro de una encuesta.
 * El tipo de pregunta puede ser:
 * - "UNICA": Selección simple (RadioButtons)
 * - "MULTIPLE": Casillas múltiples (CheckBoxes)
 */
data class Pregunta(
    val id: Long = 0,
    val idEncuesta: Long,
    val texto: String,
    val tipo: String
)

/**
 * 3. Modelo de Alternativa
 * Representa una opción de respuesta vinculada a una pregunta.
 */
data class Alternativa(
    val id: Long = 0,
    val idPregunta: Long,
    val texto: String,
    var votos: Int = 0
)

/**
 * 4. Modelo de Respuesta
 * Representa el voto individual emitido por un participante para una alternativa específica.
 */
data class Respuesta(
    val id: Long = 0,
    val idEncuesta: Long,
    val idPregunta: Long,
    val idAlternativa: Long,
    val participante: String,
    val fechaVoto: String
)

/**
 * 5. Registro de Participante
 * Utilizado para listar quiénes han votado y cuándo en la pantalla de resultados.
 */
data class ParticipanteRegistro(
    val nombre: String,
    val fechaVoto: String
)

/**
 * 6. Datos estadísticos de una alternativa para graficar en ResultadosActivity
 */
data class AlternativaEstadistica(
    val id: Long,
    val texto: String,
    val votos: Int,
    val porcentaje: Float,
    val esGanadora: Boolean
)

/**
 * 7. Datos estadísticos de una pregunta completa para ResultadosActivity
 */
data class PreguntaEstadistica(
    val pregunta: Pregunta,
    val totalVotosPregunta: Int,
    val alternativas: List<AlternativaEstadistica>
)
