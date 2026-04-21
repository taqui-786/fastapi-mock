from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends

from app.helper import get_weather_data
from app.schemas import PostCreate
from contextlib import asynccontextmanager
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.images import imagekit, get_image_caption


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
):
    file_bytes = await file.read()  # read the actual bytes from the uploaded file
    img_data = imagekit.files.upload(  # correct SDK method name
        file=file_bytes, file_name=file.filename, folder="/python"
    )
    dynamic_img_caption = get_image_caption(img_data.url)
    post = Post(
        caption=dynamic_img_caption, url=img_data.url, file_type="Photo", file_name="Testing"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@app.get("/feed")
async def get_posts(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()
    posts_data = []

    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )
    return {"posts": posts_data}


@app.delete("/delete-post/{id}")
async def delete_images(id: str, session: AsyncSession = Depends(get_async_session)):
    await session.execute(delete(Post).where(Post.id == id))
    await session.commit()  # ← THIS saves the deletion to the database!
    return {"message": "Deleted Post "}
