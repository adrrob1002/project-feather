# Structural Analysis of Wing Spar for Project Feather
import math
import matplotlib.pyplot as plt
from itertools import groupby

# Things to do:
# - Shear Buckling
# - Column Buckling
# - Thin Sheet Buckling
# - Inter-rivet Buckling

sheet_x_width = 0.1484  # [m]
sheet_x_thickness = 0.0008  # [m]

sheet_y_width = 0.04  # [m]
sheet_y_thickness = 0.0008  # [m]

stringer_width = 0.020  # [m]
stringer_thickness = 0.0015  # [m]


def get_stringer_second_moment_of_area(width: float):
    h_stringer_d = (sheet_x_width / 2) - (stringer_thickness / 2)
    h_stringer_i = (((width * stringer_thickness ** 3) / 12)
                    + (width * stringer_thickness * h_stringer_d ** 2))

    v_stringer_d = (sheet_x_width / 2) - stringer_thickness - ((width - stringer_thickness) / 2)
    v_stringer_i = (((stringer_thickness * (width - stringer_thickness) ** 3) / 12)
                    + (stringer_thickness * (width - stringer_thickness) * v_stringer_d ** 2))

    stringer_i = h_stringer_i + v_stringer_i

    return stringer_i


def get_bending_moment_at_position(longitudinal_position: float) -> float:
    if 0 <= longitudinal_position < 0.72:
        return 1075 + (322.9435 - 1075) * longitudinal_position / 0.72
    elif 0.72 <= longitudinal_position < 1.92:
        return 322.9435 + (-18.1289 - 322.9435) * (longitudinal_position - 0.72) / 1.2
    elif 1.92 <= longitudinal_position <= 2.25:
        return -18.1289 + 18.1289 * (longitudinal_position - 1.92) / 0.33
    else:
        return 0


def get_second_moment_of_area_at_position(longitudinal_position: float, hole_pos: list[float], hole_d: float) -> float:
    # 1. Two horizontal bars, at a distance a from the neutral axis
    sheet_y_d = (sheet_x_width / 2) + (sheet_y_thickness / 2)
    sheet_y_i = (((sheet_y_width * sheet_y_thickness ** 3) / 12)
                 + (sheet_y_width * sheet_y_thickness * sheet_y_d ** 2))

    # 2. Stringers, which you can assume have a cross-sectional area of 60mm2 and are positioned at a distance a from
    # the neutral axis
    stringer_i = get_stringer_second_moment_of_area(stringer_width)

    # 3. Vertical sheet (stiffener)
    sheet_x_i = (sheet_x_thickness * sheet_x_width ** 3) / 12

    # 4. Subtract the vertical section of a circle, if we're inside of one
    hole_i = 0.0
    hole_r = hole_d / 2

    for pos in hole_pos:
        x_offset = abs(longitudinal_position - pos)
        if x_offset <= hole_r:
            # Inside hole
            # Get the vertical size at this point
            y_size = 2 * math.sqrt((hole_r ** 2) - (x_offset ** 2))
            hole_i = -(sheet_x_thickness * y_size ** 3) / 12

    n_stringers = 2 if longitudinal_position >= 1.920 else 4

    return 2 * sheet_y_i + n_stringers * stringer_i + sheet_x_i + hole_i


def get_normal_stress_due_to_bending_at_position(
        longitudinal_position: float,
        perpendicular_distance: float,
        second_moment_of_area: float
) -> float:
    moment_at_position = get_bending_moment_at_position(longitudinal_position)  # [Nm]

    return (moment_at_position * perpendicular_distance) / second_moment_of_area


def get_shear_force_at_position(longitudinal_position: float) -> float:
    if 0 <= longitudinal_position < 0.72:
        return -1045
    elif 0.72 <= longitudinal_position < 1.92:
        return -284
    elif 1.92 <= longitudinal_position <= 2.25:
        return 55
    else:
        return 0


def get_critical_shear_buckling_stress(
        shear_buckling_coefficient: float, young_modulus: float, thickness: float, width: float
) -> float:
    return shear_buckling_coefficient * young_modulus * (thickness / width) ** 2


def get_critical_column_buckling_force(
        end_fixity_coefficient: float, young_modulus: float, second_moment_of_area: float, column_length: float
):
    return (end_fixity_coefficient * math.pi ** 2 * young_modulus * second_moment_of_area) / column_length ** 2


def get_critical_thin_sheet_buckling_stress(
        compression_buckling_coefficient: float, young_modulus: float, thickness: float, stiffener_pitch: float
) -> float:
    return compression_buckling_coefficient * young_modulus * (thickness / stiffener_pitch) ** 2


def get_critical_inter_rivet_buckling_stress(
        rivet_strength_constant: float, young_modulus: float, thickness: float, rivet_spacing: float
) -> float:
    return 0.9 * rivet_strength_constant * young_modulus * (thickness / rivet_spacing) ** 2


def calculate_first_moment_of_area_for_segment(width: float, height: float, distance_to_centroid: float):
    return width * height * distance_to_centroid


def get_first_moment_of_area_at_position(longitudinal_position: float, hole_pos: list[float], hole_d: float) -> float:
    # part 1: top sheet
    top_sheet = calculate_first_moment_of_area_for_segment(sheet_y_width, sheet_y_thickness, (sheet_x_width / 2)
                                                           + (sheet_y_thickness / 2))

    # part 2: vertical stringer part
    vertical_stringer = calculate_first_moment_of_area_for_segment(stringer_thickness, stringer_width,
                                                                   (sheet_x_width / 2) - (stringer_width / 2))

    # part 3: horizontal stringer part
    horizontal_stringer = calculate_first_moment_of_area_for_segment(
        width=stringer_width - stringer_thickness,
        height=stringer_thickness,
        distance_to_centroid=(sheet_x_width / 2) - (stringer_thickness / 2)
    )

    # part 4: web
    web_sheet = calculate_first_moment_of_area_for_segment(
        sheet_x_thickness,
        sheet_x_width / 2,
        sheet_x_width / 4
    )

    # part 5: hole
    hole = 0.0
    hole_r = hole_d / 2

    for pos in hole_pos:
        x_offset = abs(longitudinal_position - pos)
        if x_offset <= hole_r:
            # Inside hole
            # Get the vertical size at this point
            y_size = 2 * math.sqrt((hole_r ** 2) - (x_offset ** 2))
            hole = -1 * calculate_first_moment_of_area_for_segment(sheet_x_thickness, y_size / 2, y_size / 4)

    n_stringers = 1 if longitudinal_position >= 1.920 else 2

    return top_sheet + n_stringers * (vertical_stringer + horizontal_stringer) + web_sheet + hole


def get_transverse_shear_at_position(longitudinal_position: float, second_moment_of_area: float,
                                     first_moment_of_area: float) -> float:
    shear_force_at_position = get_shear_force_at_position(longitudinal_position)

    thickness = 0.0008  # [m]

    return (shear_force_at_position * first_moment_of_area) / (second_moment_of_area * thickness)


def get_consecutive_ranges(numbers: list[float], gap: float) -> list[list[float]]:
    ranges = []
    last_index = 0

    epsilon = 1e-6

    for num in numbers:
        if len(ranges) == 0:
            ranges.append([num, num])
        elif abs(num - ranges[last_index][1] - gap) < epsilon:
            ranges[last_index][1] = num
        else:
            last_index += 1
            ranges.append([num, num])

    return ranges


def main():
    web_segment_lengths = [0, 0.25, 0.5, 0.75, 2.25]  # [m]
    stringer_segment_lengths = [0, 1.5, 2.25]  # [m]
    # comp_bolt_segment_lengths = [0.075, 0.2, 0.335, 0.485, 0.655, 0.85, 1.08, 1.35, 1.65, 2.06, 2.25]  # (new)
    comp_bolt_segment_lengths = [0.075, 0.18, 0.318, 0.470, 0.640, 0.840, 1.123, 1.602, 1.83, 2.06]  # (old)

    shear_buckling_coefficients = [7.4, 7.4, 7.4, 5]  # [-]
    stringer_column_lengths = [1.5, 0.75]  # [m]
    comp_bolt_pitch = [comp_bolt_segment_lengths[index + 1] - comp_bolt_segment_lengths[index]
                       for index in range(len(comp_bolt_segment_lengths) - 1)]

    hole_positions = [0.2, 0.5, 0.8, 1.1, 1.4, 1.7, 2.0]  # [m]
    hole_diameter = 40 / 1000  # [m]

    yield_stress = 345000000  # [Pa]
    ultimate_stress = 483000000  # [Pa]

    young_modulus = 71700000000  # [Pa]

    safety_factor = 1.5
    perpendicular_distance = 0.0742

    positions = []
    moment_positions = []
    moments = []
    second_moments = []
    normal_forces = []
    transverse_shears = []

    shear_limits = []
    column_limits = []
    thin_sheet_limits = []
    inter_rivet_limits = []

    failure_points = []

    step = 0.001

    output_text = ""

    for pos_mm in range(0, 2250, int(step * 1000)):
        pos = float(pos_mm) / 1000  # [m]

        moment = get_bending_moment_at_position(pos)
        moments.append(moment)
        moment_positions.append(pos)

        # get which segment we are in:
        web_segment_index = -1
        for index in range(len(web_segment_lengths) - 1):
            segment_length = web_segment_lengths[index]
            if segment_length <= pos <= web_segment_lengths[index + 1]:
                web_segment_index = index

        flange_segment_index = -1
        for index in range(len(stringer_segment_lengths) - 1):
            segment_length = stringer_segment_lengths[index]
            if segment_length <= pos <= stringer_segment_lengths[index + 1]:
                flange_segment_index = index

        comp_bolt_segment_index = -1
        for index in range(len(comp_bolt_segment_lengths) - 1):
            segment_length = comp_bolt_segment_lengths[index]
            if segment_length <= pos <= comp_bolt_segment_lengths[index + 1]:
                comp_bolt_segment_index = index

        shear_buckling_coefficient = shear_buckling_coefficients[web_segment_index]

        critical_shear_buckling_stress = get_critical_shear_buckling_stress(
            shear_buckling_coefficient=shear_buckling_coefficient,
            young_modulus=young_modulus,
            thickness=sheet_x_thickness,
            width=sheet_x_width,
        )

        column_length = stringer_column_lengths[flange_segment_index]

        stringer_second_moment = (5 * stringer_width ** 3 * stringer_thickness) / 24

        critical_column_buckling_force = get_critical_column_buckling_force(
            end_fixity_coefficient=7.5,
            young_modulus=young_modulus,
            second_moment_of_area=stringer_second_moment,
            column_length=column_length
        )

        critical_column_buckling_stress = (critical_column_buckling_force /
                                           (stringer_width ** 2 - (stringer_width - stringer_thickness) ** 2))

        first_moment_of_area = get_first_moment_of_area_at_position(pos, hole_positions, hole_diameter)
        second_moment_of_area = get_second_moment_of_area_at_position(pos, hole_positions, hole_diameter)

        second_moments.append(second_moment_of_area)

        flange_normal_stress = safety_factor * get_normal_stress_due_to_bending_at_position(pos, perpendicular_distance,
                                                                                            second_moment_of_area)
        transverse_shear = safety_factor * get_transverse_shear_at_position(pos, second_moment_of_area,
                                                                            first_moment_of_area)

        bolt_pitch = comp_bolt_pitch[comp_bolt_segment_index]

        critical_thin_sheet_buckling_stress = get_critical_thin_sheet_buckling_stress(
            compression_buckling_coefficient=6.97,
            young_modulus=young_modulus,
            thickness=sheet_y_thickness + stringer_thickness,
            stiffener_pitch=bolt_pitch
        )

        critical_inter_rivet_buckling_stress = get_critical_inter_rivet_buckling_stress(
            rivet_strength_constant=3.5,
            thickness=sheet_y_thickness + stringer_thickness,
            young_modulus=young_modulus,
            rivet_spacing=bolt_pitch
        )

        transverse_shears.append(transverse_shear)
        shear_limits.append(critical_shear_buckling_stress)

        if comp_bolt_segment_index != -1:
            positions.append(pos)
            normal_forces.append(abs(flange_normal_stress))
            column_limits.append(critical_column_buckling_stress)
            thin_sheet_limits.append(critical_thin_sheet_buckling_stress)
            inter_rivet_limits.append(critical_inter_rivet_buckling_stress)

        yield_fail = abs(flange_normal_stress) > yield_stress
        ultimate_fail = abs(flange_normal_stress) > ultimate_stress
        shear_buckle = abs(transverse_shear) > critical_shear_buckling_stress
        column_buckle = (abs(flange_normal_stress) / 2) > critical_column_buckling_stress
        thin_sheet_buckle = abs(flange_normal_stress) > critical_thin_sheet_buckling_stress
        inter_rivet_buckle = abs(flange_normal_stress) > critical_inter_rivet_buckling_stress

        failing = (yield_fail or ultimate_fail or shear_buckle or column_buckle or thin_sheet_buckle
                   or inter_rivet_buckle)

        if failing and comp_bolt_segment_index != -1:
            failure_modes = []
            extra_info = []  # list[[str, str]]
            failure_points.append(pos)

            if yield_fail:
                failure_modes.append("yield")
                extra_info.append([flange_normal_stress, "Pa"])
                extra_info.append([yield_stress, "Pa"])

            if ultimate_fail:
                failure_modes.append("ultimate")
                extra_info.append([flange_normal_stress, "Pa"])
                extra_info.append([ultimate_stress, "Pa"])

            if shear_buckle:
                failure_modes.append("shear")
                extra_info.append([transverse_shear, "Pa"])
                extra_info.append([critical_shear_buckling_stress, "Pa"])

            if column_buckle:
                failure_modes.append("column")
                extra_info.append([flange_normal_stress, "Pa"])
                extra_info.append([critical_column_buckling_stress, "Pa"])

            if thin_sheet_buckle:
                failure_modes.append("thin-sheet")
                extra_info.append([flange_normal_stress, "Pa"])
                extra_info.append([critical_thin_sheet_buckling_stress, "Pa"])

            if inter_rivet_buckle:
                failure_modes.append("inter-rivet")
                extra_info.append([flange_normal_stress, "Pa"])
                extra_info.append([critical_inter_rivet_buckling_stress, "Pa"])

            output_text += f"failure modes at z = {pos} m:\n\n"
            output_text += f"{'moment:':>15} {get_bending_moment_at_position(pos)} Nm\n"

            for mode_index, mode in enumerate(failure_modes):
                stress_values = extra_info[2 * mode_index]
                limit_values = extra_info[2 * mode_index + 1]

                stress = stress_values[0]
                stress_units = stress_values[1]

                limit = limit_values[0]
                limit_units = limit_values[1]

                output_text += (f"{mode:>15}: stress = {stress:.2f} {stress_units}\n"
                                f"{' ' * 15}  limit  = {limit:.2f} {limit_units}\n")

            output_text += "-" * 50 + "\n"

    fig, ax = plt.subplots()

    ax.plot(positions, normal_forces, label="absolute normal stress")
    ax.plot(positions, column_limits, label="critical column buckling stress")
    ax.plot(positions, thin_sheet_limits, label="critical thin sheet buckling stress")
    ax.plot(positions, inter_rivet_limits, label="critical inter rivet buckling stress")

    failure_ranges = get_consecutive_ranges(failure_points, step)
    print(f"Failed between {', '.join(f'{f_range[0]} m to {f_range[1]} m' for f_range in failure_ranges)}.")

    for f_range in failure_ranges:
        start, stop = f_range[0], f_range[1]

        ax.axvspan(start, stop, color="red", alpha=.2)

    for bolt_pos in comp_bolt_segment_lengths:
        ax.axvline(x=bolt_pos, ls=":", color="red", alpha=.5)

    ax.axvline(x=0.150, ls="--", color="black", alpha=.7)
    ax.legend()

    plt.title(f"Internal Normal Force at y = {perpendicular_distance} [m], safety factor = {safety_factor}")
    plt.ylabel("Internal Normal Force [Pa]")
    plt.xlabel("Longitudinal Position [m]")

    # ax.plot(moment_positions, second_moments)

    # ax.plot(moment_positions, moments)

    # axs[1].plot(positions, transverse_shears, label="transverse shears")
    # axs[1].plot(positions, shear_limits, label="shear limits")
    # axs[1].legend()

    plt.show()

    print(f"Compressive bolt positions: {', '.join([f'{b_pos} m' for b_pos in comp_bolt_segment_lengths[:-1]])}")

    with open("failure_log.txt", "w") as output_file:
        output_file.write(output_text)
        output_file.close()


if __name__ == '__main__':
    main()
