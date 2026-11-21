package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import java.util.Locale
import kotlin.math.roundToInt

/**
 * ============================================================================
 * PANTALLA 5: ResultadosActivity (Conteo y Estadísticas en la Nube - Firestore)
 * ============================================================================
 */
class ResultadosActivity : AppCompatActivity() {

    private lateinit var tvResultadosTitulo: TextView
    private lateinit var tvResultadosCategoria: TextView
    private lateinit var tvResultadosEstado: TextView
    private lateinit var tvTotalParticipantes: TextView
    private lateinit var tvFechaCreacion: TextView
    private lateinit var llResultadosPreguntas: LinearLayout
    private lateinit var tvSinParticipantes: TextView
    private lateinit var llListaParticipantes: LinearLayout
    private lateinit var btnIrAVotar: Button
    private lateinit var btnReiniciarConteo: Button
    private lateinit var btnVolver: Button

    private var idEncuesta: String = ""
    private var encuestaActual: Encuesta? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_resultados)

        configurarEdgeToEdgeConHeader(findViewById(R.id.scrollResultados), findViewById(R.id.topBar))

        idEncuesta = intent.getStringExtra(MainActivity.EXTRA_ID_ENCUESTA) ?: ""
        if (idEncuesta.isBlank()) {
            Toast.makeText(this, "Error: No se encontró la encuesta especificada.", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        vincularVistas()
        configurarEventos()
    }

    override fun onResume() {
        super.onResume()
        cargarResultados()
    }

    private fun vincularVistas() {
        tvResultadosTitulo = findViewById(R.id.tvResultadosTitulo)
        tvResultadosCategoria = findViewById(R.id.tvResultadosCategoria)
        tvResultadosEstado = findViewById(R.id.tvResultadosEstado)
        tvTotalParticipantes = findViewById(R.id.tvTotalParticipantes)
        tvFechaCreacion = findViewById(R.id.tvFechaCreacion)
        llResultadosPreguntas = findViewById(R.id.llResultadosPreguntas)
        tvSinParticipantes = findViewById(R.id.tvSinParticipantes)
        llListaParticipantes = findViewById(R.id.llListaParticipantes)
        btnIrAVotar = findViewById(R.id.btnIrAVotar)
        btnReiniciarConteo = findViewById(R.id.btnReiniciarConteo)
        btnVolver = findViewById(R.id.btnVolver)
    }

    private fun configurarEventos() {
        btnIrAVotar.setOnClickListener {
            val enc = encuestaActual ?: return@setOnClickListener
            if (!enc.activa) {
                Toast.makeText(this, "Esta encuesta se encuentra cerrada.", Toast.LENGTH_SHORT).show()
            } else if (enc.totalPreguntas == 0) {
                Toast.makeText(this, "Esta encuesta no tiene preguntas registradas.", Toast.LENGTH_SHORT).show()
            } else {
                val intent = Intent(this, RegistrarVotoActivity::class.java).apply {
                    putExtra(MainActivity.EXTRA_ID_ENCUESTA, idEncuesta)
                }
                startActivity(intent)
            }
        }

        btnReiniciarConteo.setOnClickListener { mostrarDialogoReiniciarConteo() }
        btnVolver.setOnClickListener { finish() }
    }

    private fun cargarResultados() {
        FirebaseRepository.obtenerResultados(idEncuesta) { encuesta, estadisticas, participantes, err ->
            if (isFinishing || isDestroyed) return@obtenerResultados
            if (err != null) {
                Toast.makeText(this, "Error al cargar resultados: $err", Toast.LENGTH_SHORT).show()
            }
            if (encuesta == null) return@obtenerResultados
            encuestaActual = encuesta

            tvResultadosTitulo.text = encuesta.titulo
            tvResultadosCategoria.text = encuesta.categoria
            tvFechaCreacion.text = "Fecha de registro: ${encuesta.fechaCreacion} • Por ${encuesta.creadorNombre}"

            if (encuesta.activa) {
                tvResultadosEstado.text = "Activa"
                tvResultadosEstado.setBackgroundResource(R.drawable.bg_badge_active)
                tvResultadosEstado.setTextColor(ContextCompat.getColor(this, R.color.success))
                btnIrAVotar.visibility = if (encuesta.totalPreguntas > 0) View.VISIBLE else View.GONE
            } else {
                tvResultadosEstado.text = "Cerrada"
                tvResultadosEstado.setBackgroundResource(R.drawable.bg_badge_closed)
                tvResultadosEstado.setTextColor(ContextCompat.getColor(this, R.color.danger))
                btnIrAVotar.visibility = View.GONE
            }

            val totalParticipantes = participantes.size
            tvTotalParticipantes.text = "$totalParticipantes Estudiante(s) han participado"

            val esCreador = FirebaseRepository.currentUid() == encuesta.creadorUid
            btnReiniciarConteo.visibility = if (esCreador) View.VISIBLE else View.GONE
            btnReiniciarConteo.isEnabled = totalParticipantes > 0
            btnReiniciarConteo.alpha = if (totalParticipantes > 0) 1.0f else 0.5f

            renderizarGraficasPreguntas(estadisticas)
            renderizarListaVotantes(participantes)
        }
    }

    private fun renderizarGraficasPreguntas(estadisticas: List<PreguntaEstadistica>) {
        llResultadosPreguntas.removeAllViews()
        val densidad = resources.displayMetrics.density

        if (estadisticas.isEmpty()) {
            val tvSinPreguntas = TextView(this).apply {
                text = "No hay preguntas asociadas a esta encuesta."
                setBackgroundResource(R.drawable.bg_card)
                val pad = (16 * densidad).toInt()
                setPadding(pad, pad, pad, pad)
                setTextColor(ContextCompat.getColor(context, R.color.text_secondary))
            }
            llResultadosPreguntas.addView(tvSinPreguntas)
            return
        }

        val paddingTarjeta = (14 * densidad).toInt()
        val margenInferior = (12 * densidad).toInt()
        val padAltH = (10 * densidad).toInt()
        val padAltV = (8 * densidad).toInt()

        for ((index, pe) in estadisticas.withIndex()) {
            val pregunta = pe.pregunta
            val cardPregunta = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                setBackgroundResource(R.drawable.bg_card)
                setPadding(paddingTarjeta, paddingTarjeta, paddingTarjeta, paddingTarjeta)
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply { bottomMargin = margenInferior }
            }

            val tvTituloP = TextView(this).apply {
                text = "${index + 1}. ${pregunta.texto}"
                textSize = 15f
                setTypeface(null, android.graphics.Typeface.BOLD)
                setTextColor(ContextCompat.getColor(context, R.color.text_primary))
            }
            cardPregunta.addView(tvTituloP)

            val tipoTexto = if (pregunta.tipo == "MULTIPLE") "Opción Múltiple" else "Selección Única"
            val tvResumenP = TextView(this).apply {
                text = "Total votos: ${pe.totalVotosPregunta}  •  Modalidad: $tipoTexto"
                textSize = 12f
                setTextColor(ContextCompat.getColor(context, R.color.text_secondary))
                setPadding(0, (2 * densidad).toInt(), 0, (10 * densidad).toInt())
            }
            cardPregunta.addView(tvResumenP)

            for (alt in pe.alternativas) {
                val contenedorAlternativa = LinearLayout(this).apply {
                    orientation = LinearLayout.VERTICAL
                    layoutParams = LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        LinearLayout.LayoutParams.WRAP_CONTENT
                    ).apply {
                        topMargin = (4 * densidad).toInt()
                        bottomMargin = (6 * densidad).toInt()
                    }
                    setPadding(padAltH, padAltV, padAltH, padAltV)
                    if (alt.esGanadora) setBackgroundResource(R.drawable.bg_winner)
                }

                val filaTexto = LinearLayout(this).apply {
                    orientation = LinearLayout.HORIZONTAL
                    gravity = Gravity.CENTER_VERTICAL
                    layoutParams = LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        LinearLayout.LayoutParams.WRAP_CONTENT
                    )
                }

                val tvNombreAlt = TextView(this).apply {
                    text = if (alt.esGanadora) "Ganadora • ${alt.texto}" else alt.texto
                    textSize = 13f
                    setTypeface(null, if (alt.esGanadora) android.graphics.Typeface.BOLD else android.graphics.Typeface.NORMAL)
                    setTextColor(ContextCompat.getColor(context, if (alt.esGanadora) R.color.warning else R.color.text_primary))
                    layoutParams = LinearLayout.LayoutParams(0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f).apply {
                        marginEnd = (12 * densidad).toInt()
                    }
                }

                val porcentajeFormateado = String.format(Locale.US, "%.1f", alt.porcentaje)
                val tvVotosAlt = TextView(this).apply {
                    text = "${alt.votos} voto(s) ($porcentajeFormateado%)"
                    textSize = 12f
                    setTypeface(null, if (alt.esGanadora) android.graphics.Typeface.BOLD else android.graphics.Typeface.NORMAL)
                    setTextColor(ContextCompat.getColor(context, if (alt.esGanadora) R.color.warning else R.color.accent))
                }

                filaTexto.addView(tvNombreAlt)
                filaTexto.addView(tvVotosAlt)
                contenedorAlternativa.addView(filaTexto)

                val pb = ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal).apply {
                    max = 1000
                    progress = (alt.porcentaje * 10f).roundToInt()
                    progressDrawable = ContextCompat.getDrawable(
                        this@ResultadosActivity,
                        if (alt.esGanadora) R.drawable.bg_progress_bar_winner else R.drawable.bg_progress_bar
                    )
                    layoutParams = LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        (10 * densidad).toInt()
                    ).apply { topMargin = (6 * densidad).toInt() }
                }
                contenedorAlternativa.addView(pb)
                cardPregunta.addView(contenedorAlternativa)
            }

            llResultadosPreguntas.addView(cardPregunta)
        }
    }

    private fun renderizarListaVotantes(listaParticipantes: List<ParticipanteRegistro>) {
        llListaParticipantes.removeAllViews()
        if (listaParticipantes.isEmpty()) {
            tvSinParticipantes.visibility = View.VISIBLE
            return
        }
        tvSinParticipantes.visibility = View.GONE

        val densidad = resources.displayMetrics.density
        val paddingV = (6 * densidad).toInt()

        for ((index, item) in listaParticipantes.withIndex()) {
            val tvFila = TextView(this).apply {
                text = "${index + 1}. ${item.nombre}  •  ${item.fechaVoto}"
                textSize = 13f
                setTextColor(ContextCompat.getColor(context, R.color.text_primary))
                setPadding(0, paddingV, 0, paddingV)
            }
            llListaParticipantes.addView(tvFila)

            if (index < listaParticipantes.size - 1) {
                val lineaDivisora = View(this).apply {
                    layoutParams = LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        (1 * densidad).toInt().coerceAtLeast(1)
                    )
                    setBackgroundColor(ContextCompat.getColor(context, R.color.border_light))
                }
                llListaParticipantes.addView(lineaDivisora)
            }
        }
    }

    private fun mostrarDialogoReiniciarConteo() {
        AlertDialog.Builder(this)
            .setTitle("Confirmar Reinicio de Conteo")
            .setMessage("¿Está seguro de reiniciar los votos a 0 para esta encuesta?\n\nEsta acción eliminará todas las respuestas registradas en la nube.")
            .setIcon(android.R.drawable.ic_dialog_alert)
            .setPositiveButton("Sí, Reiniciar a 0") { dialog, _ ->
                FirebaseRepository.reiniciarVotosEncuesta(idEncuesta) { exito, err ->
                    if (exito) {
                        Toast.makeText(this, "Conteo de votos reiniciado exitosamente.", Toast.LENGTH_SHORT).show()
                        cargarResultados()
                    } else {
                        Toast.makeText(this, "Error al reiniciar: $err", Toast.LENGTH_SHORT).show()
                    }
                }
                dialog.dismiss()
            }
            .setNegativeButton("Cancelar", null)
            .show()
    }
}
