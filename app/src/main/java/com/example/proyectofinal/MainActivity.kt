package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.LayoutInflater
import android.view.View
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.google.android.material.chip.ChipGroup
import com.google.firebase.Firebase
import com.google.firebase.auth.UserProfileChangeRequest
import com.google.firebase.auth.auth

/**
 * ============================================================================
 * PANTALLA PRINCIPAL: MainActivity (Panel Cloud + Búsqueda + Categorías + Perfil)
 * ============================================================================
 */
class MainActivity : AppCompatActivity() {

    private lateinit var swipeRefreshMain: SwipeRefreshLayout
    private lateinit var tvUsuarioActual: TextView
    private lateinit var btnCerrarSesion: Button
    private lateinit var tvTotalEncuestas: TextView
    private lateinit var tvActivasEncuestas: TextView
    private lateinit var tvTotalVotos: TextView
    private lateinit var btnCrearEncuesta: Button
    private lateinit var etBuscarEncuesta: EditText
    private lateinit var cgCategorias: ChipGroup
    private lateinit var rgFiltro: RadioGroup
    private lateinit var rbFiltroTodas: RadioButton
    private lateinit var rbFiltroActivas: RadioButton
    private lateinit var rbFiltroCerradas: RadioButton
    private lateinit var llContenedorEncuestas: LinearLayout
    private lateinit var llEstadoVacio: LinearLayout
    private lateinit var tvSinEncuestas: TextView
    private lateinit var btnCargarDemo: Button

    private var cacheEncuestas: List<Encuesta> = emptyList()

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
        actualizarSaludo()
    }

    override fun onResume() {
        super.onResume()
        if (Firebase.auth.currentUser != null) {
            actualizarSaludo()
            cargarEncuestasDesdeNube()
        }
    }

    private fun actualizarSaludo() {
        tvUsuarioActual.text = "Hola, ${FirebaseRepository.currentDisplayName()}"
    }

    private fun vincularVistas() {
        swipeRefreshMain = findViewById(R.id.swipeRefreshMain)
        tvUsuarioActual = findViewById(R.id.tvUsuarioActual)
        btnCerrarSesion = findViewById(R.id.btnCerrarSesion)
        tvTotalEncuestas = findViewById(R.id.tvTotalEncuestas)
        tvActivasEncuestas = findViewById(R.id.tvActivasEncuestas)
        tvTotalVotos = findViewById(R.id.tvTotalVotos)
        btnCrearEncuesta = findViewById(R.id.btnCrearEncuesta)
        etBuscarEncuesta = findViewById(R.id.etBuscarEncuesta)
        cgCategorias = findViewById(R.id.cgCategorias)
        rgFiltro = findViewById(R.id.rgFiltro)
        rbFiltroTodas = findViewById(R.id.rbFiltroTodas)
        rbFiltroActivas = findViewById(R.id.rbFiltroActivas)
        rbFiltroCerradas = findViewById(R.id.rbFiltroCerradas)
        llContenedorEncuestas = findViewById(R.id.llContenedorEncuestas)
        llEstadoVacio = findViewById(R.id.llEstadoVacio)
        tvSinEncuestas = findViewById(R.id.tvSinEncuestas)
        btnCargarDemo = findViewById(R.id.btnCargarDemo)

        swipeRefreshMain.setColorSchemeResources(R.color.accent, R.color.primary)
    }

    private fun configurarEventos() {
        swipeRefreshMain.setOnRefreshListener {
            cargarEncuestasDesdeNube()
        }

        btnCrearEncuesta.setOnClickListener {
            startActivity(Intent(this, CrearEncuestaActivity::class.java))
        }

        rgFiltro.setOnCheckedChangeListener { _, _ ->
            aplicarFiltrosLocales()
        }

        cgCategorias.setOnCheckedStateChangeListener { _, _ ->
            aplicarFiltrosLocales()
        }

        etBuscarEncuesta.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                aplicarFiltrosLocales()
            }
            override fun afterTextChanged(s: Editable?) {}
        })

        btnCargarDemo.setOnClickListener {
            btnCargarDemo.isEnabled = false
            FirebaseRepository.sembrarEncuestasDemo { ok, err ->
                btnCargarDemo.isEnabled = true
                if (ok) {
                    Toast.makeText(this, "Encuestas institucionales cargadas en la nube.", Toast.LENGTH_SHORT).show()
                    cargarEncuestasDesdeNube()
                } else {
                    Toast.makeText(this, "Error al cargar demo: $err", Toast.LENGTH_SHORT).show()
                }
            }
        }

        btnCerrarSesion.setOnClickListener {
            mostrarDialogoPerfilYCuenta()
        }
        findViewById<View>(R.id.llPerfilHeader).setOnClickListener {
            mostrarDialogoPerfilYCuenta()
        }
    }

    private fun mostrarDialogoPerfilYCuenta() {
        val user = Firebase.auth.currentUser ?: return
        val uid = user.uid

        FirebaseRepository.obtenerPerfilUsuario(uid) { perfil ->
            if (isFinishing || isDestroyed) return@obtenerPerfilUsuario
            val d = resources.displayMetrics.density
            val pad = (20 * d).toInt()

            val contenedor = LinearLayout(this).apply {
                orientation = LinearLayout.VERTICAL
                setPadding(pad, (12 * d).toInt(), pad, 0)
            }

            val tvEmail = TextView(this).apply {
                text = "Correo: ${user.email ?: "No especificado"}"
                textSize = 13f
                setTextColor(ContextCompat.getColor(context, R.color.text_secondary))
                setPadding(0, 0, 0, (12 * d).toInt())
            }
            contenedor.addView(tvEmail)

            val etNombre = EditText(this).apply {
                hint = "Nombre completo"
                setText(perfil?.nombre?.ifBlank { FirebaseRepository.currentDisplayName() } ?: FirebaseRepository.currentDisplayName())
                setBackgroundResource(R.drawable.bg_input)
                setPadding((12 * d).toInt(), (10 * d).toInt(), (12 * d).toInt(), (10 * d).toInt())
            }
            contenedor.addView(etNombre)

            val etCodigo = EditText(this).apply {
                hint = "Código universitario (ej. 202201045)"
                setText(perfil?.codigoUniversitario ?: "")
                setBackgroundResource(R.drawable.bg_input)
                setPadding((12 * d).toInt(), (10 * d).toInt(), (12 * d).toInt(), (10 * d).toInt())
                layoutParams = LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
                ).apply { topMargin = (10 * d).toInt() }
            }
            contenedor.addView(etCodigo)

            AlertDialog.Builder(this)
                .setTitle("Mi Cuenta UNAMAD")
                .setView(contenedor)
                .setPositiveButton("Guardar Perfil") { _, _ ->
                    val nuevoNombre = etNombre.text.toString().trim()
                    val nuevoCodigo = etCodigo.text.toString().trim()
                    if (nuevoNombre.length >= 2) {
                        user.updateProfile(
                            UserProfileChangeRequest.Builder().setDisplayName(nuevoNombre).build()
                        )
                        FirebaseRepository.guardarPerfilUsuario(
                            uid,
                            nuevoNombre,
                            nuevoCodigo,
                            user.email ?: ""
                        ) { ok, _ ->
                            if (ok) {
                                actualizarSaludo()
                                Toast.makeText(this, "Perfil actualizado en la nube.", Toast.LENGTH_SHORT).show()
                            }
                        }
                    }
                }
                .setNeutralButton("Cerrar Sesión") { _, _ ->
                    Firebase.auth.signOut()
                    irALogin()
                }
                .setNegativeButton("Cerrar", null)
                .show()
        }
    }

    private fun irALogin() {
        startActivity(Intent(this, LoginActivity::class.java))
        finish()
    }

    private fun cargarEncuestasDesdeNube() {
        swipeRefreshMain.isRefreshing = true
        FirebaseRepository.listarEncuestas("TODAS") { todas, conteos, error ->
            if (isFinishing || isDestroyed) return@listarEncuestas
            swipeRefreshMain.isRefreshing = false

            if (error != null) {
                Toast.makeText(this, "Error Firestore: $error", Toast.LENGTH_LONG).show()
            }

            cacheEncuestas = todas
            tvTotalEncuestas.text = conteos.first.toString()
            tvActivasEncuestas.text = conteos.second.toString()
            tvTotalVotos.text = conteos.third.toString()

            aplicarFiltrosLocales()
        }
    }

    private fun aplicarFiltrosLocales() {
        val query = etBuscarEncuesta.text.toString().trim().lowercase()

        val catSeleccionada = when (cgCategorias.checkedChipId) {
            R.id.chipCatVotacion -> "Votación"
            R.id.chipCatSatisfaccion -> "Satisfacción"
            R.id.chipCatAcademica -> "Académica"
            R.id.chipCatGeneral -> "General"
            else -> "TODAS"
        }

        val filtradas = cacheEncuestas.filter { enc ->
            val cumpleEstado = when {
                rbFiltroActivas.isChecked -> enc.activa
                rbFiltroCerradas.isChecked -> !enc.activa
                else -> true
            }
            val cumpleCat = catSeleccionada == "TODAS" || enc.categoria.equals(catSeleccionada, ignoreCase = true)
            val cumpleBusqueda = query.isEmpty() ||
                enc.titulo.lowercase().contains(query) ||
                enc.descripcion.lowercase().contains(query) ||
                enc.creadorNombre.lowercase().contains(query) ||
                enc.categoria.lowercase().contains(query)

            cumpleEstado && cumpleCat && cumpleBusqueda
        }

        renderizarTarjetas(filtradas)
    }

    private fun renderizarTarjetas(listaEncuestas: List<Encuesta>) {
        llContenedorEncuestas.removeAllViews()

        if (listaEncuestas.isEmpty()) {
            llEstadoVacio.visibility = View.VISIBLE
            btnCargarDemo.visibility = if (cacheEncuestas.isEmpty()) View.VISIBLE else View.GONE
            tvSinEncuestas.text = if (cacheEncuestas.isEmpty()) {
                "Aún no hay encuestas registradas en la nube. Crea una nueva o carga las encuestas institucionales de demostración."
            } else {
                "No se encontraron encuestas que coincidan con tu búsqueda o filtro."
            }
            return
        }
        llEstadoVacio.visibility = View.GONE

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

    private fun mostrarDialogoEliminar(encuesta: Encuesta) {
        AlertDialog.Builder(this)
            .setTitle("Confirmar Eliminación")
            .setMessage("¿Está seguro de eliminar permanentemente la encuesta:\n\"${encuesta.titulo}\"?\n\nSe eliminarán todas sus preguntas, alternativas y registros de votación en la nube.")
            .setIcon(android.R.drawable.ic_dialog_alert)
            .setPositiveButton("Sí, Eliminar") { dialog, _ ->
                FirebaseRepository.eliminarEncuesta(encuesta.id) { exito, err ->
                    if (exito) {
                        Toast.makeText(this, "Encuesta eliminada correctamente.", Toast.LENGTH_SHORT).show()
                        cargarEncuestasDesdeNube()
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
