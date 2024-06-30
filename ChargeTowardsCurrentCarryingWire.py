Web VPython 3.2

scene = canvas(title='Ampere\'s Law Simulation: Current Carrying Wire', width=800, height=600, align = "left")


# Constants
mu0 = 4 * pi * 1e-7  # Permeability of free space
I = 10000  # Current in amperes

wire_length = 100
wire_start = vector(0, 0, -50)
wire_end = vector(0, 0, 50)
wire_radius = 0.005
num_wire_segments = 100

arrow_scale = 0.3

dl = vector(0, 0, 1) * wire_length / num_wire_segments

wire = cylinder(pos = wire_start, radius = wire_radius, axis = wire_end - wire_start, color = color.green)

charge = sphere(pos = vector(1, 0, 0), radius = 0.01, charge = 100, make_trail = True, color = color.blue, trail_type = "points")
charge.mass = 1e-3
initial_velocity = vector(-1, 0, 0)
charge.velocity = initial_velocity


t = 0
dt = 0.0001


def calculate_net_force(pos, velocity):
    global charge
    
    magnetic_pos = vector(pos.x, pos.y, pos.z)
    mag_field_contribution = vector(0, 0, 0)
    
    for j in range(num_wire_segments):
        wire_piece = vector(0, 0, wire_start.z + (dl.z / 2) + (dl.z) * j)
        displacement_vector = magnetic_pos - wire_piece
        
        dB = (mu0 * I * cross(dl, displacement_vector)) / (4 * pi * mag(displacement_vector) ** 3)
        mag_field_contribution += dB 
       
    mag_force = charge.charge * cross(velocity, mag_field_contribution)
    mag_force_scale = arrow_scale / mag(mag_force)
#    mag_force_arrow = arrow(pos = pos, axis = mag_force_scale * mag_force, color=color.red)
     
    return mag_force
    

while t <= 100:
    
    rate(1000)
    scene.center = charge.pos
    net_force = calculate_net_force(charge.pos, charge.velocity)
    acceleration = net_force / charge.mass
    
    charge.pos = charge.pos + charge.velocity*dt
    charge.velocity = charge.velocity + acceleration*dt
    
    t = t + dt
    
