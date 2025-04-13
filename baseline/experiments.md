# Эксперименты

В данном файле представлены метрики всех экспериментов в процессе создания `baseline`  \
Лучшая модель, ее описание, а так же выводы представлены в файле `baseline.md`

## Описание
**Предобработка данных**:
   - OneHot для категориальных
   - StandardScaler() для числовых

**Подбор гиперпараметров осуществлялся с помощью GridSearchCV**

## Метрики:

**SGD-regression**:
- MAE: 1088447.63
- R²: 0.49

**Ridge-regression с исключением специфических признаков**:
- MAE: 470973.25
- R²: 0.5846
- лучшие гиперпараметры alpha = 0.1, solver = ...

**Ridge-regression с использованием колонок `tags`, `complectation_available_options`, `equipment`**:
- MAE: 585853.76
- R²: 0.5501

**Lasso-regression**:
- MAE: 1521742.21
- R²: 0.25
- лучшие гиперпараметры: alpha = 10.0

**ElasticNet**:
- MAE: 1135296.80 руб.
- R²: 0.44

**Decision tree regression с первым набором гиперпараметров**:
- MAE: 616943.20 руб.
- R²: 0.48
- лучшие гиперпараметры: max_depth = None, min_samples_leaf = 1, min_samples_split = 2

**Decision tree regression со вторым набором гиперпараметров**:
- MAE: 970054.78
- R²: 0.57
- лучшие гиперпараметры: l1_ratio = 0.8, alpha = 0.9
