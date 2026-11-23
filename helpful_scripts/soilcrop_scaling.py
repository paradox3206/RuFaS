import json
from pathlib import Path



def scale_json_fields(filename, fields, scale_factor):
    """
    Scale specified fields in a JSON file and save the result
    as a new file. The original JSON file is not modified.

    Examples:
        scale_factor = 3.0
        animal.json -> animal_3X.json

        scale_factor = 0.5
        animal.json -> animal_0p5X.json
    """

    filename = Path(filename)

    # Always load from the original reference JSON
    with open(filename, "r") as f:
        data = json.load(f)

    def scale_fields(obj):
        """Recursively find and scale the specified fields."""

        if isinstance(obj, dict):
            for key, value in obj.items():

                if key in fields:

                    # Scale a list of numeric values
                    if isinstance(value, list):
                        obj[key] = [
                            x * scale_factor
                            if isinstance(x, (int, float))
                            and not isinstance(x, bool)
                            else x
                            for x in value
                        ]

                    # Scale an individual numeric value
                    elif (
                        isinstance(value, (int, float))
                        and not isinstance(value, bool)
                    ):
                        obj[key] = value * scale_factor

                else:
                    # Continue searching nested structures
                    scale_fields(value)

        elif isinstance(obj, list):
            for item in obj:
                scale_fields(item)

    scale_fields(data)

    # Create filesystem-friendly scaling labels:
    # 3.0  -> 3X
    # 0.5  -> 0p5X
    # 0.25 -> 0p25X
    factor_label = f"{scale_factor:g}".replace(".", "p") + "X"

    # Construct the new filename
    output_filename = filename.with_name(
        f"{filename.stem}_{factor_label}{filename.suffix}"
    )

    # Save the scaled JSON
    with open(output_filename, "w") as f:
        json.dump(data, f, indent=4)

    print(
        f"Created: {output_filename}\n"
        f"  Scaled fields: {', '.join(fields)}\n"
        f"  Factor: {scale_factor:g}X"
    )


# ============================================================
# Define the reference files and fields to scale
# ============================================================

FILES_TO_SCALE = {
    "input/data/field/GL_field_1.json": [
        "body_weight",
        "milk_production",
    ],
    "input/data/GL_field_1_fertilizer_schedule.json": [
        "nitrogen_masses",
        "phosphorus_masses",
        "potassium_masses"
    ],
    "input/data/GL_field_1_manure_schedule.json": [
        "nitrogen_masses",
        "phosphorus_masses",
        "potassium_masses"
    ],
    "input/data/field/GL_field_2.json": [
        "body_weight",
        "milk_production",
    ],
    "input/data/GL_field_2_fertilizer_schedule.json": [
        "nitrogen_masses",
        "phosphorus_masses",
        "potassium_masses"
    ],
    "input/data/GL_field_2_manure_schedule.json": [
        "nitrogen_masses",
        "phosphorus_masses",
        "potassium_masses"
    ]
}


# ============================================================
# Scaling factors to generate
# ============================================================

SCALE_FACTORS = [
    0.25,
    4.5,
    3.5
]

# ============================================================
# Generate a complete fileset for every scaling factor
# ============================================================

for scale_factor in SCALE_FACTORS:

    print(f"\n--- Generating {scale_factor:g}X fileset ---")

    for filename, fields in FILES_TO_SCALE.items():
        scale_json_fields(
            filename,
            fields,
            scale_factor
        )
