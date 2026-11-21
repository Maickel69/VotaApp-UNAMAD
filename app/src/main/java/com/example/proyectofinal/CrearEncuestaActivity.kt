package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.materialswitch.MaterialSwitch

/**
 * ============================================================================
 * PANTALLA 2: CrearEncuestaActivity (Crear y Editar Encuestas en Firestore)
 * ============================================================================
 */
class CrearEncuestaActivity : AppCompatActivity() {

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

    private var idEncuestaEdicion: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_crear_encuesta)

        configurarEdgeToEdgeConHeader(findViewById(R.id.scrollCrearEncuesta), findViewById(R.id.topBar))

        vincularVistas()

        idEncuestaEdicion = intent.getStringExtra(MainActivity.EXTRA_ID_ENCUESTA)
        if (!idEncuestaEdicion.isNullOrBlank()) {
            cargarDatosParaEdicion(idEncuestaEdicion!!)
        }

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

    private fun cargarDatosParaEdicion(idEncuesta: String) {
        tvTituloPantalla.text = "Modificar Encuesta"
        FirebaseRepository.obtenerEncuestaPorId(idEncuesta) { encuesta ->
            if (isFinishing || isDestroyed) return@obtenerEncuestaPorId
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
            } else {
                Toast.makeText(this, "No se encontró la encuesta.", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    private fun configurarEventos() {
        btnGuardarYPreguntas.setOnClickListener {
            guardarEncuesta { idGuardado ->
                val intent = Intent(this, GestionarPreguntasActivity::class.java).apply {
                    putExtra(MainActivity.EXTRA_ID_ENCUESTA, idGuardado)
                }
                startActivity(intent)
                finish()
            }
        }

        btnGuardarYVolver.setOnClickListener {
            guardarEncuesta {
                Toast.makeText(this, "Encuesta guardada en la nube con éxito.", Toast.LENGTH_SHORT).show()
                finish()
            }
        }

        btnCancelar.setOnClickListener { finish() }
    }

    private fun guardarEncuesta(onExito: (String) -> Unit) {
        val titulo = etTituloEncuesta.text.toString().trim()
        val descripcion = etDescripcionEncuesta.text.toString().trim()
        val activa = swActiva.isChecked

        if (titulo.isEmpty()) {
            etTituloEncuesta.error = "El título es obligatorio"
            etTituloEncuesta.requestFocus()
            Toast.makeText(this, "Por favor ingrese el título de la encuesta.", Toast.LENGTH_SHORT).show()
            return
        }

        if (titulo.length < 5) {
            etTituloEncuesta.error = "El título debe contener al menos 5 caracteres"
            etTituloEncuesta.requestFocus()
            Toast.makeText(this, "El título es demasiado corto (mínimo 5 caracteres).", Toast.LENGTH_SHORT).show()
            return
        }

        if (descripcion.isEmpty()) {
            etDescripcionEncuesta.error = "La descripción u objetivo es obligatorio"
            etDescripcionEncuesta.requestFocus()
            Toast.makeText(this, "Por favor ingrese una breve descripción u objetivo.", Toast.LENGTH_SHORT).show()
            return
        }

        val categoria = when (rgCategoria.checkedRadioButtonId) {
            R.id.rbCatSatisfaccion -> "Satisfacción"
            R.id.rbCatVotacion -> "Votación"
            R.id.rbCatGeneral -> "General"
            else -> "Académica"
        }

        btnGuardarYPreguntas.isEnabled = false
        btnGuardarYVolver.isEnabled = false

        val idEdit = idEncuestaEdicion
        if (!idEdit.isNullOrBlank()) {
            FirebaseRepository.actualizarEncuesta(idEdit, titulo, descripcion, categoria, activa) { ok, err ->
                btnGuardarYPreguntas.isEnabled = true
                btnGuardarYVolver.isEnabled = true
                if (ok) {
                    onExito(idEdit)
                } else {
                    Toast.makeText(this, "Error al actualizar: $err", Toast.LENGTH_SHORT).show()
                }
            }
        } else {
            FirebaseRepository.crearEncuesta(titulo, descripcion, categoria, activa) { nuevoId, err ->
                btnGuardarYPreguntas.isEnabled = true
                btnGuardarYVolver.isEnabled = true
                if (nuevoId != null) {
                    onExito(nuevoId)
                } else {
                    Toast.makeText(this, "Error al guardar: $err", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
}
