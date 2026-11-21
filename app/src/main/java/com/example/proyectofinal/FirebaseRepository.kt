package com.example.proyectofinal

import com.google.firebase.Firebase
import com.google.firebase.auth.auth
import com.google.firebase.firestore.firestore
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.UUID

/**
 * ============================================================================
 * REPOSITORIO EN LA NUBE: FirebaseRepository (Cloud Firestore + Auth)
 * ============================================================================
 * Gestiona usuarios, encuestas, preguntas, votación única por UID y conteo
 * de resultados compartidos en tiempo real entre todos los dispositivos.
 */
object FirebaseRepository {

    private val db get() = Firebase.firestore
    private val auth get() = Firebase.auth

    private const val COL_USERS = "users"
    private const val COL_ENCUESTAS = "encuestas"
    private const val SUB_VOTOS = "votos"

    fun currentUid(): String? = auth.currentUser?.uid

    fun currentDisplayName(): String {
        val user = auth.currentUser ?: return "Usuario UNAMAD"
        return user.displayName?.takeIf { it.isNotBlank() }
            ?: user.email?.substringBefore("@")
            ?: "Usuario UNAMAD"
    }

    // ========================================================================
    // PERFIL DE USUARIO (users/{uid})
    // ========================================================================

    fun guardarPerfilUsuario(
        uid: String,
        nombre: String,
        codigoUniversitario: String,
        email: String,
        onComplete: (Boolean, String?) -> Unit
    ) {
        val ref = db.collection(COL_USERS).document(uid)
        ref.get().addOnSuccessListener { snap ->
            val fechaReg = snap.getLong("fechaRegistro") ?: System.currentTimeMillis()
            val data = hashMapOf(
                "uid" to uid,
                "nombre" to nombre.trim().ifEmpty { "Usuario UNAMAD" },
                "codigoUniversitario" to codigoUniversitario.trim(),
                "email" to email.trim(),
                "fechaRegistro" to fechaReg
            )
            ref.set(data)
                .addOnSuccessListener { onComplete(true, null) }
                .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
        }.addOnFailureListener { e ->
            onComplete(false, e.localizedMessage)
        }
    }

    fun obtenerPerfilUsuario(uid: String, onResult: (UsuarioPerfil?) -> Unit) {
        db.collection(COL_USERS).document(uid).get()
            .addOnSuccessListener { doc ->
                if (doc.exists()) {
                    onResult(
                        UsuarioPerfil(
                            uid = doc.getString("uid") ?: uid,
                            nombre = doc.getString("nombre") ?: "",
                            codigoUniversitario = doc.getString("codigoUniversitario") ?: "",
                            email = doc.getString("email") ?: "",
                            fechaRegistro = doc.getLong("fechaRegistro") ?: 0L
                        )
                    )
                } else {
                    onResult(null)
                }
            }
            .addOnFailureListener { onResult(null) }
    }

    // ========================================================================
    // ENCUESTAS (encuestas/{encuestaId})
    // ========================================================================

    private fun parsearEncuesta(id: String, data: Map<String, Any?>): Encuesta {
        val rawPreguntas = (data["preguntas"] as? List<*>) ?: emptyList<Any>()
        val preguntas = rawPreguntas.mapNotNull { item ->
            val map = item as? Map<*, *> ?: return@mapNotNull null
            val rawAlts = (map["alternativas"] as? List<*>) ?: emptyList<Any>()
            val alts = rawAlts.mapNotNull { aItem ->
                val aMap = aItem as? Map<*, *> ?: return@mapNotNull null
                Alternativa(
                    id = aMap["id"] as? String ?: UUID.randomUUID().toString(),
                    texto = aMap["texto"] as? String ?: ""
                )
            }
            Pregunta(
                id = map["id"] as? String ?: UUID.randomUUID().toString(),
                texto = map["texto"] as? String ?: "",
                tipo = map["tipo"] as? String ?: "UNICA",
                alternativas = alts
            )
        }

        return Encuesta(
            id = id,
            titulo = data["titulo"] as? String ?: "",
            descripcion = data["descripcion"] as? String ?: "",
            categoria = data["categoria"] as? String ?: "General",
            activa = data["activa"] as? Boolean ?: true,
            fechaCreacion = data["fechaCreacion"] as? String ?: "",
            creadorUid = data["creadorUid"] as? String ?: "",
            creadorNombre = data["creadorNombre"] as? String ?: "Usuario",
            preguntas = preguntas,
            totalPreguntas = preguntas.size
        )
    }

    fun listarEncuestas(
        filtro: String,
        onResult: (List<Encuesta>, Triple<Int, Int, Int>, String?) -> Unit
    ) {
        db.collection(COL_ENCUESTAS).get()
            .addOnSuccessListener { snapshot ->
                val todas = snapshot.documents.mapNotNull { doc ->
                    doc.data?.let { parsearEncuesta(doc.id, it) }
                }.sortedByDescending { it.fechaCreacion }

                if (todas.isEmpty()) {
                    onResult(emptyList(), Triple(0, 0, 0), null)
                    return@addOnSuccessListener
                }

                // Contar votos de cada encuesta consultando la subcolección votos
                var pendientes = todas.size
                var totalVotosGlobal = 0

                for (enc in todas) {
                    db.collection(COL_ENCUESTAS).document(enc.id)
                        .collection(SUB_VOTOS).get()
                        .addOnSuccessListener { vSnap ->
                            enc.totalVotos = vSnap.size()
                            totalVotosGlobal += vSnap.size()
                            pendientes--
                            if (pendientes == 0) {
                                entregarListaFiltrada(todas, filtro, totalVotosGlobal, onResult)
                            }
                        }
                        .addOnFailureListener {
                            pendientes--
                            if (pendientes == 0) {
                                entregarListaFiltrada(todas, filtro, totalVotosGlobal, onResult)
                            }
                        }
                }
            }
            .addOnFailureListener { e ->
                onResult(emptyList(), Triple(0, 0, 0), e.localizedMessage)
            }
    }

    private fun entregarListaFiltrada(
        todas: List<Encuesta>,
        filtro: String,
        totalVotosGlobal: Int,
        onResult: (List<Encuesta>, Triple<Int, Int, Int>, String?) -> Unit
    ) {
        val total = todas.size
        val activas = todas.count { it.activa }
        val filtradas = when (filtro) {
            "ACTIVAS" -> todas.filter { it.activa }
            "CERRADAS" -> todas.filter { !it.activa }
            else -> todas
        }
        onResult(filtradas, Triple(total, activas, totalVotosGlobal), null)
    }

    fun obtenerEncuestaPorId(encuestaId: String, onResult: (Encuesta?) -> Unit) {
        db.collection(COL_ENCUESTAS).document(encuestaId).get()
            .addOnSuccessListener { doc ->
                val data = doc.data
                if (doc.exists() && data != null) {
                    val enc = parsearEncuesta(doc.id, data)
                    db.collection(COL_ENCUESTAS).document(encuestaId)
                        .collection(SUB_VOTOS).get()
                        .addOnSuccessListener { vSnap ->
                            enc.totalVotos = vSnap.size()
                            onResult(enc)
                        }
                        .addOnFailureListener { onResult(enc) }
                } else {
                    onResult(null)
                }
            }
            .addOnFailureListener { onResult(null) }
    }

    fun crearEncuesta(
        titulo: String,
        descripcion: String,
        categoria: String,
        activa: Boolean,
        onComplete: (String?, String?) -> Unit
    ) {
        val uid = currentUid()
        if (uid == null) {
            onComplete(null, "Sesión no iniciada.")
            return
        }
        val fecha = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault()).format(Date())
        val docRef = db.collection(COL_ENCUESTAS).document()
        val data = hashMapOf(
            "titulo" to titulo.trim(),
            "descripcion" to descripcion.trim(),
            "categoria" to categoria,
            "activa" to activa,
            "fechaCreacion" to fecha,
            "creadorUid" to uid,
            "creadorNombre" to currentDisplayName(),
            "preguntas" to emptyList<Map<String, Any>>()
        )
        docRef.set(data)
            .addOnSuccessListener { onComplete(docRef.id, null) }
            .addOnFailureListener { e -> onComplete(null, e.localizedMessage) }
    }

    fun actualizarEncuesta(
        encuestaId: String,
        titulo: String,
        descripcion: String,
        categoria: String,
        activa: Boolean,
        onComplete: (Boolean, String?) -> Unit
    ) {
        val updates = hashMapOf<String, Any>(
            "titulo" to titulo.trim(),
            "descripcion" to descripcion.trim(),
            "categoria" to categoria,
            "activa" to activa
        )
        db.collection(COL_ENCUESTAS).document(encuestaId).update(updates)
            .addOnSuccessListener { onComplete(true, null) }
            .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
    }

    fun guardarPreguntasEncuesta(
        encuestaId: String,
        preguntas: List<Pregunta>,
        onComplete: (Boolean, String?) -> Unit
    ) {
        val listaSerializada = preguntas.map { p ->
            hashMapOf(
                "id" to p.id,
                "texto" to p.texto,
                "tipo" to p.tipo,
                "alternativas" to p.alternativas.map { a ->
                    hashMapOf(
                        "id" to a.id,
                        "texto" to a.texto
                    )
                }
            )
        }
        db.collection(COL_ENCUESTAS).document(encuestaId)
            .update("preguntas", listaSerializada)
            .addOnSuccessListener { onComplete(true, null) }
            .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
    }

    fun eliminarEncuesta(encuestaId: String, onComplete: (Boolean, String?) -> Unit) {
        reiniciarVotosEncuesta(encuestaId) { _, _ ->
            db.collection(COL_ENCUESTAS).document(encuestaId).delete()
                .addOnSuccessListener { onComplete(true, null) }
                .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
        }
    }

    /**
     * Carga 2 encuestas institucionales de demostración en Cloud Firestore
     * asignadas al usuario actual como creador.
     */
    fun sembrarEncuestasDemo(onComplete: (Boolean, String?) -> Unit) {
        val uid = currentUid()
        if (uid == null) {
            onComplete(false, "Sesión no iniciada.")
            return
        }
        val autor = currentDisplayName()
        val fecha = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault()).format(Date())

        val enc1Ref = db.collection(COL_ENCUESTAS).document()
        val p1_1 = UUID.randomUUID().toString()
        val a1_1_1 = UUID.randomUUID().toString()
        val a1_1_2 = UUID.randomUUID().toString()
        val a1_1_3 = UUID.randomUUID().toString()

        val p1_2 = UUID.randomUUID().toString()
        val a1_2_1 = UUID.randomUUID().toString()
        val a1_2_2 = UUID.randomUUID().toString()
        val a1_2_3 = UUID.randomUUID().toString()

        val enc1Data = hashMapOf(
            "titulo" to "Elección de Delegado Estudiantil EPISI 2026-II",
            "descripcion" to "Proceso democrático de elección del representante estudiantil para el semestre académico actual.",
            "categoria" to "Votación",
            "activa" to true,
            "fechaCreacion" to fecha,
            "creadorUid" to uid,
            "creadorNombre" to autor,
            "preguntas" to listOf(
                hashMapOf(
                    "id" to p1_1,
                    "texto" to "Seleccione a su candidato preferido para Delegado General EPISI:",
                    "tipo" to "UNICA",
                    "alternativas" to listOf(
                        hashMapOf("id" to a1_1_1, "texto" to "Lista 1: Innovación y Liderazgo"),
                        hashMapOf("id" to a1_1_2, "texto" to "Lista 2: Unidad y Transparencia"),
                        hashMapOf("id" to a1_1_3, "texto" to "Voto en Blanco")
                    )
                ),
                hashMapOf(
                    "id" to p1_2,
                    "texto" to "¿Qué propuesta considera más urgente para el semestre?",
                    "tipo" to "UNICA",
                    "alternativas" to listOf(
                        hashMapOf("id" to a1_2_1, "texto" to "Talleres prácticos de desarrollo móvil y cloud"),
                        hashMapOf("id" to a1_2_2, "texto" to "Renovación de laboratorios de cómputo"),
                        hashMapOf("id" to a1_2_3, "texto" to "Feria tecnológica y hackathon amazónica")
                    )
                )
            )
        )

        val enc2Ref = db.collection(COL_ENCUESTAS).document()
        val p2_1 = UUID.randomUUID().toString()
        val enc2Data = hashMapOf(
            "titulo" to "Encuesta de Satisfacción de Servicios Académicos UNAMAD",
            "descripcion" to "Evaluación general sobre la calidad académica, laboratorios y conectividad en el campus universitario.",
            "categoria" to "Satisfacción",
            "activa" to true,
            "fechaCreacion" to fecha,
            "creadorUid" to uid,
            "creadorNombre" to autor,
            "preguntas" to listOf(
                hashMapOf(
                    "id" to p2_1,
                    "texto" to "¿Cómo califica la calidad de los laboratorios y servicios recibidos?",
                    "tipo" to "UNICA",
                    "alternativas" to listOf(
                        hashMapOf("id" to UUID.randomUUID().toString(), "texto" to "Excelente"),
                        hashMapOf("id" to UUID.randomUUID().toString(), "texto" to "Bueno"),
                        hashMapOf("id" to UUID.randomUUID().toString(), "texto" to "Regular"),
                        hashMapOf("id" to UUID.randomUUID().toString(), "texto" to "Por mejorar")
                    )
                )
            )
        )

        val batch = db.batch()
        batch.set(enc1Ref, enc1Data)
        batch.set(enc2Ref, enc2Data)
        batch.commit()
            .addOnSuccessListener { onComplete(true, null) }
            .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
    }

    // ========================================================================
    // VOTACIÓN ÚNICA POR UID Y RESULTADOS EN TIEMPO REAL
    // ========================================================================

    fun yaVotoUsuario(encuestaId: String, uid: String, onResult: (Boolean) -> Unit) {
        db.collection(COL_ENCUESTAS).document(encuestaId)
            .collection(SUB_VOTOS).document(uid).get()
            .addOnSuccessListener { doc -> onResult(doc.exists()) }
            .addOnFailureListener { onResult(false) }
    }

    fun registrarVoto(
        encuestaId: String,
        participante: String,
        respuestasPorPregunta: Map<String, List<String>>,
        onComplete: (Boolean, String?) -> Unit
    ) {
        val uid = currentUid()
        if (uid == null) {
            onComplete(false, "Sesión no iniciada.")
            return
        }
        val fechaVoto = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.getDefault()).format(Date())
        val votoRef = db.collection(COL_ENCUESTAS).document(encuestaId)
            .collection(SUB_VOTOS).document(uid)

        val data = hashMapOf(
            "uid" to uid,
            "participante" to participante.trim(),
            "fechaVoto" to fechaVoto,
            "respuestas" to respuestasPorPregunta
        )
        votoRef.set(data)
            .addOnSuccessListener { onComplete(true, null) }
            .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
    }

    fun reiniciarVotosEncuesta(encuestaId: String, onComplete: (Boolean, String?) -> Unit) {
        val votosRef = db.collection(COL_ENCUESTAS).document(encuestaId).collection(SUB_VOTOS)
        votosRef.get()
            .addOnSuccessListener { snap ->
                if (snap.isEmpty) {
                    onComplete(true, null)
                    return@addOnSuccessListener
                }
                val batch = db.batch()
                for (doc in snap.documents) {
                    batch.delete(doc.reference)
                }
                batch.commit()
                    .addOnSuccessListener { onComplete(true, null) }
                    .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
            }
            .addOnFailureListener { e -> onComplete(false, e.localizedMessage) }
    }

    fun obtenerResultados(
        encuestaId: String,
        onResult: (Encuesta?, List<PreguntaEstadistica>, List<ParticipanteRegistro>, String?) -> Unit
    ) {
        db.collection(COL_ENCUESTAS).document(encuestaId).get()
            .addOnSuccessListener { doc ->
                val data = doc.data
                if (!doc.exists() || data == null) {
                    onResult(null, emptyList(), emptyList(), "Encuesta no encontrada.")
                    return@addOnSuccessListener
                }
                val encuesta = parsearEncuesta(doc.id, data)

                db.collection(COL_ENCUESTAS).document(encuestaId)
                    .collection(SUB_VOTOS).get()
                    .addOnSuccessListener { vSnap ->
                        val conteo = HashMap<String, Int>()
                        val participantes = ArrayList<ParticipanteRegistro>()

                        for (vDoc in vSnap.documents) {
                            val nombre = vDoc.getString("participante") ?: "Usuario"
                            val fecha = vDoc.getString("fechaVoto") ?: ""
                            participantes.add(ParticipanteRegistro(vDoc.id, nombre, fecha))

                            val respMap = vDoc.get("respuestas") as? Map<*, *> ?: continue
                            for (listaRaw in respMap.values) {
                                val listaIds = listaRaw as? List<*> ?: continue
                                for (altIdAny in listaIds) {
                                    val altId = altIdAny as? String ?: continue
                                    conteo[altId] = (conteo[altId] ?: 0) + 1
                                }
                            }
                        }

                        encuesta.totalVotos = participantes.size
                        val stats = encuesta.preguntas.map { pregunta ->
                            val altsConVotos = pregunta.alternativas.map { alt ->
                                alt.copy(votos = conteo[alt.id] ?: 0)
                            }
                            val totalVotosP = altsConVotos.sumOf { it.votos }
                            val maxVotos = if (totalVotosP > 0) altsConVotos.maxOf { it.votos } else 0
                            val altsEst = altsConVotos.map { alt ->
                                val pct = if (totalVotosP > 0) (alt.votos.toFloat() / totalVotosP) * 100f else 0f
                                val ganadora = totalVotosP > 0 && alt.votos == maxVotos && alt.votos > 0
                                AlternativaEstadistica(alt.id, alt.texto, alt.votos, pct, ganadora)
                            }
                            PreguntaEstadistica(pregunta, totalVotosP, altsEst)
                        }

                        onResult(encuesta, stats, participantes.sortedByDescending { it.fechaVoto }, null)
                    }
                    .addOnFailureListener { e ->
                        onResult(encuesta, emptyList(), emptyList(), e.localizedMessage)
                    }
            }
            .addOnFailureListener { e ->
                onResult(null, emptyList(), emptyList(), e.localizedMessage)
            }
    }
}
