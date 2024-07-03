from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from routers.schemas import UserFriend
from db.db_friends import get_user_friends

router = APIRouter(
    prefix="/friends",
    tags=["friends"],
)



@router.get("/{user_id}", response_model=List[UserFriend])
def get_friends(user_id: int = Path(..., title="The ID of the user whose friends to retrieve"), db: Session = Depends(get_db)):
    friends = get_user_friends(db, user_id)
    if not friends:
        raise HTTPException(status_code=404, detail="No friends found")
    return [UserFriend(user_id=user_id, friend_id=f.id) for f in friends]




