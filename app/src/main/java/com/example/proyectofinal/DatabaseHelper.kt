package com.example.proyectofinal

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * ============================================================================
 * GESTOR DE BASE DE DATOS SQLITE (SQLiteOpenHelper)
 * ============================================================================
 * Proyecto: Sistema de Encuestas y Votaciones UNAMAD - EPISI
 * 
 * Gestiona de forma 100% nativa la creación, actualización y operaciones
 * CRUD (Crear, Leer, Actualizar y Eliminar) sobre las tablas relacionales:
 *  1. encuestas
 *  2. preguntas
 *  3. alternativas
 *  4. respuestas
 */
class DatabaseHelper(context: Context) : SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        private const val DATABASE_NAME = "encuestas_unamad.db"
        private const val DATABASE_VERSION = 1

        // 1. Tabla ENCUESTAS
        const val TABLA_ENCUESTAS = "encuestas"
        const val COL_ENCUESTA_ID = "id_encuesta"
        const val COL_ENCUESTA_TITULO = "titulo"
        const val COL_ENCUESTA_DESCRIPCION = "descripcion"
        const val COL_ENCUESTA_CATEGORIA = "categoria"
        const val COL_ENCUESTA_ACTIVA = "activa"
        const val COL_ENCUESTA_FECHA = "fecha_creacion"

        // 2. Tabla PREGUNTAS
        const val TABLA_PREGUNTAS = "preguntas"
        const val COL_PREGUNTA_ID = "id_pregunta"
        const val COL_PREGUNTA_ENCUESTA_ID = "id_encuesta"
        const val COL_PREGUNTA_TEXTO = "texto_pregunta"
        const val COL_PREGUNTA_TIPO = "tipo_pregunta" // "UNICA" o "MULTIPLE"

        // 3. Tabla ALTERNATIVAS
        const val TABLA_ALTERNATIVAS = "alternativas"
        const val COL_ALTERNATIVA_ID = "id_alternativa"
        const val COL_ALTERNATIVA_PREGUNTA_ID = "id_pregunta"
        const val COL_ALTERNATIVA_TEXTO = "texto_alternativa"
        const val COL_ALTERNATIVA_VOTOS = "votos"

        // 4. Tabla RESPUESTAS
        const val TABLA_RESPUESTAS = "respuestas"
        const val COL_RESPUESTA_ID = "id_respuesta"
        const val COL_RESPUESTA_ENCUESTA_ID = "id_encuesta"
        const val COL_RESPUESTA_PREGUNTA_ID = "id_pregunta"
        const val COL_RESPUESTA_ALTERNATIVA_ID = "id_alternativa"
        const val COL_RESPUESTA_PARTICIPANTE = "participante"
        const val COL_RESPUESTA_FECHA = "fecha_voto"
    }

    // Configuración inicial de la conexión SQLite
    override fun onConfigure(db: SQLiteDatabase) {
        super.onConfigure(db)
        // Habilitamos las restricciones de clave foránea con borrado en cascada (CASCADE)
        db.setForeignKeyConstraintsEnabled(true)
    }

    // Creación de las tablas relacionales y carga de datos iniciales
    override fun onCreate(db: SQLiteDatabase) {
        // 1. Crear Tabla ENCUESTAS
        val sqlEncuestas = """
            CREATE TABLE $TABLA_ENCUESTAS (
                $COL_ENCUESTA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                $COL_ENCUESTA_TITULO TEXT NOT NULL,
                $COL_ENCUESTA_DESCRIPCION TEXT NOT NULL,
                $COL_ENCUESTA_CATEGORIA TEXT NOT NULL,
                $COL_ENCUESTA_ACTIVA INTEGER DEFAULT 1,
                $COL_ENCUESTA_FECHA TEXT NOT NULL
            );
        """.trimIndent()

        // 2. Crear Tabla PREGUNTAS
        val sqlPreguntas = """
            CREATE TABLE $TABLA_PREGUNTAS (
                $COL_PREGUNTA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                $COL_PREGUNTA_ENCUESTA_ID INTEGER NOT NULL,
                $COL_PREGUNTA_TEXTO TEXT NOT NULL,
                $COL_PREGUNTA_TIPO TEXT NOT NULL,
                FOREIGN KEY ($COL_PREGUNTA_ENCUESTA_ID) REFERENCES $TABLA_ENCUESTAS($COL_ENCUESTA_ID) ON DELETE CASCADE
            );
        """.trimIndent()

        // 3. Crear Tabla ALTERNATIVAS
        val sqlAlternativas = """
            CREATE TABLE $TABLA_ALTERNATIVAS (
                $COL_ALTERNATIVA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                $COL_ALTERNATIVA_PREGUNTA_ID INTEGER NOT NULL,
                $COL_ALTERNATIVA_TEXTO TEXT NOT NULL,
                $COL_ALTERNATIVA_VOTOS INTEGER DEFAULT 0,
                FOREIGN KEY ($COL_ALTERNATIVA_PREGUNTA_ID) REFERENCES $TABLA_PREGUNTAS($COL_PREGUNTA_ID) ON DELETE CASCADE
            );
        """.trimIndent()

        // 4. Crear Tabla RESPUESTAS
        val sqlRespuestas = """
            CREATE TABLE $TABLA_RESPUESTAS (
                $COL_RESPUESTA_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                $COL_RESPUESTA_ENCUESTA_ID INTEGER NOT NULL,
                $COL_RESPUESTA_PREGUNTA_ID INTEGER NOT NULL,
                $COL_RESPUESTA_ALTERNATIVA_ID INTEGER NOT NULL,
                $COL_RESPUESTA_PARTICIPANTE TEXT NOT NULL,
                $COL_RESPUESTA_FECHA TEXT NOT NULL,
                FOREIGN KEY ($COL_RESPUESTA_ENCUESTA_ID) REFERENCES $TABLA_ENCUESTAS($COL_ENCUESTA_ID) ON DELETE CASCADE,
                FOREIGN KEY ($COL_RESPUESTA_PREGUNTA_ID) REFERENCES $TABLA_PREGUNTAS($COL_PREGUNTA_ID) ON DELETE CASCADE,
                FOREIGN KEY ($COL_RESPUESTA_ALTERNATIVA_ID) REFERENCES $TABLA_ALTERNATIVAS($COL_ALTERNATIVA_ID) ON DELETE CASCADE
            );
        """.trimIndent()

        db.execSQL(sqlEncuestas)
        db.execSQL(sqlPreguntas)
        db.execSQL(sqlAlternativas)
        db.execSQL(sqlRespuestas)

        // 5. Insertar datos de prueba iniciales (Semilla de datos)
        insertarDatosIniciales(db)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        // Si cambia la versión de la BD, se recrean las tablas limpiamente
        db.execSQL("DROP TABLE IF EXISTS $TABLA_RESPUESTAS")
        db.execSQL("DROP TABLE IF EXISTS $TABLA_ALTERNATIVAS")
        db.execSQL("DROP TABLE IF EXISTS $TABLA_PREGUNTAS")
        db.execSQL("DROP TABLE IF EXISTS $TABLA_ENCUESTAS")
        onCreate(db)
    }

    /**
     * Inserta 2 encuestas completas con preguntas, alternativas y votos iniciales
     * para que la aplicación muestre información realista desde el primer inicio.
     */
    private fun insertarDatosIniciales(db: SQLiteDatabase) {
        val formatoFecha = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())
        val fechaActual = formatoFecha.format(Date())

        // ====================================================================
        // ENCUESTA 1: Satisfacción de Servicios Académicos UNAMAD
        // ====================================================================
        val cvE1 = ContentValues().apply {
            put(COL_ENCUESTA_TITULO, "Encuesta de Satisfacción de Servicios Académicos UNAMAD")
            put(COL_ENCUESTA_DESCRIPCION, "Evaluación general sobre la calidad académica, infraestructura y atención brindada a los estudiantes.")
            put(COL_ENCUESTA_CATEGORIA, "Satisfacción")
            put(COL_ENCUESTA_ACTIVA, 1)
            put(COL_ENCUESTA_FECHA, fechaActual)
        }
        val idE1 = db.insert(TABLA_ENCUESTAS, null, cvE1)

        // Encuesta 1 - Pregunta 1: Calificación (ÚNICA)
        val cvP1 = ContentValues().apply {
            put(COL_PREGUNTA_ENCUESTA_ID, idE1)
            put(COL_PREGUNTA_TEXTO, "¿Cómo califica la calidad y atención de los servicios académicos recibidos?")
            put(COL_PREGUNTA_TIPO, "UNICA")
        }
        val idP1 = db.insert(TABLA_PREGUNTAS, null, cvP1)

        val idA1_1 = insertarAlternativaDb(db, idP1, "Excelente", 2)
        val idA1_2 = insertarAlternativaDb(db, idP1, "Bueno", 1)
        val idA1_3 = insertarAlternativaDb(db, idP1, "Regular", 0)
        val idA1_4 = insertarAlternativaDb(db, idP1, "Deficiente", 0)

        // Encuesta 1 - Pregunta 2: Aspectos a mejorar (MÚLTIPLE)
        val cvP2 = ContentValues().apply {
            put(COL_PREGUNTA_ENCUESTA_ID, idE1)
            put(COL_PREGUNTA_TEXTO, "¿Qué aspectos institucionales considera prioritario mejorar?")
            put(COL_PREGUNTA_TIPO, "MULTIPLE")
        }
        val idP2 = db.insert(TABLA_PREGUNTAS, null, cvP2)

        val idA2_1 = insertarAlternativaDb(db, idP2, "Infraestructura y laboratorios", 2)
        val idA2_2 = insertarAlternativaDb(db, idP2, "Plataforma virtual y conectividad", 1)
        val idA2_3 = insertarAlternativaDb(db, idP2, "Rapidez en trámites administrativos", 2)
        val idA2_4 = insertarAlternativaDb(db, idP2, "Ampliación de horarios de biblioteca", 1)

        // Encuesta 1 - Pregunta 3: Recomendación (ÚNICA)
        val cvP3 = ContentValues().apply {
            put(COL_PREGUNTA_ENCUESTA_ID, idE1)
            put(COL_PREGUNTA_TEXTO, "¿Recomendaría la carrera profesional a futuros postulantes?")
            put(COL_PREGUNTA_TIPO, "UNICA")
        }
        val idP3 = db.insert(TABLA_PREGUNTAS, null, cvP3)

        val idA3_1 = insertarAlternativaDb(db, idP3, "Definitivamente Sí", 2)
        val idA3_2 = insertarAlternativaDb(db, idP3, "Probablemente Sí", 1)
        val idA3_3 = insertarAlternativaDb(db, idP3, "No estoy seguro", 0)
        val idA3_4 = insertarAlternativaDb(db, idP3, "No la recomendaría", 0)

        // Registrar votos iniciales para 3 participantes en la Encuesta 1
        insertarRespuestaDb(db, idE1, idP1, idA1_1, "Carlos Mendoza - 202201", "2026-11-01 10:15")
        insertarRespuestaDb(db, idE1, idP2, idA2_1, "Carlos Mendoza - 202201", "2026-11-01 10:15")
        insertarRespuestaDb(db, idE1, idP2, idA2_3, "Carlos Mendoza - 202201", "2026-11-01 10:15")
        insertarRespuestaDb(db, idE1, idP3, idA3_1, "Carlos Mendoza - 202201", "2026-11-01 10:15")

        insertarRespuestaDb(db, idE1, idP1, idA1_1, "María Flores - 202305", "2026-11-01 11:30")
        insertarRespuestaDb(db, idE1, idP2, idA2_2, "María Flores - 202305", "2026-11-01 11:30")
        insertarRespuestaDb(db, idE1, idP2, idA2_4, "María Flores - 202305", "2026-11-01 11:30")
        insertarRespuestaDb(db, idE1, idP3, idA3_1, "María Flores - 202305", "2026-11-01 11:30")

        insertarRespuestaDb(db, idE1, idP1, idA1_2, "Juan Quispe - 202110", "2026-11-02 09:45")
        insertarRespuestaDb(db, idE1, idP2, idA2_1, "Juan Quispe - 202110", "2026-11-02 09:45")
        insertarRespuestaDb(db, idE1, idP2, idA2_3, "Juan Quispe - 202110", "2026-11-02 09:45")
        insertarRespuestaDb(db, idE1, idP3, idA3_2, "Juan Quispe - 202110", "2026-11-02 09:45")

        // ====================================================================
        // ENCUESTA 2: Elección de Delegado Estudiantil EPISI 2026-II
        // ====================================================================
        val cvE2 = ContentValues().apply {
            put(COL_ENCUESTA_TITULO, "Elección de Delegado Estudiantil EPISI 2026-II")
            put(COL_ENCUESTA_DESCRIPCION, "Proceso democrático de elección del representante estudiantil para el semestre académico actual.")
            put(COL_ENCUESTA_CATEGORIA, "Votación")
            put(COL_ENCUESTA_ACTIVA, 1)
            put(COL_ENCUESTA_FECHA, fechaActual)
        }
        val idE2 = db.insert(TABLA_ENCUESTAS, null, cvE2)

        // Encuesta 2 - Pregunta 1: Candidato (ÚNICA)
        val cvP2_1 = ContentValues().apply {
            put(COL_PREGUNTA_ENCUESTA_ID, idE2)
            put(COL_PREGUNTA_TEXTO, "Seleccione a su candidato preferido para Delegado General EPISI:")
            put(COL_PREGUNTA_TIPO, "UNICA")
        }
        val idP2_1 = db.insert(TABLA_PREGUNTAS, null, cvP2_1)

        val idA2_1_1 = insertarAlternativaDb(db, idP2_1, "Lista 1: Innovación y Liderazgo (Pres. Juan Ramos)", 3)
        val idA2_1_2 = insertarAlternativaDb(db, idP2_1, "Lista 2: Unidad y Transparencia (Pres. Laura Vega)", 1)
        val idA2_1_3 = insertarAlternativaDb(db, idP2_1, "Voto en Blanco", 0)

        // Encuesta 2 - Pregunta 2: Prioridad estudiantil (ÚNICA)
        val cvP2_2 = ContentValues().apply {
            put(COL_PREGUNTA_ENCUESTA_ID, idE2)
            put(COL_PREGUNTA_TEXTO, "¿Qué propuesta considera más urgente para el semestre?")
            put(COL_PREGUNTA_TIPO, "UNICA")
        }
        val idP2_2 = db.insert(TABLA_PREGUNTAS, null, cvP2_2)

        val idA2_2_1 = insertarAlternativaDb(db, idP2_2, "Talleres extracurriculares de programación", 2)
        val idA2_2_2 = insertarAlternativaDb(db, idP2_2, "Renovación de equipos de cómputo", 2)
        val idA2_2_3 = insertarAlternativaDb(db, idP2_2, "Organización de congresos y ferias tecnológicas", 0)

        // Registrar votos iniciales para 4 participantes en la Encuesta 2
        insertarRespuestaDb(db, idE2, idP2_1, idA2_1_1, "Ana Mamani - 202401", "2026-11-02 14:10")
        insertarRespuestaDb(db, idE2, idP2_2, idA2_2_1, "Ana Mamani - 202401", "2026-11-02 14:10")

        insertarRespuestaDb(db, idE2, idP2_1, idA2_1_1, "Luis Castro - 202214", "2026-11-02 15:20")
        insertarRespuestaDb(db, idE2, idP2_2, idA2_2_2, "Luis Castro - 202214", "2026-11-02 15:20")

        insertarRespuestaDb(db, idE2, idP2_1, idA2_1_2, "Diana Ríos - 202319", "2026-11-02 16:05")
        insertarRespuestaDb(db, idE2, idP2_2, idA2_2_1, "Diana Ríos - 202319", "2026-11-02 16:05")

        insertarRespuestaDb(db, idE2, idP2_1, idA2_1_1, "José Salazar - 202102", "2026-11-02 17:00")
        insertarRespuestaDb(db, idE2, idP2_2, idA2_2_2, "José Salazar - 202102", "2026-11-02 17:00")
    }

    private fun insertarAlternativaDb(db: SQLiteDatabase, idPregunta: Long, texto: String, votosIniciales: Int): Long {
        val cv = ContentValues().apply {
            put(COL_ALTERNATIVA_PREGUNTA_ID, idPregunta)
            put(COL_ALTERNATIVA_TEXTO, texto)
            put(COL_ALTERNATIVA_VOTOS, votosIniciales)
        }
        return db.insert(TABLA_ALTERNATIVAS, null, cv)
    }

    private fun insertarRespuestaDb(db: SQLiteDatabase, idEncuesta: Long, idPregunta: Long, idAlternativa: Long, participante: String, fecha: String) {
        val cv = ContentValues().apply {
            put(COL_RESPUESTA_ENCUESTA_ID, idEncuesta)
            put(COL_RESPUESTA_PREGUNTA_ID, idPregunta)
            put(COL_RESPUESTA_ALTERNATIVA_ID, idAlternativa)
            put(COL_RESPUESTA_PARTICIPANTE, participante)
            put(COL_RESPUESTA_FECHA, fecha)
        }
        db.insert(TABLA_RESPUESTAS, null, cv)
    }

    // ========================================================================
    // OPERACIONES CRUD: ENCUESTAS
    // ========================================================================

    /**
     * 1. Crear una nueva encuesta
     */
    fun crearEncuesta(titulo: String, descripcion: String, categoria: String, activa: Boolean = true): Long {
        val db = writableDatabase
        val formatoFecha = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())
        val fecha = formatoFecha.format(Date())

        val cv = ContentValues().apply {
            put(COL_ENCUESTA_TITULO, titulo.trim())
            put(COL_ENCUESTA_DESCRIPCION, descripcion.trim())
            put(COL_ENCUESTA_CATEGORIA, categoria)
            put(COL_ENCUESTA_ACTIVA, if (activa) 1 else 0)
            put(COL_ENCUESTA_FECHA, fecha)
        }
        return db.insert(TABLA_ENCUESTAS, null, cv)
    }

    /**
     * 2. Actualizar datos de una encuesta existente
     */
    fun actualizarEncuesta(idEncuesta: Long, titulo: String, descripcion: String, categoria: String, activa: Boolean): Boolean {
        val db = writableDatabase
        val cv = ContentValues().apply {
            put(COL_ENCUESTA_TITULO, titulo.trim())
            put(COL_ENCUESTA_DESCRIPCION, descripcion.trim())
            put(COL_ENCUESTA_CATEGORIA, categoria)
            put(COL_ENCUESTA_ACTIVA, if (activa) 1 else 0)
        }
        val filasAfectadas = db.update(
            TABLA_ENCUESTAS,
            cv,
            "$COL_ENCUESTA_ID = ?",
            arrayOf(idEncuesta.toString())
        )
        return filasAfectadas > 0
    }

    /**
     * 3. Eliminar una encuesta (y sus preguntas, alternativas y respuestas en cascada)
     */
    fun eliminarEncuesta(idEncuesta: Long): Boolean {
        val db = writableDatabase
        // Por seguridad explícita garantizamos el borrado en orden
        db.beginTransaction()
        return try {
            db.delete(TABLA_RESPUESTAS, "$COL_RESPUESTA_ENCUESTA_ID = ?", arrayOf(idEncuesta.toString()))
            val subquery = "SELECT $COL_PREGUNTA_ID FROM $TABLA_PREGUNTAS WHERE $COL_PREGUNTA_ENCUESTA_ID = ?"
            db.delete(TABLA_ALTERNATIVAS, "$COL_ALTERNATIVA_PREGUNTA_ID IN ($subquery)", arrayOf(idEncuesta.toString()))
            db.delete(TABLA_PREGUNTAS, "$COL_PREGUNTA_ENCUESTA_ID = ?", arrayOf(idEncuesta.toString()))
            val filas = db.delete(TABLA_ENCUESTAS, "$COL_ENCUESTA_ID = ?", arrayOf(idEncuesta.toString()))
            db.setTransactionSuccessful()
            filas > 0
        } finally {
            db.endTransaction()
        }
    }

    /**
     * 4. Obtener una encuesta por su ID
     */
    fun obtenerEncuestaPorId(idEncuesta: Long): Encuesta? {
        val db = readableDatabase
        val cursor = db.query(
            TABLA_ENCUESTAS,
            null,
            "$COL_ENCUESTA_ID = ?",
            arrayOf(idEncuesta.toString()),
            null, null, null
        )

        var encuesta: Encuesta? = null
        if (cursor.moveToFirst()) {
            val id = cursor.getLong(cursor.getColumnIndexOrThrow(COL_ENCUESTA_ID))
            val titulo = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_TITULO))
            val descripcion = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_DESCRIPCION))
            val categoria = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_CATEGORIA))
            val activa = cursor.getInt(cursor.getColumnIndexOrThrow(COL_ENCUESTA_ACTIVA)) == 1
            val fecha = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_FECHA))

            encuesta = Encuesta(id = id.toString(), titulo = titulo, descripcion = descripcion, categoria = categoria, activa = activa, fechaCreacion = fecha)
            encuesta.totalPreguntas = contarPreguntasDeEncuesta(id)
            encuesta.totalVotos = contarParticipantesUnicos(id)
        }
        cursor.close()
        return encuesta
    }

    /**
     * 5. Listar encuestas con filtro opcional ("TODAS", "ACTIVAS", "CERRADAS")
     */
    fun listarEncuestas(filtro: String = "TODAS"): List<Encuesta> {
        val lista = ArrayList<Encuesta>()
        val db = readableDatabase

        val seleccion: String? = when (filtro) {
            "ACTIVAS" -> "$COL_ENCUESTA_ACTIVA = 1"
            "CERRADAS" -> "$COL_ENCUESTA_ACTIVA = 0"
            else -> null
        }

        val cursor = db.query(
            TABLA_ENCUESTAS,
            null,
            seleccion,
            null,
            null, null,
            "$COL_ENCUESTA_ID DESC"
        )

        if (cursor.moveToFirst()) {
            do {
                val id = cursor.getLong(cursor.getColumnIndexOrThrow(COL_ENCUESTA_ID))
                val titulo = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_TITULO))
                val descripcion = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_DESCRIPCION))
                val categoria = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_CATEGORIA))
                val activa = cursor.getInt(cursor.getColumnIndexOrThrow(COL_ENCUESTA_ACTIVA)) == 1
                val fecha = cursor.getString(cursor.getColumnIndexOrThrow(COL_ENCUESTA_FECHA))

                val enc = Encuesta(id = id.toString(), titulo = titulo, descripcion = descripcion, categoria = categoria, activa = activa, fechaCreacion = fecha)
                enc.totalPreguntas = contarPreguntasDeEncuesta(id)
                enc.totalVotos = contarParticipantesUnicos(id)
                lista.add(enc)
            } while (cursor.moveToNext())
        }
        cursor.close()
        return lista
    }

    /**
     * 6. Contadores de resumen general para la cabecera de MainActivity
     * Retorna Triple(totalEncuestas, encuestasActivas, totalVotosGlobales)
     */
    fun obtenerConteoGeneral(): Triple<Int, Int, Int> {
        val db = readableDatabase
        var totalEncuestas = 0
        var activas = 0
        var totalVotos = 0

        // Total encuestas
        val c1 = db.rawQuery("SELECT COUNT(*) FROM $TABLA_ENCUESTAS", null)
        if (c1.moveToFirst()) totalEncuestas = c1.getInt(0)
        c1.close()

        // Activas
        val c2 = db.rawQuery("SELECT COUNT(*) FROM $TABLA_ENCUESTAS WHERE $COL_ENCUESTA_ACTIVA = 1", null)
        if (c2.moveToFirst()) activas = c2.getInt(0)
        c2.close()

        // Total de votos (participaciones únicas por encuesta)
        val c3 = db.rawQuery("SELECT COUNT(DISTINCT $COL_RESPUESTA_ENCUESTA_ID || '-' || LOWER(TRIM($COL_RESPUESTA_PARTICIPANTE))) FROM $TABLA_RESPUESTAS", null)
        if (c3.moveToFirst()) totalVotos = c3.getInt(0)
        c3.close()

        return Triple(totalEncuestas, activas, totalVotos)
    }

    // ========================================================================
    // OPERACIONES CRUD: PREGUNTAS Y ALTERNATIVAS
    // ========================================================================

    /**
     * 7. Insertar una pregunta con sus alternativas dentro de una transacción
     */
    fun insertarPreguntaConAlternativas(
        idEncuesta: Long,
        textoPregunta: String,
        tipoPregunta: String,
        alternativas: List<String>
    ): Long {
        val db = writableDatabase
        db.beginTransaction()
        return try {
            val cvP = ContentValues().apply {
                put(COL_PREGUNTA_ENCUESTA_ID, idEncuesta)
                put(COL_PREGUNTA_TEXTO, textoPregunta.trim())
                put(COL_PREGUNTA_TIPO, tipoPregunta)
            }
            val idPregunta = db.insert(TABLA_PREGUNTAS, null, cvP)

            for (alt in alternativas) {
                val textoAlt = alt.trim()
                if (textoAlt.isNotEmpty()) {
                    val cvA = ContentValues().apply {
                        put(COL_ALTERNATIVA_PREGUNTA_ID, idPregunta)
                        put(COL_ALTERNATIVA_TEXTO, textoAlt)
                        put(COL_ALTERNATIVA_VOTOS, 0)
                    }
                    db.insert(TABLA_ALTERNATIVAS, null, cvA)
                }
            }
            db.setTransactionSuccessful()
            idPregunta
        } finally {
            db.endTransaction()
        }
    }

    /**
     * 8. Actualizar el enunciado, tipo y alternativas de una pregunta existente
     */
    fun actualizarPreguntaConAlternativas(
        idPregunta: Long,
        nuevoTexto: String,
        nuevoTipo: String,
        nuevasAlternativas: List<String>
    ): Boolean {
        val db = writableDatabase
        db.beginTransaction()
        return try {
            // Actualizar pregunta
            val cvP = ContentValues().apply {
                put(COL_PREGUNTA_TEXTO, nuevoTexto.trim())
                put(COL_PREGUNTA_TIPO, nuevoTipo)
            }
            db.update(TABLA_PREGUNTAS, cvP, "$COL_PREGUNTA_ID = ?", arrayOf(idPregunta.toString()))

            // Reemplazar alternativas
            db.delete(TABLA_ALTERNATIVAS, "$COL_ALTERNATIVA_PREGUNTA_ID = ?", arrayOf(idPregunta.toString()))
            for (alt in nuevasAlternativas) {
                val textoAlt = alt.trim()
                if (textoAlt.isNotEmpty()) {
                    val cvA = ContentValues().apply {
                        put(COL_ALTERNATIVA_PREGUNTA_ID, idPregunta)
                        put(COL_ALTERNATIVA_TEXTO, textoAlt)
                        put(COL_ALTERNATIVA_VOTOS, 0)
                    }
                    db.insert(TABLA_ALTERNATIVAS, null, cvA)
                }
            }
            db.setTransactionSuccessful()
            true
        } finally {
            db.endTransaction()
        }
    }

    /**
     * 9. Eliminar una pregunta
     */
    fun eliminarPregunta(idPregunta: Long): Boolean {
        val db = writableDatabase
        db.beginTransaction()
        return try {
            db.delete(TABLA_RESPUESTAS, "$COL_RESPUESTA_PREGUNTA_ID = ?", arrayOf(idPregunta.toString()))
            db.delete(TABLA_ALTERNATIVAS, "$COL_ALTERNATIVA_PREGUNTA_ID = ?", arrayOf(idPregunta.toString()))
            val filas = db.delete(TABLA_PREGUNTAS, "$COL_PREGUNTA_ID = ?", arrayOf(idPregunta.toString()))
            db.setTransactionSuccessful()
            filas > 0
        } finally {
            db.endTransaction()
        }
    }

    /**
     * 10. Listar todas las preguntas de una encuesta
     */
    fun listarPreguntasDeEncuesta(idEncuesta: Long): List<Pregunta> {
        val lista = ArrayList<Pregunta>()
        val db = readableDatabase
        val cursor = db.query(
            TABLA_PREGUNTAS,
            null,
            "$COL_PREGUNTA_ENCUESTA_ID = ?",
            arrayOf(idEncuesta.toString()),
            null, null,
            "$COL_PREGUNTA_ID ASC"
        )
        if (cursor.moveToFirst()) {
            do {
                val id = cursor.getLong(cursor.getColumnIndexOrThrow(COL_PREGUNTA_ID))
                val texto = cursor.getString(cursor.getColumnIndexOrThrow(COL_PREGUNTA_TEXTO))
                val tipo = cursor.getString(cursor.getColumnIndexOrThrow(COL_PREGUNTA_TIPO))
                lista.add(Pregunta(id = id.toString(), texto = texto, tipo = tipo))
            } while (cursor.moveToNext())
        }
        cursor.close()
        return lista
    }

    /**
     * 11. Listar todas las alternativas de una pregunta
     */
    fun listarAlternativasDePregunta(idPregunta: Long): List<Alternativa> {
        val lista = ArrayList<Alternativa>()
        val db = readableDatabase
        val cursor = db.query(
            TABLA_ALTERNATIVAS,
            null,
            "$COL_ALTERNATIVA_PREGUNTA_ID = ?",
            arrayOf(idPregunta.toString()),
            null, null,
            "$COL_ALTERNATIVA_ID ASC"
        )
        if (cursor.moveToFirst()) {
            do {
                val id = cursor.getLong(cursor.getColumnIndexOrThrow(COL_ALTERNATIVA_ID))
                val texto = cursor.getString(cursor.getColumnIndexOrThrow(COL_ALTERNATIVA_TEXTO))
                val votos = cursor.getInt(cursor.getColumnIndexOrThrow(COL_ALTERNATIVA_VOTOS))
                lista.add(Alternativa(id = id.toString(), texto = texto, votos = votos))
            } while (cursor.moveToNext())
        }
        cursor.close()
        return lista
    }

    /**
     * 12. Contar la cantidad de preguntas registradas en una encuesta
     */
    fun contarPreguntasDeEncuesta(idEncuesta: Long): Int {
        val db = readableDatabase
        val cursor = db.rawQuery(
            "SELECT COUNT(*) FROM $TABLA_PREGUNTAS WHERE $COL_PREGUNTA_ENCUESTA_ID = ?",
            arrayOf(idEncuesta.toString())
        )
        var total = 0
        if (cursor.moveToFirst()) {
            total = cursor.getInt(0)
        }
        cursor.close()
        return total
    }

    // ========================================================================
    // OPERACIONES DE VOTACIÓN, RESULTADOS Y ESTADÍSTICAS
    // ========================================================================

    /**
     * 13. Verificar si un participante ya emitió su voto en una encuesta específica
     */
    fun yaVotoParticipante(idEncuesta: Long, participante: String): Boolean {
        val db = readableDatabase
        val cursor = db.rawQuery(
            """
            SELECT 1 FROM $TABLA_RESPUESTAS 
            WHERE $COL_RESPUESTA_ENCUESTA_ID = ? 
              AND LOWER(TRIM($COL_RESPUESTA_PARTICIPANTE)) = LOWER(TRIM(?))
            LIMIT 1
            """.trimIndent(),
            arrayOf(idEncuesta.toString(), participante)
        )
        val existe = cursor.moveToFirst()
        cursor.close()
        return existe
    }

    /**
     * 14. Registrar los votos de un participante dentro de una transacción SQLite.
     * Inserta cada opción en `respuestas` e incrementa el contador `votos` en `alternativas`.
     * @param votosPorPregunta Lista de pares (idPregunta, idAlternativa)
     */
    fun registrarVotos(
        idEncuesta: Long,
        participante: String,
        votosPorPregunta: List<Pair<Long, Long>>
    ): Boolean {
        val db = writableDatabase
        val formatoFecha = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault())
        val fechaVoto = formatoFecha.format(Date())
        val nombreLimpio = participante.trim()

        db.beginTransaction()
        return try {
            // Verificación preventiva contra doble voto
            if (yaVotoParticipante(idEncuesta, nombreLimpio)) {
                return false
            }

            for (par in votosPorPregunta) {
                val idPregunta = par.first
                val idAlternativa = par.second

                // Insertar registro en tabla respuestas
                val cv = ContentValues().apply {
                    put(COL_RESPUESTA_ENCUESTA_ID, idEncuesta)
                    put(COL_RESPUESTA_PREGUNTA_ID, idPregunta)
                    put(COL_RESPUESTA_ALTERNATIVA_ID, idAlternativa)
                    put(COL_RESPUESTA_PARTICIPANTE, nombreLimpio)
                    put(COL_RESPUESTA_FECHA, fechaVoto)
                }
                db.insert(TABLA_RESPUESTAS, null, cv)

                // Incrementar contador de votos en alternativas
                db.execSQL(
                    "UPDATE $TABLA_ALTERNATIVAS SET $COL_ALTERNATIVA_VOTOS = $COL_ALTERNATIVA_VOTOS + 1 WHERE $COL_ALTERNATIVA_ID = ?",
                    arrayOf(idAlternativa.toString())
                )
            }

            db.setTransactionSuccessful()
            true
        } finally {
            db.endTransaction()
        }
    }

    /**
     * 15. Reiniciar todos los votos de una encuesta a 0
     */
    fun reiniciarVotosEncuesta(idEncuesta: Long): Boolean {
        val db = writableDatabase
        db.beginTransaction()
        return try {
            // Eliminar respuestas
            db.delete(TABLA_RESPUESTAS, "$COL_RESPUESTA_ENCUESTA_ID = ?", arrayOf(idEncuesta.toString()))

            // Poner votos a 0 en las alternativas asociadas a esta encuesta
            val sqlReset = """
                UPDATE $TABLA_ALTERNATIVAS 
                SET $COL_ALTERNATIVA_VOTOS = 0 
                WHERE $COL_ALTERNATIVA_PREGUNTA_ID IN (
                    SELECT $COL_PREGUNTA_ID FROM $TABLA_PREGUNTAS WHERE $COL_PREGUNTA_ENCUESTA_ID = ?
                )
            """.trimIndent()
            db.execSQL(sqlReset, arrayOf(idEncuesta.toString()))

            db.setTransactionSuccessful()
            true
        } finally {
            db.endTransaction()
        }
    }

    /**
     * 16. Contar la cantidad de participantes únicos en una encuesta
     */
    fun contarParticipantesUnicos(idEncuesta: Long): Int {
        val db = readableDatabase
        val cursor = db.rawQuery(
            "SELECT COUNT(DISTINCT LOWER(TRIM($COL_RESPUESTA_PARTICIPANTE))) FROM $TABLA_RESPUESTAS WHERE $COL_RESPUESTA_ENCUESTA_ID = ?",
            arrayOf(idEncuesta.toString())
        )
        var total = 0
        if (cursor.moveToFirst()) {
            total = cursor.getInt(0)
        }
        cursor.close()
        return total
    }

    /**
     * 17. Obtener la lista de participantes que han votado en una encuesta
     */
    fun obtenerParticipantesDeEncuesta(idEncuesta: Long): List<ParticipanteRegistro> {
        val lista = ArrayList<ParticipanteRegistro>()
        val db = readableDatabase
        val cursor = db.rawQuery(
            """
            SELECT $COL_RESPUESTA_PARTICIPANTE, MAX($COL_RESPUESTA_FECHA) as fecha_ult
            FROM $TABLA_RESPUESTAS 
            WHERE $COL_RESPUESTA_ENCUESTA_ID = ?
            GROUP BY LOWER(TRIM($COL_RESPUESTA_PARTICIPANTE))
            ORDER BY MAX($COL_RESPUESTA_ID) DESC
            LIMIT 30
            """.trimIndent(),
            arrayOf(idEncuesta.toString())
        )

        if (cursor.moveToFirst()) {
            do {
                val nombre = cursor.getString(0)
                val fecha = cursor.getString(1)
                lista.add(ParticipanteRegistro(nombre, fecha))
            } while (cursor.moveToNext())
        }
        cursor.close()
        return lista
    }

    /**
     * 18. Obtener estadísticas de cada pregunta de la encuesta para la pantalla de resultados
     */
    fun obtenerEstadisticasPreguntas(idEncuesta: Long): List<PreguntaEstadistica> {
        val resultado = ArrayList<PreguntaEstadistica>()
        val preguntas = listarPreguntasDeEncuesta(idEncuesta)

        for (pregunta in preguntas) {
            val alternativas = listarAlternativasDePregunta(pregunta.id.toLongOrNull() ?: 0L)
            val totalVotosPregunta = alternativas.sumOf { it.votos }

            // Encontrar el voto máximo para determinar la(s) ganadora(s)
            val maxVotos = if (totalVotosPregunta > 0) alternativas.maxOf { it.votos } else 0

            val listaEstadisticas = alternativas.map { alt ->
                val porcentaje = if (totalVotosPregunta > 0) {
                    (alt.votos.toFloat() / totalVotosPregunta.toFloat()) * 100f
                } else {
                    0f
                }
                val esGanadora = totalVotosPregunta > 0 && alt.votos == maxVotos && alt.votos > 0
                AlternativaEstadistica(alt.id, alt.texto, alt.votos, porcentaje, esGanadora)
            }

            resultado.add(PreguntaEstadistica(pregunta, totalVotosPregunta, listaEstadisticas))
        }

        return resultado
    }
}
