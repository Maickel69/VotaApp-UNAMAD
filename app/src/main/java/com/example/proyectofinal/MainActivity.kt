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

/**
 * ============================================================================
 * PANTALLA PRINCIPAL: MainActivity (Panel de Control y Listado)
 * ============================================================================
 * Proyecto: Sistema de Encuestas y Votaciones UNAMAD - EPISI
 * 
 * Funcionalidades:
 *  1. Presenta métricas institucionales en tiempo real (Encuestas, Activas, Votos).
 *  2. Permite filtrar encuestas por estado (Todas / Activas / Cerradas).
 *  3. Lista dinámicamente cada encuesta con sus datos clave y estado visual.
 *  4. Provee acciones rápidas: Votar, Ver Resultados, Editar y Eliminar (CRUD).
 */
class MainActivity : AppCompatActivity() {

    // 1. Instancia del gestor de base de datos SQLite
    private lateinit var dbHelper: DatabaseHelper

    // 2. Elementos visuales del layout
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

        // Ajuste para barras del sistema (Edge to Edge con encabezado continuo)
        configurarEdgeToEdgeConHeader(findViewById(R.id.main), findViewById(R.id.topBar))

        // 3. Inicializar el acceso a la base de datos
        dbHelper = DatabaseHelper(this)

        // 4. Vincular controles visuales del archivo XML
        vincularVistas()

        // 5. Configurar eventos de los botones y filtros
        configurarEventos()
    }

    override fun onResume() {
        super.onResume()
        // Cada vez que el usuario regrese a la pantalla principal, recargamos la lista y contadores
        cargarEncuestas()
    }

    /**
     * Conecta las variables con sus respectivos IDs en activity_main.xml
     */
    private fun vincularVistas() {
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

    /**
     * Configura los listeners para el botón de creación y el selector de filtros
     */
    private fun configurarEventos() {
        // Botón para crear una nueva encuesta
        btnCrearEncuesta.setOnClickListener {
            val intent = Intent(this, CrearEncuestaActivity::class.java)
            startActivity(intent)
        }

        // Filtro rápido por estado (Todas / Activas / Cerradas)
        rgFiltro.setOnCheckedChangeListener { _, _ ->
            cargarEncuestas()
        }
    }

    /**
     * Consulta la base de datos SQLite y genera las tarjetas visuales de cada encuesta
     */
    private fun cargarEncuestas() {
        // A. Actualizar contadores del panel superior
        val (total, activas, votos) = dbHelper.obtenerConteoGeneral()
        tvTotalEncuestas.text = total.toString()
        tvActivasEncuestas.text = activas.toString()
        tvTotalVotos.text = votos.toString()

        // B. Determinar el filtro seleccionado
        val filtro = when {
            rbFiltroActivas.isChecked -> "ACTIVAS"
            rbFiltroCerradas.isChecked -> "CERRADAS"
            else -> "TODAS"
        }

        // C. Obtener lista desde SQLite
        val listaEncuestas = dbHelper.listarEncuestas(filtro)

        // Limpiar el contenedor previo
        llContenedorEncuestas.removeAllViews()

        // Si no hay registros, mostrar mensaje vacío
        if (listaEncuestas.isEmpty()) {
            tvSinEncuestas.visibility = View.VISIBLE
            return
        }
        tvSinEncuestas.visibility = View.GONE

        val inflater = LayoutInflater.from(this)

        // D. Construir e inflar dinámicamente cada tarjeta de encuesta
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

            // Asignar datos del modelo a la vista
            tvTitulo.text = encuesta.titulo
            tvCategoria.text = encuesta.categoria
            tvFecha.text = encuesta.fechaCreacion
            tvDescripcion.text = encuesta.descripcion
            tvInfo.text = "${encuesta.totalPreguntas} Preguntas  •  ${encuesta.totalVotos} Participantes"

            // Configurar badge de estado visual
            if (encuesta.activa) {
                tvEstado.text = "Activa"
                tvEstado.setBackgroundResource(R.drawable.bg_badge_active)
                tvEstado.setTextColor(ContextCompat.getColor(this, R.color.success))
            } else {
                tvEstado.text = "Cerrada"
                tvEstado.setBackgroundResource(R.drawable.bg_badge_closed)
                tvEstado.setTextColor(ContextCompat.getColor(this, R.color.danger))
            }

            // 1. Acción: Votar en la encuesta
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

            // 2. Acción: Ver resultados estadísticos
            btnResultados.setOnClickListener {
                val intent = Intent(this, ResultadosActivity::class.java).apply {
                    putExtra(EXTRA_ID_ENCUESTA, encuesta.id)
                }
                startActivity(intent)
            }

            // 3. Acción: Editar encuesta
            btnEditar.setOnClickListener {
                val intent = Intent(this, CrearEncuestaActivity::class.java).apply {
                    putExtra(EXTRA_ID_ENCUESTA, encuesta.id)
                }
                startActivity(intent)
            }

            // 4. Acción: Eliminar encuesta (con confirmación)
            btnEliminar.setOnClickListener {
                mostrarDialogoEliminar(encuesta)
            }

            // Agregar la tarjeta construida al contenedor principal
            llContenedorEncuestas.addView(itemVista)
        }
    }

    /**
     * Muestra una ventana de diálogo (AlertDialog) para confirmar la eliminación de la encuesta
     */
    private fun mostrarDialogoEliminar(encuesta: Encuesta) {
        AlertDialog.Builder(this)
            .setTitle("Confirmar Eliminación")
            .setMessage("¿Está seguro de eliminar permanentemente la encuesta:\n\"${encuesta.titulo}\"?\n\nSe eliminarán todas sus preguntas, alternativas y registros de votación.")
            .setIcon(android.R.drawable.ic_dialog_alert)
            .setPositiveButton("Sí, Eliminar") { dialog, _ ->
                val exito = dbHelper.eliminarEncuesta(encuesta.id)
                if (exito) {
                    Toast.makeText(this, "Encuesta eliminada correctamente.", Toast.LENGTH_SHORT).show()
                    cargarEncuestas()
                } else {
                    Toast.makeText(this, "Error al intentar eliminar la encuesta.", Toast.LENGTH_SHORT).show()
                }
                dialog.dismiss()
            }
            .setNegativeButton("Cancelar") { dialog, _ ->
                dialog.dismiss()
            }
            .show()
    }

    companion object {
        const val EXTRA_ID_ENCUESTA = "extra_id_encuesta"
    }
}
