import json
import csv
import glob
import os

def parse_json_to_csv(json_files, output_csv):
    fields = [
        ("production_year", lambda d: d.get("documents", {}).get("year", "")),
        ("mileage", lambda d: d.get("state", {}).get("mileage", "")),
        ("condition", lambda d: d.get("state", {}).get("condition", "")),
        ("owners_number", lambda d: d.get("documents", {}).get("owners_number", "")),
        ("pts_original", lambda d: d.get("documents", {}).get("pts_original", "")),
        ("horse_power", lambda d: d.get("owner_expenses", {}).get("transport_tax", {}).get("horse_power", "")),
        ("accidents_resolution", lambda d: d.get("documents", {}).get("accidents_resolution", "")),
        ("region", lambda d: d.get("seller", {}).get("location", {}).get("region_info", {}).get("name", "")),
        ("seller_type", lambda d: d.get("seller_type", "")),
        ("brand", lambda d: d.get("vehicle_info", {}).get("mark_info", {}).get("name", "")),
        ("model", lambda d: d.get("vehicle_info", {}).get("model_info", {}).get("name", "")),
        ("body_type", lambda d: d.get("vehicle_info", {}).get("configuration", {}).get("body_type", "")),
        ("doors_count", lambda d: d.get("vehicle_info", {}).get("configuration", {}).get("doors_count", "")),
        ("seats", lambda d: ";".join(map(str, d.get("vehicle_info", {}).get("configuration", {}).get("seats", []))) 
            if isinstance(d.get("vehicle_info", {}).get("configuration", {}).get("seats", []), list)
            else d.get("vehicle_info", {}).get("configuration", {}).get("seats", "")),
        ("engine_displacement", lambda d: d.get("vehicle_info", {}).get("tech_param", {}).get("displacement", "")),
        ("engine_power", lambda d: d.get("vehicle_info", {}).get("tech_param", {}).get("power", "")),
        ("fuel_rate", lambda d: d.get("vehicle_info", {}).get("tech_param", {}).get("fuel_rate", "")),
        ("steering_wheel", lambda d: d.get("vehicle_info", {}).get("steering_wheel", "")),
        ("price", lambda d: d.get("price_info", {}).get("price", "")),
        ("price_segment", lambda d: d.get("vehicle_info", {}).get("super_gen", {}).get("price_segment", "")),
        ("tags", lambda d: ";".join(d.get("tags", [])) if isinstance(d.get("tags", []), list) else d.get("tags", "")),
        ("auto_class", lambda d: d.get("vehicle_info", {}).get("configuration", {}).get("auto_class", "")),
        ("equipment", lambda d: ";".join([k for k, v in d.get("vehicle_info", {}).get("equipment", {}).items() if v])),
        ("complectation_available_options", lambda d: ";".join(d.get("vehicle_info", {}).get("complectation", {}).get("available_options", []))
            if d.get("vehicle_info", {}).get("complectation", {}).get("available_options") else "")
    ]
    
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[f[0] for f in fields])
        writer.writeheader()
        for file in json_files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                items = data if isinstance(data, list) else [data]
                for d in items:
                    row = {}
                    for name, func in fields:
                        row[name] = func(d)
                    writer.writerow(row)

if __name__ == "__main__":
    json_files = glob.glob(os.path.join("**", "offer_*.json"), recursive=True)
    parse_json_to_csv(json_files, "output.csv")
