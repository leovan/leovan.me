# Load library
library(tidyverse)
library(reshape2)
library(gridExtra)

# Ising model
each_round <- function(current_matrix, ising_config) {
    n_row <- nrow(current_matrix)
    n_col <- ncol(current_matrix)
    
    for (i in 1:n_row) {
        for (j in 1:n_col) {
            current_row <- sample(1:n_row, 1)
            current_col <- sample(1:n_col, 1)
            s <- current_matrix[current_row, current_col]
            e <- -(current_matrix[(current_row-1-1)%%n_row+1, current_col] +
                       current_matrix[current_row, (current_col-1-1)%%n_col+1] +
                       current_matrix[(current_row+1-1)%%n_row+1, current_col] +
                       current_matrix[current_row, (current_col+1-1)%%n_col+1]) *
                s * ising_config$j
            mu <- min(exp((e + e) / (ising_config$k * ising_config$t)), 1)
            mu_random <- runif(1)
            
            if (mu_random < mu) {
                s <- -1 * s
            }
            
            current_matrix[current_row, current_col] <- s
        }
    }
    
    current_matrix
}

ising_simulation <- function(N, iter, ising_config, saved_steps) {
    set.seed(112358)
    current_matrix <- matrix(sample(0:1, N^2, replace = T), N, N)*2-1
    saved_matrix <- list()
    
    if (0 %in% saved_steps) {
        saved_matrix <- c(saved_matrix, list(current_matrix))
    }
    
    for (i in 1:iter) {
        if (i %in% saved_steps) {
            saved_matrix <- c(saved_matrix, list(current_matrix))
        }
        
        current_matrix <- each_round(current_matrix, ising_config)
        
        if (i %% 1000 == 0) {
            cat(paste0("Steps: ", i, '\n'))
        }
    }
    
    saved_matrix
}

ising_plot <- function(current_matrix, title) {
    df <- melt(current_matrix, varnames=c('x', 'y'), value.name='v')
    p <- ggplot(df) +
        geom_tile(aes(x, y, fill = as.factor(v)), show.legend = F) +
        coord_fixed() + theme_void() + ggtitle(title) +
        theme(plot.title = element_text(hjust = 0.5))
}

ising_config <- list(j = 1, k = 1, t = 4)
diff_steps_matrix <- ising_simulation(100, 5000, ising_config,
                                      c(0, 1, 5, 50, 500, 5000))

diff_steps_p <- arrangeGrob(
    ising_plot(diff_steps_matrix[[1]], 'Steps = 0'),
    ising_plot(diff_steps_matrix[[2]], 'Steps = 1'),
    ising_plot(diff_steps_matrix[[3]], 'Steps = 5'),
    ising_plot(diff_steps_matrix[[4]], 'Steps = 50'),
    ising_plot(diff_steps_matrix[[5]], 'Steps = 500'),
    ising_plot(diff_steps_matrix[[6]], 'Steps = 5000'),
    ncol = 3, nrow = 2)
ggsave('../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/ising-different-steps.png',
       diff_steps_p, device = 'png',
       width = 9, height = 6, units = 'cm',
       dpi = 150, scale = 2)

ising_config_t <- c(1, 2, 2.27, 2.5, 3, 6)
diff_t_matrix <- lapply(ising_config_t, function(t) {
    ising_config <- list(j = 1, k = 1, t = t)
    ising_simulation(100, 50, ising_config, c(50))
})

diff_t_p <- arrangeGrob(
    ising_plot(diff_t_matrix[[1]], 'T = 1 [J/K]'),
    ising_plot(diff_t_matrix[[2]], 'T = 2 [J/K]'),
    ising_plot(diff_t_matrix[[3]], 'T = 2.27 [J/K]'),
    ising_plot(diff_t_matrix[[4]], 'T = 2.5 [J/K]'),
    ising_plot(diff_t_matrix[[5]], 'T = 3 [J/K]'),
    ising_plot(diff_t_matrix[[6]], 'T = 6 [J/K]'),
    ncol = 3, nrow = 2)
ggsave('../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/ising-different-t.png',
       diff_t_p, device = 'png',
       width = 9, height = 6, units = 'cm',
       dpi = 150, scale = 2)

# Hopfield

## DHNN
library(EBImage)

digits <- lapply(0:9, function(num) {
    readImage(paste0('../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/', num, '.png'))
})

digits_combine <- combine(digits)
png(filename = '../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/digits.png',
    width = 6, height = 0.5, units = 'cm', res = 150)
old_par <- par()
par(mar = c(1, 1, 1, 1))
display(digits_combine, method = 'raster', all = T, spacing = 10, nx = 10)
par(old_par)
dev.off()

#' 训练 Hopfield 网络
#'
#' @param n 网络节点个数
#' @param pattern_list 模式列表
#' @return 训练好的 Hopfield 网络
train_hopfield <- function(n, pattern_list) {
    weights <- matrix(rep(0, n*n), n, n)
    n_patterns <- length(pattern_list)

    for (i in 1:n_patterns) {
        weights <- weights + pattern_list[[i]] %o% pattern_list[[i]]
    }
    diag(weights) <- 0
    weights <- weights / n_patterns

    list(weights = weights, n = n)
}

#' 运行 Hopfiled 网络
#' @param hopfield_network 训练好的 Hopfield 网络
#' @param pattern 输入的模式
#' @param max_iter 最大迭代次数
#' @param save_history 是否保存状态变化历史
#' @return 最终的模式 (以及历史模式)
run_hopfield <- function(hopfield_network, pattern,
                         max_iter = 100, save_history = T) {
    last_pattern <- pattern
    history_patterns <- list()

    for (iter in 1:max_iter) {
        current_pattern <- last_pattern

        i <- round(runif(1, 1, hopfield_network$n))
        net_i <- hopfield_network$weights[i, ] %*% current_pattern
        current_pattern[i] <- ifelse(net_i < 0, -1, 1)

        if (save_history) {
            history_patterns[[iter]] <- last_pattern
        }

        last_pattern <- current_pattern
    }

    list(history_patterns = history_patterns,
         final_pattern = last_pattern)
}

# 载入数据
library(EBImage)
digits <- lapply(0:9, function(num) {
    readImage(paste0('../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/',
                     num, '.png'))
})

# 转换图像为 16*16 的一维向量
# 将 (0, 1) 转换为 (-1, 1)
digits_patterns <- lapply(digits, function(digit) {
    pixels <- c(digit)
    pixels * 2 - 1
})

# 训练 Hopfield 网络
digits_hopfield_network <- train_hopfield(16*16, digits_patterns)

# 构造测试数据
digits_test_remove_right <- lapply(0:9, function(num) {
    digit_test <- digits[[num+1]]
    digit_test[12:16, ] <- 1
    digit_test
})
digits_test_remove_bottom <- lapply(0:9, function(num) {
    digit_test <- digits[[num+1]]
    digit_test[, 12:16] <- 1
    digit_test
})
digits_test <- c(digits_test_remove_right, digits_test_remove_bottom)

digits_test_combine <- combine(digits_test)
png(filename = '../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/digits-test.png',
    width = 6, height = 1, units = 'cm', res = 150)
old_par <- par()
par(mar = c(1, 1, 1, 1))
display(digits_test_combine, method = 'raster', all = T, spacing = 10, nx = 10)
par(old_par)
dev.off()

# 转换图像为 16*16 的一维向量
# 将 (0, 1) 转换为 (-1, 1)
digits_test_patterns <- lapply(digits_test, function(digit) {
    pixels <- c(digit)
    pixels * 2 - 1
})

# 运行 Hopfield 网络，获取测试数据结果
digits_test_results_patterns <- lapply(digits_test_patterns,
                                       function(pattern) {
    run_hopfield(digits_hopfield_network, pattern, max_iter = 300)
})

# 转换测试数据结果为图片
digits_test_results <- lapply(digits_test_results_patterns,
                              function(result) {
    each_dim <- sqrt(digits_hopfield_network$n)
    Image((result$final_pattern + 1) / 2,
          dim = c(each_dim, each_dim),
          colormode = 'Grayscale')
})

digits_test_results_combine <- combine(digits_test_results)
png(filename = '../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/digits-test-results.png',
    width = 6, height = 1, units = 'cm', res = 150)
old_par <- par()
par(mar = c(1, 1, 1, 1))
display(digits_test_results_combine, method = 'raster', all = T, spacing = 10, nx = 10)
par(old_par)
dev.off()

# 变换动画
library(animation)

saveGIF({
    ani.options(nmax = 300)
    steps <- 10
    for (i in seq(steps, 300, by = steps)) {
        digits_test_results <- lapply(digits_test_results_patterns, function(result) {
            each_dim <- sqrt(digits_hopfield_network$n)
            Image((result$history_patterns[[i]] + 1) / 2,
                  dim = c(each_dim, each_dim),
                  colormode = 'Grayscale')
        })

        digits_test_results_combine <- combine(digits_test_results)
        display(digits_test_results_combine, method = 'raster',
                all = T, spacing = 10, nx = 10)

        ani.pause()
    }
}, interval = 0.001, movie.name = 'digits-test-results.gif',
ani.width = 354, ani.height = 59)

## CHNN

# 城市座标
cities <- data.frame(
    l = LETTERS[1:10],
    x = c(0.4000, 0.2439, 0.1707, 0.2293, 0.5171,
          0.8732, 0.6878, 0.8488, 0.6683, 0.6195),
    y = c(0.4439, 0.1463, 0.2293, 0.7610, 0.9414,
          0.6536, 0.5219, 0.3609, 0.2536, 0.2634)
)

# 通过城市座标构建距离矩阵
distance_matrix <- function(points) {
    n <- nrow(points)
    d <- matrix(rep(0, n^2), n, n)

    for (i in 1:n) {
        for (j in i:n) {
            distance <- sqrt((points[i, ]$x - points[j, ]$x)^2 +
                                 (points[i, ]$y - points[j, ]$y)^2)
            d[i, j] <- distance
            d[j, i] <- distance
        }
    }

    d
}

# 结果约束校验
check_path_valid <- function(v, n) {
    # 城市约束
    c1 <- 0
    for (x in 1:n) {
        for (i in 1:(n-1)) {
            for (j in (i+1):n) {
                c1 <- c1 + v[x, i] * v[x, j]
            }
        }
    }

    # 时间约束
    c2 <- 0
    for (i in 1:n) {
        for (x in 1:(n-1)) {
            for (y in (x+1):n) {
                c2 <- c2 + v[x, i] * v[y, i]
            }
        }
    }

    # 有效性约束
    c3 <- sum(v)

    ifelse(c1 == 0 & c2 == 0 & c3 == n, T, F)
}

# 根据结果矩阵获取路径
v_to_path <- function(v, n) {
    p <- c()

    for (i in 1:n) {
        for (x in 1:n) {
            if (v[x, i] == 1) {
                p <- c(p, x)
                break
            }
        }
    }

    p
}

# 计算结果矩阵的路径长度
path_distance <- function(v, n, d) {
    p <- v_to_path(v, n)
    p <- c(p, p[1])
    distance <- 0
    for (i in 1:(length(p)-1)) {
        distance <- distance + d[p[i], p[i+1]]
    }

    distance
}

# 构建 Hopfield 网络
tsp_chnn <- function(d, n, gamma = 0.02, alpha = 0.0001,
                     theta = 0.7, tau = 1,
                     A = 500, B = 500, C = 1000, D = 500,
                     max_iter = 1000) {
    v <- matrix(runif(n^2), n, n)
    u <- matrix(rep(1, n^2), n, n) * (-gamma * log(n-1) / 2)
    du <- matrix(rep(0, n^2), n, n)

    for (iter in 1:max_iter) {
        for (x in 1:n) {
            for (i in 1:n) {
                # E1
                e1 <- 0
                for (j in 1:n) {
                    if (j != i) {
                        e1 <- e1 + v[x, j]
                    }
                }
                e1 <- -A * e1

                # E2
                e2 <- 0
                for (y in 1:n) {
                    if (y != x) {
                        e2 <- e2 + v[y, i]
                    }
                }
                e2 <- -B * e2

                # E3
                e3 <- -C * (sum(v) - n)

                # E4
                e4 <- 0
                for (y in 1:n) {
                    if (y != x) {
                        e4 <- e4 + d[x, y] *
                            (v[y, (i+1-1)%%n+1] + v[y, (i-1-1)%%n+1])
                    }
                }
                e4 <- -D * e4

                du[x, i] <- e1 + e2 + e3 + e4 - u[x, i] / tau
            }
        }

        u <- u + alpha * du
        v <- (1 + tanh(u / gamma)) / 2
        v <- ifelse(v >= theta, 1, 0)
    }

    v
}

# 利用 Hopfiled 网络求解 TSP 问题
set.seed(112358)

n <- 10
d <- distance_matrix(cities)

# 模拟 100 次并获取最终结果
tsp_solutions <- lapply(1:100, function(round) {
    v <- tsp_chnn(d, n)
    valid <- check_path_valid(v, n)
    distance <- ifelse(valid, path_distance(v, n, d), NA)

    list(round = round, valid = valid,
         distance = distance, v = v)
})

# 获取最优结果
best_tsp_solution <- NA
for (tsp_solution in tsp_solutions) {
    if (tsp_solution$valid) {
        if (!is.na(best_tsp_solution)) {
            if (tsp_solution$distance < best_tsp_solution$distance) {
                best_tsp_solution <- tsp_solution
            }
        } else {
            best_tsp_solution <- tsp_solution
        }
    }
}

# 可视化最优结果
best_tsp_solution_path <- v_to_path(best_tsp_solution$v, n)
ordered_cities <- cities[best_tsp_solution_path, ] %>%
    mutate(ord = seq(1:10))

best_tsp_solution_path_p <- ggplot(ordered_cities) +
    geom_polygon(aes(x, y), color = 'black', fill = NA) +
    geom_point(aes(x, y)) +
    geom_text(aes(x, y, label = l), vjust = -1) +
    geom_text(aes(x, y, label = ord), vjust = 2) +
    coord_fixed() + ylim(c(0, 1)) + xlim(c(0, 1)) +
    theme(axis.title = element_blank())
ggsave('../../static/images/cn/2017-12-25-ising-hopfield-and-rbm/tsp-best-solution-path.png',
       best_tsp_solution_path_p, device = 'png',
       width = 4, height = 4, units = 'cm',
       dpi = 150, scale = 2)
