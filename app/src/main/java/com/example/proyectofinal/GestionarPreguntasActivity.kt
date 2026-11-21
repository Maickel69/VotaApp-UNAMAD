package com.example.proyectofinal

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.*
import androidx.activity.OnBackPressedCallback
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity

/**
 * ============================================================================
 * PANTALLA 3: GestionarPreguntasActivity (Gestión de Preguntas y Alternativas)
 * ============================================================================
 * Proyecto: Sistema de Encuestas y Votaciones UNAMAD - EPISI
 * 
 * Funcionalidades:
 *  1. Permite agregar preguntas de Selección Única o de Opción Múltiple.
 *  2. Permite definir de 2 a 4 alternativas de respuesta por pregunta.
 *  3. Lista todas las preguntas actuales de la encuesta en tiempo real.
 *  4. Permite editar y eliminar preguntas con sus alternativas en cascada.
 *  5. Valida que la encuesta tenga al menos una pregunta antes de finalizar.
 */
class GestionarPreguntasActivity : AppCompatActivity() {

    // 1. Gestor de base de datos
    private lateinit var dbHelper: DatabaseHelper

    // 2. Elementos visuales del layout
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

    // 3. Variables de control
    private var idEncuesta: Long = -1L
    private var idPreguntaEnEdicion: Long = -1L // -1 = Creando nueva pregunta; >0 = Editando
    private lateinit var scrollView: ScrollView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_gestionar_preguntas)

        scrollView = findViewById(R.id.scrollGestionarPreguntas)
        configurarEdgeToEdgeConHeader(scrollView, findViewById(R.id.topBar))

        // Obtener ID de la encuesta recibido por Intent
        idEncuesta = intent.getLongExtra(MainActivity.EXTRA_ID_ENCUESTA, -1L)
        if (idEncuesta == -1L) {
            Toast.makeText(this, "Error: No se recibió una encuesta válida.", Toast.LENGTH_SHORT).show()
            finish()
            return
        }

        dbHelper = DatabaseHelper(this)

        vincularVistas()
        cargarDatosEncuesta()
        cargarListaPreguntas()
        configurarEventos()

        // Restaurar modo edición tras rotación de pantalla
        idPreguntaEnEdicion = savedInstanceState?.getLong(KEY_ID_PREGUNTA_EDICION, -1L) ?: -1L
        if (idPreguntaEnEdicion > 0L) {
            tvTituloFormPregunta.text = "Modificar Pregunta"
            btnGuardarPregunta.text = "Actualizar Pregunta"
            btnCancelarEdicion.visibility = View.VISIBLE
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putLong(KEY_ID_PREGUNTA_EDICION, idPreguntaEnEdicion)
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

    /**
     * Muestra el título de la encuesta en la cabecera
     */
    private fun cargarDatosEncuesta() {
        val encuesta = dbHelper.obtenerEncuestaPorId(idEncuesta)
        if (encuesta != null) {
            tvEncuestaTitulo.text = "Encuesta: ${encuesta.titulo}"
        }
    }

    private fun configurarEventos() {
        // Botón Guardar / Actualizar Pregunta
        btnGuardarPregunta.setOnClickListener {
            guardarPregunta()
        }

        // Botón Cancelar modo edición
        btnCancelarEdicion.setOnClickListener {
            limpiarFormulario()
        }

        // Botón Finalizar y Volver
        btnFinalizar.setOnClickListener {
            intentarSalir()
        }

        // Interceptar botón/gesto Atrás del sistema para validar mínimo 1 pregunta
        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                intentarSalir()
            }
        })
    }

    private fun intentarSalir() {
        val total = dbHelper.contarPreguntasDeEncuesta(idEncuesta)
        if (total == 0) {
            AlertDialog.Builder(this)
                .setTitle("Atención")
                .setMessage("Debe registrar al menos 1 pregunta en esta encuesta antes de finalizar.")
                .setPositiveButton("Entendido", null)
                .show()
        } else {
            Toast.makeText(this, "Configuración de preguntas completada.", Toast.LENGTH_SHORT).show()
            finish()
        }
    }

    /**
     * Valida el formulario de la pregunta e inserta o actualiza en SQLite
     */
    private fun guardarPregunta() {
        val textoPregunta = etTextoPregunta.text.toString().trim()

        // Validación 1: Enunciado de la pregunta
        if (textoPregunta.isEmpty()) {
            etTextoPregunta.error = "El enunciado de la pregunta es obligatorio"
            etTextoPregunta.requestFocus()
            Toast.makeText(this, "Por favor ingrese la pregunta.", Toast.LENGTH_SHORT).show()
            return
        }

        // Validación 2: Tipo de pregunta
        val tipo = if (rbTipoMultiple.isChecked) "MULTIPLE" else "UNICA"

        // Validación 3: Al menos 2 alternativas obligatorias
        val alt1 = etAlternativa1.text.toString().trim()
        val alt2 = etAlternativa2.text.toString().trim()
        val alt3 = etAlternativa3.text.toString().trim()
        val alt4 = etAlternativa4.text.toString().trim()

        val alternativas = mutableListOf<String>()
        if (alt1.isNotEmpty()) alternativas.add(alt1)
        if (alt2.isNotEmpty()) alternativas.add(alt2)
        if (alt3.isNotEmpty()) alternativas.add(alt3)
        if (alt4.isNotEmpty()) alternativas.add(alt4)

        if (alternativas.size < 2) {
            Toast.makeText(this, "Debe ingresar al menos 2 alternativas de respuesta.", Toast.LENGTH_LONG).show()
            etAlternativa1.requestFocus()
            return
        }

        // Inserción o Actualización
        if (idPreguntaEnEdicion > 0L) {
            val exito = dbHelper.actualizarPreguntaConAlternativas(idPreguntaEnEdicion, textoPregunta, tipo, alternativas)
            if (exito) {
                Toast.makeText(this, "Pregunta actualizada con éxito.", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Error al actualizar la pregunta.", Toast.LENGTH_SHORT).show()
            }
        } else {
            val idInsertado = dbHelper.insertarPreguntaConAlternativas(idEncuesta, textoPregunta, tipo, alternativas)
            if (idInsertado > 0L) {
                Toast.makeText(this, "Pregunta guardada con éxito.", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Error al guardar la pregunta.", Toast.LENGTH_SHORT).show()
            }
        }

        // Limpiar formulario y refrescar listado
        limpiarFormulario()
        cargarListaPreguntas()
    }

    /**
     * Restaura el formulario a su estado original de "Nueva Pregunta"
     */
    private fun limpiarFormulario() {
        idPreguntaEnEdicion = -1L
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

    /**
     * Carga y dibuja las preguntas registradas de la encuesta
     */
    private fun cargarListaPreguntas() {
        llListaPreguntas.removeAllViews()
        val listaPreguntas = dbHelper.listarPreguntasDeEncuesta(idEncuesta)

        tvTituloListaPreguntas.text = "Preguntas Registradas (${listaPreguntas.size})"

        if (listaPreguntas.isEmpty()) {
            tvSinPreguntas.visibility = View.VISIBLE
            return
        }
        tvSinPreguntas.visibility = View.GONE

        val inflater = LayoutInflater.from(this)

        for ((index, pregunta) in listaPreguntas.withIndex()) {
            val itemVista = inflater.inflate(R.layout.item_pregunta_gestion, llListaPreguntas, false)

            val tvTexto = itemVista.findViewById<TextView>(R.id.tvItemPreguntaTexto)
            val tvTipo = itemVista.findViewById<TextView>(R.id.tvItemPreguntaTipo)
            val tvAlternativas = itemVista.findViewById<TextView>(R.id.tvItemPreguntaAlternativas)
            val btnEditar = itemVista.findViewById<Button>(R.id.btnItemPreguntaEditar)
            val btnEliminar = itemVista.findViewById<Button>(R.id.btnItemPreguntaEliminar)

            tvTexto.text = "${index + 1}. ${pregunta.texto}"
            tvTipo.text = if (pregunta.tipo == "MULTIPLE") "Opción Múltiple" else "Selección Única"

            // Obtener alternativas
            val listaAlt = dbHelper.listarAlternativasDePregunta(pregunta.id)
            val altsTexto = StringBuilder()
            for (alt in listaAlt) {
                altsTexto.append("• ${alt.texto}\n")
            }
            tvAlternativas.text = altsTexto.toString().trimEnd()

            // Acción: Editar pregunta
            btnEditar.setOnClickListener {
                cargarPreguntaParaEditar(pregunta, listaAlt)
            }

            // Acción: Eliminar pregunta
            btnEliminar.setOnClickListener {
                mostrarDialogoEliminarPregunta(pregunta)
            }

            llListaPreguntas.addView(itemVista)
        }
    }

    /**
     * Carga los datos de una pregunta existente en el formulario para modificarla
     */
    private fun cargarPreguntaParaEditar(pregunta: Pregunta, alternativas: List<Alternativa>) {
        idPreguntaEnEdicion = pregunta.id
        tvTituloFormPregunta.text = "Modificar Pregunta"
        btnGuardarPregunta.text = "Actualizar Pregunta"
        btnCancelarEdicion.visibility = View.VISIBLE

        etTextoPregunta.setText(pregunta.texto)
        if (pregunta.tipo == "MULTIPLE") {
            rbTipoMultiple.isChecked = true
        } else {
            rbTipoUnica.isChecked = true
        }

        etAlternativa1.setText(alternativas.getOrNull(0)?.texto ?: "")
        etAlternativa2.setText(alternativas.getOrNull(1)?.texto ?: "")
        etAlternativa3.setText(alternativas.getOrNull(2)?.texto ?: "")
        etAlternativa4.setText(alternativas.getOrNull(3)?.texto ?: "")

        // Desplazar arriba y enfocar el campo para facilidad del usuario
        scrollView.smoothScrollTo(0, 0)
        etTextoPregunta.requestFocus()
        Toast.makeText(this, "Datos cargados en el formulario superior.", Toast.LENGTH_SHORT).show()
    }

    companion object {
        private const val KEY_ID_PREGUNTA_EDICION = "key_id_pregunta_edicion"
    }

    /**
     * Diálogo de confirmación para eliminar una pregunta
     */
    private fun mostrarDialogoEliminarPregunta(pregunta: Pregunta) {
        AlertDialog.Builder(this)
            .setTitle("Confirmar Eliminación")
            .setMessage("¿Desea eliminar la pregunta:\n\"${pregunta.texto}\"?\nSe eliminarán sus alternativas y votos asociados.")
            .setPositiveButton("Eliminar") { dialog, _ ->
                val exito = dbHelper.eliminarPregunta(pregunta.id)
                if (exito) {
                    Toast.makeText(this, "Pregunta eliminada.", Toast.LENGTH_SHORT).show()
                    if (idPreguntaEnEdicion == pregunta.id) {
                        limpiarFormulario()
                    }
                    cargarListaPreguntas()
                } else {
                    Toast.makeText(this, "Error al eliminar la pregunta.", Toast.LENGTH_SHORT).show()
                }
                dialog.dismiss()
            }
            .setNegativeButton("Cancelar", null)
            .show()
    }
}
