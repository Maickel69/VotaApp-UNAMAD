package com.example.proyectofinal

import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat

/**
 * Configura Edge-to-Edge de forma uniforme:
 * - Extiende el fondo azul del encabezado detrás de la barra de estado con íconos blancos.
 * - Aplica márgenes de sistema e IME (teclado virtual) al ScrollView raíz para no tapar campos.
 */
fun AppCompatActivity.configurarEdgeToEdgeConHeader(scrollRaiz: View, headerView: View) {
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
