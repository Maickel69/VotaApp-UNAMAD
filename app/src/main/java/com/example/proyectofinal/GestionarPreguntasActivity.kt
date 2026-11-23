package com.example.proyectofinal

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.*
import androidx.activity.OnBackPressedCallback
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import java.util.UUID

/**
 * ============================================================================
 * PANTALLA 3: GestionarPreguntasActivity (CRUD Preguntas en Firestore)
 * ============================================================================
 */
class GestionarPreguntasActivity : AppCompatActivity() {

    private lateinit var tvEncuestaTitulo: TextView
    private lateinit var tvTituloFormPregunta: TextView
    private lateinit var etTextoPregunta: EditText
    private lateinit var rgTipoPregunta: RadioGroup
    private lateinit var rbTipoUnica: RadioButton
    private lateinit var rbTipoMultiple: RadioButton
    private lateinit var etAlternativa1: EditText
    private lateinit var etAlternativa2: EditText
    private lateinit var etAlternativa3: EditText
    private lateinit var etAlternativa4: EditText
    private lateinit var btnGuardarPregunta: Button
    private lateinit var btnCancelarEdicion: Button
    private lateinit var tvTituloListaPreguntas: TextView
    private lateinit var tvSinPreguntas: TextView
    private lateinit var llListaPreguntas: LinearLayout
    private lateinit var btnFinalizar: Button
    private lateinit var scrollView: ScrollView

    private var idEncuesta: String = ""
    private var idPreguntaEnEdicion: String? = null
    private val preguntasActuales = ArrayList<Pregunta>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_gestionar_preguntas)

        scrollView = findViewById(R.id.scrollGestionarPreguntas)
        configurarEdgeToEdgeConHeader(scrollView, findViewById(R.id.topBar))

        idEncuesta = intent.getStringExtra(MainActivity.EXTRA_ID_ENCUESTA) ?: ""
        if (idEncuesta.isBlank()) {
            Toast.makeText(this, "Error: No se recibió una encuesta válida.", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        vincularVistas()
        configurarEventos()

        idPreguntaEnEdicion = savedInstanceState?.getString(KEY_ID_PREGUNTA_EDICION)
        if (!idPreguntaEnEdicion.isNullOrBlank()) {
            tvTituloFormPregunta.text = "Modificar Pregunta"
            btnGuardarPregunta.text = "Actualizar Pregunta"
            btnCancelarEdicion.visibility = View.VISIBLE
        }

        cargarEncuestaYPreguntas()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        if (idPreguntaEnEdicion != null) {
            outState.putString(KEY_ID_PREGUNTA_EDICION, idPreguntaEnEdicion)
        }
    }

    private fun vincularVistas() {
        tvEncuestaTitulo = findViewById(R.id.tvEncuestaTitulo)
        tvTituloFormPregunta = findViewById(R.id.tvTituloFormPregunta)
        etTextoPregunta = findViewById(R.id.etTextoPregunta)
        rgTipoPregunta = findViewById(R.id.rgTipoPregunta)
        rbTipoUnica = findViewById(R.id.rbTipoUnica)
        rbTipoMultiple = findViewById(R.id.rbTipoMultiple)
        etAlternativa1 = findViewById(R.id.etAlternativa1)
        etAlternativa2 = findViewById(R.id.etAlternativa2)
        etAlternativa3 = findViewById(R.id.etAlternativa3)
        etAlternativa4 = findViewById(R.id.etAlternativa4)
        btnGuardarPregunta = findViewById(R.id.btnGuardarPregunta)
        btnCancelarEdicion = findViewById(R.id.btnCancelarEdicion)
        tvTituloListaPreguntas = findViewById(R.id.tvTituloListaPreguntas)
        tvSinPreguntas = findViewById(R.id.tvSinPreguntas)
        llListaPreguntas = findViewById(R.id.llListaPreguntas)
        btnFinalizar = findViewById(R.id.btnFinalizar)
    }

    private fun cargarEncuestaYPreguntas() {
        FirebaseRepository.obtenerEncuestaPorId(idEncuesta) { encuesta ->
            if (isFinishing || isDestroyed) return@obtenerEncuestaPorId
            if (encuesta == null) {
                Toast.makeText(this, "No se encontró la encuesta.", Toast.LENGTH_SHORT).show()
                finish()
                return@obtenerEncuestaPorId
            }
            tvEncuestaTitulo.text = "Encuesta: ${encuesta.titulo}"
            preguntasActuales.clear()
            preguntasActuales.addAll(encuesta.preguntas)
            renderizarListaPreguntas()
        }
    }

    private fun configurarEventos() {
        btnGuardarPregunta.setOnClickListener { guardarPregunta() }
        btnCancelarEdicion.setOnClickListener { limpiarFormulario() }
        btnFinalizar.setOnClickListener { intentarSalir() }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                intentarSalir()
            }
        })
    }

    private fun intentarSalir() {
        if (preguntasActuales.isEmpty()) {
            MaterialAlertDialogBuilder(this)
                .setTitle("Atención")
                .setMessage("Debe registrar al menos 1 pregunta en esta encuesta antes de finalizar.")
                .setPositiveButton("Entendido", null)
                .show()
        } else {
            Toast.makeText(this, "Configuración de preguntas completada.", Toast.LENGTH_SHORT).show()
            finish()
        }
    }

    private fun guardarPregunta() {
        val textoPregunta = etTextoPregunta.text.toString().trim()
        if (textoPregunta.isEmpty()) {
            etTextoPregunta.error = "El enunciado de la pregunta es obligatorio"
            etTextoPregunta.requestFocus()
            Toast.makeText(this, "Por favor ingrese la pregunta.", Toast.LENGTH_SHORT).show()
            return
        }

        val tipo = if (rbTipoMultiple.isChecked) "MULTIPLE" else "UNICA"

        val textosAlt = listOf(
            etAlternativa1.text.toString().trim(),
            etAlternativa2.text.toString().trim(),
            etAlternativa3.text.toString().trim(),
            etAlternativa4.text.toString().trim()
        ).filter { it.isNotEmpty() }

        if (textosAlt.size < 2) {
            Toast.makeText(this, "Debe ingresar al menos 2 alternativas de respuesta.", Toast.LENGTH_LONG).show()
            etAlternativa1.requestFocus()
            return
        }

        val nuevasAlternativas = textosAlt.map { texto ->
            Alternativa(id = UUID.randomUUID().toString(), texto = texto)
        }

        val nuevaLista = ArrayList(preguntasActuales)
        val editId = idPreguntaEnEdicion
        if (!editId.isNullOrBlank()) {
            val idx = nuevaLista.indexOfFirst { it.id == editId }
            if (idx >= 0) {
                nuevaLista[idx] = Pregunta(id = editId, texto = textoPregunta, tipo = tipo, alternativas = nuevasAlternativas)
            }
        } else {
            nuevaLista.add(
                Pregunta(
                    id = UUID.randomUUID().toString(),
                    texto = textoPregunta,
                    tipo = tipo,
                    alternativas = nuevasAlternativas
                )
            )
        }

        btnGuardarPregunta.isEnabled = false
        FirebaseRepository.guardarPreguntasEncuesta(idEncuesta, nuevaLista) { ok, err ->
            btnGuardarPregunta.isEnabled = true
            if (ok) {
                preguntasActuales.clear()
                preguntasActuales.addAll(nuevaLista)
                Toast.makeText(
                    this,
                    if (!editId.isNullOrBlank()) "Pregunta actualizada con éxito." else "Pregunta guardada con éxito.",
                    Toast.LENGTH_SHORT
                ).show()
                limpiarFormulario()
                renderizarListaPreguntas()
            } else {
                Toast.makeText(this, "Error al guardar: $err", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun limpiarFormulario() {
        idPreguntaEnEdicion = null
        tvTituloFormPregunta.text = "Agregar Nueva Pregunta"
        btnGuardarPregunta.text = "Guardar Pregunta"
        btnCancelarEdicion.visibility = View.GONE

        etTextoPregunta.setText("")
        etTextoPregunta.error = null
        rbTipoUnica.isChecked = true

        etAlternativa1.setText("")
        etAlternativa2.setText("")
        etAlternativa3.setText("")
        etAlternativa4.setText("")
    }

    private fun renderizarListaPreguntas() {
        llListaPreguntas.removeAllViews()
        tvTituloListaPreguntas.text = "Preguntas Registradas (${preguntasActuales.size})"

        if (preguntasActuales.isEmpty()) {
            tvSinPreguntas.visibility = View.VISIBLE
            return
        }
        tvSinPreguntas.visibility = View.GONE

        val inflater = LayoutInflater.from(this)
        for ((index, pregunta) in preguntasActuales.withIndex()) {
            val itemVista = inflater.inflate(R.layout.item_pregunta_gestion, llListaPreguntas, false)

            val tvTexto = itemVista.findViewById<TextView>(R.id.tvItemPreguntaTexto)
            val tvTipo = itemVista.findViewById<TextView>(R.id.tvItemPreguntaTipo)
            val tvAlternativas = itemVista.findViewById<TextView>(R.id.tvItemPreguntaAlternativas)
            val btnEditar = itemVista.findViewById<Button>(R.id.btnItemPreguntaEditar)
            val btnEliminar = itemVista.findViewById<Button>(R.id.btnItemPreguntaEliminar)

            tvTexto.text = "${index + 1}. ${pregunta.texto}"
            tvTipo.text = if (pregunta.tipo == "MULTIPLE") "Opción Múltiple" else "Selección Única"
            tvAlternativas.text = pregunta.alternativas.joinToString("\n") { "• ${it.texto}" }

            btnEditar.setOnClickListener { cargarPreguntaParaEditar(pregunta) }
            btnEliminar.setOnClickListener { mostrarDialogoEliminarPregunta(pregunta) }

            llListaPreguntas.addView(itemVista)
        }
    }

    private fun cargarPreguntaParaEditar(pregunta: Pregunta) {
        idPreguntaEnEdicion = pregunta.id
        tvTituloFormPregunta.text = "Modificar Pregunta"
        btnGuardarPregunta.text = "Actualizar Pregunta"
        btnCancelarEdicion.visibility = View.VISIBLE

        etTextoPregunta.setText(pregunta.texto)
        if (pregunta.tipo == "MULTIPLE") rbTipoMultiple.isChecked = true else rbTipoUnica.isChecked = true

        etAlternativa1.setText(pregunta.alternativas.getOrNull(0)?.texto ?: "")
        etAlternativa2.setText(pregunta.alternativas.getOrNull(1)?.texto ?: "")
        etAlternativa3.setText(pregunta.alternativas.getOrNull(2)?.texto ?: "")
        etAlternativa4.setText(pregunta.alternativas.getOrNull(3)?.texto ?: "")

        scrollView.smoothScrollTo(0, 0)
        etTextoPregunta.requestFocus()
        Toast.makeText(this, "Datos cargados en el formulario superior.", Toast.LENGTH_SHORT).show()
    }

    private fun mostrarDialogoEliminarPregunta(pregunta: Pregunta) {
        MaterialAlertDialogBuilder(this)
            .setTitle("Confirmar Eliminación")
            .setMessage("¿Desea eliminar la pregunta:\n\"${pregunta.texto}\"?")
            .setPositiveButton("Eliminar") { dialog, _ ->
                val nuevaLista = preguntasActuales.filter { it.id != pregunta.id }
                FirebaseRepository.guardarPreguntasEncuesta(idEncuesta, nuevaLista) { ok, err ->
                    if (ok) {
                        preguntasActuales.clear()
                        preguntasActuales.addAll(nuevaLista)
                        Toast.makeText(this, "Pregunta eliminada.", Toast.LENGTH_SHORT).show()
                        if (idPreguntaEnEdicion == pregunta.id) limpiarFormulario()
                        renderizarListaPreguntas()
                    } else {
                        Toast.makeText(this, "Error al eliminar: $err", Toast.LENGTH_SHORT).show()
                    }
                }
                dialog.dismiss()
            }
            .setNegativeButton("Cancelar", null)
            .show()
    }

    companion object {
        private const val KEY_ID_PREGUNTA_EDICION = "key_id_pregunta_edicion"
    }
}
