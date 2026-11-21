package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.android.material.textfield.TextInputLayout
import com.google.firebase.Firebase
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import com.google.firebase.auth.UserProfileChangeRequest
import com.google.firebase.auth.auth

/**
 * ============================================================================
 * PANTALLA DE ACCESO: LoginActivity (Firebase Authentication + Modo Oscuro)
 * ============================================================================
 */
class LoginActivity : AppCompatActivity() {

    private lateinit var auth: FirebaseAuth

    private lateinit var btnTemaLogin: TextView
    private lateinit var tvBienvenidaLogin: TextView
    private lateinit var tvSubtituloLogin: TextView
    private lateinit var llCamposRegistro: LinearLayout
    private lateinit var tilAuthNombre: TextInputLayout
    private lateinit var tilAuthEmail: TextInputLayout
    private lateinit var tilAuthPassword: TextInputLayout
    private lateinit var etAuthNombre: EditText
    private lateinit var etAuthCodigo: EditText
    private lateinit var etAuthEmail: EditText
    private lateinit var etAuthPassword: EditText
    private lateinit var tvToggleAuthModo: TextView
    private lateinit var tvForgotPassword: TextView
    private lateinit var pbAuth: ProgressBar
    private lateinit var btnAuthAccion: Button
    private lateinit var btnGoogleSignIn: Button

    private var modoRegistro: Boolean = false

    private val googleSignInLauncher = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { result ->
        val task = GoogleSignIn.getSignedInAccountFromIntent(result.data)
        try {
            val account = task.getResult(ApiException::class.java)
            val idToken = account.idToken
            if (idToken != null) {
                autenticarConGoogleEnFirebase(
                    idToken,
                    account.displayName ?: "Usuario Google",
                    account.email ?: ""
                )
            } else {
                mostrarCargando(false)
                Toast.makeText(this, "No se obtuvo el token de Google.", Toast.LENGTH_SHORT).show()
            }
        } catch (e: ApiException) {
            mostrarCargando(false)
            Toast.makeText(this, "Acceso con Google cancelado (${e.statusCode}).", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)

        configurarEdgeToEdgeConHeader(findViewById(R.id.scrollLogin), findViewById(R.id.topBar))

        auth = Firebase.auth

        if (auth.currentUser != null) {
            irAMain()
            return
        }

        vincularVistas()
        modoRegistro = savedInstanceState?.getBoolean(KEY_MODO_REGISTRO, false) ?: false
        aplicarEstadoModo()
        configurarEventos()
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        outState.putBoolean(KEY_MODO_REGISTRO, modoRegistro)
    }

    private fun vincularVistas() {
        btnTemaLogin = findViewById(R.id.btnTemaLogin)
        tvBienvenidaLogin = findViewById(R.id.tvBienvenidaLogin)
        tvSubtituloLogin = findViewById(R.id.tvSubtituloLogin)
        llCamposRegistro = findViewById(R.id.llCamposRegistro)
        tilAuthNombre = findViewById(R.id.tilAuthNombre)
        tilAuthEmail = findViewById(R.id.tilAuthEmail)
        tilAuthPassword = findViewById(R.id.tilAuthPassword)
        etAuthNombre = findViewById(R.id.etAuthNombre)
        etAuthCodigo = findViewById(R.id.etAuthCodigo)
        etAuthEmail = findViewById(R.id.etAuthEmail)
        etAuthPassword = findViewById(R.id.etAuthPassword)
        tvToggleAuthModo = findViewById(R.id.tvToggleAuthModo)
        tvForgotPassword = findViewById(R.id.tvForgotPassword)
        pbAuth = findViewById(R.id.pbAuth)
        btnAuthAccion = findViewById(R.id.btnAuthAccion)
        btnGoogleSignIn = findViewById(R.id.btnGoogleSignIn)

        btnTemaLogin.text = if (esModoOscuroActivo()) "Modo Claro" else "Modo Oscuro"
    }

    private fun aplicarEstadoModo() {
        llCamposRegistro.visibility = if (modoRegistro) View.VISIBLE else View.GONE
        btnAuthAccion.text = if (modoRegistro) "Crear Cuenta Institucional" else "Iniciar Sesión"
        tvToggleAuthModo.text = if (modoRegistro) "Ya tengo cuenta" else "Crear cuenta"
        tvBienvenidaLogin.text = if (modoRegistro) "Crear cuenta nueva" else "Bienvenido de nuevo"
        tvSubtituloLogin.text = if (modoRegistro) {
            "Completa tus datos para participar en encuestas y votaciones."
        } else {
            "Ingresa con tu cuenta para participar o gestionar encuestas."
        }
        tilAuthNombre.error = null
        tilAuthEmail.error = null
        tilAuthPassword.error = null
    }

    private fun configurarEventos() {
        btnTemaLogin.setOnClickListener {
            alternarModoOscuro()
        }

        tvToggleAuthModo.setOnClickListener {
            modoRegistro = !modoRegistro
            aplicarEstadoModo()
        }

        btnAuthAccion.setOnClickListener {
            tilAuthNombre.error = null
            tilAuthEmail.error = null
            tilAuthPassword.error = null
            if (modoRegistro) {
                registrarConCorreo()
            } else {
                iniciarSesionConCorreo()
            }
        }

        tvForgotPassword.setOnClickListener {
            mostrarDialogoRecuperarPassword()
        }

        btnGoogleSignIn.setOnClickListener {
            iniciarGoogleSignIn()
        }
    }

    private fun mostrarDialogoRecuperarPassword() {
        val emailActual = etAuthEmail.text.toString().trim()
        val input = EditText(this).apply {
            hint = "usuario@unamad.edu.pe"
            setText(emailActual)
            setPadding(48, 32, 48, 32)
        }

        AlertDialog.Builder(this)
            .setTitle("Recuperar Contraseña")
            .setMessage("Ingresa tu correo registrado y te enviaremos un enlace de restablecimiento:")
            .setView(input)
            .setPositiveButton("Enviar Enlace") { _, _ ->
                val correo = input.text.toString().trim()
                if (correo.isEmpty()) {
                    Toast.makeText(this, "Ingresa un correo válido.", Toast.LENGTH_SHORT).show()
                } else {
                    auth.sendPasswordResetEmail(correo)
                        .addOnSuccessListener {
                            Toast.makeText(this, "Enlace enviado a $correo.", Toast.LENGTH_LONG).show()
                        }
                        .addOnFailureListener { e ->
                            Toast.makeText(this, "Error: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
                        }
                }
            }
            .setNegativeButton("Cancelar", null)
            .show()
    }

    private fun iniciarSesionConCorreo() {
        val email = etAuthEmail.text.toString().trim()
        val password = etAuthPassword.text.toString()

        if (email.isEmpty()) {
            tilAuthEmail.error = "Ingresa tu correo electrónico"
            etAuthEmail.requestFocus()
            return
        }
        if (password.isEmpty()) {
            tilAuthPassword.error = "Ingresa tu contraseña"
            etAuthPassword.requestFocus()
            return
        }

        mostrarCargando(true)
        auth.signInWithEmailAndPassword(email, password)
            .addOnSuccessListener {
                mostrarCargando(false)
                irAMain()
            }
            .addOnFailureListener { e ->
                mostrarCargando(false)
                Toast.makeText(this, "No se pudo iniciar sesión: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
    }

    private fun registrarConCorreo() {
        val nombre = etAuthNombre.text.toString().trim()
        val codigo = etAuthCodigo.text.toString().trim()
        val email = etAuthEmail.text.toString().trim()
        val password = etAuthPassword.text.toString()

        if (nombre.length < 2) {
            tilAuthNombre.error = "Ingresa tu nombre completo"
            etAuthNombre.requestFocus()
            return
        }
        if (email.isEmpty()) {
            tilAuthEmail.error = "Ingresa tu correo electrónico"
            etAuthEmail.requestFocus()
            return
        }
        if (password.length < 6) {
            tilAuthPassword.error = "La contraseña debe tener al menos 6 caracteres"
            etAuthPassword.requestFocus()
            return
        }

        mostrarCargando(true)
        auth.createUserWithEmailAndPassword(email, password)
            .addOnSuccessListener { result ->
                val user = result.user
                if (user != null) {
                    val profileUpdates = UserProfileChangeRequest.Builder()
                        .setDisplayName(nombre)
                        .build()
                    user.updateProfile(profileUpdates).addOnCompleteListener {
                        FirebaseRepository.guardarPerfilUsuario(user.uid, nombre, codigo, email) { _, _ ->
                            mostrarCargando(false)
                            irAMain()
                        }
                    }
                } else {
                    mostrarCargando(false)
                    irAMain()
                }
            }
            .addOnFailureListener { e ->
                mostrarCargando(false)
                Toast.makeText(this, "No se pudo crear la cuenta: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
    }

    private fun iniciarGoogleSignIn() {
        val webClientIdRes = resources.getIdentifier("default_web_client_id", "string", packageName)
        if (webClientIdRes == 0) {
            Toast.makeText(this, "Configuración OAuth no disponible.", Toast.LENGTH_LONG).show()
            return
        }

        mostrarCargando(true)
        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(getString(webClientIdRes))
            .requestEmail()
            .build()
        val client = GoogleSignIn.getClient(this, gso)
        googleSignInLauncher.launch(client.signInIntent)
    }

    private fun autenticarConGoogleEnFirebase(idToken: String, nombre: String, email: String) {
        val credential = GoogleAuthProvider.getCredential(idToken, null)
        auth.signInWithCredential(credential)
            .addOnSuccessListener { result ->
                val user = result.user
                if (user != null) {
                    FirebaseRepository.guardarPerfilUsuario(
                        user.uid,
                        user.displayName ?: nombre,
                        "",
                        user.email ?: email
                    ) { _, _ ->
                        mostrarCargando(false)
                        irAMain()
                    }
                } else {
                    mostrarCargando(false)
                    irAMain()
                }
            }
            .addOnFailureListener { e ->
                mostrarCargando(false)
                Toast.makeText(this, "Error Firebase Google Auth: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
    }

    private fun mostrarCargando(cargando: Boolean) {
        pbAuth.visibility = if (cargando) View.VISIBLE else View.GONE
        btnAuthAccion.isEnabled = !cargando
        btnGoogleSignIn.isEnabled = !cargando
    }

    private fun irAMain() {
        startActivity(Intent(this, MainActivity::class.java))
        finish()
    }

    companion object {
        private const val KEY_MODO_REGISTRO = "key_modo_registro"
    }
}
