from multiprocessing import Manager

manager = Manager()              
models = manager.dict()    
active_model_id = manager.Value('i', -1)  

shared_state = {
    "models": models,
    "active_model_id": active_model_id
}


STANDARD_MODELS = {
    "final_model",
    "catboost_pipeline",
    "catboost_pipeline_old",
    "lgbm_pipeline",
    "lgbm_pipeline_old",
}

OLD_MODEL_IDS = {"catboost_pipeline_old", "lgbm_pipeline_old"}
NEW_MODEL_IDS = {"catboost_pipeline", "lgbm_pipeline"}
