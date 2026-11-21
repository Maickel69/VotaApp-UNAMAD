package com.example.proyectofinal

import android.animation.ValueAnimator
import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.RectF
import android.graphics.Typeface
import android.util.AttributeSet
import android.view.View
import android.view.animation.DecelerateInterpolator
import androidx.core.content.ContextCompat
import kotlin.math.min

/**
 * Gráfico de Dona (DonutChartView) animado nativo en Kotlin Canvas.
 * Renderiza la distribución porcentual de las alternativas de cada pregunta
 * con el total de votos centrado.
 */
class DonutChartView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null
) : View(context, attrs) {

    data class Slice(val label: String, val value: Float, val color: Int)

    private var slices: List<Slice> = emptyList()
    private var totalVotos: Int = 0
    private var animProgress: Float = 1f

    private val arcPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        strokeCap = Paint.Cap.BUTT
    }

    private val bgTrackPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.STROKE
        color = ContextCompat.getColor(context, R.color.border_light)
    }

    private val centerNumPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        textAlign = Paint.Align.CENTER
        typeface = Typeface.create(Typeface.DEFAULT, Typeface.BOLD)
        color = ContextCompat.getColor(context, R.color.text_primary)
    }

    private val centerLabelPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        textAlign = Paint.Align.CENTER
        color = ContextCompat.getColor(context, R.color.text_muted)
    }

    private val legendDotPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        style = Paint.Style.FILL
    }

    private val legendTextPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = ContextCompat.getColor(context, R.color.text_secondary)
    }

    private val arcRect = RectF()

    fun setData(alternatives: List<AlternativaEstadistica>, total: Int) {
        totalVotos = total
        slices = alternatives.mapIndexed { idx, alt ->
            Slice(
                label = "${alt.texto.take(22)}${if (alt.texto.length > 22) "…" else ""} (${String.format("%.0f", alt.porcentaje)}%)",
                value = alt.votos.toFloat(),
                color = if (alt.esGanadora) Color.parseColor("#D97706") else PALETTE[idx % PALETTE.size]
            )
        }
        ValueAnimator.ofFloat(0f, 1f).apply {
            duration = 650
            interpolator = DecelerateInterpolator()
            addUpdateListener {
                animProgress = it.animatedValue as Float
                invalidate()
            }
            start()
        }
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val d = resources.displayMetrics.density
        val chartSize = min(height.toFloat(), width * 0.42f) - 16f * d
        if (chartSize <= 0f) return

        val strokeW = 14f * d
        arcPaint.strokeWidth = strokeW
        bgTrackPaint.strokeWidth = strokeW

        val cx = 12f * d + chartSize / 2f
        val cy = height / 2f
        val radius = (chartSize - strokeW) / 2f
        arcRect.set(cx - radius, cy - radius, cx + radius, cy + radius)

        canvas.drawOval(arcRect, bgTrackPaint)

        val sum = slices.sumOf { it.value.toDouble() }.toFloat()
        if (sum > 0f) {
            var startAngle = -90f
            for (slice in slices) {
                if (slice.value <= 0f) continue
                val sweep = (slice.value / sum) * 360f * animProgress
                arcPaint.color = slice.color
                canvas.drawArc(arcRect, startAngle, sweep, false, arcPaint)
                startAngle += sweep
            }
        }

        centerNumPaint.textSize = 16f * d
        centerLabelPaint.textSize = 10f * d
        canvas.drawText(totalVotos.toString(), cx, cy + 2f * d, centerNumPaint)
        canvas.drawText("votos", cx, cy + 14f * d, centerLabelPaint)

        // Leyenda lateral derecha
        val legendX = cx + chartSize / 2f + 16f * d
        legendTextPaint.textSize = 11.5f * d
        val lineH = 18f * d
        val totalLegendH = slices.size * lineH
        var curY = (height - totalLegendH) / 2f + 11f * d

        for (slice in slices) {
            legendDotPaint.color = slice.color
            canvas.drawCircle(legendX + 4f * d, curY - 4f * d, 4.5f * d, legendDotPaint)
            canvas.drawText(slice.label, legendX + 14f * d, curY, legendTextPaint)
            curY += lineH
        }
    }

    companion object {
        private val PALETTE = intArrayOf(
            Color.parseColor("#2563EB"),
            Color.parseColor("#0D9488"),
            Color.parseColor("#7C3AED"),
            Color.parseColor("#64748B")
        )
    }
}
