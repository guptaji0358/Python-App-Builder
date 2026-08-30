import random

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QFont, QGuiApplication

FIREWORK_COLORS = [
    QColor(255, 90, 90),
    QColor(255, 200, 60),
    QColor(90, 200, 255),
    QColor(140, 255, 140),
    QColor(230, 130, 255),
    QColor(255, 255, 255),
]


class Particle:
    def __init__(self, X, Y, Angle, Speed, Color):
        self.X = X
        self.Y = Y
        self.VelocityX = Speed * (Angle.real if False else __import__("math").cos(Angle))
        self.VelocityY = Speed * __import__("math").sin(Angle)
        self.Color = Color
        self.Life = 1.0

    def Step(self, Dt):
        self.X += self.VelocityX * Dt
        self.Y += self.VelocityY * Dt
        self.VelocityY += 60 * Dt
        self.Life -= Dt * 0.6


class Firework:
    def __init__(self, X, Y):
        import math
        Color = random.choice(FIREWORK_COLORS)
        Count = random.randint(40, 60)
        self.Particles = []
        for _ in range(Count):
            Angle = random.uniform(0, math.tau)
            Speed = random.uniform(60, 220)
            self.Particles.append(Particle(X, Y, Angle, Speed, Color))

    def Step(self, Dt):
        for P in self.Particles:
            P.Step(Dt)
        self.Particles = [P for P in self.Particles if P.Life > 0]

    def IsDone(self):
        return len(self.Particles) == 0


class FireworksOverlay(QWidget):
    """Fullscreen 'Thank you for installing' celebration shown once, right
    after the app's first post-install launch. Auto-closes itself after a
    fixed duration - purely decorative, holds no app state."""

    def __init__(self, DurationMs=6000, Message="Thank you for installing Pywix!"):
        super().__init__(None)
        self.Message = Message
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        Screen = QGuiApplication.primaryScreen()
        Geometry = Screen.geometry() if Screen else self.geometry()
        self.setGeometry(Geometry)

        self.Fireworks = []
        self.ElapsedMs = 0
        self.DurationMs = DurationMs

        self.SpawnTimer = QTimer(self)
        self.SpawnTimer.timeout.connect(self.SpawnFirework)
        self.SpawnTimer.start(350)

        self.TickTimer = QTimer(self)
        self.TickTimer.timeout.connect(self.Tick)
        self.TickTimer.start(16)

        self.CloseTimer = QTimer(self)
        self.CloseTimer.setSingleShot(True)
        self.CloseTimer.timeout.connect(self.close)
        self.CloseTimer.start(self.DurationMs)

        self.SpawnFirework()

    def SpawnFirework(self):
        Width = self.width() or 1920
        Height = self.height() or 1080
        X = random.uniform(Width * 0.15, Width * 0.85)
        Y = random.uniform(Height * 0.2, Height * 0.55)
        self.Fireworks.append(Firework(X, Y))

    def Tick(self):
        self.ElapsedMs += 16
        for FireworkItem in self.Fireworks:
            FireworkItem.Step(0.016)
        self.Fireworks = [F for F in self.Fireworks if not F.IsDone()]
        if self.ElapsedMs >= self.DurationMs - 500:
            self.SpawnTimer.stop()
        self.update()

    def paintEvent(self, Event):
        Painter = QPainter(self)
        Painter.setRenderHint(QPainter.Antialiasing)
        Painter.fillRect(self.rect(), QColor(8, 10, 18))

        for FireworkItem in self.Fireworks:
            for P in FireworkItem.Particles:
                Color = QColor(P.Color)
                Color.setAlphaF(max(0.0, min(1.0, P.Life)))
                Painter.setPen(Qt.NoPen)
                Painter.setBrush(Color)
                Radius = 2.5 + 2 * max(0.0, P.Life)
                Painter.drawEllipse(QRectF(P.X - Radius, P.Y - Radius, Radius * 2, Radius * 2))

        Painter.setPen(QColor(255, 255, 255))
        TitleFont = QFont("Segoe UI", 28, QFont.Bold)
        Painter.setFont(TitleFont)
        TitleRect = QRectF(0, self.height() * 0.72, self.width(), 60)
        Painter.drawText(TitleRect, Qt.AlignCenter, self.Message)

        SubFont = QFont("Segoe UI", 13)
        Painter.setFont(SubFont)
        Painter.setPen(QColor(200, 200, 210))
        SubRect = QRectF(0, self.height() * 0.72 + 55, self.width(), 40)
        Painter.drawText(SubRect, Qt.AlignCenter, "Enjoy building your apps!")

    def mousePressEvent(self, Event):
        self.close()

    def keyPressEvent(self, Event):
        self.close()


def ShowThankYouFireworks(DurationMs=6000):
    Overlay = FireworksOverlay(DurationMs=DurationMs)
    Overlay.showFullScreen()
    return Overlay
