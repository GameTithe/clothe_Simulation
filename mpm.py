import taichi as ti  

ti.init(arch=ti.gpu)

n = 128

# x is an n x n field + 3D floating vector 
x = ti.Vector.field(3, dtype = float, shape = (n, n))
v = ti.Vector.field(3, dtype = float, shape = (n, n))
quad_size = 1.0 / n

# ball

#radius = 0.3
#center[0] = [0,0,0]

# @ti.data_oriented 
# class Ball:
#     def __init__(self, radius, center): 
#         self.ball_radius = radius
#         self.ball_center = ti.Vector.field(3, dtype = float, shape = (1, ))
#         self.ball_center[0] = ti.Vector(center)

balls_count = 3
balls_center = ti.Vector.field(3, dtype = float, shape = (balls_count, ))
balls_radius = ti.field(dtype =float, shape = (balls_count, )) #0.3

balls_radius_render =  ti.field(dtype =float, shape = (balls_count, ))

@ti.kernel
def initialize_balls():  
    balls_center[0] = ti.Vector([0, 0, 0])
    balls_radius[0] = 0.3
    balls_radius_render[0] = 0.3 * 0.95
    
    balls_center[1] = ti.Vector([-0.3, -0.3, 0])
    balls_radius[1] = 0.4
    balls_radius_render[1] = 0.4 * 0.95
    
    balls_center[2] = ti.Vector([0.3, -0.3, 0])
    balls_radius[2] = 0.2
    balls_radius_render[2] = 0.2 * 0.95

#gravity
gravity = ti.Vector([0, -9.8, 0])

#spring
spring_Y = 3e4 
dashpot_damping = 1e4
drag_damping = 1

spring_offsets = []
for i in range (-1 , 2):
    for j in range(-1, 2):
        if( i , j ) != (0,0):
            spring_offsets.append(ti.Vector([i,j]))
              
#time step            
dt = 4e-2 / n
substeps = int(1 / 60 // dt)


# automatically parallelize all top-level for loops 
@ti.kernel
def initialize_mass_points() : 
    random_offset = ti.Vector([ti.random() - 0.5, ti.random() - 0.5]) * 0.1 
    
    for i,j in x:
        x[i,j] = [
            i * quad_size - 0.5 + random_offset[0], 0.6,
            j * quad_size - 0.5 + random_offset[1]
        ]
        
        # inital velocity of each mass point is set to 0
        v[i,j] = [0,0,0]
        

@ti.kernel
def substep() :
    for i in ti.grouped(x):
        v[i] += gravity * dt    
        
    # traverse the field x
    # 'i' is absolute index
    for i in ti.grouped(x):
        force = ti.Vector([0.0, 0.0, 0.0]) 
        for spring_offset in ti.static(spring_offsets):
            j = i + spring_offset
            
            if 0 <= j[0] < n and 0 <= j[1] < n :
                x_ij = x[i] - x[j]
                v_ij = v[i] - v[j]
                
                dir = x_ij.normalized() 
                current_dist = x_ij.norm()
                original_dist = quad_size * float(i - j).norm()
                
                #Hooke's Law
                force += -spring_Y * dir * (current_dist / original_dist - 1 )
                
                # daming force
                # quad_size -> original_dist? 
                force += -dashpot_damping * (v_ij.dot(dir)) * dir * quad_size

        v[i]  += force * dt
    
    #damping
    for i in ti.grouped(x):
        v[i] *= ti.exp( -drag_damping * dt)
    
    #collision with the ball 
    for i in ti.grouped(x): 
        for j in range(balls_count):     
            offset_to_center = x[i] - balls_center[j] 
            if offset_to_center.norm() <= balls_radius[j]:
                normal = offset_to_center.normalized()
                v[i] -= min(v[i].dot(normal), 0) * normal
                
        x[i] += v[i] * dt
                

num_triangles = (n - 1) * (n - 1) * 2
indices = ti.field(int, shape=num_triangles * 3)
vertices = ti.Vector.field(3, dtype=float, shape=n * n)
colors = ti.Vector.field(3, dtype=float, shape=n * n)

@ti.kernel 
def update_vertices():
    for i,j in ti.ndrange(n,n):
        vertices[i *n + j] = x[i,j]
        
@ti.kernel
def initialize_mesh_indices():
    for i, j in ti.ndrange(n - 1, n - 1):
        quad_id = (i * (n - 1)) + j
        # First triangle of the square
        indices[quad_id * 6 + 0] = i * n + j
        indices[quad_id * 6 + 1] = (i + 1) * n + j
        indices[quad_id * 6 + 2] = i * n + (j + 1)
        # Second triangle of the square
        indices[quad_id * 6 + 3] = (i + 1) * n + j + 1
        indices[quad_id * 6 + 4] = i * n + (j + 1)
        indices[quad_id * 6 + 5] = (i + 1) * n + j

    for i, j in ti.ndrange(n, n):
        if (i // 4 + j // 4) % 2 == 0:
            colors[i * n + j] = (0.22, 0.72, 0.52)
        else:
            colors[i * n + j] = (1, 0.334, 0.52)
            
initialize_mesh_indices()

window = ti.ui.Window("Taichi Cloth Simulation on GGUI", (1024, 1024),
                      vsync=True)
canvas = window.get_canvas()
canvas.set_background_color((1, 1, 1))
scene = ti.ui.Scene()
camera = ti.ui.Camera()

current_t = 0.0
initialize_mass_points()
initialize_balls()

while window.running:
    if current_t > 1.5:
        # Reset
        initialize_mass_points()
        current_t = 0

    for i in range(substeps):
        substep()
        current_t += dt
        
    update_vertices()

    camera.position(0.0, 0.0, 3)
    camera.lookat(0.0, 0.0, 0)
    scene.set_camera(camera)

    scene.point_light(pos=(0, 1, 2), color=(1, 1, 1))
    scene.ambient_light((0.5, 0.5, 0.5))
    scene.mesh(vertices,
               indices=indices,
               per_vertex_color=colors,
               two_sided=True)

    # Draw a smaller ball to avoid visual penetration
    #for i in range(balls_count):
    # float 
    scene.particles(balls_center, radius= 0, per_vertex_radius=balls_radius_render, color=(0.5, 0.42, 0.8))

    
    canvas.scene(scene)
    window.show()
    