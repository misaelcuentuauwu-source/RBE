from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect, QObject, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget

class Animador(QObject):
    def __init__(self, duration=500):
        super().__init__()
        self.duration = duration
        self.anim_group = None

    # --- TRANSICIÓN NEGRA (fade a negro y aparecer nueva ventana) ---
from PySide6.QtCore import QObject, QPropertyAnimation, QEasingCurve, QRect, QParallelAnimationGroup
from PySide6.QtWidgets import QWidget

class Animador(QObject):
    def __init__(self, duration=700):
        super().__init__()
        self.duration = duration
        self.anim_group = None

    # --- TRANSICIÓN FADE SIMPLE ---
    def transicion_fade(self, viejo, nuevo):
        geo = viejo.geometry()
        nuevo.setGeometry(geo)
        nuevo.setWindowOpacity(0)
        nuevo.show()

        anim_out = QPropertyAnimation(viejo, b"windowOpacity")
        anim_out.setDuration(self.duration)
        anim_out.setStartValue(1)
        anim_out.setEndValue(0)

        anim_in = QPropertyAnimation(nuevo, b"windowOpacity")
        anim_in.setDuration(self.duration)
        anim_in.setStartValue(0)
        anim_in.setEndValue(1)

        grupo = QParallelAnimationGroup()
        grupo.addAnimation(anim_out)
        grupo.addAnimation(anim_in)

        self.anim_group = grupo
        grupo.start()

    # --- TRANSICIÓN GIRO ---
    def transicion_giro(self, viejo, nuevo):
        geo = viejo.geometry()
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

        anim_out = QPropertyAnimation(viejo, b"geometry")
        anim_out.setDuration(self.duration)
        anim_out.setStartValue(QRect(x, y, w, h))
        anim_out.setEndValue(QRect(x + w//2, y, 0, h))
        anim_out.setEasingCurve(QEasingCurve.InCubic)

        nuevo.setGeometry(QRect(x + w//2, y, 0, h))
        nuevo.show()
        anim_in = QPropertyAnimation(nuevo, b"geometry")
        anim_in.setDuration(self.duration)
        anim_in.setStartValue(QRect(x + w//2, y, 0, h))
        anim_in.setEndValue(QRect(x, y, w, h))
        anim_in.setEasingCurve(QEasingCurve.OutCubic)

        grupo = QParallelAnimationGroup()
        grupo.addAnimation(anim_out)
        grupo.addAnimation(anim_in)
        self.anim_group = grupo
        grupo.start()

    # --- TRANSICIÓN POP ---
    def transicion_pop(self, viejo, nuevo):
        geo = viejo.geometry()
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

        anim_out = QPropertyAnimation(viejo, b"geometry")
        anim_out.setDuration(self.duration)
        anim_out.setStartValue(QRect(x, y, w, h))
        anim_out.setEndValue(QRect(x + w//4, y + h//4, w//2, h//2))
        anim_out.setEasingCurve(QEasingCurve.InBack)

        anim_out_op = QPropertyAnimation(viejo, b"windowOpacity")
        anim_out_op.setDuration(self.duration)
        anim_out_op.setStartValue(1)
        anim_out_op.setEndValue(0)

        nuevo.setGeometry(QRect(x + w//4, y + h//4, w//2, h//2))
        nuevo.setWindowOpacity(0)
        nuevo.show()

        anim_in = QPropertyAnimation(nuevo, b"geometry")
        anim_in.setDuration(self.duration)
        anim_in.setStartValue(QRect(x + w//4, y + h//4, w//2, h//2))
        anim_in.setEndValue(QRect(x, y, w, h))
        anim_in.setEasingCurve(QEasingCurve.OutBack)

        anim_in_op = QPropertyAnimation(nuevo, b"windowOpacity")
        anim_in_op.setDuration(self.duration)
        anim_in_op.setStartValue(0)
        anim_in_op.setEndValue(1)

        grupo = QParallelAnimationGroup()
        grupo.addAnimation(anim_out)
        grupo.addAnimation(anim_out_op)
        grupo.addAnimation(anim_in)
        grupo.addAnimation(anim_in_op)
        self.anim_group = grupo
        grupo.start()

    # --- TRANSICIÓN CORTINA ---
    def transicion_cortina(self, viejo, nuevo):
        geo = viejo.geometry()
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

        anim_out = QPropertyAnimation(viejo, b"geometry")
        anim_out.setDuration(self.duration)
        anim_out.setStartValue(QRect(x, y, w, h))
        anim_out.setEndValue(QRect(x, y - h, w, h))
        anim_out.setEasingCurve(QEasingCurve.InCubic)

        nuevo.setGeometry(QRect(x, y - h, w, h))
        nuevo.show()
        anim_in = QPropertyAnimation(nuevo, b"geometry")
        anim_in.setDuration(self.duration)
        anim_in.setStartValue(QRect(x, y - h, w, h))
        anim_in.setEndValue(QRect(x, y, w, h))
        anim_in.setEasingCurve(QEasingCurve.OutBounce)

        grupo = QParallelAnimationGroup()
        grupo.addAnimation(anim_out)
        grupo.addAnimation(anim_in)
        self.anim_group = grupo
        grupo.start()

    # --- TRANSICIÓN HERMOSA ---
    def transicion_hermosa(self, viejo, nuevo):
        geo = viejo.geometry()
        x, y, w, h = geo.x(), geo.y(), geo.width(), geo.height()

        anim_out_slide = QPropertyAnimation(viejo, b"geometry")
        anim_out_slide.setDuration(self.duration)
        anim_out_slide.setStartValue(QRect(x, y, w, h))
        anim_out_slide.setEndValue(QRect(x + w, y, w, h))
        anim_out_slide.setEasingCurve(QEasingCurve.OutCubic)

        anim_out_fade = QPropertyAnimation(viejo, b"windowOpacity")
        anim_out_fade.setDuration(self.duration)
        anim_out_fade.setStartValue(1)
        anim_out_fade.setEndValue(0)

        nuevo.setGeometry(QRect(x - w, y, w, h))
        nuevo.setWindowOpacity(0)
        nuevo.show()

        anim_in_slide = QPropertyAnimation(nuevo, b"geometry")
        anim_in_slide.setDuration(self.duration)
        anim_in_slide.setStartValue(QRect(x - w, y, w, h))
        anim_in_slide.setEndValue(QRect(x, y, w, h))
        anim_in_slide.setEasingCurve(QEasingCurve.OutCubic)

        anim_in_fade = QPropertyAnimation(nuevo, b"windowOpacity")
        anim_in_fade.setDuration(self.duration)
        anim_in_fade.setStartValue(0)
        anim_in_fade.setEndValue(1)

        grupo = QParallelAnimationGroup()
        grupo.addAnimation(anim_out_slide)
        grupo.addAnimation(anim_out_fade)
        grupo.addAnimation(anim_in_slide)
        grupo.addAnimation(anim_in_fade)
        self.anim_group = grupo
        grupo.start()
