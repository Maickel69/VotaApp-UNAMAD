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
    val email: String = "",
    val fechaRegistro: Long = 0L
)

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
    val preguntas: List<Pregunta> = emptyList(),
    var totalPreguntas: Int = 0,
    var totalVotos: Int = 0
)

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
