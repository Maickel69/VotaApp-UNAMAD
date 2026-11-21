package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat

/**
 * ============================================================================
 * PANTALLA 4: RegistrarVotoActivity (Emisión y Registro de Votos / Respuestas)
 * ============================================================================
 * Proyecto: Sistema de Encuestas y Votaciones UNAMAD - EPISI
 * 
 * Funcionalidades:
 *  1. Carga dinámicamente las preguntas y alternativas desde SQLite.
 *  2. Renderiza RadioGroups para preguntas 'UNICA' y CheckBoxes para 'MULTIPLE'.
 *  3. Valida que el nombre o código del participante sea obligatorio.
 *  4. Controla la restricción de NO DUPLICIDAD: un participante no puede votar 2 veces.
 *  5. Valida que todas las preguntas sean respondidas antes del envío.
 *  6. Registra las respuestas en SQLite e incrementa los votos en una transacción.
 *  7. Muestra resumen detallado en AlertDialog con navegación a Resultados.
 */
class RegistrarVotoActivity : AppCompatActivity() {

    // 1. Gestor de base de datos
    private lateinit var dbHelper: DatabaseHelper

    // 2. Elementos visuales
    private lateinit var tvVotoTituloEncuesta: TextView
    private lateinit var tvVotoCategoria: TextView
    private lateinit var tvVotoEstado: TextView
    private lateinit var tvVotoDescripcion: TextView
    private lateinit var etParticipante: EditText
    private lateinit var llContenedorPreguntasVoto: LinearLayout
    private lateinit var btnEnviarVoto: Button
    private lateinit var btnCancelarVoto: Button

    // 3. Estructuras de datos auxiliares para el control dinámico de vistas
    private var idEncuesta: Long = -1L
    private var encuestaActiva: Boolean = true
    private val listaPreguntas = ArrayList<Pregunta>()

    // Para preguntas UNICA: Mapa de (idPregunta -> RadioGroup)
    private val mapaRadioGroups = HashMap<Long, RadioGroup>()

    // Para preguntas MULTIPLE: Mapa de (idPregunta -> Lista de CheckBox)
    private val mapaCheckBoxes = HashMap<Long, List<CheckBox>>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_registrar_voto)

        configurarEdgeToEdgeConHeader(findViewById(R.id.scrollRegistrarVoto), findViewById(R.id.topBar))

        idEncuesta = intent.getLongExtra(MainActivity.EXTRA_ID_ENCUESTA, -1L)
        if (idEncuesta == -1L) {
            Toast.makeText(this, "Error: Encuesta no encontrada.", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        dbHelper = DatabaseHelper(this)

        vincularVistas()
        cargarDatosEncuesta()
        val seleccionesPrevias = savedInstanceState?.getLongArray(KEY_SELECCIONES)?.toSet() ?: emptySet()
        construirCuestionarioDinamico(seleccionesPrevias)
        configurarEventos()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        val seleccionadas = ArrayList<Long>()
        for (rg in mapaRadioGroups.values) {
            if (rg.checkedRadioButtonId != -1) {
                val idAlt = rg.findViewById<RadioButton>(rg.checkedRadioButtonId)?.tag as? Long
                if (idAlt != null) seleccionadas.add(idAlt)
            }
        }
        for (lista in mapaCheckBoxes.values) {
            for (cb in lista) {
                if (cb.isChecked) {
                    val idAlt = cb.tag as? Long
                    if (idAlt != null) seleccionadas.add(idAlt)
                }
            }
        }
        outState.putLongArray(KEY_SELECCIONES, seleccionadas.toLongArray())
    }

    private fun vincularVistas() {
        tvVotoTituloEncuesta = findViewById(R.id.tvVotoTituloEncuesta)
        tvVotoCategoria = findViewById(R.id.tvVotoCategoria)
        tvVotoEstado = findViewById(R.id.tvVotoEstado)
        tvVotoDescripcion = findViewById(R.id.tvVotoDescripcion)
        etParticipante = findViewById(R.id.etParticipante)
        llContenedorPreguntasVoto = findViewById(R.id.llContenedorPreguntasVoto)
        btnEnviarVoto = findViewById(R.id.btnEnviarVoto)
        btnCancelarVoto = findViewById(R.id.btnCancelarVoto)
    }

    /**
     * Muestra la información general de la encuesta
     */
    private fun cargarDatosEncuesta() {
        val encuesta = dbHelper.obtenerEncuestaPorId(idEncuesta)
        if (encuesta == null) {
            Toast.makeText(this, "No se pudo cargar la encuesta.", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        tvVotoTituloEncuesta.text = encuesta.titulo
        tvVotoCategoria.text = encuesta.categoria
        tvVotoDescripcion.text = encuesta.descripcion

        encuestaActiva = encuesta.activa
        if (encuesta.activa) {
            tvVotoEstado.text = "Activa"
            tvVotoEstado.setBackgroundResource(R.drawable.bg_badge_active)
            tvVotoEstado.setTextColor(ContextCompat.getColor(this, R.color.success))
        } else {
            tvVotoEstado.text = "Cerrada"
            tvVotoEstado.setBackgroundResource(R.drawable.bg_badge_closed)
            tvVotoEstado.setTextColor(ContextCompat.getColor(this, R.color.danger))
            etParticipante.isEnabled = false
            btnEnviarVoto.isEnabled = false
            btnEnviarVoto.text = "Encuesta Cerrada para Votaciones"
        }
    }

    /**
     * Genera dinámicamente en código Kotlin las preguntas y controles de opciones
     */
    private fun construirCuestionarioDinamico(seleccionesPrevias: Set<Long> = emptySet()) {
        llContenedorPreguntasVoto.removeAllViews()
        mapaRadioGroups.clear()
        mapaCheckBoxes.clear()

        listaPreguntas.clear()
        listaPreguntas.addAll(dbHelper.listarPreguntasDeEncuesta(idEncuesta))

        val densidad = resources.displayMetrics.density
        if (listaPreguntas.isEmpty()) {
            val tvAviso = TextView(this).apply {
                text = "Esta encuesta no tiene preguntas registradas para votar."
                setBackgroundResource(R.drawable.bg_card)
                val pad = (16 * densidad).toInt()
                setPadding(pad, pad, pad, pad)
                textSize = 14f
                setTextColor(ContextCompat.getColor(context, R.color.text_secondary))
            }
            llContenedorPreguntasVoto.addView(tvAviso)
            btnEnviarVoto.isEnabled = false
            if (encuestaActiva) {
                btnEnviarVoto.text = "Encuesta Sin Preguntas"
            }
            return
        }

        val paddingTarjeta = (14 * densidad).toInt()
        val margenInferior = (12 * densidad).toInt()
        val minTouchPx = (48 * densidad).toInt()

        for ((index, pregunta) in listaPreguntas.withIndex()) {
            // Contenedor tipo Tarjeta para la pregunta
            val contenedorPregunta = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                setBackgroundResource(R.drawable.bg_card)
                setPadding(paddingTarjeta, paddingTarjeta, paddingTarjeta, paddingTarjeta)
                val params = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                )
                params.bottomMargin = margenInferior
                layoutParams = params
            }

            // Enunciado de la pregunta
            val tvTexto = TextView(this).apply {
                text = "${index + 1}. ${pregunta.texto}"
                textSize = 15f
                setTypeface(null, android.graphics.Typeface.BOLD)
                setTextColor(ContextCompat.getColor(context, R.color.text_primary))
            }
            contenedorPregunta.addView(tvTexto)

            // Indicación del tipo de respuesta
            val tvInstruccion = TextView(this).apply {
                text = if (pregunta.tipo == "MULTIPLE") {
                    "(Seleccione una o varias opciones)"
                } else {
                    "(Seleccione una sola opción)"
                }
                textSize = 12f
                setTextColor(ContextCompat.getColor(context, R.color.text_secondary))
                setPadding(0, (2 * densidad).toInt(), 0, (8 * densidad).toInt())
            }
            contenedorPregunta.addView(tvInstruccion)

            // Cargar las alternativas de la pregunta
            val listaAlternativas = dbHelper.listarAlternativasDePregunta(pregunta.id)

            if (pregunta.tipo == "UNICA") {
                // RadioGroup para selección simple
                val radioGroup = RadioGroup(this).apply {
                    orientation = RadioGroup.VERTICAL
                    layoutParams = LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        LinearLayout.LayoutParams.WRAP_CONTENT
                    )
                }

                for (alt in listaAlternativas) {
                    val rb = RadioButton(this).apply {
                        text = alt.texto
                        tag = alt.id // Guardamos el ID de la alternativa en la propiedad tag
                        textSize = 14f
                        minHeight = minTouchPx
                        isEnabled = encuestaActiva
                        setTextColor(ContextCompat.getColor(context, R.color.text_primary))
                        setPadding((6 * densidad).toInt(), (4 * densidad).toInt(), 0, (4 * densidad).toInt())
                        layoutParams = RadioGroup.LayoutParams(
                            RadioGroup.LayoutParams.MATCH_PARENT,
                            RadioGroup.LayoutParams.WRAP_CONTENT
                        )
                    }
                    radioGroup.addView(rb)
                    if (alt.id in seleccionesPrevias) {
                        rb.isChecked = true
                    }
                }

                mapaRadioGroups[pregunta.id] = radioGroup
                contenedorPregunta.addView(radioGroup)

            } else {
                // CheckBoxes para selección múltiple
                val listaChecks = ArrayList<CheckBox>()

                for (alt in listaAlternativas) {
                    val cb = CheckBox(this).apply {
                        text = alt.texto
                        tag = alt.id // Guardamos el ID de la alternativa en la propiedad tag
                        textSize = 14f
                        minHeight = minTouchPx
                        isEnabled = encuestaActiva
                        isChecked = alt.id in seleccionesPrevias
                        setTextColor(ContextCompat.getColor(context, R.color.text_primary))
                        setPadding((6 * densidad).toInt(), (4 * densidad).toInt(), 0, (4 * densidad).toInt())
                        layoutParams = LinearLayout.LayoutParams(
                            LinearLayout.LayoutParams.MATCH_PARENT,
                            LinearLayout.LayoutParams.WRAP_CONTENT
                        )
                    }
                    listaChecks.add(cb)
                    contenedorPregunta.addView(cb)
                }

                mapaCheckBoxes[pregunta.id] = listaChecks
            }

            llContenedorPreguntasVoto.addView(contenedorPregunta)
        }
    }

    private fun configurarEventos() {
        btnEnviarVoto.setOnClickListener {
            procesarVoto()
        }

        btnCancelarVoto.setOnClickListener {
            finish()
        }
    }

    /**
     * Valida y procesa la emisión del voto
     */
    private fun procesarVoto() {
        val participante = etParticipante.text.toString().trim()

        // 1. Validación: Nombre o código obligatorio
        if (participante.isEmpty()) {
            etParticipante.error = "Debe ingresar su nombre completo o código universitario"
            etParticipante.requestFocus()
            Toast.makeText(this, "Por favor ingrese su identificación.", Toast.LENGTH_SHORT).show()
            return
        }

        if (participante.length < 3) {
            etParticipante.error = "Ingrese un nombre o código válido"
            etParticipante.requestFocus()
            Toast.makeText(this, "La identificación debe tener al menos 3 caracteres.", Toast.LENGTH_SHORT).show()
            return
        }

        // 2. Validación de VOTO ÚNICO (Control anti-duplicados)
        if (dbHelper.yaVotoParticipante(idEncuesta, participante)) {
            AlertDialog.Builder(this)
                .setTitle("Voto Ya Registrado")
                .setMessage("El participante \"$participante\" ya emitió su voto previamente en esta encuesta.\n\nPor políticas de transparencia institucional de la UNAMAD, solo se permite un voto por estudiante.")
                .setIcon(android.R.drawable.ic_dialog_alert)
                .setPositiveButton("Entendido", null)
                .show()
            return
        }

        // 3. Validación: Todas las preguntas deben ser respondidas
        val votosPorRegistrar = ArrayList<Pair<Long, Long>>() // Pair(idPregunta, idAlternativa)
        val resumenLineas = ArrayList<String>()

        for ((index, pregunta) in listaPreguntas.withIndex()) {
            val numPregunta = index + 1

            if (pregunta.tipo == "UNICA") {
                val rg = mapaRadioGroups[pregunta.id]
                val idRadioSeleccionado = rg?.checkedRadioButtonId ?: -1

                if (idRadioSeleccionado == -1) {
                    Toast.makeText(this, "Por favor responda la pregunta #$numPregunta.", Toast.LENGTH_LONG).show()
                    return
                }

                val rbSeleccionado = rg?.findViewById<RadioButton>(idRadioSeleccionado)
                val idAlternativa = rbSeleccionado?.tag as? Long ?: -1L
                val textoAlternativa = rbSeleccionado?.text?.toString() ?: ""

                votosPorRegistrar.add(Pair(pregunta.id, idAlternativa))
                resumenLineas.add("• ${pregunta.texto}\n   Respuesta: $textoAlternativa")

            } else {
                val listaChecks = mapaCheckBoxes[pregunta.id] ?: emptyList()
                val checksSeleccionados = listaChecks.filter { it.isChecked }

                if (checksSeleccionados.isEmpty()) {
                    Toast.makeText(this, "Por favor seleccione al menos una opción en la pregunta #$numPregunta.", Toast.LENGTH_LONG).show()
                    return
                }

                val textosSeleccionados = ArrayList<String>()
                for (cb in checksSeleccionados) {
                    val idAlternativa = cb.tag as? Long ?: -1L
                    votosPorRegistrar.add(Pair(pregunta.id, idAlternativa))
                    textosSeleccionados.add(cb.text.toString())
                }

                resumenLineas.add("• ${pregunta.texto}\n   Respuestas: ${textosSeleccionados.joinToString(", ")}")
            }
        }

        // 4. Registrar los votos en SQLite dentro de una transacción
        val exito = dbHelper.registrarVotos(idEncuesta, participante, votosPorRegistrar)

        if (exito) {
            // Construir texto de resumen de confirmación
            val mensajeResumen = StringBuilder().apply {
                append("Participante: $participante\n\n")
                append("Respuestas emitidas:\n")
                for (linea in resumenLineas) {
                    append("$linea\n\n")
                }
                append("¡Su voto ha sido contabilizado exitosamente en el sistema!")
            }.toString()

            AlertDialog.Builder(this)
                .setTitle("¡Voto Registrado con Éxito!")
                .setMessage(mensajeResumen)
                .setIcon(android.R.drawable.ic_dialog_info)
                .setCancelable(false)
                .setPositiveButton("Ver Resultados") { dialog, _ ->
                    dialog.dismiss()
                    val intent = Intent(this, ResultadosActivity::class.java).apply {
                        putExtra(MainActivity.EXTRA_ID_ENCUESTA, idEncuesta)
                    }
                    startActivity(intent)
                    finish()
                }
                .setNeutralButton("Volver al Inicio") { dialog, _ ->
                    dialog.dismiss()
                    finish()
                }
                .show()

        } else {
            Toast.makeText(this, "Error al guardar el voto. Inténtelo nuevamente.", Toast.LENGTH_SHORT).show()
        }
    }

    companion object {
        private const val KEY_SELECCIONES = "key_selecciones_voto"
    }
}
