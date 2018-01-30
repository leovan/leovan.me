# -*- coding: UTF-8 -*-

# %%
from pylab import *
rc('text', usetex = True)
rc('font', family = 'serif')

# %%
# Inner product and projection
dpi = 100
fig_width = 300
fig_height = 300

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

annotate(r'$A$',
         xy = (1, 2), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)
annotate(r'$B$',
         xy = (2, 1), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)
annotate(r'$O$',
         xy = (0, 0), xycoords = 'data',
         xytext = (-20, -20), textcoords = 'offset points', fontsize = 12)
annotate(r'$C$',
         xy = (8/5, 4/5), xycoords = 'data',
         xytext = (10, -20), textcoords = 'offset points', fontsize = 12)
annotate(r'$\theta$',
         xy = (0, 0), xycoords = 'data',
         xytext = (10, 10), textcoords = 'offset points', fontsize = 12)

plot([1, 8/5], [2, 4/5], color = 'g', linestyle = '--')
arrow(0, 0, 1, 2,
      head_width = 0.1, length_includes_head = True,
      fc = 'b', ec = 'b', overhang = 0.3)
arrow(0, 0, 2, 1,
      head_width = 0.1, length_includes_head = True,
      fc = 'b', ec = 'b', overhang = 0.3)
plot([1, 2, 8/5], [2, 1, 4/5], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
yticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
xlim(-0.5, 2.5)
ylim(-0.5, 2.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-inner-product-and-projection.png', dpi = dpi)

# %%
# Bases
dpi = 100
fig_width = 300
fig_height = 200

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

arrow(0, 0, 3, 2,
      head_width = 0.1, length_includes_head = True,
      fc = 'b', ec = 'b', overhang = 0.3)
plot([0, 3], [2, 2], color = 'g', linestyle='--')
plot([3, 3], [0, 2], color = 'g', linestyle='--')
arrow(0, 0, 0, 1,
      head_width = 0.1, length_includes_head = True,
      fc = 'r', ec = 'r', overhang = 0.3)
arrow(0, 0, 1, 0,
      head_width = 0.1, length_includes_head = True,
      fc = 'r', ec = 'r', overhang = 0.3)
plot([3], [2], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([0, 1, 2, 3], [r'$0$', r'$1$', r'$2$', r'$3$'])
yticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
xlim(-0.5, 3.5)
ylim(-0.5, 2.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-bases.png', dpi = dpi)

# %%
# Change of bases
dpi = 100
fig_width = 400
fig_height = 400

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

plot([-1, 3], [-1, 3], color = 'r', linestyle='-')
plot([-1, 1], [1, -1], color = 'r', linestyle='-')
plot([2.5, 3], [2.5, 2], color = 'g', linestyle='--')
plot([0.5, 3], [-0.5, 2], color = 'g', linestyle='--')
arrow(0, 0, 3, 2,
      head_width = 0.1, length_includes_head = True,
      fc = 'b', ec = 'b', overhang = 0.3)
arrow(0, 0, 1/sqrt(2), 1/sqrt(2),
      head_width = 0.1, length_includes_head = True, width = 0.03,
      fc = 'r', ec = 'r', overhang = 0.3)
arrow(0, 0, -1/sqrt(2), 1/sqrt(2),
      head_width = 0.1, length_includes_head = True, width = 0.03,
      fc = 'r', ec = 'r', overhang = 0.3)
plot([3], [2], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([-1, 0, 1, 2, 3], [r'$-1$', r'$0$', r'$1$', r'$2$', r'$3$'])
yticks([-1, 0, 1, 2, 3], [r'$-1$', r'$0$', r'$1$', r'$2$', r'$3$'])
xlim(-1.5, 3.5)
ylim(-1.5, 3.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-change-of-bases.png', dpi = dpi)

# %%
# Points projection in changed bases
dpi = 100
fig_width = 400
fig_height = 400

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

plot([-1, -1, 0, 0, 2], [-2, 0, 0, 1, 1], 'o', color = 'k')
plot([-2, 2], [-2, 2], color = 'r', linestyle = '-')
arrow(0, 0, 1/sqrt(2), 1/sqrt(2),
      head_width = 0.1, length_includes_head = True, width = 0.03,
      fc = 'r', ec = 'r', overhang = 0.3)
plot([-1, -1.5], [-2, -1.5], color = 'g', linestyle = '--')
plot([-1, -0.5], [0, -0.5], color = 'g', linestyle = '--')
plot([0, 0.5], [1, 0.5], color = 'g', linestyle = '--')
plot([2, 1.5], [1, 1.5], color = 'g', linestyle = '--')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([-2, -1, 0, 1, 2], [r'$-2$', r'$-1$', r'$0$', r'$1$', r'$2$'])
yticks([-2, -1, 0, 1, 2], [r'$-2$', r'$-1$', r'$0$', r'$1$', r'$2$'])
xlim(-2.5, 2.5)
ylim(-2.5, 2.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/pca-projection.png', dpi = dpi)

# Vector linear transformation

# %%
dpi = 100
fig_width = 200
fig_height = 200

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

annotate(r'$x$',
         xy = (2, 1), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)
annotate(r"$x'$",
         xy = (2, -1), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)

plot([2, 2], [1, -1], color = 'g', linestyle = '--')
plot([2, 2], [1, -1], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
yticks([-1, 0, 1,], [r'$-1$', r'$0$', r'$1$'])
xlim(-0.5, 2.5)
ylim(-1.5, 1.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-linear-transformation-1.png', dpi = dpi)
# %%
dpi = 100
fig_width = 200
fig_height = 200

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

annotate(r'$x$',
         xy = (2, 1), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)
annotate(r"$x'$",
         xy = (1, 2), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)

plot([0, 2], [0, 2], color = 'b', linestyle = '-')
plot([2, 1], [1, 2], color = 'g', linestyle = '--')
plot([2, 1], [1, 2], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
yticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
xlim(-0.5, 2.5)
ylim(-0.5, 2.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-linear-transformation-2.png', dpi = dpi)
# %%
dpi = 100
fig_width = 200
fig_height = 200

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

annotate(r'$x$',
         xy = (1, 1), xycoords = 'data',
         xytext = (-10, +10), textcoords = 'offset points', fontsize = 12)
annotate(r"$x'$",
         xy = (2, 2), xycoords = 'data',
         xytext = (+10, -20), textcoords = 'offset points', fontsize = 12)

plot([0, 2], [0, 2], color = 'b', linestyle = '-')
plot([1, 2], [1, 2], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
yticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
xlim(-0.5, 2.5)
ylim(-0.5, 2.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-linear-transformation-3.png', dpi = dpi)
# %%
dpi = 100
fig_width = 200
fig_height = 200

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

annotate(r'$x$',
         xy = (2, 1), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)
annotate(r"$x'$",
         xy = (1, 2), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)
annotate(r'$\theta$',
         xy = (0, 0), xycoords = 'data',
         xytext = (+10, +10), textcoords = 'offset points', fontsize = 12)

plot([0, 1], [0, 2], color = 'b', linestyle = '-')
plot([0, 2], [0, 1], color = 'b', linestyle = '-')
plot([2, 1], [1, 2], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
yticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
xlim(-0.5, 2.5)
ylim(-0.5, 2.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-linear-transformation-4.png', dpi = dpi)
# %%
dpi = 100
fig_width = 200
fig_height = 200

figure(figsize = (fig_width/dpi, fig_height/dpi), dpi = dpi)

annotate(r'$x$',
         xy = (2, 2), xycoords = 'data',
         xytext = (-20, -10), textcoords = 'offset points', fontsize = 12)
annotate(r"$x'$",
         xy = (2, 0), xycoords = 'data',
         xytext = (-20, +10), textcoords = 'offset points', fontsize = 12)

plot([2, 2], [0, 2], color = 'g', linestyle = '--')
plot([2, 2], [0, 2], 'o', color = 'k')

ax = gca()

ax.set_aspect(1)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

xticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
yticks([0, 1, 2], [r'$0$', r'$1$', r'$2$'])
xlim(-0.5, 2.5)
ylim(-0.5, 2.5)

savefig('../../static/images/cn/2017-12-11-evd-svd-and-pca/vector-linear-transformation-5.png', dpi = dpi)
