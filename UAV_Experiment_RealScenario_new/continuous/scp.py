import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os

space_dimension = 2


def draw_circle(center, c_radius, colors=(0, 0, 0)):
    _vert_list = []
    for _i in range(1000):
        _x = c_radius*np.cos(_i*2*np.pi/1000) + center[0]
        _y = c_radius*np.sin(_i*2*np.pi/1000) + center[1]
        _vert_list.append([_x, _y])
    _vert = np.asarray(_vert_list)
    _ax = plt.plot(_vert[:, 0], _vert[:, 1], color=colors)
    return _ax


class CvxStep(object):
    def __init__(self, current_state, safe_radius, obstacles, pre_path, current_time, time_horizon, end_time, time_step, target):
        self.current_state = np.asarray(current_state) # ndarray, [x, y, vx, vy]
        self.safe_radius = safe_radius
        self.obstacles = np.asarray(obstacles) # type ndarray, obstacle =[obs_i], obs_i = [px, py, vx, vy, radius]
        self.pre_path = np.asarray(pre_path) # pre_path = [trajectory[ct+], ..., trajectory[T], trajectory[t]= [x, y]
        self.current_time = current_time
        self.mpc_horizon = time_horizon
        self.target_time = end_time
        self.time_step = time_step
        self.target_pose = target
        self.collision_index = []
        self.static_obs = np.asarray(obstacles)
        if np.shape(self.obstacles)[0]:
            if np.shape(self.obstacles)[1] != 2*space_dimension + 1 or np.shape(pre_path)[1] != space_dimension:
                print("The dimension is {}, the dimension of each obstacle should be {}, trajectory should be {}".format(
                    space_dimension, 2*space_dimension + 1, 3*space_dimension))

    def horizon(self):
        current_horizon = self.mpc_horizon if self.current_time + self.mpc_horizon < self.target_time else \
            self.target_time - self.current_time
        return current_horizon

    def collision(self):
        have_checked = False
        _current_horizon = self.horizon()
        _unchecked_steps = [item for item in list(range(_current_horizon)) if item not in self.collision_index]
        for _, step in enumerate(_unchecked_steps):
            for _, _value in enumerate(self.obstacles):
                obs_x = _value[0] + _value[2]*self.time_step*(step + 1)
                obs_y = _value[1] + _value[3]*self.time_step*(step + 1)
                _dis = np.sqrt((self.pre_path[step, 0]-obs_x)**2 + (self.pre_path[step, 1] - obs_y)**2)
                if _dis < self.safe_radius + _value[-1]:
                    self.collision_index = np.append(self.collision_index, step)
                    have_checked = True
                if have_checked:
                    break
            if have_checked:
                break

    def reset_path(self): # only for static obstacles
        _path = self.pre_path
        for position_index, position in enumerate(self.pre_path):
            for _, _value in enumerate(self.static_obs):
                _obs_x = _value[0]
                _obs_y = _value[1]
                dis = np.sqrt((position[0] - _obs_x)**2 + (position[1] - _obs_y)**2)
                safe_rho = _value[-1] + self.safe_radius
                if 1e-3 <= dis < safe_rho:
                    sin_theta = (position[1] - _obs_y) / dis
                    cos_theta = (position[0] - _obs_x) / dis
                    new_position = [safe_rho*cos_theta + _value[0], safe_rho*sin_theta + _value[1]]
                    _path[position_index] = new_position
                elif dis < 1e-3:
                    new_position = _path[position_index-1]
                    _path[position_index] = new_position
        self.pre_path = _path
        self.collision_index = []

    def convex_obs(self):
        # to construct collision avoidance equation
        # A_x*x +A_y*y >= b
        self.collision()
        obs_size = np.shape(self.obstacles)
        if obs_size[0] == 0:
            return [], [], []
        current_horizon = self.horizon()
        path_len = self.pre_path.__len__()
        if path_len < self.target_time - self.current_time:
            remain_len = self.target_time - self.current_time
            remain_path = np.zeros((remain_len, 2))
            self.pre_path = np.append(self.pre_path, remain_path, axis=0)
        # if path_len > current_horizon:
        #     self.pre_path = self.pre_path[0:current_horizon]
        # elif path_len < current_horizon:
        #     remain_len = current_horizon - path_len
        #     remain_path = np.zeros((remain_len, 2))
        #     self.pre_path = np.append(self.pre_path, remain_path, axis=0)
        A_x, A_y, b = [], [], [] # Construct collision avoidance constraints for each obstacle in the form
                                    # "A_x*x +A_y*y >= b".
        non_collision = [item for item in list(range(current_horizon)) if item not in self.collision_index]
        # non_collision = []
        collision_check_path = self.pre_path[0:current_horizon]
        for index, obs_value in enumerate(self.obstacles):
            obs_x = obs_value[0] + [obs_value[2]*self.time_step*(np.asarray(range(current_horizon)) + 1)]
            obs_y = obs_value[1] + [obs_value[3]*self.time_step*(np.asarray(range(current_horizon)) + 1)]
            obs_path = np.hstack((obs_x.transpose(), obs_y.transpose()))
            A_index = collision_check_path - obs_path
            b_index = (self.safe_radius + obs_value[-1]) * np.linalg.norm(A_index, axis=1)
            b_index = b_index + np.sum(np.multiply(obs_path, A_index), axis=1)
            A_index[non_collision, ] = 0
            b_index[non_collision] = 0
            Ax_diag = np.diag(A_index[:, 0])
            Ay_diag = np.diag(A_index[:, 1])
            A_x.append(Ax_diag)
            A_y.append(Ay_diag)
            b.append(b_index)
        return A_x, A_y, b

    def kinematics(self):
        # generate the kinematics equations
        # initialization is the current_state: x(0), y(0), v_x(0), v_y(0)
        # x = Aeq*a_x + b_x, x=[x(1),x(2), ..., x(H)], a_x = [a(0), a(1), ..., a(H-1)]
        # y = Aeq*a_y + b_y, y=[y(1),y(2), ..., y(H)], a_y = [a(0), a(1), ..., a(H-1)]
        # x(h) = x(h-1) + v_x(h-1)*t + 1/2 a_x(h-1)*t^2
        #      = x(0) + hv_x(0)*t + \sum_{i=1}^H (2i-1)/2*a_x(i-1)*t^2
        # y(h) = y(h-1) + v_y(h-1)*t + 1/2 a_y(h-1)*t^2
        current_x = self.current_state[0]
        current_y = self.current_state[1]
        current_v_x = self.current_state[2]
        current_v_y = self.current_state[3]
        remain_len = self.target_time - self.current_time
        Aeq = np.zeros((remain_len, remain_len))
        for i in range(remain_len):
            for j in range(i+1):
                Aeq[i, j] = (2*i-2*j+1)/2*self.time_step**2
        one = np.ones((remain_len, 1))
        b_x = current_x*one + current_v_x*self.time_step*(np.asarray(range(remain_len)).reshape(remain_len, 1)+1)
        b_x = np.squeeze(b_x)
        b_y = current_y*one + current_v_y*self.time_step*(np.asarray(range(remain_len)).reshape(remain_len, 1)+1)
        b_y = np.squeeze(b_y)
        Aeq_v = np.tri(remain_len)
        b_v_x = current_v_x + np.ones((remain_len, 1))*self.time_step
        b_v_x = np.squeeze(b_v_x)
        b_v_y = current_v_y + np.ones((remain_len, 1)) * self.time_step
        b_v_y = np.squeeze(b_v_y)
        return Aeq, b_x, b_y, Aeq_v, b_v_x, b_v_y

    def convex_solver(self, acc):
        problem_size = self.target_time - self.current_time
        current_view = self.horizon()
        _iteration = 0
        while _iteration <= 100:
            a_x = cp.Variable(problem_size)
            a_y = cp.Variable(problem_size)
            if current_view == problem_size:
                objective = cp.Minimize(cp.sum_squares(a_x[0:current_view])+cp.sum_squares(a_y[0:current_view]))
            else:
                objective = cp.Minimize(cp.sum_squares(a_x[0:current_view]) + cp.sum_squares(a_y[0:current_view])
                                        + cp.sum_squares(a_x[current_view:]) + cp.sum_squares(a_y[current_view:]))
            constr = []
            # kinematics constrains
            _Aeq_xy, _b_x, _b_y, _Aeq_vxy, _bv_x, _bv_y = self.kinematics()
            x = _Aeq_xy*a_x + _b_x
            y = _Aeq_xy*a_y + _b_y
            vx = _Aeq_vxy*a_x + _bv_x
            vy = _Aeq_vxy*a_y + _bv_y
            constr += [acc[0] <= a_x, a_x <= acc[1], acc[0] <= a_y, a_y <= acc[1]]
            constr += [x[-1] == self.target_pose[0], y[-1] == self.target_pose[1]]
            constr += [vx[-1] == self.target_pose[2], vy[-1] == self.target_pose[3]]
            # collision avoidance constraints
            _A_x, _A_y, _b = self.convex_obs()
            if _A_x.__len__():
                for obs_i in range(_A_x.__len__()):
                    constr += [_A_x[obs_i]*x[0: current_view] + _A_y[obs_i]*y[0:current_view] >= _b[obs_i]]
            prob = cp.Problem(objective, constr)
            try:
                opt_value = prob.solve(solver=cp.MOSEK)
                # print(prob.status)
            except cp.SolverError:
                opt_value = prob.solve(solver=cp.SCS)
            _iteration += 1
            if prob.status == "infeasible":
                # for _i in range(self.obstacles.__len__()):
                #     draw_circle(self.obstacles[_i, 0:2], self.obstacles[_i, -1])
                #     plt.plot(self.obstacles[_i, 0], self.obstacles[_i, 1], '.k')
                # plt.plot(self.pre_path[:, 0], self.pre_path[:, 1], '.r')
                # plt.axis('scaled')
                # plt.show()
                self.reset_path()
                # for _i in range(self.obstacles.__len__()):
                #     draw_circle(self.obstacles[_i, 0:2], self.obstacles[_i, -1])
                #     plt.plot(self.obstacles[_i, 0], self.obstacles[_i, 1], '.k')
                # plt.plot(self.pre_path[:, 0], self.pre_path[:, 1], '.r')
                # plt.axis('scaled')
                # plt.show()
            elif prob.status == "optimal":
                try:
                    com_path = np.vstack((x.value.transpose(), y.value.transpose()))
                    # this_velocity = np.vstack((vx.value.transpose(), vy.value.transpose()))
                    this_path = com_path.transpose()
                    # this_velocity = this_velocity.transpose()
                    error = np.sum(np.linalg.norm(this_path - self.pre_path, axis=1))
                    if error <= 1e-3:
                        return prob.status, a_x.value, a_y.value, vx.value, vy.value, x.value, y.value
                        break
                    else:
                        self.pre_path = this_path
                except AttributeError:
                    return prob.status, [], [], [], [], [], []
            else:
                return prob.status, [], [], [], [], [], []
        if _iteration > 100:
            _status = "infeasible"
            return _status, [], [], [], [], [], []

# class robot_obstacle_generation(object):
#     def __init__(self, pre_path, current_time, time_horizon, end_time, time_step, target):

class ScenarioSolution(object):
    def __init__(self, cur_pose, t_pose, time_horizon, target_instant, delta, robot_radius, acc_limit, no_obs, boundary):
        self.initial = cur_pose #[x0, y0, vx0, vy0]
        self.target = t_pose
        self.current_instant = 0
        self.horizon_len = time_horizon
        self.finish_instant = target_instant
        self.time_step = delta
        self.radius = robot_radius
        self.acceleration_range = acc_limit
        self.max_num_obs = no_obs
        self.static_obstacle_generation()
        # self.fix_static_obstacle_generation(boundary)

    def static_obstacle_generation(self):
        _static_obstacles = []
        # generate obstacles randomly
        for _i in range(self.max_num_obs):
            _static_obstacles.append(list(np.append(np.random.uniform([self.initial[0], self.initial[1]],
                                                                      [self.target[0], self.target[1]], 2),
                                                   [0, 0, float(np.random.uniform(0.5, 1.5, 1))])))
        # delete obstalces that collide with initial and target positions
        for _index in reversed(list(range(_static_obstacles.__len__()))):
            _a_obs = np.asarray(_static_obstacles[_index])
            _dis2init = np.linalg.norm(np.asarray(self.initial[0:2]) - _a_obs[0:2])
            _dis2goal = np.linalg.norm(np.asarray(self.target[0:2]) - _a_obs[0:2])
            _rho = self.radius + _a_obs[-1]
            if _dis2init < _rho or _dis2goal < _rho:
                _static_obstacles.remove(_static_obstacles[_index])
                continue
        # merge overlapped obstacles in the configuration space
        for _i in reversed(list(range(_static_obstacles.__len__()))):
            _a_obs = np.asarray(_static_obstacles[_i][0:2])
            for _j in range(_i):
                _b_obs = np.asarray(_static_obstacles[_j][0:2])
                _dis = np.linalg.norm(_a_obs - _b_obs)
                if _dis < 2.*self.radius + _static_obstacles[_i][-1] + _static_obstacles[_j][-1]:
                    _static_obstacles[_j] = _static_obstacles[_i]
        # print("with duplicate:", _static_obstacles)
        obs_array = np.asarray(_static_obstacles)
        if obs_array.size:
            self.obstacles = np.unique(obs_array, axis=0)
            self.static_obs = np.unique(obs_array, axis=0)
        else:
            self.obstacles = obs_array
            self.static_obs = obs_array

    def fix_static_obstacle_generation(self, boundary):
        _new = 0
        _static_obstacles = []
        _try_number = 0
        while _new < self.max_num_obs and _try_number < 2000*self.max_num_obs:
            _try_number += 1
            if _new < 3:
                _temporary_obs = np.append(np.random.uniform([self.initial[0], self.initial[1]],
                                                             [self.target[0], self.target[1]], 2),
                                           [0, 0, float(np.random.uniform(0.5, 1.5, 1))])
            else:
                _temporary_obs = np.append(np.random.uniform(boundary[0], boundary[1], 2),
                                           [0, 0, float(np.random.uniform(0.5, 1.5, 1))])
            _dis2init = np.linalg.norm(np.asarray(self.initial[0:2]) - _temporary_obs[0:2])
            _dis2goal = np.linalg.norm(np.asarray(self.target[0:2]) - _temporary_obs[0:2])
            _rho = self.radius + _temporary_obs[-1]
            if _dis2init < _rho or _dis2goal < _rho:
                continue
            elif not _static_obstacles.__len__():
                _static_obstacles.append(list(_temporary_obs))
                _new += 1
            else:
                _merge = False
                for _i, _value in enumerate(_static_obstacles):
                    _a_obs = np.asarray(_value[0:2])
                    _dis = np.linalg.norm(_a_obs - _temporary_obs[0:2])
                    if _dis < 2. * self.radius + _value[-1] + _temporary_obs[-1]:
                        _merge = True
                        break
                if not _merge:
                    _static_obstacles.append(list(_temporary_obs))
                    _new += 1
        self.obstacles = np.asarray(_static_obstacles)
        self.static_obs = np.asarray(_static_obstacles)
        # print("generated obstacles: ", self.obstacles)

    def show_obstacle(self):
        for _item, _value in enumerate(self.obstacles):
            plt.plot(_value[0], _value[1], '.k')
            draw_circle(_value[0:2], _value[-1])

    def generate_solution(self):
        _init_x = np.linspace(self.initial[0], self.target[0], num=self.finish_instant + 1).reshape(self.finish_instant + 1, 1)
        _init_y = np.linspace(self.initial[1], self.target[1], num=self.finish_instant + 1).reshape(self.finish_instant + 1, 1)
        _path = np.hstack((_init_x[1:], _init_y[1:]))
        _P = CvxStep(self.initial, self.radius, self.obstacles, _path, self.current_instant,
                     self.horizon_len, self.finish_instant, self.time_step, self.target)
        _status, _ax, _ay, _vx, _vy, _x, _y = _P.convex_solver(self.acceleration_range)
        return _status, _ax, _ay, _vx, _vy, _x, _y


class ScenarioGeneration(object):
    steps, horizon, step_len = 40, 40, 0.1
    robot_radius = 0.5

    def __init__(self, space_boundary=[-10, 10], velocity_boundary=[-5, 5], acceleration_boundary=[-10, 10]):
        self.rec_space = space_boundary # [low, up]
        self.vel_space = velocity_boundary
        self.acc_space = acceleration_boundary
        self.current_step = 0

    def generate_configuration(self):
        _current_pose = [0, 0, 0, 0]
        while True:
            _rand_pos = list(np.random.uniform(low=[self.rec_space[0]]*2, high=[self.rec_space[1]]*2, size=2))
            _dis = np.sqrt(_rand_pos[0]**2+_rand_pos[1]**2)
            if _dis > 6:
                _target_pose = np.append(_rand_pos, [0, 0])
                break
        _obs_numbers = np.random.randint(5, 15) # number of obstacles generated initially
        return _current_pose, _target_pose, _obs_numbers


if __name__ == "__main__":
    file_name = 'data.csv'
    total_case = 0
    if os.path.isfile(file_name):
        os.remove(file_name)
    epochs, iterations = 200, 1000
    space_limit = [-10, 10]
    for epoch in range(epochs):
        robot_init = ScenarioGeneration(space_boundary=space_limit)
        current_pose, target_pose, max_obs = robot_init.generate_configuration()
        max_obs = 5
        df1 = pd.DataFrame(current_pose)
        df2 = pd.DataFrame(target_pose)
        for iteration in range(iterations):
            S = ScenarioSolution(current_pose, target_pose, robot_init.horizon, robot_init.steps,
                                 robot_init.step_len, robot_init.robot_radius, robot_init.acc_space, max_obs,
                                 space_limit)
            S.show_obstacle()
            plt.axis('scaled')
            plt.show()
            status, ax, ay, vx, vy, x, y = S.generate_solution()
            print("Epoch: {}, Iteration: {}/{}, Status: {}".format(epoch + 1, iteration + 1, iterations, status))
            if status == "optimal":
                total_case += 1
                title = "Case"
                df_title = pd.DataFrame([title])
                df_title.to_csv(file_name, mode='a', header=False, index=False)
                # no last acceleration, set to 0
                ax = np.concatenate((ax, np.zeros(1)))
                ay = np.concatenate((ay, np.zeros(1)))
                # add initial pose
                vx = np.concatenate((np.asarray([current_pose[0]]), vx))
                vy = np.concatenate((np.asarray([current_pose[1]]), vy))
                x = np.concatenate((np.asarray([current_pose[2]]), x))
                y = np.concatenate((np.asarray([current_pose[3]]), y))
                # Transfer to DataFrame and writ to file
                df = pd.DataFrame({'ax': ax, 'ay': ay, 'vx': vx, 'vy': vy, 'x': x, 'y': y})
                df.to_csv(file_name, mode='a', header=True, index=False)
                if S.obstacles.size:
                    df1 = pd.DataFrame(S.obstacles, columns=['obs_x', 'obs_y', 'obs_vx', 'obs_vy', 'obs_r'])
                    df1.to_csv(file_name, mode='a', header=True, index=False)
                plt.plot(x, y, 'r')
                for i in range(x.__len__()):
                    draw_circle([x[i], y[i]], robot_init.robot_radius, (1, 0, 0))
                plt.axis('scaled')
                plt.show()
            else:
                plt.axis('scaled')
                plt.title("No Solution")
                plt.show()
    print("Success Rate: {}/{}".format(total_case, epochs*iterations))
