package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat

/**
 * ============================================================================
 * PANTALLA 4: RegistrarVotoActivity (Votación Única por Cuenta Firebase)
 * ============================================================================
 */
class RegistrarVotoActivity : AppCompatActivity() {

    private lateinit var tvVotoTituloEncuesta: TextView
    private lateinit var tvVotoCategoria: TextView
    private lateinit var tvVotoEstado: TextView
    private lateinit var tvVotoDescripcion: TextView
    private lateinit var etParticipante: EditText
    private lateinit var llContenedorPreguntasVoto: LinearLayout
    private lateinit var btnEnviarVoto: Button
    private lateinit var btnCancelarVoto: Button

    private var idEncuesta: String = ""
    private var encuestaActiva: Boolean = true
    private var yaVoto: Boolean = false
    private val listaPreguntas = ArrayList<Pregunta>()
    private val mapaRadioGroups = HashMap<String, RadioGroup>()
    private val mapaCheckBoxes = HashMap<String, List<CheckBox>>()
    private var seleccionesRestauradas: Set<String> = emptySet()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_registrar_voto)

        configurarEdgeToEdgeConHeader(findViewById(R.id.scrollRegistrarVoto), findViewById(R.id.topBar))

        idEncuesta = intent.getStringExtra(MainActivity.EXTRA_ID_ENCUESTA) ?: ""
        if (idEncuesta.isBlank()) {
            Toast.makeText(this, "Error: Encuesta no encontrada.", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        seleccionesRestauradas = savedInstanceState?.getStringArray(KEY_SELECCIONES)?.toSet() ?: emptySet()

        vincularVistas()
        configurarEventos()
        precargarParticipante()
        cargarEncuestaDesdeNube()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        val seleccionadas = ArrayList<String>()
        for (rg in mapaRadioGroups.values) {
            if (rg.checkedRadioButtonId != -1) {
                val idAlt = rg.findViewById<RadioButton>(rg.checkedRadioButtonId)?.tag as? String
                if (idAlt != null) seleccionadas.add(idAlt)
            }
        }
        for (lista in mapaCheckBoxes.values) {
            for (cb in lista) {
                if (cb.isChecked) {
                    val idAlt = cb.tag as? String
                    if (idAlt != null) seleccionadas.add(idAlt)
                }
            }
        }
        outState.putStringArray(KEY_SELECCIONES, seleccionadas.toTypedArray())
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

    private fun precargarParticipante() {
        val uid = FirebaseRepository.currentUid() ?: return
        etParticipante.setText(FirebaseRepository.currentDisplayName())
        FirebaseRepository.obtenerPerfilUsuario(uid) { perfil ->
            if (perfil != null && etParticipante.text.isBlank()) {
                val etiqueta = if (perfil.codigoUniversitario.isNotBlank()) {
                    "${perfil.nombre} - ${perfil.codigoUniversitario}"
                } else {
                    perfil.nombre
                }
                etParticipante.setText(etiqueta)
            } else if (perfil != null && perfil.codigoUniversitario.isNotBlank()) {
                etParticipante.setText("${perfil.nombre} - ${perfil.codigoUniversitario}")
            }
        }
    }

    private fun cargarEncuestaDesdeNube() {
        val uid = FirebaseRepository.currentUid()
        if (uid == null) {
            finish()
            return
        }

        FirebaseRepository.obtenerEncuestaPorId(idEncuesta) { encuesta ->
            if (isFinishing || isDestroyed) return@obtenerEncuestaPorId
            if (encuesta == null) {
                Toast.makeText(this, "No se pudo cargar la encuesta.", Toast.LENGTH_SHORT).show()
                finish()
                return@obtenerEncuestaPorId
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

            listaPreguntas.clear()
            listaPreguntas.addAll(encuesta.preguntas)

            FirebaseRepository.yaVotoUsuario(idEncuesta, uid) { votoPrevio ->
                if (isFinishing || isDestroyed) return@yaVotoUsuario
                yaVoto = votoPrevio
                if (votoPrevio) {
                    etParticipante.isEnabled = false
                    btnEnviarVoto.isEnabled = false
                    btnEnviarVoto.text = "Ya Emitiste Tu Voto"
                }
                construirCuestionarioDinamico(seleccionesRestauradas)
            }
        }
    }

    private fun construirCuestionarioDinamico(seleccionesPrevias: Set<String>) {
        llContenedorPreguntasVoto.removeAllViews()
        mapaRadioGroups.clear()
        mapaCheckBoxes.clear()

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
            if (encuestaActiva && !yaVoto) {
                btnEnviarVoto.text = "Encuesta Sin Preguntas"
            }
            return
        }

        val puedeVotar = encuestaActiva && !yaVoto
        val paddingTarjeta = (14 * densidad).toInt()
        val margenInferior = (12 * densidad).toInt()
        val minTouchPx = (48 * densidad).toInt()

        for ((index, pregunta) in listaPreguntas.withIndex()) {
            val contenedorPregunta = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                setBackgroundResource(R.drawable.bg_card)
                setPadding(paddingTarjeta, paddingTarjeta, paddingTarjeta, paddingTarjeta)
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply { bottomMargin = margenInferior }
            }

            val tvTexto = TextView(this).apply {
                text = "${index + 1}. ${pregunta.texto}"
                textSize = 15f
                setTypeface(null, android.graphics.Typeface.BOLD)
                setTextColor(ContextCompat.getColor(context, R.color.text_primary))
            }
            contenedorPregunta.addView(tvTexto)

            val tvInstruccion = TextView(this).apply {
                text = if (pregunta.tipo == "MULTIPLE") "(Seleccione una o varias opciones)" else "(Seleccione una sola opción)"
                textSize = 12f
                setTextColor(ContextCompat.getColor(context, R.color.text_secondary))
                setPadding(0, (2 * densidad).toInt(), 0, (8 * densidad).toInt())
            }
            contenedorPregunta.addView(tvInstruccion)

            if (pregunta.tipo == "UNICA") {
                val radioGroup = RadioGroup(this).apply {
                    orientation = RadioGroup.VERTICAL
                    layoutParams = LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        LinearLayout.LayoutParams.WRAP_CONTENT
                    )
                }
                for (alt in pregunta.alternativas) {
                    val rb = RadioButton(this).apply {
                        text = alt.texto
                        tag = alt.id
                        textSize = 14f
                        minHeight = minTouchPx
                        isEnabled = puedeVotar
                        setTextColor(ContextCompat.getColor(context, R.color.text_primary))
                        setPadding((6 * densidad).toInt(), (4 * densidad).toInt(), 0, (4 * densidad).toInt())
                        layoutParams = RadioGroup.LayoutParams(
                            RadioGroup.LayoutParams.MATCH_PARENT,
                            RadioGroup.LayoutParams.WRAP_CONTENT
                        )
                    }
                    radioGroup.addView(rb)
                    if (alt.id in seleccionesPrevias) rb.isChecked = true
                }
                mapaRadioGroups[pregunta.id] = radioGroup
                contenedorPregunta.addView(radioGroup)
            } else {
                val listaChecks = ArrayList<CheckBox>()
                for (alt in pregunta.alternativas) {
                    val cb = CheckBox(this).apply {
                        text = alt.texto
                        tag = alt.id
                        textSize = 14f
                        minHeight = minTouchPx
                        isEnabled = puedeVotar
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
        btnEnviarVoto.setOnClickListener { procesarVoto() }
        btnCancelarVoto.setOnClickListener { finish() }
    }

    private fun procesarVoto() {
        val participante = etParticipante.text.toString().trim()
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

        val respuestasMap = HashMap<String, List<String>>()
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
                val idAlt = rbSeleccionado?.tag as? String ?: ""
                val textoAlt = rbSeleccionado?.text?.toString() ?: ""
                respuestasMap[pregunta.id] = listOf(idAlt)
                resumenLineas.add("• ${pregunta.texto}\n   Respuesta: $textoAlt")
            } else {
                val listaChecks = mapaCheckBoxes[pregunta.id] ?: emptyList()
                val seleccionados = listaChecks.filter { it.isChecked }
                if (seleccionados.isEmpty()) {
                    Toast.makeText(this, "Por favor seleccione al menos una opción en la pregunta #$numPregunta.", Toast.LENGTH_LONG).show()
                    return
                }
                respuestasMap[pregunta.id] = seleccionados.mapNotNull { it.tag as? String }
                resumenLineas.add("• ${pregunta.texto}\n   Respuestas: ${seleccionados.joinToString(", ") { it.text.toString() }}")
            }
        }

        btnEnviarVoto.isEnabled = false
        FirebaseRepository.registrarVoto(idEncuesta, participante, respuestasMap) { exito, err ->
            if (exito) {
                val mensajeResumen = StringBuilder().apply {
                    append("Participante: $participante\n\n")
                    append("Respuestas emitidas:\n")
                    for (linea in resumenLineas) append("$linea\n\n")
                    append("¡Su voto ha sido registrado en la nube exitosamente!")
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
                btnEnviarVoto.isEnabled = true
                Toast.makeText(this, "No se pudo registrar el voto: $err", Toast.LENGTH_LONG).show()
            }
        }
    }

    companion object {
        private const val KEY_SELECCIONES = "key_selecciones_voto"
    }
}
