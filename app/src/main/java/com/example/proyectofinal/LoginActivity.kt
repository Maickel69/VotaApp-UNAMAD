package com.example.proyectofinal

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.firebase.Firebase
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider
import com.google.firebase.auth.UserProfileChangeRequest
import com.google.firebase.auth.auth

/**
 * ============================================================================
 * PANTALLA DE ACCESO: LoginActivity (Firebase Authentication)
 * ============================================================================
 * Permite iniciar sesión o registrarse con Correo/Contraseña o Google Sign-In,
 * guardando el perfil del usuario en Cloud Firestore (`users/{uid}`).
 */
class LoginActivity : AppCompatActivity() {

    private lateinit var auth: FirebaseAuth

    private lateinit var rgAuthModo: RadioGroup
    private lateinit var rbModoLogin: RadioButton
    private lateinit var rbModoRegistro: RadioButton
    private lateinit var llCamposRegistro: LinearLayout
    private lateinit var etAuthNombre: EditText
    private lateinit var etAuthCodigo: EditText
    private lateinit var etAuthEmail: EditText
    private lateinit var etAuthPassword: EditText
    private lateinit var pbAuth: ProgressBar
    private lateinit var btnAuthAccion: Button
    private lateinit var btnGoogleSignIn: Button

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
            Toast.makeText(this, "Error Google Sign-In (${e.statusCode}): ${e.localizedMessage}", Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_login)

        configurarEdgeToEdgeConHeader(findViewById(R.id.scrollLogin), findViewById(R.id.topBar))

        auth = Firebase.auth

        // Si ya hay sesión iniciada, ir directo al panel principal
        if (auth.currentUser != null) {
            irAMain()
            return
        }

        vincularVistas()
        configurarEventos()
    }

    private fun vincularVistas() {
        rgAuthModo = findViewById(R.id.rgAuthModo)
        rbModoLogin = findViewById(R.id.rbModoLogin)
        rbModoRegistro = findViewById(R.id.rbModoRegistro)
        llCamposRegistro = findViewById(R.id.llCamposRegistro)
        etAuthNombre = findViewById(R.id.etAuthNombre)
        etAuthCodigo = findViewById(R.id.etAuthCodigo)
        etAuthEmail = findViewById(R.id.etAuthEmail)
        etAuthPassword = findViewById(R.id.etAuthPassword)
        pbAuth = findViewById(R.id.pbAuth)
        btnAuthAccion = findViewById(R.id.btnAuthAccion)
        btnGoogleSignIn = findViewById(R.id.btnGoogleSignIn)
    }

    private fun configurarEventos() {
        rgAuthModo.setOnCheckedChangeListener { _, checkedId ->
            val esRegistro = checkedId == R.id.rbModoRegistro
            llCamposRegistro.visibility = if (esRegistro) View.VISIBLE else View.GONE
            btnAuthAccion.text = if (esRegistro) "Crear Cuenta" else "Iniciar Sesión"
        }

        btnAuthAccion.setOnClickListener {
            if (rbModoRegistro.isChecked) {
                registrarConCorreo()
            } else {
                iniciarSesionConCorreo()
            }
        }

        btnGoogleSignIn.setOnClickListener {
            iniciarGoogleSignIn()
        }
    }

    private fun iniciarSesionConCorreo() {
        val email = etAuthEmail.text.toString().trim()
        val password = etAuthPassword.text.toString()

        if (email.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "Ingrese su correo y contraseña.", Toast.LENGTH_SHORT).show()
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
                Toast.makeText(this, "Error al iniciar sesión: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
    }

    private fun registrarConCorreo() {
        val nombre = etAuthNombre.text.toString().trim()
        val codigo = etAuthCodigo.text.toString().trim()
        val email = etAuthEmail.text.toString().trim()
        val password = etAuthPassword.text.toString()

        if (nombre.length < 2) {
            etAuthNombre.error = "Ingrese su nombre completo"
            etAuthNombre.requestFocus()
            return
        }
        if (email.isEmpty()) {
            etAuthEmail.error = "Ingrese su correo"
            etAuthEmail.requestFocus()
            return
        }
        if (password.length < 6) {
            etAuthPassword.error = "La contraseña debe tener al menos 6 caracteres"
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
                    user.updateProfile(profileUpdates)

                    FirebaseRepository.guardarPerfilUsuario(user.uid, nombre, codigo, email) { _, _ ->
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
                Toast.makeText(this, "Error al registrar cuenta: ${e.localizedMessage}", Toast.LENGTH_LONG).show()
            }
    }

    private fun iniciarGoogleSignIn() {
        val webClientIdRes = resources.getIdentifier("default_web_client_id", "string", packageName)
        if (webClientIdRes == 0) {
            Toast.makeText(
                this,
                "Falta default_web_client_id en google-services.json. Habilita Google Sign-In en Firebase Console y descarga google-services.json.",
                Toast.LENGTH_LONG
            ).show()
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
}
