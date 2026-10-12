"""Proposed minimal registration.py correction, staged for the integrator.

No shared file changes. Independent-document RSS retains the historical
project proxy; same-document callers must supply a complete justified model.
"""
import math


def pair_error(e1: float, e2: float, same_document: bool = False,
               pick_error_m: float = 0.0, *, pair_local_error_m: float | None = None) -> float:
    """Return the existing cross-document proxy or an explicit pair error.

    A shared translation cancels. For scalar distance a common rigid rotation
    cancels, while scale and differential distortion remain. Cardinal/vector
    relations also require rotation uncertainty. Control residuals alone
    cannot partition these components or establish pair-local accuracy.

    For same_document=True, pair_local_error_m must already include all
    relevant endpoint, transform and local source terms under a declared
    bounded or covariance model. Its units/convention must match the caller's
    decision margin. This function neither assumes covariance nor adds an
    arbitrary scale budget. A picking-only argument cannot certify it.

    Cross-document hypot(e1,e2) remains a project decision proxy; its use as
    a calibrated stochastic error needs independently justified covariances.
    """
    def validate(value):
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
            raise ValueError("Error must be finite and nonnegative")

    if same_document:
        if pair_local_error_m is None:
            raise ValueError("Same-document relation needs complete pair_local_error_m; picking error alone omits scale and distortion")
        if pick_error_m != 0:
            raise ValueError("Include picking in pair_local_error_m and leave legacy pick_error_m zero")
        validate(pair_local_error_m)
        return float(pair_local_error_m)
    validate(e1)
    validate(e2)
    return math.hypot(e1, e2)
