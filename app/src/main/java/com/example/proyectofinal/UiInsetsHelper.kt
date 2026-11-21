package com.example.proyectofinal

import android.content.Context
import android.content.res.Configuration
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.app.AppCompatDelegate
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat

private const val PREFS_THEME = "votaapp_theme_prefs"
private const val KEY_DARK_MODE = "dark_mode_enabled"

/**
 * Aplica el modo oscuro por defecto (o la preferencia guardada del usuario)
 * y configura Edge-to-Edge continuo con íconos blancos en la barra de estado.
 */
fun AppCompatActivity.configurarEdgeToEdgeConHeader(scrollRaiz: View, headerView: View) {
    val prefs = getSharedPreferences(PREFS_THEME, Context.MODE_PRIVATE)
    val usarOscuro = prefs.getBoolean(KEY_DARK_MODE, true) // Modo oscuro por defecto
    val targetMode = if (usarOscuro) AppCompatDelegate.MODE_NIGHT_YES else AppCompatDelegate.MODE_NIGHT_NO
    if (AppCompatDelegate.getDefaultNightMode() != targetMode) {
        AppCompatDelegate.setDefaultNightMode(targetMode)
    }

    WindowInsetsControllerCompat(window, window.decorView).isAppearanceLightStatusBars = false

    val headerTopBase = headerView.paddingTop
    val scrollLeftBase = scrollRaiz.paddingLeft
    val scrollRightBase = scrollRaiz.paddingRight
    val scrollBottomBase = scrollRaiz.paddingBottom

    ViewCompat.setOnApplyWindowInsetsListener(scrollRaiz) { v, insets ->
        val bars = insets.getInsets(
            WindowInsetsCompat.Type.systemBars() or WindowInsetsCompat.Type.displayCutout()
        )
        val ime = insets.getInsets(WindowInsetsCompat.Type.ime())

        headerView.setPadding(
            headerView.paddingLeft,
            headerTopBase + bars.top,
            headerView.paddingRight,
            headerView.paddingBottom
        )

        v.setPadding(
            scrollLeftBase + bars.left,
            v.paddingTop,
            scrollRightBase + bars.right,
            scrollBottomBase + maxOf(bars.bottom, ime.bottom)
        )
        insets
    }
}

fun AppCompatActivity.esModoOscuroActivo(): Boolean {
    val nightMask = resources.configuration.uiMode and Configuration.UI_MODE_NIGHT_MASK
    return nightMask == Configuration.UI_MODE_NIGHT_YES
}

fun AppCompatActivity.alternarModoOscuro() {
    val nuevoOscuro = !esModoOscuroActivo()
    getSharedPreferences(PREFS_THEME, Context.MODE_PRIVATE)
        .edit()
        .putBoolean(KEY_DARK_MODE, nuevoOscuro)
        .apply()
    AppCompatDelegate.setDefaultNightMode(
        if (nuevoOscuro) AppCompatDelegate.MODE_NIGHT_YES else AppCompatDelegate.MODE_NIGHT_NO
    )
}
