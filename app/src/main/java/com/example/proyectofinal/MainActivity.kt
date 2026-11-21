package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.google.firebase.Firebase
import com.google.firebase.auth.auth

/**
 * ============================================================================
 * PANTALLA PRINCIPAL: MainActivity (Panel de Control en la Nube - Firestore)
 * ============================================================================
 */
class MainActivity : AppCompatActivity() {

    private lateinit var tvUsuarioActual: TextView
    private lateinit var btnCerrarSesion: Button
    private lateinit var tvTotalEncuestas: TextView
    private lateinit var tvActivasEncuestas: TextView
    private lateinit var tvTotalVotos: TextView
    private lateinit var btnCrearEncuesta: Button
    private lateinit var rgFiltro: RadioGroup
    private lateinit var rbFiltroTodas: RadioButton
    private lateinit var rbFiltroActivas: RadioButton
    private lateinit var rbFiltroCerradas: RadioButton
    private lateinit var llContenedorEncuestas: LinearLayout
    private lateinit var tvSinEncuestas: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        configurarEdgeToEdgeConHeader(findViewById(R.id.main), findViewById(R.id.topBar))

        if (Firebase.auth.currentUser == null) {
            irALogin()
            return
        }

        vincularVistas()
        configurarEventos()
        tvUsuarioActual.text = "Hola, ${FirebaseRepository.currentDisplayName()}"
    }

    override fun onResume() {
        super.onResume()
        if (Firebase.auth.currentUser != null) {
            cargarEncuestas()
        }
    }

    private fun vincularVistas() {
        tvUsuarioActual = findViewById(R.id.tvUsuarioActual)
        btnCerrarSesion = findViewById(R.id.btnCerrarSesion)
        tvTotalEncuestas = findViewById(R.id.tvTotalEncuestas)
        tvActivasEncuestas = findViewById(R.id.tvActivasEncuestas)
        tvTotalVotos = findViewById(R.id.tvTotalVotos)
        btnCrearEncuesta = findViewById(R.id.btnCrearEncuesta)
        rgFiltro = findViewById(R.id.rgFiltro)
        rbFiltroTodas = findViewById(R.id.rbFiltroTodas)
        rbFiltroActivas = findViewById(R.id.rbFiltroActivas)
        rbFiltroCerradas = findViewById(R.id.rbFiltroCerradas)
        llContenedorEncuestas = findViewById(R.id.llContenedorEncuestas)
        tvSinEncuestas = findViewById(R.id.tvSinEncuestas)
    }

    private fun configurarEventos() {
        btnCrearEncuesta.setOnClickListener {
            startActivity(Intent(this, CrearEncuestaActivity::class.java))
        }

        rgFiltro.setOnCheckedChangeListener { _, _ ->
            cargarEncuestas()
        }

        btnCerrarSesion.setOnClickListener {
            AlertDialog.Builder(this)
                .setTitle("Cerrar Sesión")
                .setMessage("¿Desea cerrar su sesión actual (${FirebaseRepository.currentDisplayName()})?")
                .setPositiveButton("Sí, Salir") { _, _ ->
                    Firebase.auth.signOut()
                    irALogin()
                }
                .setNegativeButton("Cancelar", null)
                .show()
        }
    }

    private fun irALogin() {
        startActivity(Intent(this, LoginActivity::class.java))
        finish()
    }

    private fun cargarEncuestas() {
        val filtro = when {
            rbFiltroActivas.isChecked -> "ACTIVAS"
            rbFiltroCerradas.isChecked -> "CERRADAS"
            else -> "TODAS"
        }

        FirebaseRepository.listarEncuestas(filtro) { listaEncuestas, conteos, error ->
            if (isFinishing || isDestroyed) return@listarEncuestas

            if (error != null) {
                Toast.makeText(this, "Error Firestore: $error", Toast.LENGTH_LONG).show()
            }

            tvTotalEncuestas.text = conteos.first.toString()
            tvActivasEncuestas.text = conteos.second.toString()
            tvTotalVotos.text = conteos.third.toString()

            llContenedorEncuestas.removeAllViews()

            if (listaEncuestas.isEmpty()) {
                tvSinEncuestas.visibility = View.VISIBLE
                return@listarEncuestas
            }
            tvSinEncuestas.visibility = View.GONE

            val inflater = LayoutInflater.from(this)
            val miUid = FirebaseRepository.currentUid()

            for (encuesta in listaEncuestas) {
                val itemVista = inflater.inflate(R.layout.item_encuesta, llContenedorEncuestas, false)

                val tvTitulo = itemVista.findViewById<TextView>(R.id.tvItemTitulo)
                val tvEstado = itemVista.findViewById<TextView>(R.id.tvItemEstado)
                val tvCategoria = itemVista.findViewById<TextView>(R.id.tvItemCategoria)
                val tvFecha = itemVista.findViewById<TextView>(R.id.tvItemFecha)
                val tvDescripcion = itemVista.findViewById<TextView>(R.id.tvItemDescripcion)
                val tvInfo = itemVista.findViewById<TextView>(R.id.tvItemInfo)
                val btnVotar = itemVista.findViewById<Button>(R.id.btnItemVotar)
                val btnResultados = itemVista.findViewById<Button>(R.id.btnItemResultados)
                val btnEditar = itemVista.findViewById<Button>(R.id.btnItemEditar)
                val btnEliminar = itemVista.findViewById<Button>(R.id.btnItemEliminar)

                tvTitulo.text = encuesta.titulo
                tvCategoria.text = encuesta.categoria
                tvFecha.text = "${encuesta.fechaCreacion} • Por ${encuesta.creadorNombre}"
                tvDescripcion.text = encuesta.descripcion
                tvInfo.text = "${encuesta.totalPreguntas} Preguntas  •  ${encuesta.totalVotos} Participantes"

                if (encuesta.activa) {
                    tvEstado.text = "Activa"
                    tvEstado.setBackgroundResource(R.drawable.bg_badge_active)
                    tvEstado.setTextColor(ContextCompat.getColor(this, R.color.success))
                } else {
                    tvEstado.text = "Cerrada"
                    tvEstado.setBackgroundResource(R.drawable.bg_badge_closed)
                    tvEstado.setTextColor(ContextCompat.getColor(this, R.color.danger))
                }

                // Solo el creador de la encuesta puede editarla o eliminarla
                val esCreador = miUid != null && encuesta.creadorUid == miUid
                btnEditar.visibility = if (esCreador) View.VISIBLE else View.GONE
                btnEliminar.visibility = if (esCreador) View.VISIBLE else View.GONE

                btnVotar.setOnClickListener {
                    if (!encuesta.activa) {
                        Toast.makeText(this, "Esta encuesta se encuentra cerrada para votaciones.", Toast.LENGTH_SHORT).show()
                    } else if (encuesta.totalPreguntas == 0) {
                        Toast.makeText(this, "Esta encuesta no tiene preguntas registradas aún.", Toast.LENGTH_SHORT).show()
                    } else {
                        val intent = Intent(this, RegistrarVotoActivity::class.java).apply {
                            putExtra(EXTRA_ID_ENCUESTA, encuesta.id)
                        }
                        startActivity(intent)
                    }
                }

                btnResultados.setOnClickListener {
                    val intent = Intent(this, ResultadosActivity::class.java).apply {
                        putExtra(EXTRA_ID_ENCUESTA, encuesta.id)
                    }
                    startActivity(intent)
                }

                btnEditar.setOnClickListener {
                    val intent = Intent(this, CrearEncuestaActivity::class.java).apply {
                        putExtra(EXTRA_ID_ENCUESTA, encuesta.id)
                    }
                    startActivity(intent)
                }

                btnEliminar.setOnClickListener {
                    mostrarDialogoEliminar(encuesta)
                }

                llContenedorEncuestas.addView(itemVista)
            }
        }
    }

    private fun mostrarDialogoEliminar(encuesta: Encuesta) {
        AlertDialog.Builder(this)
            .setTitle("Confirmar Eliminación")
            .setMessage("¿Está seguro de eliminar permanentemente la encuesta:\n\"${encuesta.titulo}\"?\n\nSe eliminarán todas sus preguntas, alternativas y registros de votación en la nube.")
            .setIcon(android.R.drawable.ic_dialog_alert)
            .setPositiveButton("Sí, Eliminar") { dialog, _ ->
                FirebaseRepository.eliminarEncuesta(encuesta.id) { exito, err ->
                    if (exito) {
                        Toast.makeText(this, "Encuesta eliminada correctamente.", Toast.LENGTH_SHORT).show()
                        cargarEncuestas()
                    } else {
                        Toast.makeText(this, "Error al eliminar: $err", Toast.LENGTH_SHORT).show()
                    }
                }
                dialog.dismiss()
            }
            .setNegativeButton("Cancelar") { dialog, _ -> dialog.dismiss() }
            .show()
    }

    companion object {
        const val EXTRA_ID_ENCUESTA = "extra_id_encuesta"
    }
}
