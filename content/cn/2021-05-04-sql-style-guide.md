---
title: SQL 样式指南 (SQL Style Guide)
author: 范叶亮
date: '2021-05-04'
slug: sql-style-guide
categories:
  - 编程
tags:
  - SQL
  - 样式指南
  - Style Guide
  - Common Table Expressions
  - CTEs
images:
  - /images/cn/2021-05-04-sql-style-guide/wtfsm.jpg
---

代码样式指南主要用于规范项目中代码的一致性，使得代码简单、可读和易于维护，从一定程度上也影响代码的质量。一句话概括如何评价代码的质量：

> 衡量代码质量的唯一有效标准：WTF/min -- [Robert C. Martin](https://en.wikipedia.org/wiki/Robert_C._Martin)

![](/images/cn/2021-05-04-sql-style-guide/wtfsm.jpg)

Google 针对大多数编程语言（例如：C/C++，Java，JavaScript，Python，R 等）都整理了相关的[代码风格](https://google.github.io/styleguide/)，但对于 SQL 这种用于数据库查询特殊目的的编程语言并没有整理对应的风格。同其他编程语言代码风格一样，没有哪种风格是最好的，只要在项目中采用统一合理的风格即可。

本文参考的 SQL 样式指南有如下几种：

1. https://www.sqlstyle.guide/zh/
2. https://about.gitlab.com/handbook/business-technology/data-team/platform/sql-style-guide/
3. https://docs.telemetry.mozilla.org/concepts/sql_style.html
4. https://github.com/mattm/sql-style-guide

本文给出的 SQL 样式指南基于上述几种进行整理和修改。

## 一般原则

- 使用一致的、描述性名称。
- 使用空格（2 个或 4 个，项目中保持一致），避免使用 TAB 缩进。
- 在 SQL 中加入必要的注释，块注释使用 `/* */`，行注释使用 `--`，并在末尾换行。
- 使用单引号 `'` 作为被引号包裹的标识符。
- 运算符前后添加空格，逗号 `,` 后添加空格，避免行尾有空格。
- 每行代码不超过 80 个字符。

## 命名惯例

- 避免名称和保留字一样。
- 关键词、函数名称采用大写，字段名、表名采用小蛇式（lower snake case）命名。
- 名称要以字母开头，不能以下划线结尾，名称中仅可以使用字母、数字和下划线。
- 不要在名字中出现连续下划线 `__`，这样很难辨认。
- 尽量避免使用缩写词。使用时一定确定这个缩写简明易懂。
- 字段名总是使用单数。

## 对齐和换行

- 避免[川流](https://zh.wikipedia.org/wiki/川流_\(字体排印学\))式对齐代码。

    ```sql
    /* Good */
    SELECT id
    FROM table_name
    WHERE column = "test"
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT id
      FROM talbe_name
     WHERE column = "test"
    ;
    ```
    
- 多个元素组合无法呈现在一行中时，应将第一个元素另起一行。

    ```sql
    /* Good */
    SELECT
      CASE postcode
        WHEN 'BN1' THEN 'Brighton'
        WHEN 'EH1' THEN 'Edinburgh'
      END AS city
    FROM table_name
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT
      CASE postcode WHEN 'BN1' THEN 'Brighton'
                    WHEN 'EH1' THEN 'Edinburgh'
      END AS city
    FROM table_name
    ;
    ```
    
- 由括号构成的多行，结尾括号应单独一行。
    
    ```sql
    /* Good */
    SELECT id
    FROM table_name
    WHERE postcode IN (
      'looooooooooooooooooooooooong_BN1',
      'loooooooooooooooooooooooooog_EH1'
    )
    ```
    
    ```sql
    /* Bad */
    SELECT id
    FROM table_name
    WHERE postcode IN ('looooooooong_BN1',
                       'looooooooong_EH1')
    ```
    
- 多行采用右侧逗号和左侧关键字连接。

    ```sql
    /* Good */
    SELECT
      id,
      name
    FROM
      talbe_name
    WHERE
      id > 1
      AND name LIKE "%Tom%"
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT
      id
      , name
    FROM
      table_name
    WHERE
      id > 1 AND
      name LIKE "%Tom%"
    ;
    ```
    
- 根关键词建议单独一行，多个参数单独一行。

    ```sql
    /* Good */
    SELECT
      id,
      name
    FROM
      table_name
    WHERE
      id > 1
      AND name LIKE "%Tom%"
    LIMIT
      10
    ;
    ```
    
    ```sql
    /* Acceptable */
    SELECT
      id,
      name
    FROM table_name
    WHERE
      id > 1
      AND name LIKE "%Tom%"
    LIMIT 10
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT id, name
    FROM table_name
    WHERE
      id > 1
      AND name LIKE "%Tom%"
    LIMIT 10
    ;
    ```

## 明确指定

- 使用 `AS` 明确指定别名，而非隐式。

    ```sql
    /* Good */
    SELECT
      table_name_1.id AS user_id,
      table_name_2.name AS user_name
    FROM
      looooooooong_table_name_1 AS table_name_1
    LEFT JOIN
      looooooooong_table_name_2 AS table_name_2
    ON
      table_name_1.id = table_name_2.id
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT
      table_name_1.id user_id,
      table_name_2.name user_name
    FROM
      looooooooong_table_name_1 table_name_1
    LEFT JOIN
      looooooooong_table_name_2 table_name_2
    ON
      table_name_1.id = table_name_2.id
    ;
    ```
    
- 避免使用隐式关联。

    ```sql
    /* Good */
    SELECT
      table_name_1.id,
      table_name_2.name
    FROM
      table_name_1
    INNER JOIN
      table_name_2
    ON
      table_name_1.id = table_name_2.id
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT
      table_name_1.id,
      table_name_2.name
    FROM
      table_name_1,
      table_name_2
    ON
      table_name_1.id = table_name_2.id
    ;
    ```
    
- 明确关联类型。

    ```sql
    /* Good */
    SELECT
      table_name_1.id,
      table_name_2.name
    FROM
      table_name_1
    INNER JOIN
      table_name_2
    ON
      table_name_1.id = table_name_2.id
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT
      table_name_1.id,
      table_name_2.name
    FROM
      table_name_1
    JOIN
      table_name_2
    ON
      table_name_1.id = table_name_2.id
    ;
    ```
    
- 明确指定分组列。

    ```sql
    /* Good */
    SELECT
      submission_date,
      normalized_channel IN ('nightly', 'aurora', 'beta') AS is_prerelease,
      COUNT(*) AS count
    FROM
      telemetry.clients_daily
    WHERE
      submission_date > '2019-07-01'
    GROUP BY
      submission_date,
      is_prerelease
    ;
    ```
    
    ```sql
    /* Bad */
    SELECT
      submission_date,
      normalized_channel IN ('nightly', 'aurora', 'beta') AS is_prerelease,
      COUNT(*) AS count
    FROM
      telemetry.clients_daily
    WHERE
      submission_date > '2019-07-01'
    GROUP BY
      1, 2
    ;
    ```

## 子查询

- 尽量使用 [Common Table Expressions (CTEs)](https://en.wikipedia.org/wiki/Hierarchical_and_recursive_queries_in_SQL#Common_table_expression) 而非子查询。

    ```sql
    /* Good */
    WITH sample AS (
      SELECT
        client_id,
        submission_date
      FROM
        main_summary
      WHERE
        sample_id = '42'
    )
    
    SELECT *
    FROM sample
    LIMIT 10
    ```
    
    ```sql
    /* Bad */
    SELECT *
    FROM (
      SELECT
        client_id,
        submission_date
      FROM
        main_summary
      WHERE
        sample_id = '42'
    )
    LIMIT 10
    ```
    
- 尽量在 CTEs 中处理查询而非主语句中。

    ```sql
    /* Good */
    WITH backings_per_category AS (
      SELECT
        ...
    ), backers AS (
      SELECT
        backings_per_category.backer_id,
        COUNT(backings_per_category.id) AS projects_backed_per_category
      INNER JOIN ksr.users AS users ON users.id = backings_per_category.backer_id
      GROUP BY backings_per_category.backer_id
    ), backers_and_creators AS (
      ...
    )
    SELECT * FROM backers_and_creators;
    ```
    
    ```sql
    /* Bad */
    WITH backings_per_category AS (
      SELECT
        ...
    ), backers AS (
      SELECT
        backer_id,
        COUNT(backings_per_category.id) AS projects_backed_per_category
    ), backers_and_creators AS (
      ...
    )
    SELECT *
    FROM backers_and_creators
    INNER JOIN backers
    ON backers_and_creators
    ON backers.backer_id = backers_and_creators.backer_id
    ```

## 其他

- 尽量使用 `!=` 而不是 `<>` 表示不等于。
- 尽量使用 `BETWEEN` 而不是多个 `AND` 语句。
- 尽量使用 `IN()` 而不是多个 `OR` 语句。
- 尽量避免使用 `SELECT *`。
- 尽量避免使用无意义的别名，例如：`a, b, c`。
