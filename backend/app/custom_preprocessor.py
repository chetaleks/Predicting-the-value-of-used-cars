import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PolynomialFeatures
from pandas.api.types import is_numeric_dtype

class CustomPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, year=2025):
        self.year = year

    def fit(self, X, y=None):
        # сохраняем уникальные значения для создания бинарных признаков
        self.all_tags_ = self.get_unique_values(X["tags"])
        self.all_options_ = self.get_unique_values(X["complectation_available_options"])
        self.all_equipments_ = self.get_unique_values(X["equipment"])
        # инициализируем полиномиальный трансформер
        self.poly_ = PolynomialFeatures(degree=2, include_bias=False)
        return self

    def transform(self, X):
        df = X.copy()

        # бинарные признаки для мультизначных колонок
        tags_dummies = self.create_binary_features(df, "tags", self.all_tags_)
        options_dummies = self.create_binary_features(
            df, "complectation_available_options", self.all_options_
        )
        equipment_dummies = self.create_binary_features(
            df, "equipment", self.all_equipments_
        )

        # объединяем исходные данные и дамми-признаки
        full_df = pd.concat(
            [
                df.drop(
                    columns=["tags", "complectation_available_options", "equipment"]
                ),
                tags_dummies,
                options_dummies.drop(columns=["condition"], errors="ignore"),
                equipment_dummies.drop(columns=["condition"], errors="ignore"),
            ],
            axis=1,
        )

        full_df = full_df.fillna(0)
        full_df.replace({'True': 1, 'False': 0}, inplace=True)
        
        # приводим дублирующиеся колонки к int8
        duplicated_cols = full_df.columns[full_df.columns.duplicated()].unique()
        for col in duplicated_cols:
            full_df[col] = full_df[col].astype("int8")

        # объединяем дубликаты
        names = duplicated_cols
        new_cols = {}
        for name in names:
            cols_i = [col for col in full_df.columns if col == name]
            sub_df = full_df.loc[:, cols_i].astype("int8")
            max_series = sub_df.max(axis=1).astype("int8")
            new_cols[name] = max_series
            full_df.drop(columns=cols_i, inplace=True)
        for name, s in new_cols.items():
            full_df[name] = s

        # Список ожидаемых признаков: оставляем только те, что есть в full_df
        features = [
            "production_year",
            "mileage",
            "condition",
            "owners_number",
            "accidents_resolution",
            "region",
            "seller_type",
            "brand",
            "model",
            "body_type",
            "doors_count",
            "seats",
            "engine_displacement",
            "engine_power",
            "fuel_rate",
            "steering_wheel",
            "auto_class",
            "certificate_Favorit_Warranty",
            "high_price",
            "preset.nadezhnie_yaponskie_avto_starshe_10_let",
            "real_photo",
            "reduced_price",
            "paris2016",
            "new4new",
            "compact",
            "style",
            "prestige",
            "vin_resolution_in_progress",
            "Detroit2016",
            "predict_match_price",
            "big",
            "certificate_KiaSure",
            "BOND_CARS",
            "options",
            "certificate_avilon_warranty",
            "economical",
            "history_increase",
            "NFS_2015_CARS",
            "active_in_buyout",
            "reseller_status_accepted",
            "small",
            "prev_offer_photos",
            "catalog_china_landing_russian_official",
            "certificate_DasWeltAuto",
            "safe_car",
            "new_car_old_price",
            "increased_price",
            "big-trunk",
            "user_reseller_7days",
            "vin_resolution_ok",
            "too_high_price",
            "catalog_china_landing_china_unofficial",
            "jeneva2016",
            "certificate_ttc_warranty",
            "description_using_yagpt",
            "drift",
            "frankfurt2015",
            "liquid",
            "vin_resolution_unknown",
            "vin_resolution_error",
            "preset.top_nadezhnih_vnedorozhnikov_s_probegom",
            "little",
            "vin_resolution_invalid",
            "withNumericEnumFeaturePairs",
            "vin_service_history",
            "autoru_exclusive",
            "has_exterior_poi",
            "certificate_bmw_service_inclusive",
            "affordable",
            "m",
            "amg",
            "muscle",
            "medium",
            "offroad",
            "fast",
            "chats_preferred",
            "very_large",
            "proven_owner",
            "comfort",
            "badge",
            "preset.samie_komfortnie_avto_dlya_dalnih_poezdok",
            "hotsuv",
            "discount",
            "preset.semeynie_avto",
            "wide-back-seats",
            "active_safe_deal_exists",
            "stable_price",
            "handling",
            "calls_preferred",
            "with_lbu_auction_rank",
            "vin_unknown_color",
            "hothatch",
            "novice-drivers",
            "all-terrain",
            "high_reviews_mark",
            "large",
            "rs",
            "video",
            "too_low_price",
            "vin_checked",
            "custom_cleared_without_pts",
            "jeneva2018",
            "external_panoramas",
            "middle",
            "jeneva2017",
            "sport",
            "has_vendor_colors",
            "warranty",
            "certificate_business-car_warranty",
            "frame",
            "newyork2016",
            "no_accidents",
            "with_calls_stat",
            "oversize",
            "dealer_discount",
            "almost_new",
            "available_for_carp_auction",
            "no_answer",
            "catalog_china_landing_official_adaptation",
            "catalog_china_landing_europe_like",
            "online_view_available",
            "fresh",
            "preset.samie_nadezhnie_i_ekonomichnie_avto",
            "certificate_avtodom_warranty",
            "jeneva2019",
            "cm_finance",
            "frankfurt2017",
            "preset.kitayskie_elektromobili",
            "fivestars",
            "one_owner",
            "preset.top_nadezhnih_kitayskih_avto",
            "preset.top_avto_do_500_tis",
            "catalog_china_landing_official_twins",
            "checked_dealer",
            "allowed_for_cartinder",
            "certificate_manufacturer",
            "interior_panoramas",
            "losangeles2017",
            "certificate_pango_select",
            "vin_resolution_untrusted",
            "haggle_possible",
            "preset.top_koreyskih_avto",
            "low_price",
            "trump_cars",
            "preset.samie_bistrie_avto",
            "type_top_crown",
            "certificate_asc_warranty",
            "fake-complect",
            "ignor-cme",
            "migration-flag",
            "26-inch-wheels",
            "8RF",
            "500",
            "LMS",
            "23-inch-wheels",
            "seats-7",
            "7AA",
            "rus-multi",
            "seats-8",
            "alloy-wheel-disks",
            "443",
            "13-inch-wheels",
            "27-inch-wheels",
            "4A3",
            "534",
            "7X5",
            "465",
            "632",
            "seats-4",
            "armored",
            "881",
            "248",
            "airbrush",
            "3B3",
            "gbo",
            "seats-9",
            "seats-2",
            "873",
            "597",
            "414",
            "engine-proof",
            "C3U",
            "12-inch-wheels",
            "234",
            "25-inch-wheels",
            "5AC",
            "872",
            "seats-6",
            "608",
            "28-inch-wheels",
            "turnbuckle",
            "light-interior",
            "dark-interior",
            "pts_original",
            "xenon",
            "roller-blind-for-rear-window",
            "paint-metallic",
            "sport-suspension",
            "remote-car-services",
            "alarm",
            "duo-body-color",
            "servo",
            "wheel-power",
            "massage-seats",
            "front-seats-heat-vent",
            "16-inch-wheels",
            "adaptive-light",
            "black-roof",
            "windcleaner-heat",
            "body-mouldings",
            "cooling-box",
            "night-vision",
            "19-inch-wheels",
            "airbag-rear-side",
            "ashtray-and-cigarette-lighter",
            "wheel-memory",
            "easy-trunk-opening",
            "reduce-spare-wheel",
            "front-seat-support",
            "power-latching-doors",
            "alcantara",
            "door-sill-panel",
            "passenger-seat-updown",
            "wheel-heat",
            "third-rear-headrest",
            "multizone-climate-control",
            "feedback-alarm",
            "laser-lights",
            "roof-rails",
            "seat-memory",
            "rear-seat-heat-vent",
            "isofix-front",
            "folding-front-passenger-seat",
            "knee-airbag-pass",
            "spare-wheel",
            "driver-seat-support",
            "seat-transformation",
            "vsm",
            "eco-leather",
            "power-child-locks-rear-doors",
            "roller-blinds-for-rear-side-windows",
            "220v-socket",
            "24-inch-wheels",
            "traffic-sign-recognition",
            "remote-engine-start",
            "fabric-seats",
            "tja",
            "knee-airbag",
            "music-super",
            "15-inch-wheels",
            "entertainment-system-for-rear-seat-passengers",
            "light-cleaner",
            "glonass",
            "sport-pedals",
            "hatch",
            "activ-suspension",
            "mirrors-memory",
            "pedestrian-detection",
            "rear-armrest",
            "third-row-seats",
            "android-auto",
            "steering-wheel-gear-shift-paddles",
            "ptf",
            "steel-wheels",
            "voice-recognition",
            "leather",
            "leather-gear-stick",
            "18-inch-wheels",
            "drive-mode-sys",
            "start-stop-function",
            "14-inch-wheels",
            "laminated-safety-glass",
            "rcta",
            "driver-seat-electric",
            "auto-dimming-mirror",
            "folding-tables-rear",
            "ldw",
            "auto-park",
            "air-suspension",
            "multi-wheel",
            "17-inch-wheels",
            "dha",
            "21-inch-wheels",
            "combo-interior",
            "ya-auto",
            "aux",
            "body-kit",
            "decorative-interior-lighting",
            "drowsy-driver-alert-system",
            "electro-rear-seat",
            "automatic-lighting-control",
            "adj-pedals",
            "20-inch-wheels",
            "volume-sensor",
            "velvet-seats",
            "tinted-glass",
            "sport-seats",
            "22-inch-wheels",
            "projection-display",
            "programmed-block-heater",
            "navigation",
            "central-airbag",
        ]
        # Оставляем только колонки, которые есть в full_df
        full_df = full_df.loc[:, full_df.columns.intersection(features)]

        df_mod = full_df.copy()

        # возраст автомобиля
        df_mod["age"] = self.year - df_mod["production_year"]
        numeric_cols = ["mileage", "engine_displacement", "engine_power", "age"]

        # лог и квадрат базовых числовых признаков
        for col in numeric_cols:
            if col in df_mod:
                df_mod[f"log_{col}"] = np.log1p(df_mod[col].fillna(0))
                df_mod[f"square_{col}"] = df_mod[col].fillna(0) ** 2

        # полиномиальные признаки
        poly_array = self.poly_.fit_transform(df_mod[numeric_cols].fillna(0))
        poly_feature_names = self.poly_.get_feature_names_out(numeric_cols)
        poly_df = pd.DataFrame(
            poly_array, columns=poly_feature_names, index=df_mod.index
        )
        poly_new = poly_df.drop(
            columns=[c for c in poly_df.columns if c in numeric_cols]
        )
        df_mod = pd.concat([df_mod, poly_new.add_prefix("poly_")], axis=1)

        df_mod['power_to_disp'] = df_mod['engine_power'] / df_mod['engine_displacement'].clip(lower=0.01)

        # Произведения признаков
        df_mod['mileage_x_power'] = df_mod['mileage'] * df_mod['engine_power']
        df_mod['disp_x_power'] = df_mod['engine_displacement'] * df_mod['engine_power']
        df_mod['owners_x_power'] = df_mod['owners_number'] * df_mod['engine_power']
        df_mod["age_x_power"]    = df_mod["age"] * df_mod["engine_power"]
        df_mod["age_x_mileage"]  = df_mod["age"] * df_mod["mileage"]

        # Частные признаков
        df_mod['power_div_mileage'] = df_mod['engine_power'] / df_mod['mileage'].clip(lower=0.01)
        df_mod['disp_per_mile'] = df_mod['engine_displacement'] / df_mod['mileage'].clip(lower=0.01)
        df_mod['mileage_per_hp'] = df_mod['mileage'] / df_mod['engine_power'].clip(lower=0.01)
        df_mod['milage_per_year'] = df_mod['mileage'] / df_mod['age'].clip(lower=0.01)
        df_mod['power_div_owners'] = df_mod['engine_power'] / df_mod['owners_number'].clip(lower=0.01)
        df_mod['disp_div_owners'] = df_mod['engine_displacement'] / df_mod['owners_number'].clip(lower=0.01)
        df_mod['disp_div_fuel'] = df_mod['engine_displacement'] / df_mod['fuel_rate'].clip(lower=0.01)
        df_mod['fuel_div_disp'] = df_mod['fuel_rate'] / df_mod['engine_displacement'].clip(lower=0.01)
        df_mod['power_div_fuel'] = df_mod['engine_power'] / df_mod['fuel_rate'].clip(lower=0.01)
        df_mod['fuel_div_power'] = df_mod['fuel_rate'] / df_mod['engine_power'].clip(lower=0.01)

        # Лог-взаимодействие
        df_mod['log_mileage_x_log_power'] = df_mod['log_mileage'] * df_mod['log_engine_power']
        df_mod['log_age_x_log_power'] = df_mod['log_age'] * df_mod['log_engine_power']

        # Разности признаков
        df_mod['power_minus_disp'] = df_mod['engine_power'] - df_mod['engine_displacement']

        # Отношение дверей к местам
        df_mod["seats_num"] = pd.to_numeric(df_mod["seats"], errors="coerce")
        df_mod['doors_to_seats_ratio'] = df_mod['doors_count'] / df_mod['seats_num'].clip(lower=0.01)

        # Индикатор аварий
        df_mod['has_accident'] = (
            ~df_mod['accidents_resolution'].fillna('none').str.lower().isin(['none', 'no', 'unknown'])
        ).astype(int)

        binary_cols = [
            col for col in df.columns
            if is_numeric_dtype(df[col]) and
              set(df[col].dropna().unique()).issubset({0, 1})
        ]
        df_mod['num_binary_features'] = df[binary_cols] \
            .astype(bool).sum(axis=1)

        # Счетчики безопасности и комфорта
        safety_keywords = ['airbag', 'detection', 'vsm', 'ldw', 'tja', 'rcta', 'ptf']
        safety_cols = [c for c in df_mod.columns if any(k in c.lower() for k in safety_keywords)]
        df_mod['safety_feature_count'] = df_mod[safety_cols] \
            .astype(bool).sum(axis=1)

        comfort_keywords = ['heat', 'leather', 'massage', 'climate', 'vent', 'seat']
        comfort_cols = [c for c in df_mod.columns if any(k in c.lower() for k in comfort_keywords)]
        df_mod['comfort_feature_count'] = df_mod[comfort_cols] \
            .astype(bool).sum(axis=1)

        # Количество preset-тегов
        preset_cols = [c for c in df_mod.columns if c.startswith('preset')]
        df_mod['num_presets'] = df_mod[preset_cols] \
            .astype(bool).sum(axis=1)

        # Является ли машина новой
        df_mod['is_new'] = ((df_mod['mileage'] < 1000) & (df_mod['owners_number'] <= 1)).astype(int)
        df_mod['is_very_old'] = (df_mod['age'] > 20).astype(int)

        df_mod['is_one_owner'] = (df_mod['owners_number'] == 1).astype(int)

        return df_mod

    @staticmethod
    def get_unique_values(series, sep=";"):
        uniq = set()
        for cell in series.dropna():
            for piece in cell.split(sep):
                s = piece.strip()
                if s:
                    uniq.add(s)
        return np.array(list(uniq))

    @staticmethod
    def create_binary_features(df, column, unique_values, sep=";"):
        return (
            df[column]
            .str.get_dummies(sep=sep)
            .reindex(columns=unique_values, fill_value=0)
            .astype("int8")
        )