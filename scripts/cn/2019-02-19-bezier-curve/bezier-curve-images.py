# -*- coding: UTF-8 -*-

# %%
import numpy as np
import matplotlib.pyplot as plt

from typing import List
from scipy.special import comb
from matplotlib import animation

# %%
color_red = '#F07769'
color_blue = '#6C9BFF'
color_green = '#34BA27'
color_pupple = '#9933FF'
color_black = '#000000'
color_gray = '#DDDDDD'

plt.rc('text', usetex = True)
plt.rc('font', family = 'serif')

# %%
def get_bezier_curve(points: List[List[float]], t: float) -> List[float]:
    count = len(points)
    dims = np.shape(points)[1]
    b_t = [0.0] * dims

    for idx in range(count):
        for dim in range(dims):
            b_t[dim] += t**idx * (1 - t)**(count - 1 - idx) * points[idx][dim] * comb(count - 1, idx)

    return b_t

# %%
def get_center_point(point1: List[float], point2: List[float], t: float) -> List[float]:
    dims = len(point1)
    center_t = [0.0] * dims

    for dim in range(dims):
        center_t[dim] = point1[dim] * (1 - t) + point2[dim] * t

    return center_t

# %%
def get_min_max_values(p_points: List[List[float]]):
    _, dims = np.shape(p_points)
    assert dims == 2

    min_x = np.min([p_point[0] for p_point in p_points])
    max_x = np.max([p_point[0] for p_point in p_points])
    min_y = np.min([p_point[1] for p_point in p_points])
    max_y = np.max([p_point[1] for p_point in p_points])

    return min_x, max_x, min_y, max_y

# %%
def gen_cavans(p_points: List[List[float]], figure_max_width=3, figure_max_height=1.5, dpi=100):
    min_x, max_x, min_y, max_y = get_min_max_values(p_points)

    x_scale = (max_x - min_x) / figure_max_width
    y_scale = (max_y - min_y) / figure_max_height
    max_scale = max(x_scale, y_scale)

    fig_width = (max_x - min_x) / max_scale
    fig_height = (max_y - min_y) / max_scale

    return plt.figure(figsize=(fig_width, fig_height), dpi=dpi)

# %%
def cavans_init(fig, p_points: List[List[float]]):
    min_x, max_x, min_y, max_y = get_min_max_values(p_points)
    
    plt.axis('off')
    plt.xlim(min_x - 0.5, max_x + 0.5)
    plt.ylim(min_y - 0.5, max_y + 0.5)

# %%
def plot_reference_lines(
    fig, points: List[List[float]], points_anno_positions: List[List[float]],
    anno_text='P', point_color=color_black, line_color=color_gray, line_width=1):
    count, dims = np.shape(points)
    assert dims == 2

    for idx in range(count - 1):
        plt.plot(
            [points[idx][0], points[idx+1][0]], [points[idx][1], points[idx+1][1]],
            color=line_color, linestyle='-', linewidth=line_width)
    
    for idx in range(count):
        plt.plot(points[idx][0], points[idx][1], marker='.', color=point_color)
        plt.annotate(
            r'${anno_text}_{idx}$'.format(anno_text=anno_text, idx=idx),
            xy=(points[idx][0], points[idx][1]), xycoords='data',
            xytext=(points_anno_positions[idx][0], points_anno_positions[idx][1]),
            textcoords='offset points')

# %%
def plot_bezier_curve(
    fig, p_points: List[List[float]], t: float, draw_curve='current', t_window=0.01):
    min_x, max_x, min_y, max_y = get_min_max_values(p_points)

    # bezier curve
    if draw_curve.lower() == 'current':
        t_stop = t
    elif draw_curve.lower() == 'full':
        t_stop = 1.0
    else:
        raise ValueError('Unsupprted draw_curve value [{draw_curve}]'.format(draw_curve=draw_curve))

    ts = [idx * t_window for idx in range(int(np.ceil(t_stop / t_window) + 1))]
    t_idx = int(np.ceil(t / t_window))
    bc_points = [get_bezier_curve(p_points, t) for t in ts]
    bc_points_x = [bc_point[0] for bc_point in bc_points]
    bc_points_y = [bc_point[1] for bc_point in bc_points]

    plt.plot(bc_points_x, bc_points_y, color=color_pupple, linestyle='-', linewidth=2)

    # bezier curve point
    plt.plot(bc_points_x[t_idx], bc_points_y[t_idx], marker='.', color=color_black)
    plt.annotate(
        r'$B$', xy=(bc_points_x[t_idx], bc_points_y[t_idx]), xycoords='data',
        xytext=(6, 0), textcoords='offset points')

    # other annotations
    plt.annotate(
        r'$t={t:.2f}$'.format(t=t), xy=(max_x, max_y), xycoords='data',
        xytext=(-18, 0), textcoords='offset points')

# %%
def plot_1st_powers_bezier_curve(
    fig, p_points: List[List[float]], t: float, draw_curve='current', t_window=0.01):
    count, dims = np.shape(p_points)
    assert count == 2
    assert dims == 2

    # reference lines
    p_points_anno_positions = [[6, 0], [6, -6]]
    plot_reference_lines(fig, p_points, p_points_anno_positions, anno_text='P', line_width=2)

    # bezier curve
    plot_bezier_curve(fig, p_points, t, draw_curve=draw_curve ,t_window=t_window)

# %%
p_points = [[4, 6], [10, 0]]
fig = gen_cavans(p_points)
cavans_init(fig, p_points)
plot_1st_powers_bezier_curve(fig, p_points, t=0.25, draw_curve='full')
plt.savefig('1st-power-bezier-curve.png')

# %%
def plot_1st_powers_bezier_curve_animation(
    p_points: List[List[float]], t_window=0.01, dpi=100):
    fig = gen_cavans(p_points, dpi=dpi)

    def plot_1st_powers_bezier_curve_frame(frame, frames):
        t = frame / frames
        fig.clear()
        cavans_init(fig, p_points)
        plot_1st_powers_bezier_curve(fig, p_points, t, t_window=t_window)

        return fig

    return animation.FuncAnimation(fig, plot_1st_powers_bezier_curve_frame, frames=100, fargs=[100])

# %%
p_points = [[4, 6], [10, 0]]
anim = plot_1st_powers_bezier_curve_animation(p_points)
anim.save('1st-power-bezier-curve.gif', writer='imagemagick', fps=30)


# %%
def plot_2nd_powers_bezier_curve(
    fig, p_points: List[List[float]], t: float, draw_curve='current', t_window=0.01):
    count, dims = np.shape(p_points)
    assert count == 3
    assert dims == 2

    # reference lines
    p_points_anno_positions = [[6, -6], [6, 0], [6, -6]]
    plot_reference_lines(fig, p_points, p_points_anno_positions, anno_text='P', line_width=2)

    q_points = [get_center_point(p_points[idx], p_points[idx+1], t) for idx in range(len(p_points) - 1)]
    q_points_anno_positions = [[-18, 0], [6, 0]]
    plot_reference_lines(fig, q_points, q_points_anno_positions, anno_text='Q', point_color=color_red, line_color=color_red)

    # bezier curve
    plot_bezier_curve(fig, p_points, t, draw_curve=draw_curve ,t_window=t_window)

# %%
p_points = [[0, 0], [4, 6], [10, 0]]
fig = gen_cavans(p_points)
cavans_init(fig, p_points)
plot_2nd_powers_bezier_curve(fig, p_points, t=0.25, draw_curve='full')
plt.savefig('2nd-power-bezier-curve.png')

# %%
def plot_2nd_powers_bezier_curve_animation(
    p_points: List[List[float]], t_window=0.01, dpi=100):
    fig = gen_cavans(p_points, dpi=dpi)

    def plot_2nd_powers_bezier_curve_frame(frame, frames):
        t = frame / frames
        fig.clear()
        cavans_init(fig, p_points)
        plot_2nd_powers_bezier_curve(fig, p_points, t, t_window=t_window)

        return fig

    return animation.FuncAnimation(fig, plot_2nd_powers_bezier_curve_frame, frames=100, fargs=[100])

# %%
p_points = [[0, 0], [4, 6], [10, 0]]
anim = plot_2nd_powers_bezier_curve_animation(p_points)
anim.save('2nd-power-bezier-curve.gif', writer='imagemagick', fps=30)

# %%
def plot_3rd_powers_bezier_curve(
    fig, p_points: List[List[float]], t: float, draw_curve='current', t_window=0.01):
    count, dims = np.shape(p_points)
    assert count == 4
    assert dims == 2

    # reference lines
    p_points_anno_positions = [[-18, -6], [-18, 0], [6, 0], [6, -6]]
    plot_reference_lines(fig, p_points, p_points_anno_positions, anno_text='P', line_width=2)

    q_points = [get_center_point(p_points[idx], p_points[idx+1], t) for idx in range(len(p_points) - 1)]
    q_points_anno_positions = [[-18, -6], [-9, 6], [6, -6]]
    plot_reference_lines(fig, q_points, q_points_anno_positions, anno_text='Q', point_color=color_red, line_color=color_red)

    r_points = [get_center_point(q_points[idx], q_points[idx+1], t) for idx in range(len(q_points) - 1)]
    r_points_anno_positions = [[-18, -6], [6, -6]]
    plot_reference_lines(fig, r_points, r_points_anno_positions, anno_text='R', point_color=color_green, line_color=color_green)

    # bezier curve
    plot_bezier_curve(fig, p_points, t, draw_curve=draw_curve ,t_window=t_window)

# %%
p_points = [[0, 0], [-1, 6], [6, 6], [12, 0]]
fig = gen_cavans(p_points)
cavans_init(fig, p_points)
plot_3rd_powers_bezier_curve(fig, p_points, t=0.25, draw_curve='full')
plt.savefig('3rd-power-bezier-curve.png')

# %%
def plot_3rd_powers_bezier_curve_animation(
    p_points: List[List[float]], t_window=0.01, dpi=100):
    fig = gen_cavans(p_points, dpi=dpi)

    def plot_3rd_powers_bezier_curve_frame(frame, frames):
        t = frame / frames
        fig.clear()
        cavans_init(fig, p_points)
        plot_3rd_powers_bezier_curve(fig, p_points, t, t_window=t_window)

        return fig

    return animation.FuncAnimation(fig, plot_3rd_powers_bezier_curve_frame, frames=100, fargs=[100])

# %%
p_points = [[0, 0], [-1, 6], [6, 6], [12, 0]]
anim = plot_3rd_powers_bezier_curve_animation(p_points)
anim.save('3rd-power-bezier-curve.gif', writer='imagemagick', fps=30)

# %%
def plot_4th_powers_bezier_curve(
    fig, p_points: List[List[float]], t: float, draw_curve='current', t_window=0.01):
    count, dims = np.shape(p_points)
    assert count == 5
    assert dims == 2

    # reference lines
    p_points_anno_positions = [[-18, -6], [-18, 0], [6, 0], [6, -6], [6, 0]]
    plot_reference_lines(fig, p_points, p_points_anno_positions, anno_text='P', line_width=2)

    q_points = [get_center_point(p_points[idx], p_points[idx+1], t) for idx in range(len(p_points) - 1)]
    q_points_anno_positions = [[-18, -6], [-18, 0], [6, 0], [6, -6]]
    plot_reference_lines(fig, q_points, q_points_anno_positions, anno_text='Q', point_color=color_red, line_color=color_red)

    r_points = [get_center_point(q_points[idx], q_points[idx+1], t) for idx in range(len(q_points) - 1)]
    r_points_anno_positions = [[-18, -6], [-9, 6], [6, -6]]
    plot_reference_lines(fig, r_points, r_points_anno_positions, anno_text='R', point_color=color_green, line_color=color_green)

    s_points = [get_center_point(r_points[idx], r_points[idx+1], t) for idx in range(len(r_points) - 1)]
    s_points_anno_positions = [[-18, 0], [6, -6]]
    plot_reference_lines(fig, s_points, s_points_anno_positions, anno_text='S', point_color=color_blue, line_color=color_blue)

    # bezier curve
    plot_bezier_curve(fig, p_points, t, draw_curve=draw_curve ,t_window=t_window)

# %%
p_points = [[0, 0], [-1, 6], [6, 6], [9, 0], [12, 4]]
fig = gen_cavans(p_points)
cavans_init(fig, p_points)
plot_4th_powers_bezier_curve(fig, p_points, t=0.25, draw_curve='full')
plt.savefig('4th-power-bezier-curve.png')

# %%
def plot_4th_powers_bezier_curve_animation(
    p_points: List[List[float]], t_window=0.01, dpi=100):
    fig = gen_cavans(p_points, dpi=dpi)

    def plot_4th_powers_bezier_curve_frame(frame, frames):
        t = frame / frames
        fig.clear()
        cavans_init(fig, p_points)
        plot_4th_powers_bezier_curve(fig, p_points, t, t_window=t_window)

        return fig

    return animation.FuncAnimation(fig, plot_4th_powers_bezier_curve_frame, frames=100, fargs=[100])

# %%
p_points = [[0, 0], [-1, 6], [6, 6], [9, 0], [12, 4]]
anim = plot_4th_powers_bezier_curve_animation(p_points)
anim.save('4th-power-bezier-curve.gif', writer='imagemagick', fps=30)
