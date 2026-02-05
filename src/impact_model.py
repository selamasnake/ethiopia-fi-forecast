import numpy as np

class ImpactModel:
    """
    Models the time-varying impact of discrete events on financial inclusion indicators.
    """

    IMPACT_MAP = {
        "low": 0.25,
        "medium": 0.50,
        "high": 1.00
    }

    def __init__(self, ramp: float = 12.0, decay: bool = False, decay_rate: float = 0.0):
        """
        Parameters
        ----------
        ramp : float
            Months over which event impacts ramp up
        decay : bool
            Whether impacts decay over time
        decay_rate : float
            Monthly decay rate (if decay=True)
        """
        self.ramp = ramp
        self.decay = decay
        self.decay_rate = decay_rate

    # Magnitude mapping

    def map_magnitude(self, magnitude: str) -> float:
        """
        Maps qualitative impact magnitudes to normalized numeric weights.
        """
        if magnitude is None:
            return 0.0
        return self.IMPACT_MAP.get(str(magnitude).lower(), 0.0)

    # Event impact function


    def event_effect(
        self,
        t: float,
        t_event: float,
        lag: float,
        magnitude: float
    ) -> float:
        """
        Computes the effect of an event at time t.

        Functional form:
        - Zero until lag
        - Linear ramp-up
        - Plateau
        - Optional exponential decay
        """

        dt = t - (t_event + lag)

        if dt <= 0:
            return 0.0

        # Ramp-up
        if dt < self.ramp:
            effect = magnitude * (dt / self.ramp)
        else:
            effect = magnitude

        # Optional decay
        if self.decay and self.decay_rate > 0:
            effect *= np.exp(-self.decay_rate * max(dt - self.ramp, 0))

        return effect
