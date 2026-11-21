package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.materialswitch.MaterialSwitch

/**
 * ============================================================================
 * PANTALLA 2: CrearEncuestaActivity (Crear y Editar Encuestas - CRUD Encuestas)
 * ============================================================================
 * Proyecto: Sistema de Encuestas y Votaciones UNAMAD - EPISI
 * 
 * Funcionalidades:
 *  1. Permite registrar una nueva encuesta con título, descripción, categoría y estado.
 *  2. Permite editar una encuesta existente si recibe el ID por Intent.
 *  3. Valida campos obligatorios con retroalimentación clara para el usuario.
 *  4. Da la opción de guardar y volver o guardar y pasar a gestionar preguntas.
 */
class CrearEncuestaActivity : AppCompatActivity() {

    // 1. Instancia del gestor de base de datos
    private lateinit var dbHelper: DatabaseHelper

    // 2. Elementos visuales del layout
    private lateinit var tvTituloPantalla: TextView
    private lateinit var etTituloEncuesta: EditText
    private lateinit var etDescripcionEncuesta: EditText
    private lateinit var rgCategoria: RadioGroup
    private lateinit var rbCatAcademica: RadioButton
    private lateinit var rbCatSatisfaccion: RadioButton
    private lateinit var rbCatVotacion: RadioButton
    private lateinit var rbCatGeneral: RadioButton
    private lateinit var swActiva: MaterialSwitch
    private lateinit var btnGuardarYPreguntas: Button
    private lateinit var btnGuardarYVolver: Button
    private lateinit var btnCancelar: Button

    // 3. Variable para identificar si estamos creando (-1) o editando (> 0)
    private var idEncuestaEdicion: Long = -1L

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_crear_encuesta)

        configurarEdgeToEdgeConHeader(findViewById(R.id.scrollCrearEncuesta), findViewById(R.id.topBar))

        // Inicializar helper de base de datos
        dbHelper = DatabaseHelper(this)

        // Vincular componentes XML
        vincularVistas()

        // Verificar si se recibió un ID para edición
        idEncuestaEdicion = intent.getLongExtra(MainActivity.EXTRA_ID_ENCUESTA, -1L)
        if (idEncuestaEdicion > 0L) {
            cargarDatosParaEdicion()
        }

        // Configurar acciones de los botones
        configurarEventos()
    }

    private fun vincularVistas() {
        tvTituloPantalla = findViewById(R.id.tvTituloPantalla)
        etTituloEncuesta = findViewById(R.id.etTituloEncuesta)
        etDescripcionEncuesta = findViewById(R.id.etDescripcionEncuesta)
        rgCategoria = findViewById(R.id.rgCategoria)
        rbCatAcademica = findViewById(R.id.rbCatAcademica)
        rbCatSatisfaccion = findViewById(R.id.rbCatSatisfaccion)
        rbCatVotacion = findViewById(R.id.rbCatVotacion)
        rbCatGeneral = findViewById(R.id.rbCatGeneral)
        swActiva = findViewById(R.id.swActiva)
        btnGuardarYPreguntas = findViewById(R.id.btnGuardarYPreguntas)
        btnGuardarYVolver = findViewById(R.id.btnGuardarYVolver)
        btnCancelar = findViewById(R.id.btnCancelar)
    }

    /**
     * Carga la información de la encuesta en los campos cuando se está en modo edición
     */
    private fun cargarDatosParaEdicion() {
        tvTituloPantalla.text = "Modificar Encuesta"
        val encuesta = dbHelper.obtenerEncuestaPorId(idEncuestaEdicion)

        if (encuesta != null) {
            etTituloEncuesta.setText(encuesta.titulo)
            etDescripcionEncuesta.setText(encuesta.descripcion)
            swActiva.isChecked = encuesta.activa

            when (encuesta.categoria) {
                "Satisfacción" -> rbCatSatisfaccion.isChecked = true
                "Votación", "Votación Estudiantil" -> rbCatVotacion.isChecked = true
                "General" -> rbCatGeneral.isChecked = true
                else -> rbCatAcademica.isChecked = true
            }
        }
    }

    private fun configurarEventos() {
        // Opción 1: Guardar e ir a gestionar preguntas de inmediato
        btnGuardarYPreguntas.setOnClickListener {
            val idGuardado = guardarEncuesta()
            if (idGuardado > 0L) {
                val intent = Intent(this, GestionarPreguntasActivity::class.java).apply {
                    putExtra(MainActivity.EXTRA_ID_ENCUESTA, idGuardado)
                }
                startActivity(intent)
                finish()
            }
        }

        // Opción 2: Guardar y volver a la pantalla principal
        btnGuardarYVolver.setOnClickListener {
            val idGuardado = guardarEncuesta()
            if (idGuardado > 0L) {
                Toast.makeText(this, "Encuesta guardada con éxito.", Toast.LENGTH_SHORT).show()
                finish()
            }
        }

        // Opción 3: Cancelar
        btnCancelar.setOnClickListener {
            finish()
        }
    }

    /**
     * Valida los datos del formulario y realiza la inserción o actualización en SQLite
     * @return ID de la encuesta si fue exitoso, -1L si falló la validación
     */
    private fun guardarEncuesta(): Long {
        val titulo = etTituloEncuesta.text.toString().trim()
        val descripcion = etDescripcionEncuesta.text.toString().trim()
        val activa = swActiva.isChecked

        // Validación 1: Título no vacío y con longitud mínima
        if (titulo.isEmpty()) {
            etTituloEncuesta.error = "El título es obligatorio"
            etTituloEncuesta.requestFocus()
            Toast.makeText(this, "Por favor ingrese el título de la encuesta.", Toast.LENGTH_SHORT).show()
            return -1L
        }

        if (titulo.length < 5) {
            etTituloEncuesta.error = "El título debe contener al menos 5 caracteres"
            etTituloEncuesta.requestFocus()
            Toast.makeText(this, "El título es demasiado corto (mínimo 5 caracteres).", Toast.LENGTH_SHORT).show()
            return -1L
        }

        // Validación 2: Descripción no vacía
        if (descripcion.isEmpty()) {
            etDescripcionEncuesta.error = "La descripción u objetivo es obligatorio"
            etDescripcionEncuesta.requestFocus()
            Toast.makeText(this, "Por favor ingrese una breve descripción u objetivo.", Toast.LENGTH_SHORT).show()
            return -1L
        }

        // Obtener categoría seleccionada
        val categoria = when (rgCategoria.checkedRadioButtonId) {
            R.id.rbCatSatisfaccion -> "Satisfacción"
            R.id.rbCatVotacion -> "Votación"
            R.id.rbCatGeneral -> "General"
            else -> "Académica"
        }

        // Guardar o Actualizar en la base de datos
        val resultado = if (idEncuestaEdicion > 0L) {
            val actualizado = dbHelper.actualizarEncuesta(idEncuestaEdicion, titulo, descripcion, categoria, activa)
            if (actualizado) idEncuestaEdicion else -1L
        } else {
            dbHelper.crearEncuesta(titulo, descripcion, categoria, activa)
        }
        if (resultado <= 0L) {
            Toast.makeText(this, "No se pudo guardar la encuesta. Inténtelo nuevamente.", Toast.LENGTH_SHORT).show()
        }
        return resultado
    }
}
