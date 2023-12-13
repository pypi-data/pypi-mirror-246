from .lifespan import lifespan, TridentFastAPI
from .router import router

app = TridentFastAPI(lifespan=lifespan)
app.include_router(router)
