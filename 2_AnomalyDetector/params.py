log_offsets = {
    'vel': {
        'start': 0,
        'end': 3,
        'cols': ['velocity_data_x', 'velocity_data_y', 'velocity_data_z']
    },
    'acc': {
        'start': 3,
        'end': 6,
        'cols': ['acceleration_data_x', 'acceleration_data_y', 'acceleration_data_z']
    },
    'euler': {
        'start': 6,
        'end': 9,
        'cols': ['euler_data_r', 'euler_data_p', 'euler_data_y']
    },
    'angular': {
        'start': 9,
        'end': 12,
        'cols': ['angular_rate_data_vr','angular_rate_data_vp', 'angular_rate_data_vy']
    },
}