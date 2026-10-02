"""Reproduce arithmetic from recorded project inputs; no fresh page digitization."""
import json
from pathlib import Path

SIDE_LENGTHS = {"south": 19.0, "west": 15.0, "north": 18.2, "east": 16.0}
BAR_START = [622, 796]
BAR_END = [765, 796]
BAR_METRES = 50.0
PIXEL_LENGTH = 143.0
SCALE = BAR_METRES / PIXEL_LENGTH

def main():
    output = {
        "prepared_utc": "2026-10-02",
        "baseline_commit": "4a6c4434ff86f213aa2471351707ef2e8d7ab663",
        "scope": "recorded-input provenance and arithmetic; original image unavailable",
        "original_image_inspected_this_cycle": False,
        "new_digitized_geometry": None,
        "source": {
            "author": "Joseph Patrich",
            "year": 1989,
            "chapter": "אמות המים להורקניה",
            "side_length_printed_page": 255,
            "detailed_plan_printed_page": 256,
            "figure": 22,
            "historical_scan": "269.jpg",
            "url": "https://kotar.cet.ac.il/KotarApp/Viewer.aspx?nBookID=6765980",
            "current_access": "original scan absent from authorized workspace; web viewer not retried in this cycle",
            "historical_inspection": "Project record dated 30 September says full Hebrew chapter was read directly.",
        },
        "recorded_printed_dimensions": {
            "status": "reported measurements transcribed in previous direct-review project record; no original-page reinspection",
            "north_pool_side_lengths_m": SIDE_LENGTHS,
            "published_measurement_uncertainty_m": None,
        },
        "recorded_project_digitization": {
            "scale_bar_endpoints_px": [BAR_START, BAR_END],
            "scale_bar_length_px": PIXEL_LENGTH,
            "scale_bar_length_m": BAR_METRES,
            "nominal_m_per_px": SCALE,
            "independently_repeated_picks": 0,
            "recorded_pool_corner_coordinates_px": None,
            "source_image_pixel_origin": "top left, x right, y down",
            "geographic_fit": None,
        },
        "derived_arithmetic": {
            "reported_side_sum_m": sum(SIDE_LENGTHS.values()),
            "expected_side_lengths_px_at_recorded_scale": {k: v / SCALE for k, v in SIDE_LENGTHS.items()},
            "expected_pixel_lengths_status": "computed target values from printed dimensions, not digitized boundary measurements",
            "nominal_pick_uncertainty_m": {str(p): p * SCALE for p in [8, 10, 12]},
            "pixel_equivalent_of_two_metres": 2.0 / SCALE,
            "twenty_four_cubits_m": {"0.445_to_0.525": [24*.445,24*.525], "0.40_to_0.60": [24*.40,24*.60]},
            "minimum_reported_side_minus_model_upper_bound_m": {"0.445_to_0.525": min(SIDE_LENGTHS.values())-24*.525, "0.40_to_0.60": min(SIDE_LENGTHS.values())-24*.60},
            "cubit_m_required_to_equal_each_reported_side": {k: v/24.0 for k,v in SIDE_LENGTHS.items()},
        },
        "conditional_scale_sensitivity": {
            "status": "illustrative assumption; no measured endpoint error or confidence level",
            "assumed_each_endpoint_displacement_px": 2,
            "conservative_bar_length_interval_px": [139,147],
            "resulting_m_per_px_interval": [50/147,50/139],
        },
        "interpretation": {
            "side_length_test": "Repeated conditional arithmetic retains failure of a 24-cubit side-length or perimeter reading under both tested unit ranges. Source measurement uncertainty is unreported; wider unit range leaves a 0.6 m minimum numerical gap.",
            "offset_model": "Unresolved; no origin, inward/outward convention or digitized pool boundary.",
            "release_decision": "No accepted geographic footprint. Existing nominal 8-pixel pool picking translates to approximately 2.80 m before scale/registration error and cannot certify the declared two-metre 95% target.",
            "new_primary_source_targets": 0,
            "new_decisive_candidate_tests": 0,
            "question_closures": 0,
        },
        "missing_inputs": [
            "Original 269.jpg/full-resolution Fig.22 with image identity, unaltered dimensions and scale labels",
            "Printed p.255 (historical268.jpg) to reinspect complete pool-dimension passage",
            "Two independent scale endpoint pick sets, recorded before comparison",
            "Actual northern-pool corner/edge picks distinguishing water face, wall face and reconstructed segments",
            "Drawing north convention and any scan anisotropy or distortion information",
            "Published or empirically estimated measurement/pick uncertainty",
            "Six geographic fit controls and three withheld controls with surveyed identity, datum and accuracy",
        ],
    }
    assert abs(SCALE - 0.34965034965034963) < 1e-14
    assert abs(sum(SIDE_LENGTHS.values()) - 68.2) < 1e-12
    Path(__file__).with_name("hyrcania_dimensions_audit.json").write_text(json.dumps(output, ensure_ascii=False, indent=2)+"\n")

if __name__ == "__main__":
    main()
