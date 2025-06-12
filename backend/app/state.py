from multiprocessing import Manager

manager = Manager()               # <-- создаётся один раз, при импорте модуля
models = manager.dict()          # <-- сюда будут складываться ваши модели
active_model_id = manager.Value('i', -1)  # или можно тоже manager.dict(), в котором хранить примитив

# expose
shared_state = {
    "models": models,
    "active_model_id": active_model_id
}
