router=APIRouter()
@router.post("/user",status_code=201,response_model=schema.UserOut)
def create_user(user:schema.CreateUser, db:Session(get_db)):
    new_user=